"""The navigation contract (1.6.38) — uniform where it must be, free where it may.

Owner's brief of 2026-08-30 (DESIGN-navigation-uniformity): the sidebar's
sections come from frontmatter against CATEGORY_ORDER; the network is ONE
registry rendered as the top bar's Other Apps menu; Resources is one
constant; Admin is owner-only and absent from the tree otherwise; every
icon-only control has a name; no `dcc.*` where DMC has the component. Each
pin here is one line of that brief.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
ALLOWED_DCC = {"Location", "Store", "Interval", "Upload", "Graph"}


def _calls(src: str, name: str):
    """Yield the source text of every `name(` call, parens balanced."""
    for m in re.finditer(re.escape(name) + r"\(", src):
        depth, i = 0, m.start()
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    yield src[m.start():i + 1]
                    break
            i += 1


# ------------------------------------------------------------- a11y --


@pytest.mark.parametrize("control", ["dmc.Burger", "dmc.ActionIcon"])
def test_every_icon_only_control_in_components_has_a_name(control):
    """Requirement 9: the audits named the unlabelled Burger and copy
    button. Every Burger/ActionIcon in components/ carries aria-label."""
    unlabelled = []
    for path in sorted((REPO / "components").glob("*.py")):
        for call in _calls(path.read_text(), control):
            if "aria-label" not in call:
                unlabelled.append(f"{path.name}: {call[:60]}…")
    assert unlabelled == [], unlabelled


def test_code_highlight_copy_button_has_a_name():
    src = (REPO / "lib" / "directives" / "source.py").read_text()
    assert "copyLabel=" in src and "copiedLabel=" in src


def test_no_dcc_where_dmc_has_the_component():
    """Requirement 10, fleet-wide: `dcc.` only for Location, Store,
    Interval, Upload, Graph (no DMC equivalent)."""
    offenders = []
    for folder in ("pages", "components"):
        for path in sorted((REPO / folder).glob("*.py")):
            code = "\n".join(line for line in path.read_text().splitlines()
                             if not line.lstrip().startswith("#"))
            for m in re.finditer(r"\bdcc\.([A-Za-z]+)", code):
                if m.group(1) not in ALLOWED_DCC:
                    offenders.append(f"{folder}/{path.name}: dcc.{m.group(1)}")
    assert offenders == [], offenders


def test_the_traffic_page_uses_a_date_picker_not_a_dropdown():
    src = (REPO / "pages" / "traffic.py").read_text()
    assert "dcc.Dropdown" not in src
    assert "dmc.DatePickerInput" in src and 'valueFormat="YYYY-MM-DD"' in src
    assert "presets=" in src and "minDate=" in src and "maxDate=" in src


# --------------------------------------------------------- registry --


def test_other_apps_menu_is_the_registrys_primary_set(app_module):
    """Requirement 4 + the owner's review (2026-08-30): the PRIMARY
    applications only — never the docs subdomains — from the registry,
    no duplicates, self omitted, short labels (the domain)."""
    from components.header import create_other_apps_menu
    from lib.constants import BASE_URL
    from lib.network_directory import AFFILIATED, PEERS, PRIMARY, other_apps_for

    menu = create_other_apps_menu()
    items = menu.children[1].children
    hrefs = [i.href for i in items]
    expected = [e["url"] for e in other_apps_for(BASE_URL)]
    assert hrefs == expected
    assert set(h.rstrip("/") for h in hrefs) == PRIMARY - {BASE_URL.rstrip("/")}
    assert {"https://2plot.ai", "https://2plot.dev", "https://2plot.media",
            "https://piratesbargain.com", "https://ai-agent.buzz"} == set(PRIMARY)
    assert PRIMARY <= {e["url"].rstrip("/") for e in PEERS + AFFILIATED}, "PRIMARY names a URL the registry lacks"
    assert not any(".2plot.dev" in h for h in hrefs), "a docs subdomain leaked into the menu"
    assert len(set(hrefs)) == len(hrefs), "a host is listed twice"
    for item in items:
        label = item.children
        assert "." in label and " " not in label and "—" not in label, label
        assert item.target == "_blank"


def test_resources_are_third_party_only():
    """Owner's review (2026-08-30): the sidebar's Resources holds dmc and
    the upstream project only; the owner's own links are top bar + footer."""
    from lib.constants import DISCORD_URL, GITHUB_URL, YOUTUBE_URL, resources

    items = resources()
    assert items[0]["label"] == "dmc" and items[0]["url"] == "https://www.dash-mantine-components.com/"
    urls = [r["url"] for r in items]
    for banned in (GITHUB_URL, DISCORD_URL, YOUTUBE_URL, "github.com", "discord", "youtube",
                   "community.plotly.com", "https://2plot.dev"):
        assert not any(banned in u for u in urls), banned


