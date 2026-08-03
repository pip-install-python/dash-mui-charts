"""Cross-host directory for the 2plot network — one definition, every satellite.

Search engines follow links between hosts weakly; agents don't follow them at
all. Landing on muicharts.2plot.dev a model sees one library, with nothing in
the markup saying the other hosts exist — sitemap.xml cannot fix that, being
scoped to its own origin by design. dash-improve-my-llms emits an explicit
machine-readable directory instead: ``<link rel="related">`` tags in
``<head>``, a ``## Network`` section in ``/llms.txt``, and followed links in
the prerendered body.

The canonical copy lives in the boilerplate; satellites copy it and note any
deliberate divergence. This copy is based on dash-email's (whose peer list
was verified host-by-host on 2026-07-31, dropping two NXDOMAIN entries the
boilerplate still lists) with two changes of its own:

- dash-mui-charts (muicharts.2plot.dev) is ADDED — this is the change that
  ships it; ``peers_for()`` drops it from this host's own peer list, and
  every other satellite's copy should gain it via the boilerplate.
- MUI X (mui.com/x) joins EXTERNAL: it is the upstream library all 13 of
  this site's components wrap, referenced on nearly every page.

Usage in app.py, before ``add_llms_routes(app)``::

    from lib.constants import BASE_URL
    from lib import network_directory

    app._base_url = BASE_URL
    network_directory.apply(BASE_URL)
"""

from __future__ import annotations

from typing import Any, Dict, List

PEERS: List[Dict[str, str]] = [
    {
        "name": "2plot.ai",
        "url": "https://2plot.ai",
        "description": "Network hub and account origin.",
    },
    {
        "name": "2plot.dev",
        "url": "https://2plot.dev",
        "description": "Package index for every open-source component in the network.",
    },
    {
        "name": "Documentation boilerplate",
        "url": "https://boilerplate.2plot.dev",
        "description": "The markdown-driven documentation template every satellite site is built from.",
    },
    {
        "name": "dash-leaflet2",
        "url": "https://leaflet.2plot.dev",
        "description": "Leaflet 2 maps as Dash components.",
    },
    {
        "name": "dash-mui-scheduler",
        "url": "https://muischeduler.2plot.dev",
        "description": "MUI X Scheduler — calendars and event scheduling for Dash.",
    },
    {
        "name": "dash-mui-charts",
        "url": "https://muicharts.2plot.dev",
        "description": "MUI X charts, tree views and time pickers for Dash.",
    },
    {
        "name": "dash-flows",
        "url": "https://flows.2plot.dev",
        "description": "Node-graph editors built on React Flow.",
    },
    {
        "name": "dash-improve-my-llms",
        "url": "https://llms.2plot.dev",
        "description": "The AI/LLM and SEO package every site in this network is built on.",
    },
    {
        "name": "dash-email",
        "url": "https://email.2plot.dev",
        "description": "Email composition and delivery components.",
    },
    # dash-pannellum (pannellum.2plot.dev) and dash-emoji-mart
    # (emojimart.2plot.dev) belong here the day their DNS resolves. Both were
    # NXDOMAIN as of 2026-07-31 (dash-email's verified sweep).
]

AFFILIATED: List[Dict[str, str]] = [
    {
        "name": "Pip Install Python",
        "url": "https://pip-install-python.com",
        "description": "The original component documentation site.",
    },
    {
        "name": "Pirate's Bargain",
        "url": "https://piratesbargain.com",
        "description": "Deal aggregator built on the same Dash stack.",
    },
    {
        "name": "ai-agent.buzz",
        "url": "https://ai-agent.buzz",
        "description": "Agent tooling directory.",
    },
]

EXTERNAL: List[Dict[str, Any]] = [
    {
        "name": "MUI X Charts",
        "url": "https://mui.com/x/react-charts/",
        "description": "The upstream React charting library these components wrap.",
    },
    {
        "name": "Dash Mantine Components",
        "url": "https://www.dash-mantine-components.com",
        "description": "The UI component layer these docs are built with.",
        "llms_txt": "https://www.dash-mantine-components.com/llms.txt",
    },
    {
        "name": "Plotly Dash documentation",
        "url": "https://dash.plotly.com",
        "description": "Upstream framework documentation.",
    },
]

NETWORK_NAME = "The 2plot network"
NETWORK_DESCRIPTION = (
    "Open-source Dash component libraries by Pip Install Python. Each component "
    "has its own documentation site and its own llms.txt; 2plot.dev indexes all "
    "of them, and 2plot.ai is the hub."
)
HUB_URL = "https://2plot.dev"

# The mark drawn in the header of the rendered llms.txt view: "2" + morse
# encoding of "plot" + "ai". Defined here rather than per-app because this
# module is copied verbatim into every satellite — that is what keeps one
# mark across the network instead of twelve slightly different ones.
WORDMARK = {
    "morse": "plot",
    "prefix": "2",
    "suffix": "ai",
    "label": "2plot.ai",
}


def peers_for(app_url: str) -> List[Dict[str, str]]:
    """`PEERS` with this app removed.

    A site listing itself as its own peer reads as generated rather than
    curated, and it wastes a slot in a list an agent may only skim.
    """
    own = app_url.rstrip("/")
    return [p for p in PEERS if p["url"].rstrip("/") != own]


def apply(app_url: str) -> None:
    """Publish the directory for the app served at ``app_url``.

    Degrades rather than fails on older releases of the package: losing the
    directory, or losing the wordmark, is a degradation — refusing to start
    is not.
    """
    try:
        from dash_improve_my_llms import register_network
    except ImportError:  # pragma: no cover - only on <2.1
        import warnings

        warnings.warn(
            "dash-improve-my-llms is older than 2.1, so the cross-host network "
            "directory will not be published. Upgrade to publish it.",
            RuntimeWarning,
            stacklevel=2,
        )
        return

    import inspect

    extra: Dict[str, Any] = {}
    if "wordmark" in inspect.signature(register_network).parameters:
        extra["wordmark"] = WORDMARK

    register_network(
        name=NETWORK_NAME,
        description=NETWORK_DESCRIPTION,
        hub_url=HUB_URL,
        peers=peers_for(app_url),
        affiliated=AFFILIATED,
        external=EXTERNAL,
        **extra,
    )
