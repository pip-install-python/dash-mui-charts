"""Route smoke + the preservation invariants of the network-standard pass.

The exact-tree route-parity gate lives in scripts/route_parity.py and needs
the real MUI_PRO_API_KEY (its baseline was recorded with Pro charts mounted).
CI is secretless BY DESIGN (LESSONS §18), so this suite asserts the layer
below exact parity: every page module imports, every layout constructs,
every route serves 200, and the 17 Pro pages DEGRADE rather than die — the
zero-secret posture is the test, not a limitation.

The second half pins the app-shell invariants the kickoff names: the three
subsystems hanging off `dcc.Location(id="url")`, the SimpleTreeView sidebar
(the library dogfooding itself), and the asset contracts that fail silently
(muiChartsFunctions.js, the 00- asset ordering, the liquid-glass CSS two
pages die without).
"""
from __future__ import annotations

import json

from conftest import CRAWLER_UA, REPO_ROOT, STUB_MARKER, layout_text, page_layout

EXPECTED_ROUTES = 40

# Routes whose demos read MUI_PRO_API_KEY (17, measured 2026-08-02). Pinned
# by ROUTE, not by source file: the boilerplate migration moves a page's
# key-reading code from pages/<x>.py into N exec modules under docs/, but
# the route's degradation obligation never moves.
PRO_ROUTES = [
    "/barchart-pro", "/composite", "/composite-render-bp", "/composite-v120",
    "/crosshair", "/heatmap", "/heatmap-props", "/highlighting-sync",
    "/linechart-basic", "/linechart-brush", "/linechart-highlighting",
    "/linechart-pro", "/linechart-referencelines", "/linechart-tick-hover",
    "/linechart-zoom-preview", "/live-trading", "/tree-pro",
]

# The subset that explains the missing key IN the page (a visible banner in
# the keyless layout). The others degrade to unlicensed charts silently.
BANNER_ROUTES = {
    "/barchart-pro", "/heatmap", "/heatmap-props", "/linechart-brush",
    "/linechart-pro", "/tree-pro",
}


# ------------------------------------------------------------- route smoke --


def test_the_full_route_set_is_registered(page_paths):
    assert len(page_paths) == EXPECTED_ROUTES, (
        f"{len(page_paths)} routes registered — a page module failed to "
        f"import, or one was added without updating this gate: {page_paths}"
    )
    assert "/" in page_paths
    assert "/changelog" in page_paths


def test_every_layout_constructs_without_secrets(pages):
    """Module-level layouts are built at import with whatever env exists —
    this proves all 40 build with NONE."""
    broken = []
    for path, entry in pages:
        layout = page_layout(entry)
        if layout is None:
            broken.append(path)
    assert broken == [], f"pages with no constructible layout: {broken}"


def test_every_route_serves_200(client, page_paths):
    failing = {}
    for path in page_paths:
        status = client.get(path).status
        if status != 200:
            failing[path] = status
    assert failing == {}, failing


def test_healthz_returns_ok_true(client):
    """A 200 with different JSON is a deploy-blocking "unhealthy" to the
    network battery (LESSONS §11) — the field, not just the status."""
    response = client.get("/healthz")
    assert response.ok
    body = json.loads(response.text)
    assert body.get("ok") is True
    assert body.get("app") == "muicharts"


def test_dash_plumbing_answers(client):
    assert client.get("/_dash-layout").ok
    assert client.get("/_dash-dependencies").ok


def test_the_changelog_page_reads_its_file(client, pages):
    """pages/changelog.py is the only module in pages/ with a filesystem
    dependency (it renders CHANGELOG.md from disk) — the page that breaks
    first when the working directory or the file moves."""
    entry = dict(pages)["/changelog"]
    text = layout_text(page_layout(entry))
    assert "Changelog" in text or "changelog" in text
    assert client.get("/changelog").ok


def test_a_crawler_gets_prose_not_the_stub(client):
    """The dimll prerender path: a crawler that receives the JavaScript stub
    indexes nothing, while the page looks perfect in a browser."""
    response = client.get("/", user_agent=CRAWLER_UA)
    assert response.ok
    assert STUB_MARKER not in response.text


# --------------------------------------------------------- Pro degradation --


def test_every_pro_route_is_still_registered(page_paths):
    missing = sorted(set(PRO_ROUTES) - set(page_paths))
    assert missing == [], f"Pro routes gone from the registry: {missing}"


def test_pro_routes_degrade_not_die(client, pages):
    """With no license key every Pro route must still construct and serve —
    showing its license banner or an unlicensed chart, never a traceback.
    This posture is what lets CI run with zero secrets."""
    by_path = dict(pages)
    for path in PRO_ROUTES:
        assert page_layout(by_path[path]) is not None, f"{path} has no layout"
        assert client.get(path).ok, f"{path} does not serve without a key"


def test_banner_routes_show_their_banner(pages):
    """The routes that explain the missing key must actually say so when it
    is missing — the banner is the difference between "degraded" and
    "silently broken" for a reader. Set equality both ways: a banner
    disappearing is a regression, a banner appearing is a deliberate
    improvement that updates BANNER_ROUTES."""
    by_path = dict(pages)
    showing = {
        path for path in PRO_ROUTES
        if "MUI_PRO_API_KEY" in layout_text(page_layout(by_path[path]))
    }
    assert showing == BANNER_ROUTES, (
        f"missing banner: {sorted(BANNER_ROUTES - showing)}; "
        f"new banner (update BANNER_ROUTES): {sorted(showing - BANNER_ROUTES)}"
    )


