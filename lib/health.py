"""
``/healthz`` liveness probe for the Flask and Quart backends.

The 2plot.ai hub sweeps every satellite's ``/healthz`` once an hour and records
up/down + latency — that's the "Satellite health & reach" panel on ``/traffic``
(the traffic rollup this app POSTs supplies the other half). The FastAPI build
declares a typed ``/healthz`` in ``lib/asgi_routes`` so it shows up in Swagger,
but it renders from the SAME ``health_payload`` below — one payload builder on
every backend, so the probe contract doesn't depend on which backend a
deployment happens to run.

Keep it cheap: the hub measures the round trip, so any work done here is
reported back as this app being slow.
"""
from __future__ import annotations

import os
import platform

import dash


def _resolved_country() -> str:
    """``geo.explain_resolution`` over THIS request's headers, or a reason.

    Reads the framework's request object directly rather than anything the
    package threads through, so it answers "did the country header reach this
    app at all?" independently of how the enforcement seam is wired.
    """
    try:
        from dash_improve_my_llms import geo
        from dash_improve_my_llms._headers import normalize_headers
    except Exception:
        return "unavailable (pre-2.7.0 package)"

    try:
        from flask import has_request_context, request

        if not has_request_context():
            return "no request context"
        return geo.explain_resolution(normalize_headers(request.headers))
    except Exception:
        return "unavailable"


def _llms_version() -> dict:
    """``{"llms_version": "2.10.0"}``, or ``{}`` if the package cannot be read.

    Omitted rather than reported as "unknown": a health payload that invents
    a version is worse than one silent about it, and run.py's boot floor
    already refuses to start below the floor — so an absent key here means
    the import broke AFTER boot, which is itself the finding.

    Why it is worth a wire field at all: this fork pins a `>=` FLOOR, so the
    resolved version is a build-time fact that no public surface reported.
    "Which dash-improve-my-llms is production actually running?" had no
    answer from outside the container, which made every version-dependent
    diagnosis a guess — including whether a CI leg and production had
    resolved the same wheel at all.
    """
    try:
        import dash_improve_my_llms as _pkg

        version = getattr(_pkg, "__version__", None)
        return {"llms_version": version} if version else {}
    except Exception:
        return {}


def _ledger_block() -> dict:
    """``{"path", "persistent", "visits", "reads"}`` — the ledger, from outside.

    Sync 1.6.44 item 20. Three facts that were previously invisible on the
    wire, and one of them cannot be obtained any other way.

    ``persistent`` is MEASURED, NEVER DECLARED. It is true iff the resolved
    path lies OUTSIDE the repository root — i.e. on a mounted disk such as
    ``/var/data/...``. A path under the app tree is the container filesystem
    and reads false EVEN WHERE A BLUEPRINT DECLARES A DISK, which is the
    whole point: leaflet ran for weeks with a declared disk and no disk, and
    nothing on the wire could contradict the declaration. A boolean
    reporting the deployment's INTENTION is worth nothing; this one reports
    the filesystem.

    ``visits`` and ``reads`` are the two tables' current row counts, read
    from the same file the tracker writes. A missing file is ``0`` and
    ``0`` — never an error, and ``/healthz`` stays 200: this is a
    diagnostic, and a diagnostic that can take the health probe down with it
    is a liability.

    ROW CONTENTS NEVER APPEAR HERE. Counts, a boolean and a path — nothing
    about any visitor, which matters more since item 16 made this host's
    position on that explicit.
    """
    block = {"path": None, "persistent": False, "visits": 0, "reads": 0}
    try:
        import json
        from pathlib import Path

        from lib.analytics_tracker import analytics_path

        path = Path(analytics_path()).resolve()
        block["path"] = str(path)
        repo_root = Path(__file__).resolve().parent.parent
        try:
            path.relative_to(repo_root)
            block["persistent"] = False      # inside the tree: container fs
        except ValueError:
            block["persistent"] = True       # outside it: a mounted disk

        if path.exists():
            data = json.loads(path.read_text())
            if isinstance(data, dict):
                for table in ("visits", "reads"):
                    rows = data.get(table)
                    block[table] = len(rows) if isinstance(rows, list) else 0
    except Exception:
        # Never let a diagnostic break the health probe. An unreadable or
        # half-written ledger reports zeros, and the `path` already in the
        # block is what a reader needs in order to go and look.
        pass
    return block