def test_github_icon_and_same_as_share_one_constant(app_module):
    from components.header import create_header
    from lib.constants import GITHUB_URL, SAME_AS

    assert GITHUB_URL in SAME_AS
    assert GITHUB_URL.startswith("https://github.com/pip-install-python/")
    assert GITHUB_URL.count("/") == 4, "the REPOSITORY, not the profile"
    assert GITHUB_URL in str(create_header([]))


# ---------------------------------------------------------- sidebar --


def test_sections_follow_category_order_and_never_hold_admin(app_module):
    import dash

    from components.navbar import sections_for
    from lib.constants import CATEGORY_ORDER

    data = list(dash.page_registry.values())
    sections = sections_for(data)
    titles = [t for t, _ in sections]
    known = [t for t in titles if t in CATEGORY_ORDER]
    assert known == [c for c in CATEGORY_ORDER if c in titles], titles
    for _, entries in sections:
        assert not any(e["path"].startswith("/admin/") for e in entries)
        assert not any(e["path"] in ("/", "/changelog", "/api") for e in entries)
    # the template's own docs all declare a category
    assert "Documentation" not in titles, "a docs page lost its category: frontmatter"


def test_frontmatter_order_sorts_within_a_section(app_module):
    import dash

    from components.navbar import sections_for

    for title, entries in sections_for(dash.page_registry.values()):
        orders = [int(e.get("order") or 1000) for e in entries]
        assert orders == sorted(orders), (title, orders)


def test_anonymous_tree_has_no_admin_href(app_module, monkeypatch):
    """Requirement 7: hidden, not blocked. The startup tree carries only an
    empty Admin placeholder; the callback returns nothing to a non-admin."""
    import dash

    from components.navbar import create_content, render_admin_section

    tree = str(create_content(dash.page_registry.values()))
    assert "/admin/" not in tree
    assert "navbar-admin-desktop" in tree
    monkeypatch.delenv("ALLOW_UNGATED_ADMIN", raising=False)
    assert render_admin_section("navbar-admin-desktop") == (None, None)


def test_admin_tree_lists_every_admin_page(app_module, monkeypatch):
    from components.navbar import render_admin_section

    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "1")
    desktop, mobile = render_admin_section("navbar-admin-desktop")
    text = str(desktop)
    assert "/admin/control-board" in text and "/admin/traffic" in text
    assert str(mobile) == text


def test_search_lists_only_sidebar_pages(app_module):
    import dash

    from components.navbar import search_data

    values = [d["value"] for d in search_data(dash.page_registry.values())]
    assert values and not any(v.startswith("/admin/") for v in values)
    assert "/" not in values and "/changelog" not in values


# ---------------------------------------------------------- footer --


def test_footer_is_the_contract(app_module):
    from datetime import datetime

    from components.footer import create_footer
    from lib.constants import DISCORD_URL, GITHUB_PROFILE_URL, GITHUB_URL, YOUTUBE_SUBSCRIBE_URL

    text = str(create_footer())
    assert f"© {datetime.now().year} Pip Install Python LLC" in text
    for href in (GITHUB_PROFILE_URL, DISCORD_URL, YOUTUBE_SUBSCRIBE_URL):
        assert href in text
    assert GITHUB_URL not in text, "the repo link is the top bar's; the footer links the profile"
    assert "/changelog" not in text, "the sidebar's single Changelog link is the one"
    assert "/terms" not in text and "/privacy" not in text


