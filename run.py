"""
dash-mui-charts documentation site — MUI X charts for Dash, markdown-driven.

Serves the component documentation (docs/**/*.md with live examples, plus
the Python pages still awaiting their boilerplate-migration phase) at
https://muicharts.2plot.dev, a 2plot network satellite.

Run locally:

    python run.py                          # backend from .env (DASH_BACKEND)

Production (Render/Docker):

    gunicorn run:server -b 0.0.0.0:8550
"""
import inspect
import os
import sys

from dotenv import load_dotenv

# MUST come before the first-party imports below, and this is not style.
# Several modules read os.environ at *import* time — lib/constants.py
# (APP_BASE_URL) and lib/ad_client.py (AD_SERVER_URL, AD_APP_ID). Loading
# the .env after importing them means every one of those silently falls
# back to its default no matter what the file says.
load_dotenv()

import dash  # noqa: E402
from dash import Dash  # noqa: E402

from components.appshell import create_appshell  # noqa: E402


def _version(text: str) -> tuple:
    """("4.4.1rc0") -> (4, 4, 1). Trailing rc/dev segments are dropped."""
    parts = []
    for chunk in text.split(".")[:3]:
        digits = ""
        for char in chunk:
            if not char.isdigit():
                break
            digits += char
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


DASH_VERSION = _version(dash.__version__)

# AI/LLM Integration & SEO — dash-improve-my-llms >= 2.8.0 from PyPI.
# 2.5.1 was the Tier-B SEO standard: per-page `title`/`image_url`/
# `schema_type` actually reaching the crawler document, `configure_seo`
# (icons, social card, publisher/sameAs), /favicon.ico answered with a
# redirect instead of the app shell, the crawler <title> carrying the site
# name, and a prerender that no longer clobbers the browser's per-page
# <title>. 2.6.0 adds the honesty standard: sitemap <lastmod> emitted
# verbatim from `register_page_metadata(lastmod=)` and OMITTED when unset,
# icon AUTODISCOVERY over app assets, JSON-LD publisher.logo, and the llms
# viewer's banner de-dup. 2.6.1 makes the universal prerender VISIBLE:
# below it the injected div carries a literal `hidden` attribute, so a
# non-JS reader — an html-to-text extractor, a text browser, arguably
# crawler content weighting — got "Loading..." and nothing else. 2.7.0
# dedups what that now-visible block says (one H1 per page, one footer
# llms.txt link) and hardens the idempotency probe; 2.7.1 adds the
# llms.txt v2 discovery relations + Link headers, the text/plain Accept
# ramp, and the representation digest. (2.4.0
# brought the tiered corpus docs /llms-small.txt + /llms-full.txt; 2.3.4
# brought `resolve_site_title`, which carries SITE_BRAND into the /llms.txt
# H1 and the viewer's brand chip.)
from dash_improve_my_llms import (  # noqa: E402
    __version__ as LLMS_PKG_VERSION,
    add_llms_routes,
    LLMSConfig,
    RobotsConfig,
    on_document_read,
    register_page_metadata,
)

# The floor is load-bearing for what a NON-JS READER GETS, and for honesty,
# not for crash avoidance. Below 2.7.1 this host loses the llms.txt v2
# discovery relations and Link headers, the text/plain Accept ramp and the
# representation digest; below 2.7.0 every page serves TWO h1s to a generic
# client (the injected prerender header plus the doc body's own — a
# duplicate-H1 page in every crawler's eyes) and the home footer prints its
# /llms.txt link twice. Below 2.6.1 the prerender div ships `hidden` and
# this site has no hand-written <noscript> to fall back on any more — the
# block was retired in the same deploy that brought 2.6.1, deliberately, so
# that no window exists where a non-JS reader has neither. Below 2.6.0,
# `lastmod=` is additionally swallowed into **kwargs and the sitemap goes
# back to swearing everything changed at build time.
#
# 2.8.0 is the ledger floor (2026-08-29, sync item 12): ONE classifier —
# `classify()` is the same vendor registry robots.txt is rendered from, and
# lib/analytics_tracker delegates to it instead of carrying a fourth UA list
# that filed ClaudeBot as *search*; and the READ EVENT — `on_document_read`
# hands this app one row per corpus document served (tier, verdict, bytes,
# verified vendor), which the tracker keeps as the ledger's `reads` table and
# lib/traffic_rollup folds into rollup v4's vendors[]. 2.8.1 will write the
# resolved `policy` on every event; until then it is None and the rollup
# groups it as "default". Nothing here waits on it.
#
# Moving this tuple is HALF the job: the requirements.txt line is what
# busts the Docker dependency layer and actually delivers the release. A
# floor raised here alone would refuse to boot the image it was shipped in.
LLMS_PKG_FLOOR = (2, 8, 0)

