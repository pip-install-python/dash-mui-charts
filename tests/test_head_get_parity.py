"""HEAD parity, and why this fork never needed the ASGI shim.

SYNC 1.6.44 item 2, with the ops seat's correction (2026-09-05): an ABSENT
`HeadAsGetMiddleware` must not be read as a RETIRED one. This fork has never
carried it and the item's "retire it" half therefore does not apply — what
applies is the "or record" half, and the record is `DIVERGENCES.md`'s
recorded-conventions entry plus this file.

The mechanism, which is the whole reason the fleet has a trap about it:
`werkzeug.routing` derives a HEAD rule from every GET rule, so on a Flask
backend HEAD parity is free. FastAPI's `APIRoute` does NOT — it takes
`methods` literally — so a route declared `@router.get(...)` answers HEAD
with 405, which is what the two ASGI forks needed a middleware to fix.
`starlette.routing.Route` is not the culprit and does add HEAD; the layer
matters and the kit's trap names it.

MEASURED IN-PROCESS, DELIBERATELY. A HEAD probe answers a question about the
ROUTER'S METHOD TABLE, never about the document, and that table is exactly
what is asserted here — so the in-process lane is the honest one for this
claim, not a weaker substitute for the wire. It also keeps three crawler- and
browser-UA probes out of production's read ledger, which the wire lane cannot
do.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# The five paths the item names, and the three lanes a UA can land in.
PATHS = ("/healthz", "/llms.txt", "/robots.txt", "/sitemap.xml", "/")
UAS = {
    "browser": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "crawler": (
        "Mozilla/5.0 (compatible; Googlebot/2.1; "
        "+http://www.google.com/bot.html)"
    ),
    "library": "curl/8.7.1",
}


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("lane", sorted(UAS))
def test_head_matches_get_status(app, path, lane):
    """15 pairs. HEAD must not 405 where GET answers.

    Goes to the raw Werkzeug client rather than conftest's `Client` wrapper,
    which exposes only `.get()` — the asymmetry under test needs both verbs
    from the same client.
    """
    raw = app.server.test_client()
    headers = {"User-Agent": UAS[lane]}
    get = raw.get(path, headers=headers)
    head = raw.head(path, headers=headers)
    assert head.status_code == get.status_code, (
        f"{path} as {lane}: HEAD {head.status_code} != GET {get.status_code}"
    )


def test_the_shim_is_absent_from_the_tree():
    """Non-vacuity, half one: parity is not being provided by a shim.

    If someone ports the ASGI middleware here later, this test fails and the
    recorded convention in DIVERGENCES.md must be revisited rather than the
    assertion relaxed.

    SCOPED TO APPLICATION CODE, not the whole tree — a sweep including
    `tests/` matches this file's own prose about the thing it is hunting and
    reports the defect it documents the absence of (1.6.44 item 13's exact
    failure, hit here on the first run).
    """
    roots = [REPO_ROOT / "lib", REPO_ROOT / "components", REPO_ROOT / "pages"]
    swept, hits = 0, []
    for root in roots:
        for py in root.rglob("*.py"):
            if "__pycache__" in py.parts:
                continue
            swept += 1
            if "HeadAsGet" in py.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(py.relative_to(REPO_ROOT)))
    swept += 1
    if "HeadAsGet" in (REPO_ROOT / "run.py").read_text(encoding="utf-8"):
        hits.append("run.py")
    # Print-the-count rule: a sweep that swept nothing and a sweep that found
    # nothing produce the same green, and only one of them is evidence.
    assert swept > 20, f"corpus too small to trust a negative: {swept} files"
    assert hits == [], f"a HEAD→GET shim appeared: {hits}"


def test_werkzeug_is_the_thing_providing_parity(app):
    """Non-vacuity, half two: the rule map really carries HEAD.

    The parity assertions above would pass just as well against a router that
    answered every method identically. This pins the actual mechanism — each
    GET rule in Werkzeug's map has HEAD in its method set — so the day this
    fork acquires an ASGI lane, the parity tests go red for the right reason
    instead of quietly measuring nothing.
    """
    rules = list(app.server.url_map.iter_rules())
    get_rules = [r for r in rules if "GET" in (r.methods or set())]
    assert get_rules, "no GET rules registered — the sweep swept nothing"
    missing = [r.rule for r in get_rules if "HEAD" not in (r.methods or set())]
    assert missing == [], f"GET rules without a derived HEAD: {missing[:10]}"
