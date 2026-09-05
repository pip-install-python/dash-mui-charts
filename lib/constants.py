"""Site identity + network contract constants — one string, every surface.

The network standard (STANDARD.md §1): a site states what it is, in the same
words, on every surface an agent or a reader can reach. The surfaces this
brand reaches, and what serves each:

    Dash(title=SITE_BRAND)              -> <title>, and resolve_site_title's
                                           second candidate
    register_page_metadata(path="/",    -> the /llms.txt H1 and the llms
        name=SITE_BRAND)                   viewer's brand chip (via
                                           dash-improve-my-llms 2.3.4)
    templates/index.html og:site_name   -> substituted from here at boot

Naming rules, from the network standard:
    - LIBRARY RULE: the package name comes FIRST in the brand (people
      install `dash-mui-charts`; the brand must match PyPI and GitHub);
    - "Pip Install Python" is the byline (who made it), never the site name.
"""
import os

SITE_BRAND = "dash-mui-charts — MUI X charts for Dash"

# What Dash(title=...) receives. Kept equal to the brand — resolve_site_title
# treats it as the second candidate after the home page's registered name.
APP_TITLE = SITE_BRAND

# The brand without its tagline, for surfaces that prefix something else and
# would otherwise run past platform truncation points.
SITE_SHORT_NAME = "dash-mui-charts"

# Prefixed to every per-page title. NOT only a browser-tab string: Dash passes
# the page title straight into og:title and twitter:title (dash/_pages.py
# _page_meta_tags), so this is the headline on every share card the site
# produces. Derived, not retyped, so brand and prefix cannot drift apart.
# --- Header identity (sync item 18) ----------------------------------------
# The header used to hardcode the logo path, its box, the wordmark colour and
# the breakpoint its text appears from. A fork edits this identity block and
# reasonably assumes that is the whole job — llms shipped the template's
# wordmark beside its own logo for exactly that reason. components/header.py
# holds no fork content now; these four do.
#
# LOGO_ASSET is served from assets/. This fork's avatar id `header-avatar` is
# a contract with the per-load favicon randomiser in templates/index.html
# (DIVERGENCES §1) — the randomiser re-points that image for browser TABS
# only; the mark itself is stable.
LOGO_ASSET = "favicon.ico"
LOGO_STYLE = {"height": "28px", "width": "28px"}
WORDMARK = "Dash MUI Charts"
WORDMARK_COLOR = "#1976d2"
# Below this breakpoint the wordmark text is REMOVED FROM THE TREE
# (visibleFrom, never opacity/width): at 390px it wrapped the header onto two
# rows. Hiding a control at a breakpoint pairs with its aria-label — the home
# anchor carries one, because display:none takes the text out of the
# accessibility tree and the logo is decorative.
WORDMARK_VISIBLE_FROM = "xs"

PAGE_TITLE_PREFIX = f"{SITE_SHORT_NAME} | "

SITE_DESCRIPTION = (
    "dash-mui-charts — 13 Plotly Dash components wrapping MUI X: LineChart, "
    "BarChart, CandlestickChart, PieChart, ScatterChart, CompositeChart, "
    "Heatmap, SparklineChart, LiveTradingChart, TreeView, SimpleTreeView, "
    "TreeViewPro and TimeClock. Interactive documentation with live "
    "examples, dark mode and MUI X Pro features. By Pip Install Python."
)

