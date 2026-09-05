"""The accessibility / agentic block — sync 1.6.44 item 6.

Each sub-item is pinned where a pin can actually see it. Where the template's
finding did NOT reproduce here, that is recorded rather than assumed (6d), and
where a decision was taken rather than a fix applied, the decision is what the
test asserts.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HEADER = REPO_ROOT / "components" / "header.py"
FOOTER = REPO_ROOT / "components" / "footer.py"
MAIN_CSS = REPO_ROOT / "assets" / "main.css"


# Item 13's rule, applied to this file's own detects — and applied because
# the first draft tripped over it twice. The commit that fixes `trigger=
# "hover"` naturally contains a COMMENT saying `trigger="hover"` was the
# defect, and the CSS comment above the coarse-pointer rule names
# `pointer: coarse`. A raw substring check therefore reported both fixes as
# defects. Parse the construct; do not grep the file.

def _trigger_values(path: Path) -> list[str]:
    """Every literal `trigger=` keyword argument in a module's real CODE."""
    import ast

    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "trigger" and isinstance(kw.value, ast.Constant):
                    out.append(kw.value.value)
    return out


def _css_without_comments(text: str) -> str:
    """CSS with `/* ... */` removed, so prose cannot answer for a rule."""
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


# ---------------------------------------------------------------- 6a: menu --

def test_no_chrome_menu_is_pointer_only():
    """`trigger="hover"` is operable by pointer and NOTHING else.

    The target was already a real Button, which is what made this easy to
    miss — the control looked accessible. But a keyboard user could tab to it
    and never open it, and a touch user got a menu depending on a hover state
    their device does not have.
    """
    for path in (HEADER, FOOTER):
        assert "hover" not in _trigger_values(path), (
            f"{path.name}: a chrome menu is pointer-only"
        )


def test_the_menu_is_still_wired_to_something():
    """Non-vacuity: the fix must be a working trigger, not a deleted one.

    Removing the line entirely would also pass the test above while leaving
    the menu on DMC's default — this pins that the click trigger is explicit.
    """
    assert "click" in _trigger_values(HEADER)


# ------------------------------------------------------ 6b: prose underline --

def test_prose_underline_is_scoped_to_the_document():
    """Underlining every anchor is right; doing it globally repaints chrome.

    The navbar rows, the header's icon anchors and the footer's link groups
    are all anchors, and they are already distinguishable by position and
    shape. A bare `a { text-decoration: underline }` would restyle all of
    them.
    """
    css = _css_without_comments(MAIN_CSS.read_text())
    assert ".m2d-block a" in css, "no scoped prose-link rule"

    # No unscoped global anchor underline.
    bare = re.findall(r"(?m)^\s*a\s*\{[^}]*text-decoration:\s*underline",
                      css)
    assert bare == [], f"a global anchor underline would repaint the chrome: {bare}"


# ----------------------------------------------------------- 6c: touch size --

def test_touch_targets_reach_44px_at_coarse_pointer():
    """ActionIcon size="lg" computes to 34px — under the 44px minimum.

    The whole site chrome is built from those, so on a phone every header and
    footer control was below the minimum while the mobile drawer's rows,
    which already carried the rule, were not.
    """
    css = _css_without_comments(MAIN_CSS.read_text())
    assert "pointer: coarse" in css, "no coarse-pointer touch-target rule"
    block = css.split("pointer: coarse", 1)[1]
    assert "min-height: 44px" in block and "min-width: 44px" in block


def test_the_touch_rule_is_not_applied_to_fine_pointers():
    """Scoping matters: inflating a 34px icon button to 44px on a desktop
    changes the header's proportions for no accessibility gain."""
    css = _css_without_comments(MAIN_CSS.read_text())
    idx = css.index("pointer: coarse")
    # The rule must live inside a media query, not at top level.
    assert "@media" in css[max(0, idx - 80):idx]


# --------------------------------------------------------------- 6d: record --

