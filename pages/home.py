"""
Home Page - Dash MUI Charts Examples
"""

import dash
import dash_mantine_components as dmc
from dash import html
from dash_mui_charts import __version__ as _PKG_VERSION

from lib.constants import OG_IMAGE_URL, SITE_BRAND, SITE_DESCRIPTION

dash.register_page(
    __name__,
    path='/',
    name='Home',
    title=SITE_BRAND,
    description=SITE_DESCRIPTION,
    image_url=OG_IMAGE_URL,
)

LLMS_DOC = """\
# dash-mui-charts

dash-mui-charts is a Plotly Dash component library of 13 components wrapping
MUI X Charts, MUI X Tree View, and MUI X Date & Time Pickers for Python
developers. Every component ships with full Python type hints and exposes
its interactions (clicks, selections, zoom, edits) as Dash callback
properties. Built by Pip Install Python; MIT licensed.

## Install

```bash
pip install dash-mui-charts
```

## Components

Charts (MUI X Charts):

- **LineChart** — line/area charts, biaxial axes, zoom/pan, brush selection,
  reference lines (Community / Pro). Docs: /linechart-basic
- **BarChart** — vertical/horizontal bars, stacking, bar labels, dataset
  mode, zoom/brush (Community / Pro). Docs: /barchart-basic
- **CandlestickChart** — OHLC candlesticks with volume overlay, reference
  lines, click events (Community / Pro). Docs: /candlestick
- **PieChart** — pie, donut, and nested pies (Community). Docs: /pie
- **ScatterChart** — scatter/point charts, z-axis color mapping, voronoi
  interaction (Community). Docs: /scatter
- **CompositeChart** — layer scatter + line plots on one surface, multi-axis
  (Community / Pro). Docs: /composite
- **Heatmap** — matrix/grid visualization with color scales (Pro).
  Docs: /heatmap
- **SparklineChart** — compact inline charts for dashboards and tables
  (Community). Docs: /sparkline
- **LiveTradingChart** — real-time streaming charts (Community / Pro).
  Docs: /live-trading

Tree View (MUI X Tree View):

- **TreeView** — data-driven RichTreeView: selection, expansion, inline
  label editing, disabling (Community). Docs: /tree-basic
- **SimpleTreeView** — lightweight JSX-driven tree for navigation sidebars
  (Community). Docs: /tree-simple
- **TreeViewPro** — drag-and-drop reordering, lazy loading, per-item
  slider + kebab menu controls (Pro). Docs: /tree-pro

Date & Time Pickers (MUI X Date Pickers):

- **TimeClock** — inline clock-face time picker, string in/out values
  (Community). Docs: /time-clock

## Community vs Pro

Community features work with no license. MUI X Pro features — LineChart /
BarChart / CompositeChart zoom, pan, slider, brush and toolbar; Heatmap;
TreeViewPro reordering, lazy loading and per-item controls — require an
MUI X Pro license key passed via the `licenseKey` prop (the demo app reads
it from the `MUI_PRO_API_KEY` environment variable).

## Quick start

```python
from dash import Dash, html
from dash_mui_charts import LineChart

app = Dash(__name__)

app.layout = html.Div([
    LineChart(
        id='my-chart',
        height=400,
        series=[
            {'data': [1, 4, 2, 5, 7], 'label': 'Series A'},
        ],
        xAxis=[{'data': [1, 2, 3, 4, 5]}],
    )
])

if __name__ == '__main__':
    app.run(debug=True)
```

## More documentation pages

- LineChart: /linechart-pro, /linechart-brush, /linechart-referencelines,
  /linechart-highlighting, /highlighting-sync, /linechart-zoom-preview,
  /linechart-tick-hover, /crosshair
- BarChart: /barchart-dataset, /barchart-stacking, /barchart-interaction,
  /barchart-reference, /barchart-pro
- Pie / Heatmap / Sparkline explorers: /pie-props, /heatmap-props,
  /sparkline-style, /sparkline-style-advanced
- CompositeChart: /composite-v120, /composite-render-bp
- Tree View: /tree-selection, /tree-expansion, /tree-editing, /tree-icons,
  /tree-disabled, /tree-pro
- TimeClock: /time-clock-lab
- Release history: /changelog

## Links

- GitHub: https://github.com/pip-install-python/dash-mui-charts
- PyPI: https://pypi.org/project/dash-mui-charts/
- MUI X Charts: https://mui.com/x/react-charts/
"""

