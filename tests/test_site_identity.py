"""Site identity: one brand, every surface, verbatim.

The network standard (STANDARD.md §1) says a site states what it is in the
same words everywhere an agent or a reader can reach. The failure this pins
is silent, which is why it needs tests rather than a code review: nothing
errors when a surface falls back to a default. Before Phase 1 of the
network-standard pass this host published its identity from a hardcoded
template block — with two <title> elements, og tags pinned to
dash-mui-charts.onrender.com, and a JSON-LD version two releases stale.
"""
from __future__ import annotations

import re

from conftest import BROWSER_ACCEPT, REPO_ROOT
from lib.constants import (
    PAGE_TITLE_PREFIX,
    SITE_BRAND,
    SITE_DESCRIPTION,
    SITE_SHORT_NAME,
)

# Spelled out rather than imported, so that renaming the constant cannot
# silently rename the site. Changing the brand should require changing this
# line, deliberately.
EXPECTED_BRAND = "dash-mui-charts — MUI X charts for Dash"

# A community page with registered LLMS_DOC prose — its /llms.txt viewer is
# where the brand chip renders.
PROSE_PAGE = "/sparkline"


def test_brand_constant_is_the_agreed_identity():
    assert SITE_BRAND == EXPECTED_BRAND


def test_app_title_is_the_brand(app):
    """`Dash(title=...)` — the <title> and `resolve_site_title`'s fallback."""
    assert app.title == EXPECTED_BRAND


def test_llms_index_h1_is_the_brand(client):
    """The single most-read line of this site, and the one nobody looks at."""
    response = client.get("/llms.txt")
    assert response.ok
    assert response.content_type.startswith("text/markdown")
    assert response.text.splitlines()[0] == f"# {EXPECTED_BRAND}"


def test_llms_index_tagline_is_the_description(client):
    body = client.get("/llms.txt").text
    assert f"> {SITE_DESCRIPTION}" in body


def test_the_viewer_brand_chip_is_not_a_framework_default(client):
    """The chip that reads a bare "Dash" on a pre-2.3.4 artifact.

    Rendered from the same `resolve_site_title` call as the /llms.txt H1, so
    asserting the brand is present catches both a stale package and a
    regressed constant. The brand arrives HTML-escaped (the em dash and any
    apostrophes), so compare the escaped form.
    """
    import html as html_module

    page = client.get(f"{PROSE_PAGE}/llms.txt", accept=BROWSER_ACCEPT)
    assert page.ok
    assert "text/html" in page.content_type
    assert html_module.escape(EXPECTED_BRAND) in page.text or EXPECTED_BRAND in page.text, (
        "the viewer banner does not name this site"
    )


def test_the_package_name_is_first_in_the_brand():
    """The LIBRARY rule (STANDARD §1): people install `dash-mui-charts`, so
    the brand must lead with the package name — unlike the boilerplate,
    which keeps its package name out because nobody installs a template."""
    assert SITE_BRAND.startswith("dash-mui-charts")


def test_the_byline_is_in_the_description_not_the_brand():
    """"Pip Install Python" is who made it, never what the site is called.
    A brand of "Pip Install Python" would make every satellite in the
    network share one name."""
    assert "Pip Install Python" in SITE_DESCRIPTION
    assert "Pip Install Python" not in SITE_BRAND


def test_no_surface_falls_back_to_a_generic_title():
    """The values `resolve_site_title` is designed to skip. If the brand were
    ever set to one of these, the package would silently fall through to the
    next candidate and this repo would have no idea which string it was
    publishing."""
    from dash_improve_my_llms.handlers import _GENERIC_SITE_TITLES

    assert SITE_BRAND.strip().lower() not in _GENERIC_SITE_TITLES


def test_llms_package_floor_is_the_network_standard():
    """Identity resolution lives in the package; the floor is what delivers it."""
    import dash_improve_my_llms as pkg

    parts = tuple(int(p) for p in pkg.__version__.split(".")[:3] if p.isdigit())
    assert parts >= (2, 3, 4), (
        f"dash-improve-my-llms {pkg.__version__} predates resolve_site_title; "
        "the viewer chip and the /llms.txt H1 would fall back to app.title"
    )