from dash_mui_charts import __version__ as _COMPONENT_VERSION  # noqa: E402

# The network's analytics trio, ported from the boilerplate at 1.3.0:
# lib/analytics_tracker records every document request into the visitor
# ledger, lib/traffic_rollup folds it into the daily payload, and
# lib/satellite_reporter POSTs that to 2plot.ai hourly. ONE measurement
# rule fleet-wide — traffic_rollup's _SKIP stays byte-identical to the
# boilerplate's. (Request-level on purpose: SPA navigations are not
# counted until the network ports the doc/spa split everywhere at once —
# the x402 data window needs every satellite counting the same way.)
from lib import network_directory  # noqa: E402
from lib.analytics_tracker import tracker  # noqa: E402
from lib.constants import (  # noqa: E402
    APP_TITLE,
    BASE_URL,
    OG_IMAGE_ALT,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
    ORIGIN_PLACEHOLDER,
    PUBLISHER,
    SAME_AS,
    SITE_BRAND,
    SITE_DESCRIPTION,
    require_owned_base_url,
)
from lib.satellite_reporter import start_reporter  # noqa: E402

# Backend selection (flask | fastapi | quart) — see lib/backend.py. The
# machinery is the boilerplate's; this app's analytics hooks and /healthz
# are Flask-first, so anything else refuses to boot rather than silently
# serving uncounted, unprobed traffic.
from lib.backend import resolve_backend, get_backend_info  # noqa: E402

BACKEND = resolve_backend()
BACKEND_INFO = get_backend_info(BACKEND)

if BACKEND != "flask":
    raise RuntimeError(
        f"DASH_BACKEND={BACKEND!r}: this site's visitor-tracking hook is "
        "wired for Flask only. Port the boilerplate's Quart/FastAPI "
        "track_visitor variants (its run.py + lib/asgi_middleware) before "
        "flipping the backend."
    )

print(
    f"[muicharts] Starting Dash {dash.__version__} "
    f"(dash-improve-my-llms {LLMS_PKG_VERSION}, dash_mui_charts "
    f"{_COMPONENT_VERSION}) on backend='{BACKEND}'"
)

# ----------------------------------------------------------------------------
# Dependency floors — enforced, not advised. A version below the floor stops
# the boot and says what to do; the app is never wrong-but-running. Set
# ALLOW_STALE_DEPS=1 to downgrade to warnings when deliberately testing an
# older release.
# ----------------------------------------------------------------------------

ALLOW_STALE_DEPS = os.environ.get("ALLOW_STALE_DEPS", "0") == "1"


def _dependency_floor(message: str, fatal: bool) -> None:
    detail = (
        f"{message}\n"
        f"    running from: {sys.executable}\n"
        "    fix: reinstall with `pip install -r requirements.txt && "
        "pip install --no-deps markdown2dash==0.1.2`.\n"
        "    (set ALLOW_STALE_DEPS=1 to start anyway)"
    )
    if fatal and not ALLOW_STALE_DEPS:
        raise RuntimeError("\n[muicharts] " + detail)
    print("[muicharts] WARNING: " + detail)