# ---------------------------------------------------------------------------
# Public origin
# ---------------------------------------------------------------------------
# BASE_URL drives <link rel="canonical"> on every page, the absolute URLs in
# sitemap.xml and llms.txt, and og:url. The name BASE_URL is REQUIRED by the
# network's shared scripts and tests (LESSONS §12) — alias, never rename.
#
# require_owned_base_url() below refuses to boot in production on a
# platform-generated hostname: *.onrender.com keeps resolving after the
# custom domain is attached, and canonicals pointing there split link equity
# across two hosts while nothing about the running site looks wrong.
DEFAULT_BASE_URL = "https://muicharts.2plot.dev"
BASE_URL = os.environ.get("APP_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

# Token in templates/index.html that app.py substitutes with BASE_URL at
# boot. A static file cannot import this module, and two hand-maintained
# copies of an origin is how half a site ends up pointing at one hostname
# and half at another.
ORIGIN_PLACEHOLDER = "__CANONICAL_ORIGIN__"

# ---------------------------------------------------------------------------
# The social card
# ---------------------------------------------------------------------------
# Every register_page call passes image_url=OG_IMAGE_URL and a description=
# — one page missing either and Dash emits content="" for it, and the empty
# tag, later in document order, wins with scrapers (LESSONS §1).
#
# THE CARD LIVES ON THE CDN, NOT IN assets/: a card served by the app is
# fetched by the scraper at unfurl time, and on a cold free-tier container
# that request times out and the platform caches the miss. HARD GATE
# (STANDARD §3): the object must answer 200 with IHDR 1200x630 at this URL
# BEFORE a deploy whose og:image points here.
OG_IMAGE_URL = "https://cdn.2plot.ai/github_assets/muicharts.2plot.dev.png"
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_TYPE = "image/png"
OG_IMAGE_ALT = SITE_BRAND

# ---------------------------------------------------------------------------
# Publisher identity for the crawler document's JSON-LD
# ---------------------------------------------------------------------------
# `configure_seo(publisher=, same_as=)` puts these in the crawler page's
# JSON-LD. For a docs satellite `same_as` should name the documented
# package's GitHub repo and its PyPI project: three URLs pointing at each
# other is the strongest available statement of which host is this package's
# canonical documentation home. The other half of that loop — PyPI
# project_urls and the GitHub README pointing back at muicharts.2plot.dev —
# is a per-package checklist item, not code.
PUBLISHER = "Pip Install Python LLC"

# ONE constant for the repository. The header's GitHub icon, the Resources
# block and JSON-LD `sameAs` all read it (sync item 16): a fork sets it once.
# muischeduler's icon pointed at the profile while its sameAs named the repo —
# two truths, one of them wrong.
GITHUB_URL = "https://github.com/pip-install-python/dash-mui-charts"

# The owner's PROFILE — the footer's GitHub link. The repo is the top bar's
# icon; the design (2026-08-30) puts one in each place, not both in both.
GITHUB_PROFILE_URL = "https://github.com/pip-install-python"

# DIVERGENCE from the template's `SAME_AS = [GITHUB_URL]`: this host documents
# a published package, so the PyPI project belongs in the sameAs loop. Three
# properties pointing at each other is the strongest available statement of
# which URL is dash-mui-charts' canonical documentation home; the template
# ships no package and has nothing to add.
SAME_AS = [
    GITHUB_URL,
    "https://pypi.org/project/dash-mui-charts/",
]

# ---------------------------------------------------------------------------
# Navigation contract (sync item 16) — the parts of the sidebar and top bar
# that are IDENTICAL on every host come from template code and the constants
# below; this app's own sections come from each page's frontmatter. A fork
# edits THIS block and its docs' frontmatter, never components/navbar.py.
# ---------------------------------------------------------------------------

# This app's own sections, in sidebar order — the component FAMILIES that used
# to live as a hand-written map in components/navbar.py. The names are kept
# exactly (the freedom the design grants each app); what moved is where the
# order is stated: `category:` + `order:` in every page's frontmatter, read
# from the page registry. A category not listed here still renders, after
# these, alphabetically — a new family is visible-but-unsorted, never lost,
# which is what the old map's "Other" section did.
#
# "Reference" is deliberately ABSENT: its only page is /api, and the contract
# gives /api its own section below the app's own (navbar._has_api_page).
CATEGORY_ORDER = [
    "SparklineChart",
    "PieChart",
    "BarChart",
    "Heatmap",
    "ScatterChart",
    "LineChart",
    "CandlestickChart",
    "LiveTradingChart",
    "CompositeChart",
    "TreeView",
    "Date & Time Pickers",
]

# Network-wide community links — identical on every host.
DISCORD_URL = "https://discord.gg/e5s5uHWUHH"
YOUTUBE_URL = "https://www.youtube.com/@2plotai"
YOUTUBE_SUBSCRIBE_URL = YOUTUBE_URL + "?sub_confirmation=1"
DMC_URL = "https://www.dash-mantine-components.com/"

# The upstream project this component library wraps. Rendered as the last
# Resources link. dash-mui-charts is a Dash wrapper over MUI X Charts, so the
# upstream API reference is the page a reader of these docs most often needs
# next — it was already in this fork's Resources section and is now stated
# once, here, in the shape the contract reads.
UPSTREAM = {
    "name": "MUI X Charts",
    "url": "https://mui.com/x/react-charts/",
    "icon": "simple-icons:mui",
}

# Dash component packages the /api page documents, and the source of the
# header's version badge (the first entry's __version__). This host documents
# exactly one package, and the docs image installs it from this same tree, so
# the badge cannot disagree with what a demo page renders.
API_PACKAGES: list = ["dash_mui_charts"]


def resources() -> list:
    """The sidebar's Resources section: THIRD-PARTY ONLY (owner, 2026-08-30).

    `dmc` and the upstream project, and nothing else. The owner's own links
    (repo, Discord, YouTube) live in the top bar and the footer, never here.
    Removed from this fork's previous list in the same move: the Dash
    Community forum (community.plotly.com — the owner asked for it out) and
    2plot.dev (the network is the top bar's Other Apps menu now, listed once).
    """
    items = [
        {"label": "dmc", "url": DMC_URL, "icon": "ic:baseline-design-services"},
    ]
    if UPSTREAM:
        items.append({"label": UPSTREAM["name"], "url": UPSTREAM["url"],
                      "icon": UPSTREAM.get("icon", "mdi:open-in-new")})
    return items


# ---------------------------------------------------------------------------
# The network's internal-traffic contract
# ---------------------------------------------------------------------------
# Any request whose User-Agent contains INTERNAL_UA_TOKEN is 2plot network
# machinery talking to itself — the hub's hourly health sweep, CI smoke
# batteries, this app's own server-to-server calls. It is counted NOWHERE.
#
#   inbound  — lib/analytics.record drops token-carrying requests at WRITE
#              time, before bot classification;
#   outbound — every call this host makes to another network host sends
#              internal_ua(...), so the far side can apply the same rule.
#
# The token must stay byte-identical across the network; it mirrors
# 2plotai/lib/constants.py and pip-docs+/lib/constants.py.
INTERNAL_UA_TOKEN = "2plot-internal"
INTERNAL_UA = "2plot-internal/1.0 (+https://2plot.ai/docs/satellite-analytics)"


def internal_ua(caller: str = "") -> str:
    """``INTERNAL_UA`` with a caller suffix, e.g. ``"ad-client"``.

    The suffix is for reading logs on the far side; only the token matters
    to the contract, and it stays intact whatever the suffix says.
    """
    caller = (caller or "").strip()
    return f"{INTERNAL_UA} {caller}" if caller else INTERNAL_UA


# The fleet probe convention (sync 1.6.44 item 4)
# ---------------------------------------------------------------------------
# A PROBE is machinery fetching a network host to CHECK it: a workflow's
# `curl /healthz`, a smoke battery, a link audit, the Dockerfile HEALTHCHECK.
# That is not the same shape as `internal_ua()`, which names this app calling
# a peer server-to-server, and the difference earns a spelling of its own so
# whoever reads the far side's log can tell "a host checking itself" from "a
# host using another host".
#
# The rule, and BOTH halves matter:
#
#   * the string LEADS with a real vendor-or-engine token — Chrome, Googlebot,
#     curl — because dash_improve_my_llms classifies on those tokens and a
#     probe must exercise the SAME LANE as the thing it is checking serves;
#   * it is GENERIC-WORD-FREE otherwise. `2plot-monitoring/1` is not a probe
#     UA: measured on dimll 2.9.4, that string classifies `bot_type='monitor'`
#     off the word "monitoring" alone, so a probe named that way changes the
#     document it was sent to measure.
#
# Suppression is the TRACKER's job, not the UA's: PROBE_UA_SUFFIX carries
# INTERNAL_UA_TOKEN, so `track_visit` and `record_read` drop the row at write
# time. Lane, vendor and class therefore hold by construction — measured on
# dimll 2.9.4, appending the suffix moves none of the three. This fork
# re-measures that table in `tests/test_internal_traffic.py` on the RESOLVED
# wheel rather than trusting the comment, because a floor bump is exactly
# what would move it.
PROBE_UA_SUFFIX = f"{INTERNAL_UA_TOKEN}/probe"


def probe_ua(engine: str, caller: str = "") -> str:
    """A fleet probe UA: ``engine`` token, ``PROBE_UA_SUFFIX``, then ``caller``.

    ``engine`` is REQUIRED and must be a real vendor-or-engine token. A probe
    carrying only the internal suffix classifies crawler-lane at dimll >= 2.8
    whatever it meant, which silently swaps the document under a browser-lane
    check — so this refuses rather than returning a string that would measure
    the wrong lane.

    ``caller`` names which probe this is — ``"network-smoke"``, ``"link-audit"``
    — for whoever reads the far side's log, exactly as ``internal_ua()``'s
    suffix does. It is not part of the contract: only the token is, and the
    caller tag must never be a generic word (see the ``2plot-monitoring``
    measurement above).
    """
    engine = (engine or "").strip()
    if not engine:
        raise ValueError(
            "probe_ua() needs a vendor-or-engine token: a UA carrying only "
            "the internal suffix classifies crawler-lane and changes which "
            "document the probe is answered with"
        )
    caller = (caller or "").strip()
    ua = f"{engine} {PROBE_UA_SUFFIX}"
    return f"{ua} {caller}" if caller else ua


def require_owned_base_url(base_url: str = BASE_URL) -> None:
    """Fail fast in production when BASE_URL isn't this app's real origin.

    Only enforced when a hosting platform is detected (Render sets
    ``RENDER``; ``APP_ENV=production`` works anywhere else), so local
    development and the test suite are unaffected.
    """
    in_production = bool(os.environ.get("RENDER")
                         or os.environ.get("APP_ENV") == "production")
    if not in_production:
        return

    for platform_host in ("onrender.com", "herokuapp.com", "railway.app",
                          "fly.dev"):
        if platform_host in base_url:
            raise RuntimeError(
                f"APP_BASE_URL={base_url!r} is a platform-generated "
                "hostname. Canonical tags, sitemap.xml and llms.txt would "
                "all point at it instead of the custom domain, splitting "
                "link equity across two hosts. Set APP_BASE_URL to the "
                "public domain (https://muicharts.2plot.dev)."
            )


# ---------------------------------------------------------------------------
# Boilerplate shell constants (components/appshell.py, header.py, navbar.py)
# ---------------------------------------------------------------------------
# Mantine primary — MUI's blue, matching the template's theme-color #1976d2.
PRIMARY_COLOR = "blue"
HEADER_HEIGHT = 70

# Raw markdown per page name, filled by pages/markdown.py at import — the
# llms_copy directive's copy-for-LLM button reads from it.
NAME_CONTENT_MAP = {}
