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

# 40 originals + /api (added in M5). CRAWLABLE pages only: the `pages`
# fixture excludes /admin/*, so the control board is not counted here and
# tests/test_control_board.py owns its assertions. scripts/smoke_test.py
# deliberately says 42 — it asks "which page modules import and render on
# this Dash version", where the board belongs. Two numbers, two questions.
EXPECTED_ROUTES = 41

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

# Since M3, EVERY Pro route explains the key requirement in-page — a
# keyless-only banner, or (on markdown-driven pages) a Pro admonition that
# names MUI_PRO_API_KEY permanently. Silent degradation to a watermarked
# chart with no explanation is no longer an allowed posture.
BANNER_ROUTES = set(PRO_ROUTES)


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
    network battery (LESSONS §11) — the field, not just the status. The
    payload shape is the boilerplate's lib/health.py (ok + backend), the
    fleet's shared probe contract."""
    response = client.get("/healthz")
    assert response.ok
    body = json.loads(response.text)
    assert body.get("ok") is True
    assert body.get("backend") == "flask"


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


def test_the_analytics_sink_is_retired(app):
    """The SPA page-view recorder retired with the trio retrofit (the
    fleet's one-measurement-rule pass): tracking is the request-level
    lib/analytics_tracker hook, wired in run.py. The sink store coming
    back means the second, SPA-side counting path came back with it —
    and this host's numbers stop being comparable to the fleet's."""
    from conftest import component_iter

    # String ids only — ad slots' pattern-matching dict ids are unhashable.
    ids = {c.id for c in component_iter(app.layout)
           if isinstance(getattr(c, "id", None), str)}
    assert "analytics-sink" not in ids, "the retired SPA page-view sink is back"


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


def test_healthz_identity_fields(monkeypatch):
    """`build` says which commit answered, `app` says which satellite —
    different questions on a fleet where every host shares one template and
    a hostname can be repointed between services.

    `build` is what cd.yml's wait polls before it will verify a deploy: the
    platform keeps the previous instance answering throughout a build, and
    a disk-backed service restarts with a blip rather than overlapping, so
    a bare 200 proves nothing about WHICH build answered. This repo shipped
    the field as `commit` in the CD fix of 2026-08-21; the template adopted
    the idea under the fleet's name, and the floor round moved it here.

    Both stay OPTIONAL in the sense that matters: with no platform variable
    `build` is omitted entirely, and `app` degrades to "unknown" rather
    than disappearing — the payload never grows an error flag for a host
    that simply predates a diagnostic.
    """
    from lib.health import health_payload

    monkeypatch.setenv("RENDER_GIT_COMMIT", "cafebabe")
    monkeypatch.setenv("SATELLITE_APP_KEY", "muicharts")
    payload = health_payload("flask")
    assert payload["build"] == "cafebabe"
    assert payload["app"] == "muicharts"
    # The shape the fleet's probe contract depends on is untouched.
    assert payload["ok"] is True and payload["backend"] == "flask"

    monkeypatch.delenv("SATELLITE_APP_KEY")
    assert health_payload("flask")["app"] == "unknown"

    monkeypatch.delenv("RENDER_GIT_COMMIT")
    assert "build" not in health_payload("flask")


def test_healthz_is_live_not_a_snapshot(monkeypatch):
    """The payload must be built per request, not closed over at registration.

    A snapshot was harmless while every field was static and silently wrong
    the moment one is not: on llms-2plot-dev the route is registered before
    configure_geo runs, so a snapshot reported the geo guardrail
    unconfigured on a host where it IS configured — the diagnostic lying in
    exactly the situation it exists for (found 2026-08-23, fixed fork-side
    first, then upstream in template 1.6.10).
    """
    from types import SimpleNamespace

    from flask import Flask

    from lib.health import register_health_route

    monkeypatch.setenv("SATELLITE_APP_KEY", "before")
    stub = SimpleNamespace(server=Flask("healthz_snapshot_pin"))
    register_health_route(stub, "flask")
    probe = stub.server.test_client()
    assert probe.get("/healthz").get_json()["app"] == "before"

    monkeypatch.setenv("SATELLITE_APP_KEY", "after")
    assert probe.get("/healthz").get_json()["app"] == "after"


def test_healthz_geo_block_is_counts_not_codes():
    """Present on dash-improve-my-llms >= 2.7.0 (counts and flags only — a
    health endpoint is not where anyone learns policy), OMITTED on older
    packages rather than error-flagged: a host on an older floor is not
    broken, it predates the diagnostic.

    Its ABSENCE in production is also the fleet's stale-image alarm: a host
    that deployed but kept a cached dependency layer answers without a geo
    block, which says the floor bump never reached the image.
    """
    from lib.health import health_payload

    payload = health_payload("flask")
    try:
        from dash_improve_my_llms import geo  # noqa: F401
    except ImportError:
        assert "geo" not in payload
    else:
        block = payload["geo"]
        assert isinstance(block["configured"], bool)
        assert isinstance(block["denied"], int), "counts, never country codes"