if LLMS_PKG_FLOOR > _version(LLMS_PKG_VERSION):
    _dependency_floor(
        f"dash-improve-my-llms {LLMS_PKG_VERSION} is below the "
        f"{'.'.join(str(n) for n in LLMS_PKG_FLOOR)} floor in "
        "requirements.txt. Below 2.8.0 there is no `classify()` and no "
        "`on_document_read`: the tracker cannot delegate bot classification "
        "and no read row is ever kept, so the ledger's `reads` table and "
        "rollup v4's vendors[] are empty (ImportError at boot, not a silent "
        "degrade). Below 2.7.1 this host loses the llms.txt v2 "
        "discovery relations and Link headers, the text/plain Accept ramp "
        "and the representation digest. Below 2.7.0 every page serves TWO "
        "h1s to a generic client — the injected prerender header plus the "
        "doc body's own — and the home footer prints its /llms.txt link "
        "twice. Below 2.6.1 the prerender div ships with a "
        "literal `hidden` attribute, so every non-JS reader sees "
        "'Loading...' and nothing else — and this site retired its "
        "hand-written <noscript> block when it took 2.6.1, so there is no "
        "longer a fallback underneath. Below 2.6.0 the sitemap additionally "
        "goes back to lying: `lastmod=` is accepted into **kwargs and "
        "SILENTLY IGNORED, so every date a page declares is swallowed and "
        "<lastmod> reverts to invented build dates. Below 2.5.1 the "
        "crawler document drops this "
        "site's per-page identity (title/image/schema type) and "
        "`configure_seo` does not exist at all — the root icons and the "
        "publisher block below stop being emitted; below 2.3.4 the "
        "published identity itself degrades to `app.title`.",
        fatal=True,
    )

# Imported after the floor on purpose: on a pre-2.5.0 package this name does
# not exist, and the floor's diagnosis above beats a bare ImportError. The
# fallback exists only for ALLOW_STALE_DEPS=1 — the floor is fatal otherwise.
try:
    from dash_improve_my_llms import configure_seo  # noqa: E402
except ImportError:  # pragma: no cover — ALLOW_STALE_DEPS on a pre-2.5.0 pkg

    def configure_seo(**_kwargs) -> None:
        print(
            "[muicharts] WARNING: configure_seo unavailable (pre-2.5.0 "
            "package) — crawler identity tags and root icons not emitted."
        )

if DASH_VERSION < (4, 4):
    _dependency_floor(
        f"dash {dash.__version__} is below the 4.4.0 floor in "
        "requirements.txt (the boilerplate docs stack's floor; the "
        "dash_mui_charts PACKAGE itself still supports >=3.3).",
        fatal=False,
    )

# Dash 4.3+ MCP server: a live introspection surface on a public host, so
# off unless DASH_MCP_ENABLED=1. Constructor argument — Dash starts the
# server during __init__; there is no supported way to enable it later.
MCP_ENABLED = os.environ.get("DASH_MCP_ENABLED", "0") == "1"
MCP_PATH = os.environ.get("DASH_MCP_PATH", "_mcp")

# ----------------------------------------------------------------------------
# Clerk satellite auth. MUST run BEFORE Dash(...) — register_clerk_auth
# installs @dash.hooks callbacks that fire during app construction. Fully
# optional: a no-op with no CLERK_* keys, which is the default.
# ----------------------------------------------------------------------------
from lib import auth as _auth  # noqa: E402

CLERK_ENABLED = _auth.register()

MCP_KWARGS = {}
if MCP_ENABLED:
    if "enable_mcp" in inspect.signature(Dash.__init__).parameters:
        MCP_KWARGS = {"enable_mcp": True, "mcp_path": MCP_PATH}
    else:
        print(
            f"[muicharts] DASH_MCP_ENABLED=1 ignored: dash "
            f"{dash.__version__} has no MCP server (needs >= 4.3)."
        )

# Custom index template: GA4, favicon randomizer, and the site-level tags
# Dash does not emit. Its __CANONICAL_ORIGIN__ tokens become BASE_URL and
# __APP_VERSION__ becomes the package version here, so the canonical origin
# and every version string come from single sources of truth — a static
# file cannot import lib/constants, and hand-maintained copies are exactly
# how this template once carried five conflicting version strings.
with open(os.path.join(os.path.dirname(__file__), "templates", "index.html"),
          encoding="utf-8") as _f:
    _index_string = (_f.read()
                     .replace(ORIGIN_PLACEHOLDER, BASE_URL)
                     .replace("__APP_VERSION__", _COMPONENT_VERSION))

