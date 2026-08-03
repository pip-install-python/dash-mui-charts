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
# (APP_BASE_URL), lib/ad_client.py (AD_SERVER_URL, AD_APP_ID) and
# lib/analytics.py (ANALYTICS_DIR). Loading the .env after importing them
# means every one of those silently falls back to its default no matter
# what the file says.
load_dotenv()

import dash  # noqa: E402
from dash import Dash, Input, Output, callback, no_update  # noqa: E402

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

# AI/LLM Integration & SEO — dash-improve-my-llms >= 2.3.4 from PyPI.
# 2.3.4 brings `resolve_site_title`, which is what carries SITE_BRAND into
# the /llms.txt H1 and the llms viewer's brand chip; 2.3.3 fixed the
# Anthropic bot taxonomy and directive stripping.
from dash_improve_my_llms import (  # noqa: E402
    __version__ as LLMS_PKG_VERSION,
    add_llms_routes,
    LLMSConfig,
    RobotsConfig,
    register_page_metadata,
)

LLMS_PKG_FLOOR = (2, 3, 4)

from dash_mui_charts import __version__ as _COMPONENT_VERSION  # noqa: E402

# This repo's OWN analytics chain — the SPA-aware doc/spa recorder, NOT the
# boilerplate's request-level analytics_tracker. See lib/traffic_report.py
# THE COUNTING RULE and BOILERPLATE_MIGRATION_PLAN.md decision 3.
from lib import analytics, network_directory  # noqa: E402
from lib.constants import (  # noqa: E402
    APP_TITLE,
    BASE_URL,
    ORIGIN_PLACEHOLDER,
    SITE_BRAND,
    SITE_DESCRIPTION,
    require_owned_base_url,
)
from lib.traffic_report import register_healthz, start_traffic_reporter  # noqa: E402

# Backend selection (flask | fastapi | quart) — see lib/backend.py. The
# machinery is the boilerplate's; this app's analytics hooks and /healthz
# are Flask-first, so anything else refuses to boot rather than silently
# serving uncounted, unprobed traffic.
from lib.backend import resolve_backend, get_backend_info  # noqa: E402

BACKEND = resolve_backend()
BACKEND_INFO = get_backend_info(BACKEND)

if BACKEND != "flask":
    raise RuntimeError(
        f"DASH_BACKEND={BACKEND!r}: this site's analytics recorder, "
        "/healthz and traffic reporter are wired for Flask only. Port "
        "lib/analytics + lib/traffic_report hooks before flipping the "
        "backend (BOILERPLATE_MIGRATION_PLAN.md, open question 4)."
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
        "requirements.txt. Below 2.3.4 this site's published identity "
        "silently degrades to whatever `app.title` happens to be.",
        fatal=True,
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
# a document-request recorder for crawlers, and the hourly traffic reporter.
# Page views themselves come from the url.pathname callback further down:
# this is a single-page app, so document requests alone would report one hit
# per visitor. See lib/traffic_report for the full counting rule.
#
# ORDER MATTERS: this before_request is registered BEFORE add_llms_routes,
# so crawler hits are recorded before the bot middleware answers them with
# prerendered HTML (a hook added after it never sees bot traffic).
# ----------------------------------------------------------------------------
register_healthz(server)


@server.before_request
def _track_document_request():
    """Record every document request. Crawlers only ever land here (they run
    no JS), which is exactly what `bot_hits` counts."""
    try:
        from flask import request as freq

        if freq.method != 'GET':
            return
        analytics.record(
            freq.path,
            freq.headers.get('User-Agent', ''),
            analytics.client_ip(freq.headers, freq.remote_addr),
            source='doc',
            country=analytics.cf_country(freq.headers),
        )
    except Exception:
        pass


start_traffic_reporter()

# ============================================================================
# AI/LLM & SEO surfaces
# ============================================================================

require_owned_base_url()
app._base_url = BASE_URL

network_directory.apply(BASE_URL)

# Training crawlers (GPTBot, ClaudeBot, CCBot, …) are disallowed; the
# user-triggered and search fetchers stay allowed — dimll >=2.3.3 buckets
# per vendor, so this split is exact.
app._robots_config = RobotsConfig(
    block_ai_training=True,
    allow_ai_search=True,
    allow_traditional=True,
    crawl_delay=10,
    disallowed_paths=[],
)

# `name` here is NOT a nav label — resolve_site_title reads it first, so it
# is the /llms.txt H1 and the llms viewer's brand chip. Markdown-driven
# pages register their own LLMS_DOC inside pages/markdown.py.
register_page_metadata(
    path="/",
    name=SITE_BRAND,
    description=SITE_DESCRIPTION,
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

ACCESS_ENABLED = _access.configure()

add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

# ============================================================================

app.layout = create_appshell(dash.page_registry.values())


# Page views for the satellite rollup. Fires on hard load AND on every
# navigation, so `pages`, `sessions` and `median_session_s` describe the doc
# pages people actually read — a request-level tracker would only ever see
# the one document GET this SPA makes. Runs inside the Flask request context
# of /_dash-update-component, so the forwarded IP and real user agent are
# both available.
@callback(
    Output("analytics-sink", "data"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)
def track_page_view(pathname):
    try:
        from flask import request as freq

        analytics.record(
            pathname or "/",
            freq.headers.get("User-Agent", ""),
            analytics.client_ip(freq.headers, freq.remote_addr),
            source="spa",
            country=analytics.cf_country(freq.headers),
        )
    except Exception:
        pass
    return no_update


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "7666")),
    )
