"""
Home Page - Dash MUI Charts Examples
"""

import dash
import dash_mantine_components as dmc
from dash import html, dcc

dash.register_page(__name__, path='/', name='Home')

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
    return dcc.Link(
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
                    dmc.Badge("v1.2.0", size="lg", variant="light", color="blue"),
                    dmc.Badge("9 Components", size="lg", variant="light", color="gray"),
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

    # New in v1.2.0
    dmc.Title("New in v1.2.0", order=2, mb="md"),
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