# NOTE: no `prevent_initial_callbacks=True` here, deliberately — unlike the
# boilerplate. The demo callbacks (both the unported Python pages and the
# exec example modules ported from them) rely on initial fires to render
# their first state; the canonical ad_client handles its own initial-call
# semantics explicitly per callback.
app = Dash(
    __name__,
    backend=BACKEND,
    title=APP_TITLE,
    use_pages=True,
    suppress_callback_exceptions=True,
    update_title=None,
    index_string=_index_string,
    **MCP_KWARGS,
)

if MCP_KWARGS:
    print(f"[muicharts] Dash MCP server enabled at /{MCP_PATH.lstrip('/')}")

# dash-clerk-auth's post-construction half: sessions, /api/auth/* routes,
# per-request identity. No-op when off.
_auth.configure_app(app)

server = app.server  # WSGI entry point for gunicorn: gunicorn run:server

# Trust the proxy's forwarded scheme — immediately after the server object
# exists, before anything serves a request. Dash builds `twitter:url` from
# `request.url`, and behind a CDN -> Render the last hop is plain HTTP, so
# production would advertise http:// URLs to every social scraper.
from lib import proxy as _proxy  # noqa: E402

PROXY_FIX_APPLIED = _proxy.apply(app, BACKEND)
print(
    "[muicharts] forwarded-scheme trust: "
    + ("on" if PROXY_FIX_APPLIED else "OFF — request.url will report the "
       "scheme of the last proxy hop")
)

app._backend_info = BACKEND_INFO

# ----------------------------------------------------------------------------
# 2plot.ai satellite analytics — /healthz for the hub's hourly health sweep,
# the per-request visitor recorder, and the hourly signed rollup POSTed to
# the hub (no-op without CROSS_APP_WEBHOOK_SECRET, and the boot log says
# so). Contract: 2plotai/docs/network/satellite-analytics.md.
#
# ORDER MATTERS: this before_request is registered BEFORE add_llms_routes,
# whose bot middleware short-circuits AI-search crawlers with its own
# prerendered response — a hook added after it never sees exactly the bot
# traffic a docs site most wants counted.
# ----------------------------------------------------------------------------
from lib.health import register_health_route  # noqa: E402

register_health_route(app, BACKEND)

from flask import request as _flask_request  # noqa: E402


@server.before_request
def track_visitor():
    """Track visitor analytics before each request."""
    try:
        # Headers are passed so the tracker can read the REAL client IP
        # and country from the proxy/CDN (behind Render or Cloudflare,
        # remote_addr is the proxy — every visitor would look like one).
        tracker.track_visit(
            _flask_request.path,
            _flask_request.headers.get('User-Agent', ''),
            _flask_request.remote_addr,
            headers=dict(_flask_request.headers),
        )
    except Exception:
        pass


start_reporter()

# ============================================================================
# AI/LLM & SEO surfaces
# ============================================================================

require_owned_base_url()
app._base_url = BASE_URL

network_directory.apply(BASE_URL)

