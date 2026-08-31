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
    """Every date a HUMAN wrote down, wherever they wrote it.

    Two sources, because /changelog is not a markdown docs page (sync item
    18): its lastmod is the newest DATED RELEASE HEADING in CHANGELOG.md,
    read by `pages.changelog.newest_date()`. That is still a declared date —
    somebody types it when they cut a release — it just is not frontmatter.
    The rule this test defends is "no date the project did not state", not
    "no date outside docs/", and widening it here is what keeps the rule
    honest rather than merely quiet.
    """
    dates = set()
    for md in Path("docs").glob("**/*.md"):
        text = md.read_text()
        head = text.split("---")[1] if text.startswith("---") else ""
        m = re.search(r"^lastmod:\s*(\d{4}-\d{2}-\d{2})\s*$", head, re.MULTILINE)
        if m:
            dates.add(m.group(1))
    changelog = Path("CHANGELOG.md")
    if changelog.exists():
        dates |= set(re.findall(r"^## \[[^\]]+\] - (\d{4}-\d{2}-\d{2})\s*$",
                                changelog.read_text(), re.MULTILINE))
    return dates


def test_the_changelog_lastmod_is_the_newest_release_heading():
    """The other end of the widening above: /changelog's date must come from
    the file, not from a build clock. If `newest_date()` ever returns
    something CHANGELOG.md does not contain, the pin above would accept it
    on the strength of a source that no longer says it."""
    from pages.changelog import newest_date

    date = newest_date()
    assert date, "no dated release heading in CHANGELOG.md"
    assert re.search(rf"^## \[[^\]]+\] - {re.escape(date)}\s*$",
                     Path("CHANGELOG.md").read_text(), re.MULTILINE), date


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


def test_apple_touch_icon_is_opaque():
    """iOS composites the icon's alpha onto ITS OWN background — black on
    some surfaces, white on others — so a transparent apple-touch icon
    renders differently everywhere it appears. scripts/make_favicons.py
    flattens exactly this one file onto opaque white (every other size
    keeps its alpha; browsers and Android handle it correctly).

    This site shipped an RGBA one for a day: the gate wave generated the
    set with the pre-fix script, and the template fixed it at the source
    the next morning (the emojimart finding). Regenerate with
    `python scripts/make_favicons.py assets/apple-touch-icon_areachart.png`.

    Read the colour type straight out of the PNG header — stdlib only, no
    Pillow in the test environment. IHDR is always the first chunk: colour
    type is the byte at offset 25. 2 = RGB (opaque), 6 = RGBA. A palette
    PNG (3) can smuggle transparency back in through a tRNS chunk, so pin
    that absent too.
    """
    icon = (
        Path(__file__).resolve().parent.parent
        / "assets" / "favicon" / "apple-touch-icon.png"
    )
    data = icon.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG?"
    colour_type = data[25]
    assert colour_type in (0, 2, 3), (
        f"apple-touch-icon.png has colour type {colour_type} (an alpha "
        "channel) — regenerate it with scripts/make_favicons.py, which "
        "flattens this one icon onto opaque white."
    )
    assert b"tRNS" not in data, (
        "apple-touch-icon.png carries a tRNS transparency chunk — iOS will "
        "composite it onto an unpredictable background."
    )