# ------------------------------------------------------- changelog --


def test_changelog_page_is_the_file(app_module, client):
    from pages.changelog import parse_changelog

    versions = parse_changelog()
    newest = re.search(r"^## \[([^\]]+)\]", (REPO / "CHANGELOG.md").read_text(), re.M).group(1)
    assert versions and versions[0]["version"] == newest
    doc = client.get("/changelog/llms.txt", user_agent="Mozilla/5.0 (compatible; Googlebot/2.1)")
    assert doc.status == 200
    assert doc.text.startswith("# Changelog") and "\n# Changelog" not in doc.text, "the file's H1 was not deduplicated"
    assert f"## [{newest}]" in doc.text
    page = client.get("/changelog", user_agent="Mozilla/5.0 (compatible; Googlebot/2.1)")
    assert page.status == 200 and newest in page.text


# ------------------------------------------------------------- api --


def test_the_api_page_documents_the_declared_package(app_module, client):
    """Contract 7, PORTED (see DIVERGENCES): this fork does not use the
    template's generated pages/api.py + lib/api_reference generator. `/api`
    is a markdown doc whose `.. kwargs::` directive builds one table per
    component from the SAME source the generator would read — the installed
    package's own metadata — so the page cannot disagree with the wheel the
    docs image installs from this tree.

    THIS TEST WAS VACUOUS UNTIL 2026-08-30 and let a real defect ship. It
    asserted that each component NAME appeared in the layout and in
    /api/llms.txt. Both were true with ZERO property rows anywhere: the
    names come from the page's own `### LineChart` headings. Assert the
    ROWS, and assert a row's CONTENT — a table with headers and no body is
    exactly what shipped.
    """
    import dash

    from lib.constants import API_PACKAGES

    assert API_PACKAGES == ["dash_mui_charts"]
    assert "/api" in [p["path"] for p in dash.page_registry.values()]

    entry = next(p for p in dash.page_registry.values() if p["path"] == "/api")
    layout = entry["layout"]
    tree = str(layout() if callable(layout) else layout)

    import dash_mui_charts

    exported = [n for n in dash_mui_charts.__all__ if n[:1].isupper()]
    assert exported, "the package exports no components"
    missing = [n for n in exported if n not in tree]
    assert missing == [], f"components with no table on /api: {missing}"

    # ROWS, not headers. One table per component and a real body in each.
    assert tree.count("m2d-block-kwargs") == len(exported), (
        f"{tree.count('m2d-block-kwargs')} tables for {len(exported)} components"
    )
    assert tree.count("TableTr") > 20 * len(exported), (
        "the tables have no body rows — the props parse returned nothing"
    )
    # a prop that only the real docstring can supply
    assert "The ID used to identify this component in Dash callbacks." in tree


def test_the_api_props_reach_the_machine_lane_too(app_module, client):
    """THE DEFECT, pinned. A markdown2dash directive renders COMPONENTS, so
    `.. kwargs::` output lived only in the browser's React tree: on the wire
    2026-08-30, /api/llms.txt was 2681 bytes with zero table rows and the
    non-JS prerender had zero `<table>`, while a real Chrome showed 13
    tables and 371 rows. Every agent, every crawler and every reader without
    JavaScript got 13 headings and nothing under them.

    pages/markdown.py expands the directive into a markdown table for the
    lane built from the SOURCE, the same way it already did for
    `.. source::`. Both lanes read ONE parse (lib/api_reference).
    """
    import re

    from conftest import BROWSER_UA, CRAWLER_UA

    llms = client.get("/api/llms.txt", user_agent=CRAWLER_UA)
    assert llms.status == 200
    rows = [ln for ln in llms.text.split("\n")
            if ln.startswith("| ") and set(ln) - set("| -")]
    assert len(rows) > 100, f"only {len(rows)} markdown table rows in /api/llms.txt"
    assert rows[0] == "| Name | Type | Description |"
    assert any("The ID used to identify this component in Dash callbacks." in r
               for r in rows)
    # the raw directive must not survive into the prose either
    assert ".. kwargs::" not in llms.text

    crawler = client.get("/api", user_agent=CRAWLER_UA)
    assert crawler.text.count("<table") >= 13, "the crawler document has no tables"

    prerender = re.search(r'<div id="dimll-prerender".*?</div>\s*(?=<script|</body)',
                          client.get("/api", user_agent=BROWSER_UA).text, re.S)
    assert prerender and prerender.group(0).count("<table") >= 13, (
        "the non-JS prerender has no tables — a text reader still gets nothing"
    )


