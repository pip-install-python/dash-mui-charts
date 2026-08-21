"""dimll 2.6.0's SEO honesty features, pinned from this app's side.

Two contracts land with the 2.6.0 floor:

1. **Icon discovery agrees with the declaration.** run.py still declares
   `configure_seo(icons=[...])` explicitly (declared wins), but 2.6 also
   DISCOVERS icons from app assets — and this site is the awkward case the
   fleet's ordering rule was written for: it ships a second, bar-chart icon
   pair for the per-load browser quirk in templates/index.html. The two
   sets must still agree, or the tab, the crawler head and the manifest
   stop describing the same site. Set-equality, not order: discovery orders
   differently (.ico first, biggest square descending, apple-touch last)
   and the release notes are explicit that order-inequality is not a
   failure.

2. **The sitemap tells the truth or says nothing.** `<lastmod>` is emitted
   verbatim from frontmatter `lastmod:` and omitted when unset. This site
   declares NO lastmod on any page — deliberately: an honest date has to be
   authored with the prose it describes, and inventing one from a file
   mtime (which every Docker build resets) is exactly the lie 2.6.0 exists
   to end. So the assertion here is the strict one: no date may appear in
   the sitemap that no page declared, which today means no date at all. The
   moment a page starts stamping real dates, this test follows it without
   an edit.
"""

from __future__ import annotations

import re
from pathlib import Path


def _normalize(entries):
    """(rel, href, sizes) triples from the package's mixed icon shapes."""
    out = set()
    for e in entries:
        if isinstance(e, str):
            out.add(("icon", e, None))
        else:
            out.add((e.get("rel", "icon"), e["href"], e.get("sizes")))
    return out


def test_discovery_agrees_with_the_declared_icons(app):
    from dash_improve_my_llms.seo import _config, discover_icons

    declared = _normalize(_config.icons or [])
    discovered = _normalize(discover_icons(app))

    assert declared, "configure_seo(icons=) is no longer declared in run.py?"
    assert discovered, "discovery found nothing in assets/ — pattern drift?"
    assert declared == discovered, (
        "Declared and discovered icon sets diverged.\n"
        f"declared only:   {sorted(declared - discovered)}\n"
        f"discovered only: {sorted(discovered - declared)}\n"
        "If a favicon file was added/renamed, update run.py's icons list — "
        "or if discovery's patterns changed upstream, this is the canary. "
        "Regenerate the set with `python scripts/make_favicons.py "
        "assets/apple-touch-icon_areachart.png`."
    )


def _declared_lastmods() -> set[str]:
    dates = set()
    for md in Path("docs").glob("**/*.md"):
        text = md.read_text()
        head = text.split("---")[1] if text.startswith("---") else ""
        m = re.search(r"^lastmod:\s*(\d{4}-\d{2}-\d{2})\s*$", head, re.MULTILINE)
        if m:
            dates.add(m.group(1))
    return dates


def test_sitemap_lastmod_is_verbatim_or_absent(client):
    sitemap = client.get("/sitemap.xml").text
    emitted = re.findall(r"<lastmod>([^<]+)</lastmod>", sitemap)
    declared = _declared_lastmods()

    undeclared = [d for d in emitted if d not in declared]
    assert not undeclared, (
        f"Sitemap emits dates nobody declared: {undeclared} — an invented "
        "date is the lie that gets the whole sitemap discarded. Either the "
        "package regressed to build-time dates, or a page's `lastmod:` "
        "frontmatter was removed while the sitemap kept its date."
    )