# Crawler posture — THE WALL IS RETIRED (sync item 15, Round 3.4, owner
# decision 2026-08-29). Until now this host blocked the AI-training
# crawlers (GPTBot, ClaudeBot, CCBot, …): robots.txt said Disallow and the
# package's middleware answered 403 on the browser document and /healthz,
# while the corpus (/llms.txt and the tiers) stayed open — a wall that
# decided by vendor CLASS what nobody could account for. The ledger changed
# that: since sync item 12 every corpus read is a row (tier, vendor,
# verified, bytes) and the hub reconciles it against the wire. A read that
# is recorded and priceable does not need a wall; it needs a policy. So
# training crawlers are ALLOWED by default, the same as search fetchers and
# traditional bots, and the per-vendor knob is the tool from here on —
# block or meter ONE vendor by name when its ledger rows justify it, never
# the whole class:
#
#     vendor_policy={"bytespider": "block", "gptbot": "meter"}
#
# (2.3.3's per-vendor buckets still matter: they are what makes a
# per-vendor line mean the vendor it names.)
#
# MEASURED HERE, in-process, before and after the flip (2026-08-30):
# ClaudeBot and GPTBot on `/`, `/llms.txt`, `/healthz` went 403/200/403 ->
# 200/200/200, and the wire before the flip was the same 403/200/403 — so
# every 403 this host ever served was the app's own middleware. There is no
# edge wall in front of muicharts.2plot.dev.
app._robots_config = RobotsConfig(
    block_ai_training=False,      # training crawlers allowed; the ledger records every read
    allow_ai_search=True,         # Allow Claude-User/-SearchBot, ChatGPT-User, ...
    allow_traditional=True,       # Allow Googlebot, Bingbot, etc.
    crawl_delay=10,
    disallowed_paths=[],
)

# ============================================================================
# Site identity for the CRAWLER document (dash-improve-my-llms 2.5.0+).
# Until 2.5.0 the generated crawler HTML carried the page's content signals
# and none of its identity: browsers got the icon links, og:image and the
# twitter card from templates/index.html while Googlebot got none of them,
# on every host in the network — so search showed the generic globe. One
# declaration covers every crawler surface, and it also claims /favicon.ico
# (Google's fallback), which Dash's page catch-all was answering with the
# app shell.
#
# THE ICON LIST IS THIS SITE'S STABLE IDENTITY. templates/index.html
# additionally runs a per-load area/bar randomizer for browser tabs — a
# brand quirk, and browsers are allowed that. Crawlers are not: the mark
# below never changes between fetches. The paths are the area-chart set,
# generated from assets/apple-touch-icon_areachart.png (the master; also
# the artwork scripts/make_social_card.py builds the card from) via
# `python scripts/make_favicons.py assets/apple-touch-icon_areachart.png`.
# Re-run that after ANY change to the master, or the tab and the search
# result quietly stop agreeing. Declaration is authoritative today and
# stays correct under 2.6's autodiscovery, which finds this same set.
# ============================================================================
configure_seo(
    icons=[
        "/assets/favicon/favicon.ico",
        {"href": "/assets/favicon/favicon-32x32.png", "sizes": "32x32"},
        {"href": "/assets/favicon/favicon-16x16.png", "sizes": "16x16"},
        {"href": "/assets/favicon/favicon-96x96.png", "sizes": "96x96"},
        {"href": "/assets/favicon/android-chrome-192x192.png", "sizes": "192x192"},
        {"href": "/assets/favicon/android-chrome-512x512.png", "sizes": "512x512"},
        {"href": "/assets/favicon/apple-touch-icon.png",
         "rel": "apple-touch-icon", "sizes": "180x180"},
    ],
    social_image=OG_IMAGE_URL,
    social_image_alt=OG_IMAGE_ALT,
    social_image_width=OG_IMAGE_WIDTH,
    social_image_height=OG_IMAGE_HEIGHT,
    publisher=PUBLISHER,
    same_as=SAME_AS,
)

# `name` here is NOT a nav label — resolve_site_title reads it first, so it
# is the /llms.txt H1 and the llms viewer's brand chip. Markdown-driven
# pages register their own LLMS_DOC inside pages/markdown.py.
register_page_metadata(
    path="/",
    name=SITE_BRAND,
    description=SITE_DESCRIPTION,
    # The home page of a component library is a SoftwareApplication, not a
    # generic WebPage — the one structured-data type that exactly describes
    # it. Docs pages default to TechArticle in pages/markdown.py.
    schema_type="SoftwareApplication",
)

# The hub's announcement feed, rendered in this site's llms.txt viewer
# header. Opt-in: with NETWORK_BULLETIN_URL unset it wires nothing.
from lib import bulletin as _bulletin  # noqa: E402