def test_the_two_lanes_report_the_same_number_of_props(app_module, client):
    """The parity that makes the fix durable: one parse, two renderings. If
    these ever disagree, someone has grown a second props implementation —
    which is the state that produced the original defect."""
    from conftest import CRAWLER_UA

    import dash

    entry = next(p for p in dash.page_registry.values() if p["path"] == "/api")
    layout = entry["layout"]
    browser_rows = str(layout() if callable(layout) else layout).count("TableTr")

    llms = client.get("/api/llms.txt", user_agent=CRAWLER_UA).text
    machine_rows = len([ln for ln in llms.split("\n")
                        if ln.startswith("| ") and set(ln) - set("| -")])

    assert browser_rows == machine_rows, (
        f"browser lane {browser_rows} rows, machine lane {machine_rows} — "
        "the lanes have drifted apart again"
    )


def test_every_kwargs_directive_in_the_docs_resolves(app_module):
    """A `.. kwargs::` naming a component that cannot be read renders as
    NOTHING in the browser (markdown2dash's render returns None on empty
    data) and as an HTML comment in the prose. Silence either way — so the
    emptiness has to be caught here."""
    import re
    from pathlib import Path

    from lib.api_reference import props_for

    repo = Path(__file__).resolve().parent.parent
    specs = []
    for md in sorted((repo / "docs").glob("**/*.md")):
        specs += re.findall(r"^\.\. kwargs::(.+?)$", md.read_text(), re.M)
    assert specs, "no .. kwargs:: directives found — this pin would be vacuous"
    empty = sorted({s.strip() for s in specs if not props_for(s.strip())})
    assert empty == [], f"kwargs directives that resolve to no props: {empty}"


def test_the_version_badge_reads_the_declared_package(app_module):
    """The badge stays (owner) and reads API_PACKAGES[0]'s version — the
    package the docs image installs from this same tree, so a demo page and
    the badge can never disagree. tests/test_version_parity.py owns the
    five-way drift gate; this pins only the nav contract's half."""
    from components.header import create_header
    from dash_mui_charts import __version__
    from lib.constants import API_PACKAGES

    assert API_PACKAGES[0] == "dash_mui_charts"
    assert f"v{__version__}" in str(create_header([]))


# ------------------------------------------------ 1.6.39 fix-forward --


def test_the_aside_collapses_on_pages_without_a_toc(app_module):
    """Owner's note 1: /changelog full width. Docs pages with `.. toc::`
    keep the column; everything else collapses it."""
    from lib.aside import aside_config, has_aside

    assert has_aside("/barchart-basic") and has_aside("/linechart-basic")
    # FORK NOTE: /api is a markdown doc here with its own `.. toc::`, so it
    # legitimately fills the aside — unlike the template's generated page.
    assert has_aside("/api")
    for path in ("/changelog", "/", "/admin/traffic", "/admin/control-board"):
        assert not has_aside(path), path
        assert aside_config(path)["collapsed"]["desktop"] is True
    assert aside_config("/barchart-basic")["collapsed"]["desktop"] is False
    assert aside_config(None)["collapsed"]["mobile"] is True


