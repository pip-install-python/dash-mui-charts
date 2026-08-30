"""The dogfooding demo: this documentation's own sidebar as a SimpleTreeView.

Before the boilerplate migration, this site's navigation WAS a
SimpleTreeView — the component navigating its own docs. The shell now uses
the network-standard navbar, so the dogfooding story lives here instead:
the tree below is built from the SAME source the real sidebar reads, so it
can never drift from the actual nav, and selecting a leaf genuinely
navigates, exactly as the old sidebar did.

That source moved with sync item 16. The sidebar used to come from a
hand-written FAMILIES map in `components/navbar.py`; it now comes from each
page's own frontmatter (`category:` + `order:`) ordered by
`lib.constants.CATEGORY_ORDER`. This module reads the frontmatter directly
rather than the page registry, because a docs demo is executed WHILE the
registry is still being built — the file on disk is the one source that is
complete at any moment.
"""
import re
from pathlib import Path

from dash import Input, Output, clientside_callback, html

from dash_mui_charts import SimpleTreeView
from lib.constants import CATEGORY_ORDER

_DOCS = Path(__file__).resolve().parent.parent

_ICON_BY_FAMILY = {
    "SparklineChart": "Timeline",
    "PieChart": "PieChart",
    "BarChart": "BarChart",
    "Heatmap": "GridOn",
    "ScatterChart": "ScatterPlot",
    "LineChart": "ShowChart",
    "CandlestickChart": "CandlestickChart",
    "LiveTradingChart": "TrendingUp",
    "CompositeChart": "Layers",
    "TreeView": "AccountTree",
    "Date & Time Pickers": "Schedule",
    "Reference": "MenuBook",
}


def _frontmatter(md):
    out = {}
    for key in ("name", "endpoint", "category", "order"):
        m = re.search(rf"^{key}:\s*(.+?)\s*$", md, re.M)
        if m:
            out[key] = m.group(1)
    return out


def _families():
    """``[(category, [(endpoint, name), ...]), ...]`` in sidebar order."""
    by_cat = {}
    for f in sorted(_DOCS.glob("**/*.md")):
        fm = _frontmatter(f.read_text())
        if not fm.get("endpoint") or not fm.get("category"):
            continue
        try:
            order = int(fm.get("order", 1000))
        except ValueError:
            order = 1000
        by_cat.setdefault(fm["category"], []).append(
            (order, fm["name"], fm["endpoint"]))
    known = [c for c in CATEGORY_ORDER if c in by_cat]
    extra = sorted(c for c in by_cat if c not in CATEGORY_ORDER)
    return [(c, [(e, n) for _o, n, e in sorted(by_cat[c])])
            for c in known + extra]


items = [
    {"itemId": "/", "label": "Home", "icon": "Home"},
    {"itemId": "/changelog", "label": "Changelog", "icon": "History"},
] + [
    {
        "itemId": f"group-{family}",
        "label": family,
        "icon": _ICON_BY_FAMILY.get(family, "Folder"),
        "children": [
            {"itemId": path, "label": name, "icon": "PlayArrow"}
            for path, name in entries
        ],
    }
    for family, entries in _families()
]

component = html.Div(
    [
        html.P(
            "Click a leaf to navigate these docs — the tree is generated "
            "from the site's real navigation map.",
            style={"color": "var(--mantine-color-dimmed)",
                   "fontSize": "14px"},
        ),
        SimpleTreeView(
            id="tree-simple-sidebar-demo",
            items=items,
            defaultExpandedItems=["group-TreeView"],
            itemChildrenIndentation="8px",
            sx={
                "& .MuiTreeItem-label": {"fontSize": "14px",
                                         "lineHeight": "1.6"},
                "& .MuiTreeItem-content": {"padding": "4px 10px",
                                           "borderRadius": "6px",
                                           "minHeight": "34px"},
            },
        ),
    ],
    style={"maxWidth": "320px"},
)


# The old shell's navigation callback, verbatim in spirit: leaf selection
# drives the URL. Groups (non-path ids) are ignored.
clientside_callback(
    """
    (selected) => {
        if (selected && typeof selected === 'string' && selected.startsWith('/')) {
            if (window.location.pathname !== selected) {
                return selected;
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("url", "href", allow_duplicate=True),
    Input("tree-simple-sidebar-demo", "selectedItems"),
    prevent_initial_call=True,
)
