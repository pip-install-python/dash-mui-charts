"""Shared machinery for /terms and /privacy — sync 1.6.44 item 15.

ONE MARKDOWN STRING PER PAGE, rendered for the browser AND handed to the
machine lane. That is the whole design constraint, and it is not tidiness:
a page whose visible prose and whose `llms.txt` are written separately is a
site with TWO privacy policies, and only one of them was ever reviewed. The
browser rendering is derived from the same string the crawler receives, so
they cannot drift.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from lib.constants import PUBLISHER, SITE_SHORT_NAME


def _render(markdown: str):
    """Render through THE SITE'S OWN markdown pipeline, not `dcc.Markdown`.

    Two reasons, and the second is the one that matters. The nav contract
    bans `dcc.` where DMC has an equivalent (requirement 10, fleet-wide) and
    the suite enforces it — this file failed that pin on its first run. But
    the substantive reason is that `pages/markdown.py` renders every other
    document on this site through `markdown2dash`, so using anything else
    here would give the legal pages different typography, different heading
    anchors and a different table style from the rest of the site.
    """
    from pages.markdown import parse

    return parse(markdown)


def legal_layout(markdown: str, updated: str):
    """Render one legal document from its markdown source."""
    return dmc.Container(
        [
            html.Div(_render(markdown), className="m2d-block legal-document"),
            dmc.Divider(my="xl"),
            dmc.Text(
                f"Last updated {updated} · {PUBLISHER} · {SITE_SHORT_NAME}",
                size="xs",
                c="dimmed",
            ),
            html.Div(style={"height": "2rem"}),
        ],
        size="md",
        px="md",
        py="lg",
    )
