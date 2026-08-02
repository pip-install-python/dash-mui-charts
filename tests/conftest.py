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
built-in tips), and the analytics hit log in a temp dir so a test run never
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
SECRET_ENV_KEYS = (
    "MUI_PRO_API_KEY",
    "CROSS_APP_WEBHOOK_SECRET",
    "NETWORK_BULLETIN_URL",
    "WIDGETBOT_SERVER",
    "WIDGETBOT_CHANNEL",
)
for _key in SECRET_ENV_KEYS:
    os.environ[_key] = ""

# --- 2. Keep app state out of the repo, and identity deterministic ----------
_TMP_STATE = tempfile.mkdtemp(prefix="muicharts-tests-")
os.environ["ANALYTICS_DIR"] = _TMP_STATE
# Reporting is already off (no secret); the explicit kill switch documents it.
os.environ["TRAFFIC_REPORT"] = "0"
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
    """Every registered page as (path, entry), sorted by path."""
    import dash

    return sorted(((entry["path"], entry) for entry in dash.page_registry.values()),
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