def health_payload(backend: str) -> dict:
    payload = {
        "ok": True,
        "backend": backend,
        "dash_version": dash.__version__,
        # WHICH interpreter is actually serving (SYNC-1.6.22-1.6.29 item 5).
        # This fork is the reason the field is worth having: `render.yaml`
        # line 4 says `runtime: python`, so the Dockerfile is a CI artifact
        # and NOT what serves traffic — for two days the image said 3.14,
        # the CI matrix said 3.12 and the platform ran 3.11.12, and nothing
        # on the wire could contradict any of the three.
        # scripts/network_smoke.py holds this minor against the Dockerfile's
        # FROM tag, so image and declaration cannot part ways silently again.
        "python": platform.python_version(),
        # WHICH dash-improve-my-llms resolved into the running image (sync
        # 1.6.44 item 1). Additive and omitted on failure — see _llms_version.
        **_llms_version(),
        # The visitor ledger, from outside (sync 1.6.44 item 20). `persistent`
        # is measured against the filesystem, not read from a declaration.
        "ledger": _ledger_block(),
    }
    # Which commit the RUNNING instance was built from. This is what lets CD
    # verify the artifact it shipped rather than whichever build happens to
    # be serving: a Render service with a disk restarts with a blip instead
    # of overlapping instances, so a bare 200 proves nothing about WHICH
    # build answered (the muicharts finding, 2026-08-21 — its battery had
    # been verifying the previous release on every run, invisibly, until a
    # new surface made the race lose). Optional on purpose: omitted where
    # the platform variable does not exist, so the fleet's probe contract
    # is unchanged.
    build = os.environ.get("RENDER_GIT_COMMIT")
    if build:
        payload["build"] = build

    # WHICH satellite answered. `build` says which commit, this says which
    # app — and on a fleet where every host shares this template and a
    # hostname can be repointed between services (llms.2plot.dev was,
    # 2026-08-23), "is this the site I think it is?" is a different question
    # from "is this the build I shipped?". Cheap, and the hub's sweep gets
    # it for free.
    payload["app"] = os.environ.get("SATELLITE_APP_KEY") or "unknown"

    # The geo guardrail's LIVE state (dash-improve-my-llms >= 2.7.0). Added
    # after llms-2plot-dev's production verification could not answer "is
    # the denylist actually in force?" from outside: the control board and
    # the public policy showcase both showed countries denied while every
    # request was served 200, and the only surfaces that could settle it
    # (the boot log, the operator panel) need credentials a verification
    # pass does not have.
    #
    # Counts and flags only — never the denylist's country codes: a health
    # endpoint is not where anyone should learn policy. `resolved` reveals
    # only the caller's own country back to them, which Cloudflare's
    # /cdn-cgi/trace already does — and it is THE per-host check
    # docs/GEO.md calls mandatory before trusting a denylist. It also
    # localises a failure: geo can be configured with a full denylist and
    # still never match if the country header is not reaching the app —
    # "configured: true, denied: 7, resolved: unknown" says that in one
    # line.
    try:
        from dash_improve_my_llms import geo
    except ImportError:
        # Pre-2.7 package: the key is OMITTED, not error-flagged — a host on
        # an older floor is not broken, it just predates the diagnostic. The
        # fleet's >=2.7.1 floor round lights this up with no further change.
        pass
    else:
        try:
            payload["geo"] = {
                "configured": bool(geo.is_configured()),
                "denied": len(
                    geo.effective_policy().get("deny_countries") or []
                ),
                "resolved": _resolved_country(),
            }
        except Exception:  # never let a diagnostic break the health probe
            payload["geo"] = {"configured": False, "denied": 0, "error": True}

    return payload


def register_health_route(app, backend: str) -> None:
    """Mount ``/healthz`` on Flask/Quart. No-op on FastAPI (already typed)."""
    if backend == "fastapi":
        return

    server = app.server

    # Built PER REQUEST, not once at registration. It used to be a snapshot
    # closed over by the route — harmless while every field was static
    # (ok/backend/dash_version/build never change for a running process),
    # and silently wrong the moment one is not: on llms-2plot-dev the route
    # is registered ~150 lines before configure_geo runs, so a snapshot
    # reported the guardrail as unconfigured on a host where it is
    # configured — the diagnostic lying in exactly the situation it exists
    # for (found 2026-08-23, fixed fork-side first).
    if backend == "quart":
        from quart import jsonify

        @server.get("/healthz")
        async def _healthz():  # pragma: no cover — quart runtime
            return jsonify(health_payload(backend))
    else:
        from flask import jsonify

        @server.get("/healthz")
        def _healthz():
            return jsonify(health_payload(backend))

    print(f"[muicharts] /healthz registered ({backend}) — "
          "the 2plot.ai hourly health sweep probes this path.")