def test_6d_is_recorded_as_not_reproduced():
    """The item says: NOT REPRODUCED on the template — record, do not assume.

    It does not reproduce here either, and the record lives in DIVERGENCES.md
    so a future sync does not "restore" a fix for a defect this fork never
    had. A test docstring is invisible to the fan-out; the file is not.
    """
    text = (REPO_ROOT / "DIVERGENCES.md").read_text()
    assert "6d" in text, "sub-item 6d has no recorded outcome"


# ------------------------------------------------------------- 6f: img props --

@pytest.mark.parametrize("prop", ["loading", "decoding"])
def test_dash_really_raises_on_the_props_that_cannot_ship(prop):
    """The REASON 6f is width/height only, measured on the resolved Dash.

    Neither is a prop of dash 4.4.1's html.Img and Dash RAISES on an unknown
    one — 196 collection errors, not a warning. Pinned as a measurement so
    that if a future Dash accepts them, this goes red and the decision is
    revisited deliberately instead of by someone's guess.
    """
    from dash import html

    with pytest.raises(TypeError):
        html.Img(src="x", **{prop: "lazy"})


def test_no_image_in_this_tree_carries_them():
    """The pin the item asks to port — the attributes themselves never ship."""
    hits = []
    for py in list((REPO_ROOT / "lib").rglob("*.py")) + \
            list((REPO_ROOT / "components").rglob("*.py")) + \
            list((REPO_ROOT / "pages").rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        src = py.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"html\.Img\((.*?)\)", src, re.S):
            if re.search(r"\b(loading|decoding)\s*=", m.group(1)):
                hits.append(str(py.relative_to(REPO_ROOT)))
    assert hits == [], f"html.Img with a prop Dash raises on: {hits}"


def test_the_one_image_reserves_its_box_some_other_way():
    """6f's GOAL is no layout shift; width/height is only one route to it.

    This tree's single html.Img is the ad creative, whose dimensions are not
    known at render time (src is filled by a callback), so intrinsic
    width/height attributes cannot be written. It reserves the box with
    aspectRatio instead, which achieves the same thing for an unknown source
    — asserted here so the reservation is not silently dropped.
    """
    src = (REPO_ROOT / "lib" / "ad_client.py").read_text()
    assert "aspectRatio" in src


# ------------------------------------------------------------ 6g: asset cache --

def test_assets_get_a_lifetime_and_documents_do_not():
    from lib.static_cache import cache_control_for

    assert cache_control_for("/assets/main.css")
    for document in ("/", "/llms.txt", "/healthz", "/api", "/admin/traffic",
                     "/_dash-component-suites/dash/x.js"):
        assert cache_control_for(document) is None, document


def test_the_lifetime_is_finite_and_revalidates():
    """An unfingerprinted asset must not be cached immutably.

    `main.css` keeps its name across deploys, so the lifetime is the longest
    a CSS fix may take to reach a returning reader — `immutable` here would
    strand them.
    """
    from lib.static_cache import ASSET_CACHE_CONTROL

    assert "immutable" not in ASSET_CACHE_CONTROL
    assert "max-age=" in ASSET_CACHE_CONTROL
    assert "stale-while-revalidate=" in ASSET_CACHE_CONTROL


# A bare test client sends `Werkzeug/x.y`, which is crawler-lane at dimll
# >= 2.8 — so every in-process fetch names its UA. tests/test_nav_contract.py
# pins this repo-wide and caught these two on their first run.
_UA = {"User-Agent": (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)}


def test_the_hook_sets_the_header_on_an_asset(app):
    """End to end through the real app, not just the pure function."""
    raw = app.server.test_client()
    r = raw.get("/assets/main.css", headers=_UA)
    if r.status_code != 200:
        pytest.skip("this checkout does not serve /assets/main.css")
    assert "max-age=3600" in r.headers.get("Cache-Control", "")


def test_the_hook_leaves_documents_alone(app):
    raw = app.server.test_client()
    r = raw.get("/healthz", headers=_UA)
    assert r.status_code == 200
    assert "max-age=3600" not in r.headers.get("Cache-Control", "")
