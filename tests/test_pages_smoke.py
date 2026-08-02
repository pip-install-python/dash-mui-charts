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

# Pages that read MUI_PRO_API_KEY at module import (home only mentions it in
# prose). Measured 2026-08-02; a page gaining or losing the dependency should
# change this deliberately.
PRO_PAGE_COUNT = 17


def _pro_modules():
    return sorted(
        p.name for p in (REPO_ROOT / "pages").glob("*.py")
        if p.name != "home.py" and "MUI_PRO_API_KEY" in p.read_text()
    )


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


def test_the_pro_page_census_is_stable():
    assert len(_pro_modules()) == PRO_PAGE_COUNT, _pro_modules()


def test_pro_pages_degrade_not_die(client, pages):
    """With no license key every Pro page must still import, construct and
    serve — showing its license banner or an unlicensed chart, never a
    traceback. This posture is what lets CI run with zero secrets."""
    by_module = {entry["module"].rsplit(".", 1)[-1] + ".py": (path, entry)
                 for path, entry in pages}
    for module_name in _pro_modules():
        assert module_name in by_module, f"{module_name} registered no page"
        path, entry = by_module[module_name]
        assert page_layout(entry) is not None, f"{path} has no layout"
        assert client.get(path).ok, f"{path} does not serve without a key"


def test_pro_pages_with_banners_show_them(pages):
    """The pages that explain the missing key must actually say so when it
    is missing — the banner is the difference between "degraded" and
    "silently broken" for a reader."""
    by_module = {entry["module"].rsplit(".", 1)[-1] + ".py": entry
                 for _path, entry in pages}
    silent = []
    for module_name in _pro_modules():
        source = (REPO_ROOT / "pages" / module_name).read_text()
        if "MUI_PRO_API_KEY environment variable" not in source:
            continue  # this page degrades without a banner — fine
        if "MUI_PRO_API_KEY" not in layout_text(page_layout(by_module[module_name])):
            silent.append(module_name)
    assert silent == [], (
        f"banner pages whose keyless layout shows no banner: {silent}"
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


def test_the_sidebar_is_the_library_dogfooding_itself(app, page_paths):
    """The nav is a dash_mui_charts.SimpleTreeView (id `nav-tree`) — keeping
    it IS the point. And every leaf it navigates to must be a registered
    route, or a sidebar click 404s."""
    from conftest import component_iter

    trees = [c for c in component_iter(app.layout)
             if getattr(c, "id", None) == "nav-tree"]
    assert len(trees) == 1, "the nav-tree SimpleTreeView is gone"
    tree = trees[0]
    assert tree._namespace == "dash_mui_charts"

    leaves = []

    def walk(items):
        for item in items or []:
            if item.get("children"):
                walk(item["children"])
            elif item["itemId"].startswith("/"):
                leaves.append(item["itemId"])

    walk(tree.items)
    dead = sorted(set(leaves) - set(page_paths))
    assert dead == [], f"nav leaves with no registered route: {dead}"


def test_the_analytics_sink_and_license_store_exist(app):
    from conftest import component_iter

    # String ids only — the ad slot's pattern-matching dict id is unhashable.
    ids = {c.id for c in component_iter(app.layout)
           if isinstance(getattr(c, "id", None), str)}
    assert "analytics-sink" in ids, "the SPA page-view callback lost its sink"
    assert "license-key-store" in ids


def test_the_floating_ad_slot_is_wired(app):
    """The intentional ad_client fork: ONE static shell slot driven by the
    url callback (the canonical MATCH mount-callback double-logged
    impressions here). The slot's pattern id must survive."""
    from conftest import component_iter

    slots = [c for c in component_iter(app.layout)
             if isinstance(getattr(c, "id", None), dict)
             and c.id.get("type") == "net-ad-container"]
    assert len(slots) == 1, f"expected one shell ad slot, found {len(slots)}"
    assert slots[0].id.get("page") == "__floating__"


# ---------------------------------------------------------- asset contracts --


def test_the_functions_registry_is_intact():
    """assets/muiChartsFunctions.js is the runtime contract for every
    `valueFormatter={'function': 'formatDate', ...}` example — deleting or
    renaming it breaks chart axes on a dozen pages with no server error."""
    src = (REPO_ROOT / "assets" / "muiChartsFunctions.js").read_text()
    assert "dashMuiChartsFunctions" in src
    assert "formatDate" in src


def test_the_asset_load_order_still_wins_the_race():
    """assets/00-loading-theme.js must sort FIRST among the JS assets — the
    00- prefix is the ordering mechanism, not decoration."""
    scripts = sorted(p.name for p in (REPO_ROOT / "assets").glob("*.js"))
    assert scripts[0] == "00-loading-theme.js", scripts
    assert "01-nav-restore.js" in scripts, "the nav-restore script is gone"


def test_the_liquid_glass_styles_exist():
    """Two pages (TimeClock Lab among them) die silently without these."""
    for name in ("liquid_glass.css", "liquid_glass_clock.css"):
        assert (REPO_ROOT / "assets" / name).exists(), f"assets/{name} missing"
