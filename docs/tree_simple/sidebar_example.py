"""The dogfooding demo: this documentation's own sidebar as a SimpleTreeView.

Before the boilerplate migration, this site's navigation WAS a
SimpleTreeView — the component navigating its own docs. The shell now uses
the network-standard navbar, so the dogfooding story lives here instead:
the tree below is built from `components/navbar.py`'s real family map (it
can never drift from the actual nav), and selecting a leaf genuinely
navigates, exactly as the old sidebar did.
"""
from dash import Input, Output, clientside_callback, html

from dash_mui_charts import SimpleTreeView
from components.navbar import FAMILIES, TOP_LINKS

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
}

items = [
    {"itemId": path, "label": label, "icon": "Home" if path == "/" else "History"}
    for path, label, _icon in TOP_LINKS
] + [
    {
        "itemId": f"group-{family}",
        "label": family,
        "icon": _ICON_BY_FAMILY.get(family, "Folder"),
        "children": [
            {"itemId": path, "label": label, "icon": "PlayArrow"}
            for path, label, _icon in entries
        ],
    }
    for family, entries in FAMILIES
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
