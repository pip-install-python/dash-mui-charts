"""Shared fixtures — boot the real app once, with ZERO secrets, and interrogate it.

The suite deliberately exercises `run.py` itself rather than a stripped-down
app assembled for testing: nearly everything worth catching lives in the
wiring — registration order, which before_request runs first, whether a page's
metadata survived to the response. A test app that re-implements that wiring
tests the re-implementation.

SECRETLESS, AND ORDER MATTERS. This suite runs against the app exactly as
CI's zero-secret container does: no MUI_PRO_API_KEY (the 17 Pro pages must
degrade to their license banners — that degradation IS a test, in
test_pages_smoke.py), no CROSS_APP_WEBHOOK_SECRET (the traffic reporter never
starts a thread), no NETWORK_BULLETIN_URL (the llms viewer falls back to
built-in tips), and the visitor ledger in a temp dir so a test run never
lands in the real ledger or the next hourly rollup.

The env block below has to run BEFORE anything imports `run.py`, because
run.py calls `load_dotenv()` during import and the developer's local `.env`
(which holds a real MUI_PRO_API_KEY) would otherwise flip the app into a
configured posture. `load_dotenv()` never overrides an existing key, so
pinning each secret to `""` here (falsy to every `os.environ.get(...)`
reader) neutralises the file without deleting it. In CI there is no `.env`
at all and this is belt-and-braces. Same pattern as the boilerplate,
dash-email and pip-docs+.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# --- 1. Neutralise every secret (must precede any import of run.py) ---------
# The CLERK_*/SESSION_SECRET block joined at the gate wave: with no Clerk keys
# the interactive gate must fall OPEN on public and auth pages and still deny
# admin/hidden, and that zero-secret boot is what every fail-closed assertion
# in tests/test_access.py rests on. A developer's local .env holding real keys
# would otherwise flip the suite into a configured posture and quietly stop
# proving the degraded one.
SECRET_ENV_KEYS = (
    "MUI_PRO_API_KEY",
    "CROSS_APP_WEBHOOK_SECRET",
    "NETWORK_BULLETIN_URL",
    "CLERK_SECRET_KEY", "CLERK_PUBLISHABLE_KEY", "CLERK_SIGN_IN_URL",
    "CLERK_SIGN_UP_URL", "CLERK_FRONTEND_API", "CLERK_WEBHOOK_SECRET",
    "CLERK_IS_SATELLITE", "CLERK_SATELLITE_DOMAIN",
    "CLERK_SATELLITE_SIGN_IN_REDIRECT",
    "SESSION_SECRET", "FLASK_SECRET_KEY",
)
for _key in SECRET_ENV_KEYS:
    os.environ[_key] = ""

# --- 2. Keep app state out of the repo, and identity deterministic ----------
_TMP_STATE = tempfile.mkdtemp(prefix="muicharts-tests-")
os.environ["TRAFFIC_ANALYTICS_FILE"] = os.path.join(
    _TMP_STATE, "visitor_analytics.json")
# Same reason for the control board's override store — and pointing it at a
# tmp path also keeps the import-time [visibility] boot warning quiet, which
# is the very warning the deploy log is read for.
os.environ["PAGE_VISIBILITY_FILE"] = os.path.join(
    _TMP_STATE, "page_visibility.json")
# Keep the suite offline: no ip-api.com lookups for synthetic visitors.
os.environ["ANALYTICS_GEO_LOOKUP"] = "0"
# A dev .env pointing APP_BASE_URL elsewhere must not change what the suite
# measures — every canonical/og assertion is against the network domain.
os.environ["APP_BASE_URL"] = "https://muicharts.2plot.dev"
os.environ.setdefault("APP_ENV", "test")

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CRAWLER_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# What a real browser sends. `/<page>/llms.txt` negotiates on this header —
# not on the User-Agent — so it is what separates "a person opened the URL"
# from "an agent fetched it".
BROWSER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

# The body dash-improve-my-llms serves when a page has no prose registered.
STUB_MARKER = "This page contains interactive content that requires JavaScript"


@pytest.fixture(scope="session")
def app_module():
    """Import run.py as a module, from the repo root.

    run.py opens templates/index.html relative to its own file, but
    pages/changelog.py reads CHANGELOG.md from disk, so the process CWD has
    to be the repo root regardless of where pytest was invoked from.
    """
    os.chdir(REPO_ROOT)
    spec = importlib.util.spec_from_file_location("appmod", REPO_ROOT / "run.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["appmod"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def app(app_module):
    return app_module.app


class Response:
    __slots__ = ("status", "text", "headers")

    def __init__(self, status: int, text: str, headers=None) -> None:
        self.status = status
        self.text = text
        # Lowercased: gunicorn sends `content-type`, Werkzeug `Content-Type`;
        # assertions must not care.
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}

    @property
    def ok(self) -> bool:
        return self.status == 200

    def header(self, name: str, default: str = "") -> str:
        return self.headers.get(name.lower(), default)

    @property
    def content_type(self) -> str:
        return self.header("Content-Type")

    def __repr__(self) -> str:  # pragma: no cover - assertion output only
        return f"<Response {self.status} {self.content_type} {len(self.text)}b>"


class Client:
    """`.get(path, user_agent=..., accept=...) -> Response` over Werkzeug."""

    def __init__(self, raw) -> None:
        self._raw = raw

    def get(self, path: str, user_agent: str = BROWSER_UA,
            accept: str | None = None) -> Response:
        headers = {"User-Agent": user_agent}
        if accept is not None:
            headers["Accept"] = accept
        r = self._raw.get(path, headers=headers)
        # errors="replace", not `as_text=True`: strict decoding raises on any
        # binary response, so a test that merely checks a favicon RESOLVES
        # would blow up on the icon's first byte.
        return Response(r.status_code, r.get_data().decode("utf-8", "replace"),
                        dict(r.headers))


@pytest.fixture(scope="session")
def client(app):
    return Client(app.server.test_client())


@pytest.fixture(scope="session")
def tmp_state_dir():
    """Where the analytics hit log lives for this run."""
    return _TMP_STATE


@pytest.fixture(scope="session")
def pages(app_module):
    """Every CRAWLABLE page as (path, entry), sorted by path.

    /admin/* is excluded on purpose: the control board fails CLOSED to
    anonymous renders (its crawler body is deliberately empty, and dimll's
    `mark_hidden` keeps it out of the sitemap), so every prose-substance
    and route-200 sweep in this suite would flag exactly the behaviour the
    board is supposed to have. tests/test_control_board.py owns that page's
    assertions, and it addresses it by path rather than through this
    fixture — which is also why EXPECTED_ROUTES stayed put when the board
    arrived. Same exclusion, same reason, as the boilerplate's conftest.
    """
    import dash

    return sorted(((entry["path"], entry)
                   for entry in dash.page_registry.values()
                   if not entry["path"].startswith("/admin/")),
                  key=lambda item: item[0])


@pytest.fixture(scope="session")
def page_paths(pages):
    return [path for path, _entry in pages]


def component_iter(node):
    """Depth-first over every Dash component reachable from ``node`` —
    through children AND through any component-valued prop (dmc uses
    label=/leftSection=/etc. freely). Same walker as scripts/route_parity.py."""
    from dash.development.base_component import Component

    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, Component):
            yield cur
            for name in cur._prop_names:
                val = getattr(cur, name, None)
                if val is not None and name != "id":
                    stack.append(val)
        elif isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, dict):
            stack.extend(cur.values())


def layout_text(layout) -> str:
    """Every string prop value in a layout tree, joined — a haystack for
    asserting that rendered copy (a license banner, a version badge) exists
    without caring where in the tree it sits."""
    parts: list[str] = []
    for comp in component_iter(layout):
        for name in comp._prop_names:
            val = getattr(comp, name, None)
            if isinstance(val, str):
                parts.append(val)
    return "\n".join(parts)


def page_layout(entry):
    """A page's constructed layout, whether registered as a value or a callable."""
    layout = entry.get("layout")
    if layout is None:
        layout = getattr(sys.modules[entry["module"]], "layout", None)
    return layout() if callable(layout) else layout