INSTALL_CODE = "pip install dash-mui-charts"

USAGE_CODE = '''from dash import Dash, html
from dash_mui_charts import LineChart

app = Dash(__name__)

app.layout = html.Div([
    LineChart(
        id='my-chart',
        height=400,
        series=[
            {'data': [1, 4, 2, 5, 7], 'label': 'Series A'},
        ],
        xAxis=[{'data': [1, 2, 3, 4, 5]}],
    )
])

if __name__ == '__main__':
    app.run(debug=True)'''

BAR_CODE = '''from dash_mui_charts import BarChart

BarChart(
    series=[
        {'data': [4, 3, 5], 'label': 'Group A', 'color': '#1976d2'},
        {'data': [1, 6, 3], 'label': 'Group B', 'color': '#388e3c'},
    ],
    xAxis=[{'data': ['Q1', 'Q2', 'Q3'], 'scaleType': 'band'}],
    height=350,
    grid={'horizontal': True},
)'''

CANDLE_CODE = '''from dash_mui_charts import CandlestickChart

CandlestickChart(
    series=[{
        'data': [
            [100, 110, 95, 105],   # [open, high, low, close]
            [105, 115, 100, 112],
            [112, 120, 108, 118],
        ],
        'upColor': '#4caf50',
        'downColor': '#f44336',
    }],
    xAxis=[{'data': ['Mon', 'Tue', 'Wed']}],
    yAxis=[{'label': 'Price ($)'}],
    height=400,
)'''

# Component cards data
COMPONENTS = [
    {
        "name": "LineChart",
        "desc": "Line and area charts with zoom/pan, multiple axes, stacking, brush selection, and reference lines.",
        "tags": ["Multi-Series", "Area", "Biaxial", "Zoom", "Brush"],
        "link": "/linechart-basic",
        "color": "blue",
    },
    {
        "name": "BarChart",
        "desc": "Vertical and horizontal bars with stacking, labels, dataset mode, and Pro zoom/brush features.",
        "tags": ["Stacking", "Labels", "Dataset", "Horizontal", "Zoom"],
        "link": "/barchart-basic",
        "color": "indigo",
    },
    {
        "name": "CandlestickChart",
        "desc": "OHLC candlestick charts with volume overlay, reference lines, and click events.",
        "tags": ["OHLC", "Volume", "Finance", "Click Events"],
        "link": "/candlestick",
        "color": "teal",
    },
    {
        "name": "PieChart",
        "desc": "Pie, donut, and nested/concentric pie charts with highlight interactions.",
        "tags": ["Donut", "Nested", "Labels", "Highlight"],
        "link": "/pie",
        "color": "grape",
    },
    {
        "name": "ScatterChart",
        "desc": "Scatter/point charts with z-axis color mapping, voronoi interaction, and batch rendering.",
        "tags": ["Z-Axis", "Voronoi", "Color Map", "Dataset"],
        "link": "/scatter",
        "color": "orange",
    },
    {
        "name": "CompositeChart",
        "desc": "Layer scatter and line plots on a single surface with multi-axis and zoom/pan.",
        "tags": ["Layered", "Multi-Axis", "Zoom", "Tooltip"],
        "link": "/composite",
        "color": "cyan",
    },
    {
        "name": "Heatmap",
        "desc": "Matrix/grid visualization with continuous or piecewise color scales.",
        "tags": ["Matrix", "Color Scale", "Pro"],
        "link": "/heatmap",
        "color": "red",
    },
    {
        "name": "SparklineChart",
        "desc": "Compact inline charts for dashboards and tables with line or bar plot types.",
        "tags": ["Compact", "Inline", "Line", "Bar"],
        "link": "/sparkline",
        "color": "pink",
    },
    {
        "name": "LiveTradingChart",
        "desc": "Real-time streaming chart component for live data visualization.",
        "tags": ["Real-time", "Streaming", "Alerts"],
        "link": "/live-trading",
        "color": "green",
    },
]


