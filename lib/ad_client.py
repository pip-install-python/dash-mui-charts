"""2plot.dev ad-network client for satellite documentation apps.

Drop-in module shared verbatim across every dash-documentation-boilerplate
app (dash-email, dash-mui-scheduler, dash-flows, dash-mui-charts, ...).
On each docs page view the ad slot fetches a campaign from the central
2plot.dev ad server (server-to-server, so ad blockers and CORS never see
it); clicks are beaconed from the browser straight back to 2plot.dev with
app + page attribution, feeding the /admin/ad-board performance tables.

Wiring (boilerplate apps):
    # pages/markdown.py — after `layout = parse(content)`:
    from lib.ad_client import inject_ad_into_aside
    inject_ad_into_aside(layout, metadata.endpoint)

Wiring (custom apps without the markdown TOC aside):
    from lib.ad_client import create_ad_component, register_shell_ad
    ...place create_ad_component("__floating__", compact=True) in the shell...
    register_shell_ad("url", exclude_paths=("/",))  # serve per navigation

Env:
    AD_SERVER_URL  — ad server origin (default https://2plot.dev)
    AD_APP_ID      — this app's identity in the network (default from
                     the APP_ID fallback below; override per deployment)

Failure behaviour: if the ad server is unreachable the slot simply stays
hidden, and a 60s circuit breaker stops retrying so an outage never adds
the HTTP timeout to every page view.
"""
from __future__ import annotations

import logging
import os
import threading
import time

import requests
import dash_mantine_components as dmc
from dash import MATCH, Input, Output, callback, clientside_callback, dcc, html, no_update
from dash_iconify import DashIconify

logger = logging.getLogger(__name__)

AD_SERVER_URL = os.environ.get("AD_SERVER_URL", "https://2plot.dev").rstrip("/")
APP_ID = os.environ.get("AD_APP_ID", "dash-mui-charts")

_TIMEOUT = 2          # seconds per fetch — never stall a page view longer
_COOLDOWN = 60        # seconds to skip fetches after a failure
_session = requests.Session()
_breaker_lock = threading.Lock()
_last_failure = 0.0


def fetch_ad(page: str) -> dict | None:
    """GET one campaign from the ad server; None on any failure.

    Deliberately no caching of last-good ads: every served ad is logged as
    an impression server-side, and a cached ad would corrupt CTR. Failures
    trip a cooldown so an ad-server outage costs at most one timeout per
    process per minute.
    """
    global _last_failure
    with _breaker_lock:
        if time.time() - _last_failure < _COOLDOWN:
            return None
    try:
        resp = _session.get(
            f"{AD_SERVER_URL}/api/ad-network/serve",
            params={"app": APP_ID, "page": page},
            timeout=_TIMEOUT,
        )
        if resp.status_code == 200 and resp.content:
            return resp.json()
        return None  # 204 = nothing to serve; not a failure
    except Exception as e:
        with _breaker_lock:
            _last_failure = time.time()
        logger.debug("Ad fetch failed (%s) — cooling down %ss", e, _COOLDOWN)
        return None


def create_ad_component(page_path: str, compact: bool = False) -> html.Div:
    """Hidden ad shell; the serve callback below fills it per page view.

    ``compact=True`` drops the section divider and adds a shadow — for
    floating placements where the card is not part of a document flow.
    """
    divider = [] if compact else [
        dmc.Divider(
            label="Advertisement",
            labelPosition="center",
            mb="md",
            mt="xl",
            styles={
                "label": {
                    "fontSize": "0.75rem",
                    "fontWeight": 600,
                    "textTransform": "uppercase",
                    "letterSpacing": "0.5px",
                    "color": "var(--mantine-color-gray-6)",
                }
            },
        ),
    ]
    return html.Div(
        id={"type": "net-ad-container", "page": page_path},
        style={"display": "none"},
        children=[
            dcc.Store(id={"type": "net-ad-data", "page": page_path}, data=None),
            *divider,
            html.A(
                href="#",
                target="_blank",
                rel="noopener noreferrer sponsored",
                id={"type": "net-ad-link", "page": page_path},
                style={"textDecoration": "none"},
                children=dmc.Paper(
                    [
                        html.Img(
                            id={"type": "net-ad-img", "page": page_path},
                            src="",
                            alt="Advertisement",
                            style={
                                "width": "100%",
                                "height": "auto",
                                "display": "block",
                                "borderRadius": "8px",
                            },
                        ),
                        dmc.Text(
                            [
                                DashIconify(icon="tabler:info-circle", width=12,
                                            style={"marginRight": "4px"}),
                                "Sponsored Content",
                            ],
                            size="xs",
                            c="gray",
                            ta="center",
                            mt="xs",
                            style={"display": "flex", "alignItems": "center",
                                   "justifyContent": "center"},
                        ),
                    ],
                    p="sm",
                    withBorder=True,
                    radius="md",
                    shadow="md" if compact else None,
                    style={"cursor": "pointer"},
                ),
            ),
        ],
    )