# ---------------------------------------------------------------------------
# The per-page title — a share-card surface, not just a browser tab.
# Dash passes each page's `title` straight into og:title and twitter:title
# (dash/_pages.py _page_meta_tags), so PAGE_TITLE_PREFIX sets the headline
# of every unfurl this site produces.
# ---------------------------------------------------------------------------


def test_the_page_title_prefix_is_this_site():
    assert PAGE_TITLE_PREFIX == f"{SITE_SHORT_NAME} | "


def test_the_short_name_cannot_drift_from_the_brand():
    """Two constants, one identity. Derived, so this should be automatic."""
    assert SITE_BRAND.startswith(SITE_SHORT_NAME)


def test_the_share_card_headline_names_this_site(client):
    """og:title and twitter:title, as a scraper reads them."""
    html = client.get("/").text
    for tag in ("og:title", "twitter:title"):
        found = re.findall(
            rf'<meta[^>]*property="{tag}"[^>]*content="([^"]*)"', html
        )
        assert found, f"no {tag} on the home page"
        for value in found:
            assert SITE_SHORT_NAME in value, f"{tag}={value!r} does not name this site"


def test_og_site_name_is_the_brand(client):
    html = client.get("/").text
    found = re.findall(
        r'<meta[^>]*property="og:site_name"[^>]*content="([^"]*)"', html
    )
    assert found == [EXPECTED_BRAND], found


# ---------------------------------------------------------------------------
# The canonical origin — the failure that deindexes a satellite
# ---------------------------------------------------------------------------


def test_base_url_defaults_to_the_network_domain():
    from lib.constants import DEFAULT_BASE_URL

    assert DEFAULT_BASE_URL == "https://muicharts.2plot.dev"


def test_production_refuses_a_platform_hostname(monkeypatch):
    """*.onrender.com keeps resolving after the custom domain is attached;
    canonicals pointing there split link equity across two hosts while
    nothing about the running site looks wrong."""
    import pytest

    from lib.constants import require_owned_base_url

    monkeypatch.setenv("RENDER", "true")
    with pytest.raises(RuntimeError):
        require_owned_base_url("https://dash-mui-charts.onrender.com")
    # The owned domain boots fine under the same flag.
    require_owned_base_url("https://muicharts.2plot.dev")


def test_identity_files_do_not_publish_the_legacy_host():
    """Scoped to files that PUBLISH identity (LESSONS §7) — a whole-repo
    grep hits legitimate strings (CHANGELOG history, .claude notes). The
    needle is the FULL legacy hostname: the bare "onrender.com" is
    legitimately part of require_owned_base_url's platform blocklist."""
    offenders = []
    for path in ("lib/constants.py", "templates/index.html",
                 "scripts/network_smoke.py"):
        text = (REPO_ROOT / path).read_text()
        stripped = re.sub(r"#.*", "", text) if path.endswith(".py") else text
        stripped = re.sub(r"<!--.*?-->", "", stripped, flags=re.S)
        if "dash-mui-charts.onrender.com" in stripped:
            offenders.append(path)
    assert offenders == [], f"the legacy host survives in {offenders}"


def test_hub_identity_fallbacks_are_this_app(monkeypatch):
    """This host may only ever identify to the hub as ITSELF.

    hub_client shipped with its fork-parent's fallback ("pannellum"), so a
    deployment missing both env keys verified agent keys — and could land
    heartbeat rows — under another satellite's identity. The reporter's
    template fallback ("boilerplate") is the same bug one fork earlier.
    Both fallbacks are pinned to this app's directory key.
    """
    from lib import hub_client, satellite_reporter

    monkeypatch.delenv("SATELLITE_APP_KEY", raising=False)
    monkeypatch.delenv("AD_APP_ID", raising=False)
    assert hub_client.app_id() == "muicharts"
    assert satellite_reporter.app_key() == "muicharts"
