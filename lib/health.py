"""
``/healthz`` liveness probe for the Flask and Quart backends.

The 2plot.ai hub sweeps every satellite's ``/healthz`` once an hour and records
up/down + latency — that's the "Satellite health & reach" panel on ``/traffic``
(the traffic rollup this app POSTs supplies the other half). The FastAPI build
already declares a typed ``/healthz`` in ``lib/asgi_routes`` so it shows up in
Swagger; this module gives the other two backends the same endpoint, so the
probe result doesn't depend on which backend a deployment happens to run.

Keep it cheap: the hub measures the round trip, so any work done here is
reported back as this app being slow.
"""
from __future__ import annotations

import os

import dash

# Which commit is this instance actually running? Render exports
# RENDER_GIT_COMMIT to every service; the others are the same idea on other
# platforms. Reported so a deploy can be WAITED FOR rather than assumed:
# .github/workflows/cd.yml polls this field until it matches the commit that
# triggered the run, and only then verifies the live site. Without it the
# verification step grades whatever happened to be serving — which, on a
# repo whose deploys come from render.yaml's `autoDeploy` rather than a
# deploy hook, is reliably the PREVIOUS release.
#
# Local runs and any platform that sets none of these simply omit the key,
# leaving the payload shape exactly as the fleet's other satellites report.
_COMMIT_ENV_KEYS = ("RENDER_GIT_COMMIT", "GIT_COMMIT", "SOURCE_COMMIT")


def running_commit() -> str | None:
    """The commit this process was built from, or None when unknowable."""
    for key in _COMMIT_ENV_KEYS:
        value = (os.environ.get(key) or "").strip()
        if value:
            return value
    return None


def health_payload(backend: str) -> dict:
    payload = {"ok": True, "backend": backend, "dash_version": dash.__version__}
    commit = running_commit()
    if commit:
        payload["commit"] = commit
    return payload


def register_health_route(app, backend: str) -> None:
    """Mount ``/healthz`` on Flask/Quart. No-op on FastAPI (already typed)."""
    if backend == "fastapi":
        return

    server = app.server
    payload = health_payload(backend)

    if backend == "quart":
        from quart import jsonify

        @server.get("/healthz")
        async def _healthz():  # pragma: no cover — quart runtime
            return jsonify(payload)
    else:
        from flask import jsonify

        @server.get("/healthz")
        def _healthz():
            return jsonify(payload)

    print(f"[muicharts] /healthz registered ({backend}) — "
          "the 2plot.ai hourly health sweep probes this path.")
