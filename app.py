"""
Dash MUI Charts — Demo Application
Professional AppShell layout with sidebar tree navigation and dark/light mode.
"""

import os

import dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Input, Output, State, page_container, clientside_callback
from dash_iconify import DashIconify

from dash_mui_charts import SimpleTreeView

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Load custom index template with SEO meta tags, favicon randomizer, and analytics
_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
with open(_template_path, encoding='utf-8') as _f:
    _index_string = _f.read()

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    index_string=_index_string,
)
server = app.server  # WSGI entry point for gunicorn: gunicorn app:server

# Store license key for pages
app.server.config['MUI_LICENSE_KEY'] = MUI_LICENSE_KEY

# ---------------------------------------------------------------------------
# Navigation tree items — groups use "group-*" ids, leaves use page paths
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    {"itemId": "/", "label": "Home"},
    {"itemId": "group-linechart", "label": "LineChart", "children": [
        {"itemId": "/linechart-basic", "label": "Basics"},
        {"itemId": "/linechart-pro", "label": "Pro Features"},
        {"itemId": "/linechart-brush", "label": "Brush Selection"},
        {"itemId": "/linechart-referencelines", "label": "Reference Lines"},
        {"itemId": "/linechart-highlighting", "label": "Highlighting"},
        {"itemId": "/highlighting-sync", "label": "Highlighting Sync"},
        {"itemId": "/linechart-zoom-preview", "label": "Zoom Preview"},
        {"itemId": "/linechart-tick-hover", "label": "Ticks & Hover"},
        {"itemId": "/crosshair", "label": "Crosshair"},
    ]},
    {"itemId": "group-barchart", "label": "BarChart", "children": [
        {"itemId": "/barchart-basic", "label": "Basic"},
        {"itemId": "/barchart-dataset", "label": "Dataset Mode"},
        {"itemId": "/barchart-stacking", "label": "Stacking"},
        {"itemId": "/barchart-interaction", "label": "Interaction"},
        {"itemId": "/barchart-reference", "label": "Reference Lines"},
        {"itemId": "/barchart-pro", "label": "Pro Features"},
    ]},
    {"itemId": "group-candlestick", "label": "CandlestickChart", "children": [
        {"itemId": "/candlestick", "label": "OHLC Charts"},
    ]},
    {"itemId": "group-pie", "label": "PieChart", "children": [
        {"itemId": "/pie", "label": "Examples"},
        {"itemId": "/pie-props", "label": "Props Explorer"},
    ]},
    {"itemId": "group-scatter", "label": "ScatterChart", "children": [
        {"itemId": "/scatter", "label": "Examples"},
    ]},
    {"itemId": "group-composite", "label": "CompositeChart", "children": [
        {"itemId": "/composite", "label": "Examples"},
        {"itemId": "/composite-v120", "label": "v1.2.0"},
        {"itemId": "/composite-render-bp", "label": "Render BP"},
    ]},
    {"itemId": "group-heatmap", "label": "Heatmap", "children": [
        {"itemId": "/heatmap", "label": "Examples"},
        {"itemId": "/heatmap-props", "label": "Props Explorer"},
    ]},
    {"itemId": "group-sparkline", "label": "SparklineChart", "children": [
        {"itemId": "/sparkline", "label": "Examples"},
        {"itemId": "/sparkline-style", "label": "Styling"},
        {"itemId": "/sparkline-style-advanced", "label": "Advanced"},
    ]},
    {"itemId": "group-livetrading", "label": "LiveTradingChart", "children": [
        {"itemId": "/live-trading", "label": "Examples"},
    ]},
    {"itemId": "group-treeview", "label": "TreeView", "children": [
        {"itemId": "/tree-basic", "label": "Basic"},
        {"itemId": "/tree-simple", "label": "Simple"},
        {"itemId": "/tree-selection", "label": "Selection"},
        {"itemId": "/tree-expansion", "label": "Expansion"},
        {"itemId": "/tree-editing", "label": "Editing"},
        {"itemId": "/tree-icons", "label": "Icons"},
        {"itemId": "/tree-disabled", "label": "Disabled"},
        {"itemId": "/tree-pro", "label": "Pro"},
    ]},
]

ALL_GROUP_IDS = [item["itemId"] for item in NAV_ITEMS if item["itemId"].startswith("group-")]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
theme_toggle = dmc.ColorSchemeToggle(
    lightIcon=DashIconify(icon="radix-icons:sun", width=18),
    darkIcon=DashIconify(icon="radix-icons:moon", width=18),
    size="md",
)

header = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Text("Dash MUI Charts", fw=700, size="lg"),
                    dmc.Badge("v1.2.0", variant="light", size="sm", color="blue",
                              visibleFrom="xs"),
                ],
                gap="xs",
            ),
            dmc.Group(
                [
                    theme_toggle,
                    html.A(
                        dmc.ActionIcon(
                            DashIconify(icon="mdi:github", width=22),
                            variant="subtle",
                            color="gray",
                            size="lg",
                        ),
                        href="https://github.com/pip-install-python/dash-mui-charts",
                        target="_blank",
                    ),
                ],
                gap="sm",
            ),
        ],
        justify="space-between",
        h="100%",
        px="md",
        style={"flex": 1},
    )
)

navbar = dmc.AppShellNavbar(
    html.Div(
        [
            html.Div(
                SimpleTreeView(
                    id="nav-tree",
                    items=NAV_ITEMS,
                    defaultExpandedItems=ALL_GROUP_IDS,
                    itemChildrenIndentation="20px",
                    sx={
                        "& .MuiTreeItem-label": {
                            "fontSize": "14px",
                            "lineHeight": "1.6",
                        },
                        "& .MuiTreeItem-content": {
                            "padding": "4px 10px",
                            "borderRadius": "6px",
                            "minHeight": "34px",
                        },
                    },
                ),
                style={
                    "flex": "1 1 0",
                    "overflowY": "auto",
                    "overflowX": "hidden",
                    "padding": "12px",
                },
            ),
            html.Div(
                dmc.Text("Pip Install Python", size="xs", c="dimmed", ta="center", py="xs"),
                style={"borderTop": "1px solid var(--mantine-color-default-border)"},
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "height": "100%",
        },
    ),
    p=0,
)

app.layout = dmc.MantineProvider(
    [
        dmc.pre_render_color_scheme(),
        dmc.AppShell(
            [
                header,
                navbar,
                dmc.AppShellMain(page_container),
            ],
            header={"height": 60},
            navbar={
                "width": 260,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            padding="md",
            id="appshell",
        ),
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="license-key-store", data=MUI_LICENSE_KEY),
    ],
)

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

# 1. Tree selection → navigate via window.location (avoids Dash circular deps)
clientside_callback(
    """
    (selected) => {
        if (selected && typeof selected === 'string' && selected.startsWith('/')) {
            if (window.location.pathname !== selected) {
                window.location.pathname = selected;
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("nav-tree", "id"),
    Input("nav-tree", "selectedItems"),
)

# 2. Sync tree highlight to current URL on page load (no cycle — url.pathname
#    is only changed by window.location, not by any Dash Output)
clientside_callback(
    """
    (pathname) => {
        return pathname || '/';
    }
    """,
    Output("nav-tree", "selectedItems"),
    Input("url", "pathname"),
)

# 3. Burger toggle for mobile navbar
@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar_config):
    navbar_config["collapsed"] = {"mobile": not opened}
    return navbar_config



if __name__ == '__main__':
    app.run(debug=True, port=7666)
