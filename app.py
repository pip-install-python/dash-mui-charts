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

# ---------------------------------------------------------------------------
# WidgetBot Discord Crate — must register BEFORE Dash()
# ---------------------------------------------------------------------------
from dash_widgetbot import add_discord_crate

WIDGETBOT_SERVER = os.environ.get('WIDGETBOT_SERVER', '')
WIDGETBOT_CHANNEL = os.environ.get('WIDGETBOT_CHANNEL', '')

if WIDGETBOT_SERVER and WIDGETBOT_CHANNEL:
    add_discord_crate(
        server=WIDGETBOT_SERVER,
        channel=WIDGETBOT_CHANNEL,
        color="#1976d2",
        location=["bottom", "right"],
        defer=True,
    )

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
    {"itemId": "/", "label": "Home", "icon": "Home"},
    {"itemId": "/changelog", "label": "Changelog", "icon": "History"},
    {"itemId": "group-sparkline", "label": "SparklineChart", "icon": "Timeline", "children": [
        {"itemId": "/sparkline", "label": "Examples", "icon": "PlayArrow"},
        {"itemId": "/sparkline-style", "label": "Styling", "icon": "Palette"},
        {"itemId": "/sparkline-style-advanced", "label": "Advanced", "icon": "AutoGraph"},
    ]},
    {"itemId": "group-pie", "label": "PieChart", "icon": "PieChart", "children": [
        {"itemId": "/pie", "label": "Examples", "icon": "PlayArrow"},
        {"itemId": "/pie-props", "label": "Props Explorer", "icon": "Tune"},
    ]},
    {"itemId": "group-barchart", "label": "BarChart", "icon": "BarChart", "children": [
        {"itemId": "/barchart-basic", "label": "Basic", "icon": "PlayArrow"},
        {"itemId": "/barchart-dataset", "label": "Dataset Mode", "icon": "TableChart"},
        {"itemId": "/barchart-stacking", "label": "Stacking", "icon": "StackedBarChart"},
        {"itemId": "/barchart-interaction", "label": "Interaction", "icon": "TouchApp"},
        {"itemId": "/barchart-reference", "label": "Reference Lines", "icon": "Rule"},
        {"itemId": "/barchart-pro", "label": "Pro Features", "icon": "Diamond"},
    ]},
    {"itemId": "group-heatmap", "label": "Heatmap", "icon": "GridOn", "children": [
        {"itemId": "/heatmap", "label": "Examples", "icon": "PlayArrow"},
        {"itemId": "/heatmap-props", "label": "Props Explorer", "icon": "Tune"},
    ]},
    {"itemId": "group-scatter", "label": "ScatterChart", "icon": "ScatterPlot", "children": [
        {"itemId": "/scatter", "label": "Examples", "icon": "PlayArrow"},
    ]},
    {"itemId": "group-linechart", "label": "LineChart", "icon": "ShowChart", "children": [
        {"itemId": "/linechart-basic", "label": "Basics", "icon": "PlayArrow"},
        {"itemId": "/linechart-pro", "label": "Pro Features", "icon": "Diamond"},
        {"itemId": "/linechart-brush", "label": "Brush Selection", "icon": "Brush"},
        {"itemId": "/linechart-referencelines", "label": "Reference Lines", "icon": "Rule"},
        {"itemId": "/linechart-highlighting", "label": "Highlighting", "icon": "Highlight"},
        {"itemId": "/highlighting-sync", "label": "Highlighting Sync", "icon": "Sync"},
        {"itemId": "/linechart-zoom-preview", "label": "Zoom Preview", "icon": "ZoomIn"},
        {"itemId": "/linechart-tick-hover", "label": "Ticks & Hover", "icon": "Mouse"},
        {"itemId": "/crosshair", "label": "Crosshair", "icon": "GpsFixed"},
    ]},
    {"itemId": "group-candlestick", "label": "CandlestickChart", "icon": "CandlestickChart", "children": [
        {"itemId": "/candlestick", "label": "OHLC Charts", "icon": "PlayArrow"},
    ]},
    {"itemId": "group-livetrading", "label": "LiveTradingChart", "icon": "TrendingUp", "children": [
        {"itemId": "/live-trading", "label": "Examples", "icon": "PlayArrow"},
    ]},
    {"itemId": "group-composite", "label": "CompositeChart", "icon": "Layers", "children": [
        {"itemId": "/composite", "label": "Examples", "icon": "PlayArrow"},
        {"itemId": "/composite-v120", "label": "v1.2.1", "icon": "Star"},
        {"itemId": "/composite-render-bp", "label": "Render BP", "icon": "Speed"},
    ]},
    {"itemId": "group-treeview", "label": "TreeView", "icon": "AccountTree", "children": [
        {"itemId": "/tree-basic", "label": "Basic", "icon": "PlayArrow"},
        {"itemId": "/tree-simple", "label": "Simple", "icon": "ViewList"},
        {"itemId": "/tree-selection", "label": "Selection", "icon": "CheckBox"},
        {"itemId": "/tree-expansion", "label": "Expansion", "icon": "UnfoldMore"},
        {"itemId": "/tree-editing", "label": "Editing", "icon": "Edit"},
        {"itemId": "/tree-icons", "label": "Icons", "icon": "Palette"},
        {"itemId": "/tree-disabled", "label": "Disabled", "icon": "Block"},
        {"itemId": "/tree-pro", "label": "Pro", "icon": "Diamond"},
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
                    dmc.Avatar(
                        id="header-avatar",
                        src="/assets/favicon_areachart.ico",
                        size="sm",
                        radius="sm",
                    ),
                    dmc.Text("Dash MUI Charts", fw=700, size="lg"),
                    dmc.Badge("v1.2.2", variant="light", size="sm", color="blue",
                              visibleFrom="xs"),
                ],
                gap="xs",
            ),
            dmc.Group(
                [
                    html.A(
                        dmc.ActionIcon(
                            DashIconify(icon="mdi:book-open-variant", width=22),
                            variant="subtle",
                            color="gray",
                            size="lg",
                        ),
                        href="https://pip-install-python.com",
                        target="_blank",
                        title="Pip Install Python — All Packages",
                    ),
                    html.A(
                        dmc.ActionIcon(
                            DashIconify(icon="mdi:github", width=22),
                            variant="subtle",
                            color="gray",
                            size="lg",
                        ),
                        href="https://github.com/pip-install-python/dash-mui-charts",
                        target="_blank",
                        title="GitHub Repository",
                    ),
                    theme_toggle,
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
                    defaultExpandedItems=[],
                    itemChildrenIndentation="8px",
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
                dmc.Text("Pip Install Python LLC", size="xs", c="dimmed", ta="center", py="xs"),
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
        dcc.Location(id="url", refresh="callback-nav"),
        dcc.Store(id="license-key-store", data=MUI_LICENSE_KEY),
    ],
)

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

# 1. Tree selection → SPA navigate via dcc.Location
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
    Output("url", "pathname"),
    Input("nav-tree", "selectedItems"),
)

# 2. Persist expanded state to localStorage (output to dummy, no cycle)
clientside_callback(
    """
    (expanded) => {
        try { localStorage.setItem('nav-tree-expanded', JSON.stringify(expanded || [])); }
        catch(e) {}
        return window.dash_clientside.no_update;
    }
    """,
    Output("nav-tree", "id"),
    Input("nav-tree", "expandedItems"),
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