# ------------------------------------------------------ shell invariants ----


def test_the_url_location_contract(app):
    """`dcc.Location(id="url", refresh="callback-nav")` is load-bearing for
    THREE subsystems — navigation, register_shell_ad, and the SPA page-view
    counter. The id changing breaks all three at once, silently."""
    from conftest import component_iter

    locations = [c for c in component_iter(app.layout)
                 if getattr(c, "id", None) == "url"]
    assert len(locations) == 1, "the url dcc.Location is gone or duplicated"
    assert getattr(locations[0], "refresh", None) == "callback-nav"


def test_the_navbar_families_cover_the_registry_exactly(page_paths):
    """The family map in components/navbar.py is the nav order authority
    (what page_order is to the boilerplate). Every mapped path must be a
    registered route (or a sidebar click 404s), and every registered route
    must be mapped (or it renders in the unsorted "Other" section)."""
    from components.navbar import FAMILIES, TOP_LINKS

    mapped = {p for _t, entries in FAMILIES for p, _label, _icon in entries}
    mapped |= {p for p, _label, _icon in TOP_LINKS}
    dead = sorted(mapped - set(page_paths))
    assert dead == [], f"nav entries with no registered route: {dead}"
    unmapped = sorted(set(page_paths) - mapped)
    assert unmapped == [], (
        f"registered routes missing from the navbar family map: {unmapped}"
    )


def test_the_analytics_sink_exists(app):
    """The SPA page-view recorder's output target. (The old shell's
    license-key-store retired with it — pages read MUI_PRO_API_KEY from the
    environment directly; the store was dead plumbing.)"""
    from conftest import component_iter

    # String ids only — ad slots' pattern-matching dict ids are unhashable.
    ids = {c.id for c in component_iter(app.layout)
           if isinstance(getattr(c, "id", None), str)}
    assert "analytics-sink" in ids, "the SPA page-view callback lost its sink"


def test_ad_slots_are_per_page_asides_not_a_shell_slot(app, pages):
    """The boilerplate ad architecture: pages/markdown.py injects one slot
    into each markdown page's TOC aside, attributed to that page's endpoint;
    the mount-fired MATCH callback serves it per view. The old floating
    shell slot (and the fork that existed to de-duplicate it) is retired —
    a "__floating__" slot reappearing means the fork came back too."""
    from conftest import component_iter

    shell_slots = [c for c in component_iter(app.layout)
                   if isinstance(getattr(c, "id", None), dict)
                   and c.id.get("type") == "net-ad-container"]
    assert shell_slots == [], "a static shell ad slot is back"

    # markdown.py registers pages under their display NAME (not a pages.*
    # module path) — that asymmetry is the marker for markdown-driven pages.
    ported = [(path, entry) for path, entry in pages
              if not entry["module"].startswith("pages.")]
    assert ported, "no markdown-driven pages registered yet?"
    for path, entry in ported:
        slots = [c for c in component_iter(page_layout(entry))
                 if isinstance(getattr(c, "id", None), dict)
                 and c.id.get("type") == "net-ad-container"]
        assert len(slots) == 1, f"{path}: expected one aside ad slot"
        assert slots[0].id.get("page") == path, (
            f"{path}: ad slot attributed to {slots[0].id.get('page')!r}"
        )


# ---------------------------------------------------------- asset contracts --


def test_the_functions_registry_is_intact():
    """assets/muiChartsFunctions.js is the runtime contract for every
    `valueFormatter={'function': 'formatDate', ...}` example — deleting or
    renaming it breaks chart axes on a dozen pages with no server error."""
    src = (REPO_ROOT / "assets" / "muiChartsFunctions.js").read_text()
    assert "dashMuiChartsFunctions" in src
    assert "formatDate" in src


def test_the_old_shell_assets_stay_deleted(app):
    """00-loading-theme.js and 01-nav-restore.js served the RETIRED shell:
    the theme script applied a stale `mantine-color-scheme-value`
    localStorage key that would fight the boilerplate shell's
    color-scheme-storage system on every load, and nav-restore set props on
    a nav-tree that no longer exists. Their return means two theme systems
    disagreeing about dark mode."""
    from conftest import component_iter

    scripts = {p.name for p in (REPO_ROOT / "assets").glob("*.js")}
    assert "00-loading-theme.js" not in scripts
    assert "01-nav-restore.js" not in scripts
    # The replacement: the appshell's persisted color-scheme store.
    ids = {c.id for c in component_iter(app.layout)
           if isinstance(getattr(c, "id", None), str)}
    assert "color-scheme-storage" in ids, "the theme persistence store is gone"


def test_the_liquid_glass_styles_exist():
    """Two pages (TimeClock Lab among them) die silently without these."""
    for name in ("liquid_glass.css", "liquid_glass_clock.css"):
        assert (REPO_ROOT / "assets" / name).exists(), f"assets/{name} missing"
