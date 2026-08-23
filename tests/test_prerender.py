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
        "the floor first moved (to 2.6.1) for exactly this, and sits at "
        ">=2.7.1 now"
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


def test_prerender_single_h1_and_deduped_footer_llms_links(client, page_paths):
    """What the >=2.7.1 floor buys, pinned from the app's side, EVERY page.

    Below dimll 2.7.0 every page served TWO h1s to a generic client — the
    injected prerender header plus the doc body's own markdown H1, a
    duplicate-H1 page in every crawler's eyes (the 2026-08-22 SEO-audit
    finding) — and the home footer printed its /llms.txt link twice (on
    "/" the per-page link equals the root's; subpages legitimately carry
    both, DISTINCT).

    The sweep also catches APP-side H1 pollution, which is why it runs over
    every route rather than a sample: on the template its first run found a
    tutorial page's machine lane serving five h1s, because the source
    expansion rewrote a `.. source::` example inside a teaching fence
    (fixed fence-aware, and ported here).

    HTML comments are stripped before counting — templates/index.html
    legitimately discusses markup inside comments, and a comment that
    quotes what a test asserts on is how an assertion passes for the wrong
    reason (this repo has already paid for that once).
    """
    for path in page_paths:
        html = client.get(path).text  # default UA — the universal lane
        stripped = re.sub(r"<!--.*?-->", "", html, flags=re.S)

        h1s = re.findall(r"<h1[\s>]", stripped)
        assert len(h1s) == 1, (
            f"{path}: {len(h1s)} h1 elements in the generic-lane document — "
            "either the pre-2.7.0 prerender-header duplicate or app-side "
            "markdown leaking headings (the fence-expansion class)"
        )

        footer = re.search(r"<footer.*?</footer>", stripped, re.S)
        assert footer, f"{path}: no prerender footer in the generic-lane document"
        llms_links = re.findall(r'href="([^"]*llms\.txt)"', footer.group(0))
        assert len(llms_links) == len(set(llms_links)), (
            f"{path}: duplicate llms.txt links in the prerender footer "
            f"({llms_links}) — 2.7.0 dedups the per-page link when it "
            "equals the root"
        )
        if path == "/":
            assert llms_links == ["/llms.txt"], (
                f"home footer llms links {llms_links} — expected exactly the "
                "root link once"
            )


def test_source_expansion_is_fence_aware(app):
    """A `.. source::` inside a fenced block is documentation, not a directive.

    Expanding one injects a ```python fence inside the already-open fence,
    which closes it early — from there the inlined file renders as markdown
    on the machine lane and every `# comment` line becomes an <h1>. No page
    here teaches the directive today, so this pin is what keeps the first
    one that does from reintroducing it. The app fixture is requested only
    so pages/markdown.py is already imported with the repo root as CWD.
    """
    import sys

    expand = sys.modules["pages.markdown"]._expand_source_directives

    expanded = expand(".. source::requirements.txt")
    assert "# File: requirements.txt" in expanded, "real directive not expanded"
    assert "```" in expanded, "expansion lost its fence"

    taught = "```markdown\n.. source::requirements.txt\n```"
    assert expand(taught) == taught, "a fenced example was expanded"

    tilde = "~~~\n.. source::requirements.txt\n~~~"
    assert expand(tilde) == tilde, "a tilde-fenced example was expanded"
