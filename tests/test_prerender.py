"""The universal prerender, as a PLAIN client sees it.

Two things this file exists to catch, both invisible to every other test in
the suite:

1. **The lane.** Every other prerender assertion here fetches with
   CRAWLER_UA, which exercises dash-improve-my-llms' separate bot-document
   path. A regression that UA-gated the UNIVERSAL lane — the one ordinary
   browsers, text browsers and html-to-text extractors ride — would pass
   the whole suite. An outside SEO audit (2026-08-22) read six hosts in
   this network as serving "Loading... and nothing else" for exactly this
   reason, on a lane that was working.

2. **The visibility.** dimll <= 2.6.0 injected that block with a literal
   `hidden` attribute, so a visibility-respecting consumer genuinely did
   read nothing — the prose was in the bytes and unreadable, the worst of
   both. 2.6.1 serves it visible and hides it with a synchronous inline
   script that only JS browsers run (React's mount then wipes the pair, so
   nothing changes for a human). requirements.txt and run.py both floor at
   2.6.1 for this; the assertions below are that floor's meaning, checked
   from the app's side.

The third assertion — that two DIFFERENT routes carry DIFFERENT prose — is
this site's own. Until 2026-08-22 a hand-written <noscript> block shipped
the same site-level catalogue on all 42 routes, which is what made an
outside reader think this host was the only one prerendering. Per-page
prose is the thing that block was mistaken for; a regression to one shared
paragraph would look fine to a naive "is there text?" check.
"""

from __future__ import annotations

import re

import pytest

# Two routes with unmistakably different subjects, both Community pages so
# they render identically with and without a MUI Pro key.
ROUTES = ("/pie", "/sparkline")


@pytest.mark.parametrize("path", ("/",) + ROUTES)
def test_the_prerender_is_present_and_visible_for_a_plain_client(client, path):
    html = client.get(path).text  # default UA — the point of the test
    div = re.search(r'<div id="dimll-prerender"[^>]*>', html)
    assert div, (
        f"{path}: no prerender block for a generic client — the universal "
        "lane is gated or off"
    )
    assert "hidden" not in div.group(0), (
        f"{path}: the prerender div carries `hidden` again — "
        "visibility-respecting consumers are back to reading 'Loading...'; "
        "the dimll floor is >=2.6.1 for exactly this"
    )
    assert 'data-dimll-prerender="1">document.getElementById' in html, (
        f"{path}: the marked synchronous hide script is missing — JS "
        "browsers would flash the prose before React mounts"
    )
    assert "<main>" in html, f"{path}: prerender block carries no <main> prose"


def _prerender_text(client, path: str) -> str:
    html = client.get(path).text
    block = html.split('id="dimll-prerender"', 1)[1]
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", block)).strip()


@pytest.mark.parametrize("path", ROUTES)
def test_each_route_prerenders_its_own_subject(client, path):
    """The page's own name, in its own prose."""
    import dash

    name = dash.page_registry[
        next(k for k, v in dash.page_registry.items() if v["path"] == path)
    ]["name"]
    text = _prerender_text(client, path)
    assert len(text) > 400, (
        f"{path}: {len(text)} characters of prerendered prose — a stub, not "
        "a page"
    )
    assert name.lower() in text.lower(), (
        f"{path}: the prerendered prose never names {name!r}"
    )


def test_two_routes_do_not_share_one_prerendered_paragraph(client):
    """The retired <noscript> block's failure mode, pinned so it cannot
    return under a different name."""
    first, second = (_prerender_text(client, p)[:1200] for p in ROUTES)
    assert first != second, (
        f"{ROUTES[0]} and {ROUTES[1]} prerender identical prose — a "
        "site-level block is standing in for per-page content again"
    )
