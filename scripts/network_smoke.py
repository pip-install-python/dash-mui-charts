#!/usr/bin/env python3
"""Smoke battery for a 2plot satellite — CI container and production alike.

One script, two seats, the SAME named checks either way, so a failure in CI
and a failure against production read identically:

    CI container   python scripts/network_smoke.py --base-url http://localhost:8550
    Production     python scripts/network_smoke.py --base-url https://boilerplate.2plot.dev

Stdlib-only on purpose: CI runs it from the host against the booted container
with a bare `python3`, before anything is pip-installed.

This is a TEMPLATE FILE. Every satellite forked from this repo copies it
verbatim and changes only the block marked "per-site" below — the expected
H1, the port, the paths that must 404. Everything else is the network
standard; if a check here is wrong, it is wrong on twenty hosts.

What a satellite is to the network is what the battery proves: that it states
its identity, that its agent-facing document surfaces are real, that it runs
the intended dash-improve-my-llms artifact, and that no owner-only surface
leaks. A satellite holds no key material, so unlike the hub's copy of this
script there is no agent-key API to fail closed — the corresponding check
here is that this host's llms.txt points *back* at the hub that does.

Every UA this script sends carries the internal-traffic token (the analytics
point of truth — https://2plot.ai/docs/satellite-analytics, "Internal
traffic"): a battery must never register as a visitor or a "bot" in any
network ledger. Even the deliberately crawler-shaped probe appends the token
— the target still exercises its bot path, but its analytics know the caller
is machinery.

Exit code: 1 if any check fails, else 0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TIMEOUT = 30


def _ssl_context() -> ssl.SSLContext:
    """Verify certificates via certifi when available.

    macOS Python ships without OS trust-store integration, so bare urllib
    fails every https fetch with CERTIFICATE_VERIFY_FAILED. This battery
    had no context until 2026-08-26, which meant running it by hand against
    production from a Mac reported ALL TWELVE checks failed — indis-
    tinguishable from the site being down, on a host that was perfectly
    healthy. CI runs on Linux and could never see it; nothing in tests/
    exercises the transport.

    Same fix, same reason as scripts/smoke_live.py's, and the same class as
    SYNC-1.6.10-1.6.16 item 7 / SYNC-1.6.22-1.6.29 item 6 — which name
    smoke_live.py in their file lists while item 6's contract sentence says
    "whatever live tool a CD run certifies with". CD certifies with BOTH
    scripts. Reported upstream as a template-class finding: the template's
    own copy of this file has no context either.

    Verification stays ON either way; certifi only supplies the CA bundle.
    """
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CONTEXT = _ssl_context()
try:
    from lib.constants import INTERNAL_UA as _INTERNAL_UA
except Exception:  # running outside a repo checkout — keep the token intact
    _INTERNAL_UA = "2plot-internal/1.0 (+https://2plot.ai/docs/satellite-analytics)"
UA = _INTERNAL_UA + " network-smoke"
CRAWLER_UA = "Mozilla/5.0 (compatible; Googlebot/2.1) " + _INTERNAL_UA

# The body dash-improve-my-llms serves when a page has no prose registered.
# Matched in full, deliberately: a substring check on "requires JavaScript"
# reported a perfectly healthy host as broken the first time this ran,
# because this app's own <noscript> block legitimately said those words.
# That block is gone (retired with the 2.6.1 pickup, 2026-08-22) — the full
# match stays anyway. It costs nothing, and the next fork to copy this file
# may well still have one.
STUB_MARKER = "This page contains interactive content that requires JavaScript"

# ---------------------------------------------------------------- per-site --
# The three values a fork changes. Everything below this block is the network
# standard and is copied verbatim.

# This app's one identity (lib/constants.SITE_BRAND). tests/test_site_identity
# asserts every local surface carries it; this pins the DEPLOYED artifact to
# it, which is the half no unit test can reach.
SITE_H1 = "# dash-mui-charts — MUI X charts for Dash"

# The container port. Matches the Dockerfile's EXPOSE and CMD.
DEFAULT_BASE_URL = "http://localhost:8550"

# A page with registered LLMS_DOC prose, used by the per-page document checks
# below. /sparkline is a Community page, so it renders identically with and
# without a MUI Pro key — the checks mean the same thing in secretless CI and
# against production.
PROSE_DOC_PATH = "/sparkline/llms.txt"

# Owner-only surfaces that must 404 their llms.txt to an anonymous reader.
# `/admin/control-board` is the real one as of the gate wave — the board can
# hide any page on this site, and `mark_hidden` in pages/control_board.py is
# what keeps it out of the sitemap, the llms.txt family, MCP and the
# prerender. The other two are canaries for surfaces this app does not have
# yet. Add real paths here in the same change that marks them hidden.
HIDDEN_DOC_PATHS = (
    "/admin/control-board/llms.txt",
    "/admin/llms.txt",
    "/analytics/llms.txt",
)

# The hub one level up the chain. A satellite's llms.txt must name it — that
# is what lets an agent walk from any leaf to the network root.
HUB_URL = "https://2plot.dev"

# ---------------------------------------------------------------------------

PASS, FAIL, WARN, SKIP = "pass", "FAIL", "warn", "skip"
_RESULTS: list[tuple[str, str, str]] = []  # (name, verdict, detail)


class SmokeFailure(Exception):
    pass


def fetch(url: str, ua: str = UA, method: str = "GET",
          body: bytes | None = None, headers: dict | None = None,
          timeout: int = TIMEOUT, retries: int = 3):
    """(status, headers, text) — HTTP errors are results, not exceptions;
    network errors raise AFTER retries.

    Response headers come back lower-cased: gunicorn sends `content-type`,
    proxies often re-case it — callers must not care. (A CI-only failure in
    the network root's battery was exactly that difference.)
    """
    last_exc: Exception | None = None
    for attempt in range(retries):
        if attempt:
            time.sleep(2 * attempt)
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("User-Agent", ua)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(
                    req, timeout=timeout, context=SSL_CONTEXT) as r:
                return (r.status, {k.lower(): v for k, v in r.headers.items()},
                        r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            return (e.code, {k.lower(): v for k, v in e.headers.items()},
                    e.read().decode("utf-8", "replace"))
        except Exception as exc:  # timeout, reset, truncated read, …
            last_exc = exc
    raise last_exc


def record(name: str, verdict: str, detail: str = "") -> None:
    _RESULTS.append((name, verdict, detail))
    print(f"[{verdict:>4}] {name}" + (f" — {detail}" if detail else ""), flush=True)
    if verdict == WARN and os.getenv("GITHUB_ACTIONS"):
        print(f"::warning title=network-smoke {name}::{detail}", flush=True)


def check(name: str, fn) -> None:
    try:
        fn()
        record(name, PASS)
    except SmokeFailure as exc:
        record(name, FAIL, str(exc))
    except Exception as exc:  # network/parse error → still a failure
        record(name, FAIL, f"{type(exc).__name__}: {exc}")


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise SmokeFailure(msg)


# ------------------------------------------------------------- the battery --

def declared_python_minor():
    """The fleet Python this checkout declares: the Dockerfile's FROM minor.

    None when there is nothing to hold the host against — no Dockerfile
    beside this script, or the seat itself is off-contract via
    SMOKE_PYTHON_DECLARED=ignore. Nothing in this repo sets that today: the
    two in-CI seats (the docs-tests boot and the docker container) both run
    the fleet minor, and the site matrix legs never invoke this script. The
    knob is here because the template's matrix does need it, and a fork that
    later boots this battery on a window leg will need it too.
    """
    if os.environ.get("SMOKE_PYTHON_DECLARED") == "ignore":
        return None
    dockerfile = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Dockerfile")
    try:
        with open(dockerfile, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"FROM\s+python:(\d+\.\d+)", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return None


def satellite_checks(base: str) -> None:
    get = lambda path, **kw: fetch(base + path, **kw)  # noqa: E731

    def healthz_ok():
        status, _, text = get("/healthz")
        expect(status == 200, f"/healthz {status}")
        expect(json.loads(text).get("ok") is True, f"unexpected body {text[:120]!r}")

    def python_matches_declared():
        # WHICH interpreter serves, versus the one this repo declares
        # (SYNC-1.6.22-1.6.29 item 5). This fork is the reason the check
        # earns its place: `render.yaml` says `runtime: python`, so the
        # Dockerfile is a CI artifact and NOT what serves traffic — the
        # image reached 3.14 while production stayed on 3.11.12 and every
        # gate in the tree was green, because nothing on the wire could
        # contradict either number. /healthz's `python` field is the
        # observability; this is the teeth.
        #
        # A red here after a render.yaml bump is the platform lagging the
        # repo, not a broken check: Blueprint env applies on a sync, so the
        # dashboard's own PYTHON_VERSION is the fix.
        status, _, text = get("/healthz")
        expect(status == 200, f"/healthz {status}")
        served = json.loads(text).get("python") or ""
        expect(bool(served), "/healthz carries no `python` field — the "
               "serving interpreter is invisible from outside")
        declared = declared_python_minor()
        if declared is None:
            return
        served_minor = ".".join(served.split(".")[:2])
        expect(served_minor == declared,
               f"host serves Python {served}, repo declares {declared} — "
               "a stale image, or a platform runtime nobody aligned")

    def llms_txt_identity():
        # The check this whole standard exists for. The H1 is what an agent
        # fetching /llms.txt cold reads as the name of this site, and a
        # pre-2.3.4 artifact publishes `app.title` (or a bare "Dash") there
        # with nothing else looking wrong.
        status, headers, text = get("/llms.txt")
        expect(status == 200, f"/llms.txt {status}")
        ct = headers.get("content-type", "")
        expect(ct.startswith("text/markdown"), f"content-type {ct!r}")
        first = text.splitlines()[0] if text else ""
        expect(first == SITE_H1, f"H1 {first!r} — identity regression?")
        expect("## Pages" in text, "page index section missing")
        expect("## Network" in text, "cross-host directory missing")

    def llms_txt_names_the_hub():
        _status, _, text = get("/llms.txt")
        expect(HUB_URL in text, f"the directory does not name {HUB_URL}")

    def page_llms_nav():
        status, _, text = get(PROSE_DOC_PATH)
        expect(status == 200, f"{PROSE_DOC_PATH} {status}")
        expect("/llms.txt" in text, "llms_nav header missing — page doc is a dead end")

    def hidden_pages_404():
        for path in HIDDEN_DOC_PATHS:
            status, _, _ = get(path)
            expect(status == 404, f"{path} {status} (owner surface leaked)")

    def robots_artifact_fingerprint():
        # pip metadata is invisible from outside, so the robots.txt crawler
        # split is how a live host is proven to run the intended package:
        # 2.3.2 allowed OAI-SearchBot; 2.3.3 moved ClaudeBot (the training
        # crawler) to Disallow while allowing Claude-User / Claude-SearchBot.
        status, _, text = get("/robots.txt")
        expect(status == 200, f"/robots.txt {status}")
        lines = [ln.strip() for ln in text.splitlines()]

        def rule(agent):
            marker = f"User-agent: {agent}"
            expect(marker in lines, f"{marker} stanza missing")
            return lines[lines.index(marker) + 1]

        for agent, expected, since in (
            ("OAI-SearchBot", "Allow: /", "2.3.2"),
            ("ClaudeBot", "Disallow: /", "2.3.3"),
            ("Claude-User", "Allow: /", "2.3.3"),
            ("Claude-SearchBot", "Allow: /", "2.3.3"),
        ):
            got = rule(agent)
            expect(got == expected,
                   f"{agent} -> {got!r}, expected {expected!r}: pre-{since} artifact")
        expect(any(ln.startswith("Sitemap:") for ln in lines), "Sitemap line missing")

    def sitemap_absolute_and_on_this_host():
        status, _, text = get("/sitemap.xml")
        expect(status == 200, f"/sitemap.xml {status}")
        expect("<loc>https://" in text or "<loc>http://" in text,
               "no absolute <loc> URLs")
        for path in HIDDEN_DOC_PATHS:
            leaked = path.rsplit("/llms.txt", 1)[0]
            expect(leaked not in text, f"hidden path {leaked} leaked into sitemap")

    def crawler_gets_prose():
        # The prerender. A crawler that receives the JavaScript stub indexes
        # nothing, and the page looks perfect in a browser the whole time.
        status, _, text = get("/", ua=CRAWLER_UA)
        expect(status == 200, f"/ {status}")
        expect("<title>" in text, "crawler HTML has no <title>")
        expect(STUB_MARKER not in text,
               "the home page served the JavaScript stub to a crawler")
        expect('rel="canonical"' in text, "no canonical tag for a crawler")

    def agents_and_browsers_get_different_types():
        # One URL, two audiences, and a `Vary` that stops a CDN mixing them.
        status, md_headers, md = get(PROSE_DOC_PATH)
        expect(status == 200, f"{PROSE_DOC_PATH} {status}")
        expect(md_headers.get("content-type", "").startswith("text/markdown"),
               f"agents got {md_headers.get('content-type')!r}")
        expect("<!DOCTYPE html>" not in md, "viewer chrome reached an agent")

        _status, html_headers, html = get(
            PROSE_DOC_PATH,
            headers={"Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
        expect("text/html" in html_headers.get("content-type", ""),
               f"browsers got {html_headers.get('content-type')!r}")
        expect("mk-wordmark" in html, "the network wordmark is missing")

        for label, headers in (("markdown", md_headers), ("html", html_headers)):
            expect("accept" in headers.get("vary", "").lower(),
                   f"no Vary: Accept on the {label} variant — a shared cache "
                   "may serve it to everyone")

    def corpus_documents_are_public():
        # The gate wave's first acceptance line: the llms.txt FAMILY answers
        # 200 with prose to an anonymous agent. run.py pins these three
        # pseudo-paths public explicitly, precisely so that flipping
        # PAGE_DEFAULT_TIER to gate the interactive site cannot take the
        # corpus documents with it — this is the check that would catch it.
        for path in ("/llms.txt", "/llms-small.txt", "/llms-full.txt"):
            status, headers, text = get(path)
            expect(status == 200, f"{path} {status}")
            ct = headers.get("content-type", "")
            expect(ct.startswith("text/markdown"), f"{path} content-type {ct!r}")
            expect(len(text) > 200 and STUB_MARKER not in text,
                   f"{path} served {len(text)}b — a stub, not prose")

    def agent_key_is_mounted_and_anonymous_gets_nothing():
        # The person→agent handoff (lib/agent_key.py). Mounted always, so a
        # 404 here means the route never registered and every copied
        # llms.txt link silently loses its key. 204 is the anonymous
        # answer; a 200 to a caller with no session would be a key leak.
        status, _, text = get("/api/agent-key")
        expect(status == 204, f"/api/agent-key {status} for an anonymous caller")
        expect(not text.strip(), f"anonymous body was not empty: {text[:80]!r}")

    for name, fn in (
        ("healthz_ok", healthz_ok),
        ("python_matches_declared", python_matches_declared),
        ("corpus_documents_are_public", corpus_documents_are_public),
        ("agent_key_is_mounted_and_anonymous_gets_nothing",
         agent_key_is_mounted_and_anonymous_gets_nothing),
        ("llms_txt_identity", llms_txt_identity),
        ("llms_txt_names_the_hub", llms_txt_names_the_hub),
        ("page_llms_nav", page_llms_nav),
        ("hidden_pages_404", hidden_pages_404),
        ("robots_artifact_fingerprint", robots_artifact_fingerprint),
        ("sitemap_absolute_and_on_this_host", sitemap_absolute_and_on_this_host),
        ("crawler_gets_prose", crawler_gets_prose),
        ("agents_and_browsers_get_different_types",
         agents_and_browsers_get_different_types),
    ):
        check(name, fn)


# ------------------------------------------------------------------- main --

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL,
                    help="the satellite under test (default: the CI container)")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    print(f"network-smoke → {base}\n")
    satellite_checks(base)

    counts = {v: sum(1 for _, verdict, _ in _RESULTS if verdict == v)
              for v in (PASS, FAIL, WARN, SKIP)}
    print(f"\n{counts[PASS]} passed, {counts[FAIL]} failed, "
          f"{counts[WARN]} warnings, {counts[SKIP]} skipped")
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