def test_the_mobile_drawer_is_always_mounted(app_module):
    """Owner's note 2: the burger must not depend on a mount-on-open
    transition, and #navbar-admin-mobile must exist on every load."""
    from components.navbar import create_navbar_drawer

    drawer = create_navbar_drawer([])
    assert drawer.keepMounted is True
    assert "navbar-admin-mobile" in str(drawer)


def test_code_blocks_cannot_widen_the_page():
    """Owner's note 3: the overflow rule lives in the stylesheet, for every
    container a code block can sit in — never a per-page fix."""
    css = (REPO / "assets" / "main.css").read_text()
    for selector in (".mantine-List-itemWrapper", ".mantine-List-itemLabel",
                     ".mantine-Timeline-itemBody", ".mantine-CodeHighlight-root",
                     ".mantine-CodeHighlightTabs-root", ".mantine-AppShell-main pre",
                     "table.m2d-block-kwargs", "code.m2d-codespan"):
        assert selector in css, selector
    # and the changelog's rows let an unbreakable code token wrap
    src = (REPO / "pages" / "changelog.py").read_text()
    assert '"overflowWrap": "anywhere"' in src and '"minWidth": 0' in src
    wrappers = css[css.index(".mantine-List-itemWrapper"):]
    assert "min-width: 0" in wrappers[:400]
    pre_rule = css[css.index(".mantine-AppShell-main pre"):]
    assert "overflow-x: auto" in pre_rule[:200]
    assert "overflow-wrap: anywhere" in css[css.index("code.m2d-codespan"):][:200]


def test_other_apps_dropdown_is_solid_and_every_primary_app_has_an_icon(app_module):
    """Seat's note 4."""
    from components.header import create_other_apps_menu
    from lib.network_directory import ICONS, PRIMARY

    dropdown = create_other_apps_menu().children[1]
    assert dropdown.styles["dropdown"]["backgroundColor"]
    for url in PRIMARY:
        assert ICONS.get(url) not in (None, "mdi:web"), f"{url} has no icon"


_REQUEST_METHODS = ("get", "post", "open", "request", "put", "delete", "head")


def _code_only(src: str) -> str:
    """Source with docstrings and `#` comments removed.

    muicharts, 2026-08-31: the words pass while the header is gone — its
    grep matched "User-Agent" inside an explanatory COMMENT, so deleting
    the real header left the pin green. This one proved the point on
    itself: the comment below describing the chained form made the pin
    flag its own file.
    """
    src = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', "", src)
    return re.sub(r"#[^\n]*", "", src)


def _client_names_a_ua(src: str, var: str) -> bool:
    """Does `var` — a bound `.test_client()` — name a UA on the wire?

    Either the client carries one for every request (`environ_base`), or
    every request call on it passes `headers=`. A client that issues no
    requests in this file cannot get the lane wrong here.
    """
    if re.search(re.escape(var) + r"\.environ_base\b[^\n]*HTTP_USER_AGENT", src):
        return True
    calls = [c for m in _REQUEST_METHODS for c in _calls(src, f"{var}.{m}")]
    return bool(calls) and all("headers=" in c for c in calls)


