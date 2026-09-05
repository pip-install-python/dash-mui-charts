"""/terms and /privacy — sync 1.6.44 item 15.

The item's binding requirement, and the reason this file is not just a
"page renders" smoke test: **the privacy prose is bound to the code that
collects, by a test that reads a REAL visit row and asserts every key in it
is described.** A policy written once and left alone becomes wrong the first
time somebody adds a field to the ledger, and nothing would have said so.

Also pinned: ONE markdown string per page, rendered for the browser AND
handed to the machine lane. A page whose visible prose and whose llms.txt
are written separately is a site with two privacy policies, only one of
which was ever reviewed.
"""
from __future__ import annotations

import pytest

CRAWLER_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


# --------------------------------------------------- the binding that matters --

def test_every_key_a_real_visit_row_carries_is_described(app_module, tmp_path, monkeypatch):
    """Build a REAL row through the REAL tracker; the prose must cover it.

    Not a fixture dict — the point is that adding a field to `track_visit`
    without describing it on /privacy turns this red. A hand-written fixture
    would drift with the prose instead of with the code.
    """
    import lib.analytics_tracker as mod
    from pages.privacy import DESCRIBED_KEYS, LLMS_DOC

    monkeypatch.setattr(mod, "VISITOR_SALT_FILE", tmp_path / ".visitor_salt")
    mod._salt_cache.clear()
    monkeypatch.setattr(mod, "KEEP_CLIENT_IP", False)

    tracker = mod.tracker
    tracker._buffer.clear()
    tracker.track_visit(
        "/sparkline", BROWSER_UA, "203.0.113.9",
        headers={"CF-IPCountry": "GB", "CF-IPCity": "Manchester"},
    )
    tracker.track_visit(
        "/pie", CRAWLER_UA, "66.249.66.1", headers={"CF-IPCountry": "US"},
    )
    rows = list(tracker._buffer)
    tracker._buffer.clear()
    assert len(rows) == 2, "the tracker wrote nothing — nothing was measured"

    keys = set()
    for row in rows:
        keys.update(row)

    undescribed = sorted(k for k in keys if k not in DESCRIBED_KEYS)
    assert undescribed == [], (
        f"the ledger stores {undescribed} and /privacy does not describe "
        f"them — either describe the field or stop storing it"
    )

    # And the description must actually appear in the published prose, not
    # only in the mapping: DESCRIBED_KEYS is the index, LLMS_DOC is the
    # document a reader gets.
    for key in sorted(keys):
        phrase = DESCRIBED_KEYS[key]
        assert phrase.lower() in LLMS_DOC.lower(), (
            f"'{key}' maps to {phrase!r}, which appears nowhere on the page"
        )


def test_the_row_really_did_carry_the_interesting_keys(tmp_path, monkeypatch):
    """Non-vacuity: if track_visit returned early, the test above passes
    while measuring an empty set."""
    import lib.analytics_tracker as mod

    monkeypatch.setattr(mod, "VISITOR_SALT_FILE", tmp_path / ".visitor_salt")
    mod._salt_cache.clear()
    tracker = mod.tracker
    tracker._buffer.clear()
    tracker.track_visit("/pie", CRAWLER_UA, "66.249.66.1",
                        headers={"CF-IPCountry": "US"})
    row = tracker._buffer[-1]
    tracker._buffer.clear()
    for expected in ("timestamp", "path", "device_type", "user_agent",
                     "visitor_key", "location", "vendor_key"):
        assert expected in row, f"{expected} missing from a crawler row"


def test_the_policy_denies_what_the_code_denies(app_module):
    """The page says no third party is told anything. Pin the mechanism.

    A policy that claims something the code does not do is worse than no
    policy, so the claim is checked against the tracker's AST rather than
    trusted.
    """
    import ast
    from pathlib import Path

    from pages.privacy import LLMS_DOC

    assert "No third party is told anything about you" in LLMS_DOC

    tracker_src = (Path(__file__).resolve().parent.parent
                   / "lib" / "analytics_tracker.py").read_text()
    tree = ast.parse(tracker_src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & {"requests", "urllib", "httpx", "aiohttp", "socket"})


# ------------------------------------------------------------ both lanes ----

@pytest.mark.parametrize("path", ["/terms", "/privacy"])
def test_the_page_answers_on_the_browser_lane(client, path):
    r = client.get(path, user_agent=BROWSER_UA)
    assert r.status == 200


@pytest.mark.parametrize("path", ["/terms", "/privacy"])
def test_the_llms_document_exists_and_is_the_same_source(client, path):
    """ONE markdown string, both lanes."""
    import importlib

    module = importlib.import_module(f"pages.{path.strip('/')}")
    r = client.get(f"{path}/llms.txt", user_agent=CRAWLER_UA)
    assert r.status == 200, f"{path}/llms.txt {r.status}"

    # A distinctive sentence from the source must be in the served document.
    marker = module.LLMS_DOC.split("\n")[0].lstrip("# ").strip()
    assert marker.lower() in r.text.lower(), (
        f"the machine lane is not serving {path}'s LLMS_DOC"
    )


@pytest.mark.parametrize("path", ["/terms", "/privacy"])
def test_the_page_is_in_the_root_index(client, path):
    """The item's acceptance: both in the root /llms.txt index."""
    root = client.get("/llms.txt", user_agent=CRAWLER_UA)
    assert root.status == 200
    assert f"{path}/llms.txt" in root.text or path in root.text, (
        f"{path} is missing from the root corpus index"
    )


@pytest.mark.parametrize("path", ["/terms", "/privacy"])
def test_the_rendered_page_is_built_from_the_same_string(app_module, path):
    """The browser lane renders the SAME source, not a second copy.

    Asserted through the HEADING SLUGS markdown2dash derives from the source
    text, rather than by looking for prose. `conftest.layout_text` collects
    string-valued PROPS, and markdown2dash nests its paragraph text inside
    child lists, so a prose search finds class names and hrefs and no
    sentences — it would have failed on a page that renders perfectly.

    The slugs are a stronger binding anyway: each is computed from a heading
    in the source string, so if the browser lane were fed a different
    document its section slugs could not match this one's headings.
    """
    import importlib
    import re

    import dash

    from conftest import layout_text, page_layout

    module = importlib.import_module(f"pages.{path.strip('/')}")
    entry = next(e for e in dash.page_registry.values() if e["path"] == path)
    rendered = layout_text(page_layout(entry))

    headings = re.findall(r"^##\s+(.+)$", module.LLMS_DOC, re.M)
    assert len(headings) >= 4, f"{path}: only {len(headings)} headings to check"

    missing = []
    for heading in headings:
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        if slug not in rendered:
            missing.append(slug)
    assert missing == [], (
        f"{path}: headings from LLMS_DOC absent from the rendered page "
        f"{missing} — the two lanes are not the same source"
    )


# ---------------------------------------------------------------- the nav ---

def test_legal_is_a_category_and_both_pages_are_in_it(app_module):
    import dash

    from lib.constants import CATEGORY_ORDER

    assert "Legal" in CATEGORY_ORDER
    in_legal = {e["path"] for e in dash.page_registry.values()
                if e.get("category") == "Legal"}
    assert in_legal == {"/terms", "/privacy"}, in_legal


def test_the_footer_links_them(app_module):
    from components.footer import create_footer

    text = str(create_footer())
    assert "/terms" in text and "/privacy" in text
