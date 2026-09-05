"""Every internal link in the app shell resolves to something real.

SYNC 1.6.44 item 11.

WHY NO HTTP SWEEP CAN SEE THIS. Dash answers 200 for ANY path — an unknown
route falls through to the pages catch-all and renders the 404 layout with a
200 status — so a status sweep over the shell's hrefs reports every one of
them healthy. And curl cannot ask the question at all: the shell is built by
React from `app.layout`, so the served HTML never contains those anchors
(the same reason `curl … | grep skip-link` returns 0 on a host whose skip
link works perfectly).

So the assertion walks the layout, exactly as `run.py` builds it:

    app.layout = create_appshell(dash.page_registry.values())

WHITELISTING, and this is where the item warns forks off a blanket entry:
`/docs` and `/redoc` exist only on the FastAPI lane. This fork is Flask
only, so they are NOT whitelisted here — an entry for them would let an
un-gated badge ship a soft 404 on the one lane this host actually serves.
"""
from __future__ import annotations

import pytest

import dash
import dash_mantine_components as dmc
from dash import html

from conftest import component_iter

# Non-page routes this app really mounts. Each is a real handler, not a page
# in `dash.page_registry`, so the registry alone would call them broken.
NON_PAGE_ROUTES = {
    "/llms.txt", "/llms-small.txt", "/llms-full.txt",
    "/robots.txt", "/sitemap.xml", "/healthz",
}

# Deliberately NOT whitelisted, and the reason is the item's own note:
#   /docs, /redoc  — FastAPI-lane only. This fork serves Flask; whitelisting
#                    them would hide a soft 404 on the lane that exists.
FORBIDDEN_WHITELIST = {"/docs", "/redoc"}


@pytest.fixture(scope="module")
def shell(app_module):
    """The shell exactly as run.py builds it."""
    from components.appshell import create_appshell

    return create_appshell(dash.page_registry.values())


def _hrefs(layout):
    out = []
    for comp in component_iter(layout):
        if isinstance(comp, (dmc.Anchor, html.A, dmc.NavLink, dmc.Button)):
            href = getattr(comp, "href", None)
            if isinstance(href, str) and href:
                out.append(href)
        else:
            href = getattr(comp, "href", None)
            if isinstance(href, str) and href:
                out.append(href)
    return out


def test_the_shell_actually_contains_links(shell):
    """Note 88: a sweep that swept nothing is not evidence."""
    hrefs = _hrefs(shell)
    assert len(hrefs) > 10, f"only {len(hrefs)} hrefs in the shell"


def test_every_internal_shell_link_is_registered_or_a_real_route(shell):
    registered = {p["path"] for p in dash.page_registry.values()}
    assert registered, "empty page registry — nothing to resolve against"

    broken = []
    checked = 0
    for href in _hrefs(shell):
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = href.split("?", 1)[0].split("#", 1)[0].rstrip("/") or "/"
        checked += 1
        if path in registered or href in registered:
            continue
        if path in NON_PAGE_ROUTES or href in NON_PAGE_ROUTES:
            continue
        broken.append(href)

    assert checked, "every href was external — the internal sweep swept nothing"
    assert broken == [], (
        f"shell links that resolve to no registered page and no mounted "
        f"route (Dash answers 200 for these, so no status sweep would "
        f"notice): {broken}"
    )


def test_the_fastapi_only_paths_are_not_whitelisted():
    """The item's per-lane warning, pinned.

    A blanket `/docs` + `/redoc` entry is the shape that lets an un-gated
    badge ship a soft 404 on a lane that does not mount them. This fork is
    Flask only; if it ever gains the FastAPI lane, the whitelist should
    become lane-conditional rather than unconditional.
    """
    assert not (FORBIDDEN_WHITELIST & NON_PAGE_ROUTES)


def test_those_paths_really_are_absent_on_this_lane(app):
    """Non-vacuity for the test above: prove they are not mounted here."""
    rules = {r.rule for r in app.server.url_map.iter_rules()}
    for path in FORBIDDEN_WHITELIST:
        assert path not in rules, (
            f"{path} IS mounted on this host — the whitelist reasoning above "
            f"needs revisiting"
        )


def test_the_check_would_catch_a_broken_link(shell):
    """MUTATION: show the sweep red, as the item's acceptance requires.

    Re-runs the same resolution logic with one fabricated href, proving the
    green above is a measurement and not the absence of one.
    """
    registered = {p["path"] for p in dash.page_registry.values()}
    fabricated = "/a-page-that-was-renamed-and-never-updated"
    assert fabricated not in registered

    broken = [
        h for h in _hrefs(shell) + [fabricated]
        if not h.startswith(("http://", "https://", "mailto:", "#"))
        and (h.split("?", 1)[0].rstrip("/") or "/") not in registered
        and h not in NON_PAGE_ROUTES
        and (h.split("?", 1)[0].rstrip("/") or "/") not in NON_PAGE_ROUTES
    ]
    assert broken == [fabricated], (
        f"the mutation did not isolate cleanly: {broken}"
    )


def test_dash_really_answers_200_for_an_unregistered_path(app):
    """The premise the whole file rests on, measured rather than asserted.

    If Dash 404'd unknown paths, a plain status sweep would be sufficient and
    this test file would be unnecessary ceremony.
    """
    raw = app.server.test_client()
    r = raw.get(
        "/a-path-that-does-not-exist-at-all",
        headers={"User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 "
            "Safari/537.36"
        )},
    )
    assert r.status_code == 200, (
        "Dash now 404s unknown paths — a status sweep would suffice and this "
        "file's premise should be revisited"
    )