def test_every_test_client_user_names_headers():
    """Notes 70/74: a bare test client sends `Werkzeug/x.y` — crawler lane
    at dimll ≥ 2.8 — so a mark_hidden page 404s and an every-page-200 loop
    goes red at the floor bump. Any file that drives `.test_client()` must
    pass a named UA.

    Resolved per CALL SITE, not per file (pannellum, 2026-08-31): the
    substring form this pin shipped with — `"headers=" in src` — read the
    whole file, so a tool whose `headers=` sat on a DIFFERENT code path
    (urllib probes) passed while all three of its in-process fetches were
    bare, and it flagged a bare-app test with no dimll middleware and no
    lane to get wrong. It missed the only real offender in the tree that
    measured it.
    """
    offenders = []
    for folder in ("tests", "scripts"):
        for path in sorted((REPO / folder).glob("*.py")):
            src = _code_only(path.read_text())
            if ".test_client()" not in src:
                continue
            # `(?!\s*\.)` — a CHAINED call binds the RESPONSE, not the
            # client (`body = app.server.test_client().get(...)`), and the
            # first cut of this pin read `body` as an unnamed client with no
            # requests and flagged a line that already passed headers (llms,
            # 2026-08-31, measured on its test_prerender_idempotency.py).
            bound = set(re.findall(r"(\w+)\s*=\s*[\w.]*\.test_client\(\)(?!\s*\.)", src))
            bound |= set(re.findall(r"\.test_client\(\)\s+as\s+(\w+)", src))
            # Chained calls still get checked — on the call itself, since
            # there is no client name to follow.
            for meth in _REQUEST_METHODS:
                for call in _calls(src, f".test_client().{meth}"):
                    if "headers=" not in call:
                        offenders.append(f"{folder}/{path.name}::<chained {meth}>")
            if not bound:
                # Wrapped in place (conftest hands the raw client to a Client
                # that always sends one) — no name to follow, so fall back.
                if "headers=" not in src and "HTTP_USER_AGENT" not in src:
                    offenders.append(f"{folder}/{path.name}")
                continue
            for var in sorted(bound):
                if not _client_names_a_ua(src, var):
                    offenders.append(f"{folder}/{path.name}::{var}")
    assert offenders == [], offenders


def test_the_crawler_lane_still_404s_a_hidden_page(app_module, client):
    """The OTHER half of the same change, and the reason repairing the lane
    alone measures strictly less: once the sweep sends a browser UA, nothing
    is checking that a CRAWLER still gets the 404. Both, or the fix quietly
    removes a check."""
    from conftest import BROWSER_UA, CRAWLER_UA

    import dash

    admin = [p["path"] for p in dash.page_registry.values()
             if p["path"].startswith("/admin/")]
    assert admin, "no admin pages — the pin would be vacuous"
    for path in admin:
        assert client.get(path, user_agent=CRAWLER_UA).status == 404, (
            f"{path} does not 404 on the crawler lane — mark_hidden is gone"
        )
        assert client.get(path, user_agent=BROWSER_UA).status == 200, (
            f"{path} does not answer a browser (it renders its fail-closed "
            "card at 200; a 404 here means the sweep's UA regressed)"
        )


def test_battery_hidden_paths_match_the_registry(app_module):
    """Note 74: the battery's literal tuple is pinned against the registry,
    so a page added, renamed or deleted moves it in the same change.

    SUBSET plus a reality check, not set equality (leaflet and
    muischeduler, who re-derived the same adaptation independently).
    Equality would delete muischeduler's `/404/llms.txt` — a real hidden
    surface the battery had checked on the wire for months — and leaflet's
    deliberate `/admin` canary. Removing live coverage to satisfy an
    assertion is the opposite of what note 74 is for.

    But subset ALONE would lose what equality was catching: stale canaries
    on FIVE forks (`/admin/llms.txt`, `/analytics/llms.txt` — paths that
    never existed, 404ing vacuously while the real admin pages went
    unchecked). So the second half asks whether each listed path is
    genuinely hidden. Extras that are real coverage pass; extras that are
    fiction do not.
    """
    import dash

    from dash_improve_my_llms import is_hidden
    from scripts.network_smoke import HIDDEN_DOC_PATHS

    admin = {p["path"] for p in dash.page_registry.values() if p["path"].startswith("/admin/")}
    required = {f"{p}/llms.txt" for p in admin}
    assert required, "no admin pages registered — the pin would be vacuous"
    missing = required - set(HIDDEN_DOC_PATHS)
    assert not missing, (
        f"registered admin pages the battery never probes: {sorted(missing)}"
    )
    fiction = [
        p for p in HIDDEN_DOC_PATHS
        if p not in required and not is_hidden(p.rsplit("/llms.txt", 1)[0])
    ]
    assert fiction == [], (
        f"battery probes paths that are not hidden pages at all: {fiction} — "
        "a 404 for a page that does not exist is not evidence that a page is hidden"
    )