BULLETIN_ENABLED = _bulletin.configure()
print(
    f"[muicharts] network bulletin: wired -> {_bulletin.url()}"
    if BULLETIN_ENABLED else
    "[muicharts] network bulletin: off (NETWORK_BULLETIN_URL unset)"
)

# Access control (dimll 2.3): reads the tiers pages declared, so it runs
# after page registration and before the routes attach. OFF unless some
# page declares a non-public tier.
from lib import access as _access  # noqa: E402
from lib import page_tiers as _page_tiers  # noqa: E402
from lib import page_visibility as _page_visibility  # noqa: E402

# Tiered corpus documents (dash-improve-my-llms >= 2.4.0). Pseudo-paths:
# they never enter dash.page_registry, so they cannot leak into listings —
# registering them here lets this satellite tier its compact briefing and
# full corpus via env (LLMS_SMALL_TIER / LLMS_FULL_TIER), and the hub can
# tighten either network-wide through its page-tier ceilings with no
# redeploy here. The explicit `or "public"` matters: these registered under
# the PAGE_DEFAULT_TIER fallback before, which meant flipping that env to
# gate the *interactive* site would silently gate the corpus documents too.
# Their tier is now always a deliberate setting, never an ambient default.
_page_tiers.register("/llms-small.txt",
                     os.environ.get("LLMS_SMALL_TIER") or "public")
_page_tiers.register("/llms-full.txt",
                     os.environ.get("LLMS_FULL_TIER") or "public")

# The home page registers via pages/home.py, not pages/markdown.py, so no
# frontmatter ever declares its tier — under PAGE_DEFAULT_TIER=auth it would
# silently inherit the gate. The funnel's front door stays public, always.
_page_tiers.register("/", "public")

# force= when either gate env is present: with every tier still public the
# auto-detect would skip the wiring, but a host that flips by env needs the
# verdict plumbing (and the prerender's use of it) live during the dark
# launch, not on the flip.
ACCESS_ENABLED = _access.configure(
    force=bool(os.environ.get("PAGE_DEFAULT_TIER")
               or os.environ.get("LLMS_PUBLIC_DEFAULT"))
)

add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

# The ledger row (sync item 12, dimll 2.8.0): the package emits one event per
# corpus document it serves and does no I/O with it; the tracker keeps it as
# the `reads` table next to `visits` in the SAME analytics file. Registered
# ONCE — this suite imports run.py more than once per process and
# `on_document_read` appends, so a marker on the callback's owner guards the
# second import (the package also dedups an identical callable; belt and
# braces).
if not getattr(tracker, "_read_hook_registered", False):
    on_document_read(tracker.record_read)
    tracker._read_hook_registered = True

# ============================================================================

app.layout = create_appshell(dash.page_registry.values())

# ============================================================================
# The person→agent handoff: /api/agent-key turns the browser's Clerk session
# into a portable ?key= for copied llms.txt URLs (lib/agent_key.py). 204 for
# everyone until Clerk and the hub are configured — safe to mount always.
# ============================================================================

from lib.agent_key import register_agent_key_route  # noqa: E402

register_agent_key_route(app, BACKEND)

# The gate's own boot line. Read it in the deploy log with the two warnings
# that must NOT be there ([visibility] = the /var/data disk never mounted,
# [auth] = the sign-in redirect is unset or not a URL): three absences and
# one presence is this host's acceptance check.
_non_public = sum(1 for t in _page_tiers.registered().values() if t != "public")
print(
    f"[muicharts] interactive gate: default tier "
    f"'{os.environ.get('PAGE_DEFAULT_TIER') or 'public'}', "
    f"{_non_public} non-public page(s), machine surfaces "
    f"{'GATED' if not _page_tiers.get_llms_public('/__probe__') else 'open'} "
    f"by default (LLMS_PUBLIC_DEFAULT), access wiring "
    f"{'ON' if ACCESS_ENABLED else 'off'}, control board at "
    f"/admin/control-board ({_page_visibility.override_count()} live "
    f"override(s))."
)


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "7666")),
    )