def make_component_card(comp):
    # dmc.Anchor, not dcc.Link (sync item 16 contract 9): never dcc where DMC
    # has the component. Only Location, Store, Interval, Upload and Graph have
    # no equivalent and stay.
    return dmc.Anchor(
        dmc.Paper(
            [
                dmc.Group(
                    [
                        dmc.Text(comp["name"], fw=600, size="lg"),
                        dmc.Badge("PRO", size="xs", color="orange", variant="light")
                        if "Zoom" in comp.get("tags", []) or "Pro" in comp.get("tags", [])
                        else None,
                    ],
                    gap="xs",
                    mb=4,
                ),
                dmc.Text(comp["desc"], size="sm", c="dimmed", mb="sm"),
                dmc.Group(
                    [dmc.Badge(tag, size="xs", variant="light", color=comp["color"]) for tag in comp["tags"]],
                    gap=6,
                ),
            ],
            p="lg",
            radius="md",
            withBorder=True,
            style={"cursor": "pointer", "transition": "box-shadow 0.15s", "height": "100%"},
            className="home-card",
        ),
        href=comp["link"],
        underline=False,
        style={"textDecoration": "none"},
    )


layout = html.Div([
    # Hero
    dmc.Stack(
        [
            dmc.Title("Dash MUI Charts", order=1, c="blue"),
            dmc.Text(
                "A Dash component library wrapping MUI X Charts for creating "
                "beautiful, interactive data visualizations in Python.",
                size="lg",
                c="dimmed",
                maw=700,
            ),
            dmc.Group(
                [
                    # Derived, never written: the hardcoded "v1.2.1" here
                    # survived two releases (network standard: version claims
                    # come from the installed package — see lib/versions.py).
                    dmc.Badge(f"v{_PKG_VERSION}", size="lg", variant="light",
                              color="blue"),
                    dmc.Badge(f"{len(COMPONENTS)} Components", size="lg",
                              variant="light", color="gray"),
                    dmc.Badge("MIT License", size="lg", variant="light", color="green"),
                ],
                gap="sm",
            ),
        ],
        align="center",
        ta="center",
        py="xl",
        gap="sm",
    ),

    # Components Grid
    dmc.Title("Components", order=2, mb="md"),
    dmc.SimpleGrid(
        [make_component_card(c) for c in COMPONENTS],
        cols={"base": 1, "sm": 2, "lg": 3},
        spacing="md",
        mb="xl",
    ),

    # Getting Started
    dmc.Title("Getting Started", order=2, mb="md"),
    dmc.Paper(
        [
            dmc.Title("Installation", order=4, mb="xs"),
            dmc.CodeHighlight(
                code=INSTALL_CODE,
                language="bash",
            ),
            dmc.Title("Basic Usage", order=4, mt="lg", mb="xs"),
            dmc.CodeHighlight(
                code=USAGE_CODE,
                language="python",
            ),
        ],
        p="lg",
        radius="md",
        withBorder=True,
        mb="xl",
    ),

    # New in v1.2.1
    dmc.Title("New in v1.2.1", order=2, mb="md"),
    dmc.SimpleGrid(
        [
            dmc.Paper(
                [
                    dmc.Title("BarChart", order=4, mb="xs"),
                    dmc.Text(
                        "Vertical/horizontal bars with stacking, labels, dataset mode, reference lines, and Pro zoom/brush.",
                        size="sm", c="dimmed", mb="sm",
                    ),
                    dmc.CodeHighlight(code=BAR_CODE, language="python"),
                ],
                p="lg",
                radius="md",
                withBorder=True,
            ),
            dmc.Paper(
                [
                    dmc.Title("CandlestickChart", order=4, mb="xs"),
                    dmc.Text(
                        "OHLC candlestick charts with volume overlay, custom styling, and click events.",
                        size="sm", c="dimmed", mb="sm",
                    ),
                    dmc.CodeHighlight(code=CANDLE_CODE, language="python"),
                ],
                p="lg",
                radius="md",
                withBorder=True,
            ),
        ],
        cols={"base": 1, "lg": 2},
        spacing="md",
        mb="xl",
    ),
])