def inject_ad_into_aside(layout_list, page_path: str) -> bool:
    """Append the ad slot below the TOC links inside the page's aside.

    The `.. toc::` directive emits
    ``AppShellAside(children=ScrollArea(Stack([...])))`` — the ad joins the
    Stack so it scrolls with the TOC. Pages without a TOC get no ad.
    Fail-silent: an unexpected layout shape must never break page
    registration.
    """
    try:
        for el in layout_list:
            if isinstance(el, dmc.AppShellAside):
                stack = el.children.children  # ScrollArea -> Stack
                kids = stack.children
                if not isinstance(kids, list):
                    kids = [kids]
                kids.append(create_ad_component(page_path))
                stack.children = kids
                return True
    except Exception as e:
        logger.warning("Ad slot injection failed for %s: %s", page_path, e)
    return False


_AD_OUTPUTS = lambda match: (  # noqa: E731 — shared output signature
    Output({"type": "net-ad-img", "page": match}, "src"),
    Output({"type": "net-ad-img", "page": match}, "alt"),
    Output({"type": "net-ad-link", "page": match}, "href"),
    Output({"type": "net-ad-data", "page": match}, "data"),
    Output({"type": "net-ad-container", "page": match}, "style"),
)


def _serve(page: str):
    ad = fetch_ad(page)
    if not ad:
        return no_update, no_update, no_update, no_update, {"display": "none"}
    return (
        ad.get("image", ""),
        ad.get("name", "Advertisement"),
        ad.get("url", "#"),
        {
            "campaign_id": ad.get("campaign_id"),
            "app": APP_ID,
            "page": page,
            "click_url": f"{AD_SERVER_URL}/api/ad-network/click",
        },
        {},
    )


# NOTE (dash-mui-charts divergence from the canonical boilerplate copy):
# this app's only ad slot lives in the static shell, so the generic
# mount-fired MATCH callback is intentionally absent — with it, every hard
# load would fetch twice (mount + location) and log a double impression.
# The location callback in register_shell_ad below is the sole driver.


# Click beacon: browser → 2plot.dev directly. text/plain keeps it a CORS
# "simple request" (no preflight), which also keeps keepalive reliable.
clientside_callback(
    """
    function(n_clicks, adData) {
        if (n_clicks && adData && adData.click_url) {
            try {
                fetch(adData.click_url, {
                    method: 'POST',
                    keepalive: true,
                    headers: {'Content-Type': 'text/plain'},
                    body: JSON.stringify({
                        campaign_id: adData.campaign_id,
                        app: adData.app,
                        page: adData.page
                    })
                }).catch(function(){});
            } catch (e) {}
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output({"type": "net-ad-link", "page": MATCH}, "title"),
    Input({"type": "net-ad-link", "page": MATCH}, "n_clicks"),
    Input({"type": "net-ad-data", "page": MATCH}, "data"),
    prevent_initial_call=True,
)


def register_shell_ad(location_id: str = "url",
                      page_key: str = "__floating__",
                      exclude_paths: tuple[str, ...] = ()) -> None:
    """Drive a static-shell ad slot from the URL bar.

    Fires on hard load and on every SPA navigation, attributing the real
    pathname. Paths in ``exclude_paths`` keep the slot hidden and fetch
    nothing (no impression is logged for them).
    """
    excluded = {(p.rstrip("/") or "/") for p in exclude_paths}

    @callback(
        *_AD_OUTPUTS(page_key),
        Input(location_id, "pathname"),
        prevent_initial_call=False,
    )
    def refresh_shell_ad(pathname):
        path = (pathname or "/").rstrip("/") or "/"
        if path in excluded:
            # clear the store too so a stale click_url can't outlive the hide
            return no_update, no_update, no_update, None, {"display": "none"}
        return _serve(path)