FLEET_HEADINGS = [
    ("## [1.4.0] - 2026-08-03", "1.4.0", "v1.4.0", "2026-08-03", ""),
    ("## [1.0.0] — 2026-08-21", "1.0.0", "v1.0.0", "2026-08-21", ""),
    ("## [0.9.0] – 2026-08-20", "0.9.0", "v0.9.0", "2026-08-20", ""),
    ("## 2.0.0 — 2026-08-02", "2.0.0", "v2.0.0", "2026-08-02", ""),
    ("## [0.2.0] — 2026-07-31 (never published)", "0.2.0", "v0.2.0", "2026-07-31", "never published"),
    ("## [0.1.0] — unreleased", "0.1.0", "v0.1.0", "", "unreleased"),
    ("## [2026-08-30] — the round in one line", "2026-08-30", "2026-08-30", "2026-08-30", "the round in one line"),
    ("## [Unreleased]", "Unreleased", "Unreleased", "", ""),
]


def test_every_fleet_heading_shape_parses(tmp_path):
    """Note 67a: the seven heading shapes measured on the fleet's main
    branches, plus Unreleased — label, badge, date and note each land.
    This fork's own CHANGELOG.md uses only two of them; the pin exists so
    the third one someone types does not render an empty heading."""
    import re as _re

    from pages.changelog import _is_version, parse_changelog

    body = "# Changelog\n\n" + "\n\n".join(h + "\n\n- a bullet" for h, *_ in FLEET_HEADINGS)
    p = tmp_path / "CHANGELOG.md"
    p.write_text(body)
    versions = parse_changelog(p)
    assert len(versions) == len(FLEET_HEADINGS)
    for got, (_, label, badge, date, note) in zip(versions, FLEET_HEADINGS):
        assert got["version"] == label, got
        assert got["date"] == date, got
        assert got["note"] == note, got
        rendered = f"v{got['version']}" if _is_version(got["version"]) else got["version"]
        assert rendered == badge, got
        assert not _re.match(r"^v(Unreleased|\d{4}-)", rendered), "note 67(a): VUNRELEASED / v<date>"


def test_a_prose_section_is_not_a_release(tmp_path):
    """This fork's finding, 2026-08-31. 1.6.41 widened the heading match to
    accept bare versions (pannellum's `## 2.0.0 — date`); the widening also
    swallowed PROSE. This repo's CHANGELOG.md ends with
    `## Component License Requirements`, which parsed as a release, rendered
    a timeline card badged with that whole sentence, and made the page count
    15 releases where there are 14.

    A release label is bracketed, or a version, or a date, or Unreleased.
    Anything else is a section of the release it sits under."""
    from pages.changelog import parse_changelog

    p = tmp_path / "CHANGELOG.md"
    p.write_text(
        "# Changelog\n\n"
        "## [1.0.0] - 2026-01-01\n\n### Added\n- a bullet\n\n"
        "## 2.0.0 — 2026-02-02\n\n- a bare-version release still parses\n\n"
        "## Component License Requirements\n\nProse that is not a release.\n"
    )
    versions = parse_changelog(p)
    assert [v["version"] for v in versions] == ["1.0.0", "2.0.0"], (
        "a free-text `##` heading was parsed as a release"
    )


def test_this_repos_own_changelog_counts_only_real_releases():
    """The non-vacuous half: the pin above uses a fixture, this one uses the
    file that actually ships. Every parsed label must be bracketed in the
    source — that is what `## [x]` means — or a bare version."""
    import re
    from pathlib import Path

    from pages.changelog import _is_version, parse_changelog

    text = (Path(__file__).resolve().parent.parent / "CHANGELOG.md").read_text()
    bracketed = set(re.findall(r"^## \[([^\]]+)\]", text, re.M))
    labels = [v["version"] for v in parse_changelog()]
    assert labels, "nothing parsed"
    stray = [x for x in labels if x not in bracketed and not _is_version(x)]
    assert stray == [], f"parsed as releases but not release headings: {stray}"
