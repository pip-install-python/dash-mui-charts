"""
ScatterChart Demo - 0.0.8
Showcases scatter chart features: multi-series, z-axis color maps,
voronoi interaction, marker sizes, click events, and axis styling.
"""

import json
import math
import random

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/scatter', name='Scatter Chart (0.0.8)')

from dash_mui_charts import ScatterChart

# ---------------------------------------------------------------------------
# Generate sample datasets
# ---------------------------------------------------------------------------
random.seed(42)

# Dataset 1: Two clusters
cluster_a = [
    {'x': random.gauss(150, 40), 'y': random.gauss(300, 60), 'id': i}
    for i in range(50)
]
cluster_b = [
    {'x': random.gauss(350, 50), 'y': random.gauss(150, 45), 'id': i}
    for i in range(50)
]

# Dataset 2: Correlated data with z-values
correlated = []
for i in range(80):
    x = random.uniform(0, 100)
    noise = random.gauss(0, 10)
    y = 2 * x + 20 + noise
    z = x + y  # z for color mapping
    correlated.append({'x': round(x, 1), 'y': round(y, 1), 'z': round(z, 1), 'id': i})

# Dataset 3: Log-scale data (simulated processor data)
log_data_a = []
log_data_b = []
for i in range(40):
    year = 1990 + i * 0.8
    density_a = 10 ** (random.uniform(1, 2) + (year - 1990) * 0.06)
    density_b = 10 ** (random.uniform(0.8, 1.8) + (year - 1990) * 0.055)
    log_data_a.append({'x': round(year, 1), 'y': round(density_a), 'id': i})
    log_data_b.append({'x': round(year, 1), 'y': round(density_b), 'id': i})

# Dataset 4: Small dataset for marker sizes
size_data_small = [
    {'x': random.uniform(10, 90), 'y': random.uniform(10, 90), 'id': i}
    for i in range(15)
]
size_data_large = [
    {'x': random.uniform(10, 90), 'y': random.uniform(10, 90), 'id': i}
    for i in range(20)
]

# Common styles
section_style = {'marginBottom': '50px'}
description_style = {'color': '#666', 'marginBottom': '15px'}
code_style = {
    'backgroundColor': '#f5f5f5',
    'padding': '15px',
    'borderRadius': '5px',
    'whiteSpace': 'pre-wrap',
    'fontSize': '12px',
    'overflow': 'auto',
}
new_badge = html.Span(
    "0.0.8",
    style={
        'backgroundColor': '#2e7d32',
        'color': 'white',
        'padding': '2px 8px',
        'borderRadius': '4px',
        'fontSize': '10px',
        'fontWeight': 'bold',
        'marginLeft': '8px',
        'verticalAlign': 'middle',
    }
)

layout = html.Div([
    html.Div([
        html.H1("Scatter Chart", style={'display': 'inline'}),
        new_badge,
    ]),
    html.P(
        "New in 0.0.8: ScatterChart for visualizing relationships between variables. "
        "Supports multiple series, z-axis color mapping, voronoi interaction, "
        "custom marker sizes, and interactive click/highlight callbacks.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # ==========================================================================
    # 1. Basic Scatter
    # ==========================================================================
    html.Div([
        html.H2("Basic Scatter - Two Series"),
        html.P(
            "Two data clusters plotted as separate series with grid lines.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-basic',
            height=350,
            series=[
                {
                    'id': 'cluster-a',
                    'label': 'Cluster A',
                    'data': cluster_a,
                    'color': '#1976d2',
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
                {
                    'id': 'cluster-b',
                    'label': 'Cluster B',
                    'data': cluster_b,
                    'color': '#ff7043',
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
            ],
            grid={'horizontal': True, 'vertical': True},
            xAxis=[{'label': 'X Value'}],
            yAxis=[{'label': 'Y Value', 'width': 50}],
            voronoiMaxRadius=30,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""ScatterChart(
    height=350,
    series=[
        {
            'id': 'cluster-a',
            'label': 'Cluster A',
            'data': [{'x': 150, 'y': 300, 'id': 0}, ...],
            'color': '#1976d2',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
        {
            'id': 'cluster-b',
            'label': 'Cluster B',
            'data': [{'x': 350, 'y': 150, 'id': 0}, ...],
            'color': '#ff7043',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
    ],
    grid={'horizontal': True, 'vertical': True},
    voronoiMaxRadius=30,
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 2. Custom Marker Sizes
    # ==========================================================================
    html.Div([
        html.H2("Custom Marker Sizes"),
        html.P(
            "Use markerSize to differentiate series. Smaller markers for dense data, "
            "larger for emphasis. markerSize is the radius in pixels.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-sizes',
            height=300,
            series=[
                {
                    'id': 'small-markers',
                    'label': 'Background (r=3)',
                    'data': size_data_large,
                    'color': '#90caf9',
                    'markerSize': 3,
                },
                {
                    'id': 'large-markers',
                    'label': 'Focus Points (r=10)',
                    'data': size_data_small,
                    'color': '#e53935',
                    'markerSize': 10,
                    'highlightScope': {'highlight': 'item', 'fade': 'global'},
                },
            ],
            xAxis=[{'label': 'X', 'min': 0, 'max': 100}],
            yAxis=[{'label': 'Y', 'min': 0, 'max': 100, 'width': 40}],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""ScatterChart(
    series=[
        {'label': 'Background (r=3)', 'markerSize': 3, ...},
        {'label': 'Focus Points (r=10)', 'markerSize': 10, ...},
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 3. Z-Axis Color Mapping
    # ==========================================================================
    html.Div([
        html.H2("Z-Axis Color Mapping"),
        html.P(
            "Use zAxis with colorMap to color scatter points by a third variable. "
            "Color priority: z-axis > y-axis > x-axis > series color.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-colormap',
            height=400,
            series=[
                {
                    'id': 'correlated',
                    'label': 'Data Points',
                    'data': correlated,
                    'markerSize': 5,
                },
            ],
            xAxis=[{
                'label': 'X Value',
                'min': -5,
                'max': 105,
            }],
            yAxis=[{
                'label': 'Y Value (2x + 20 + noise)',
                'width': 60,
                'domainLimit': 'nice',
            }],
            zAxis=[{
                'colorMap': {
                    'type': 'continuous',
                    'min': 30,
                    'max': 300,
                    'color': ['#4fc3f7', '#e53935'],
                },
            }],
            grid={'horizontal': True, 'vertical': True},
            voronoiMaxRadius=40,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""ScatterChart(
    series=[{
        'data': [{'x': 10, 'y': 42, 'z': 52, 'id': 0}, ...],
        'markerSize': 5,
    }],
    zAxis=[{
        'colorMap': {
            'type': 'continuous',
            'min': 30,
            'max': 300,
            'color': ['#4fc3f7', '#e53935'],
        },
    }],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 4. Log Scale Axis
    # ==========================================================================
    html.Div([
        html.H2("Log Scale Axis"),
        html.P(
            "Scatter charts support logarithmic axis scales for data spanning "
            "multiple orders of magnitude.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-log',
            height=350,
            series=[
                {
                    'id': 'manufacturer-a',
                    'label': 'Manufacturer A',
                    'data': log_data_a,
                    'markerSize': 4,
                    'color': '#1565c0',
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
                {
                    'id': 'manufacturer-b',
                    'label': 'Manufacturer B',
                    'data': log_data_b,
                    'markerSize': 4,
                    'color': '#e65100',
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
            ],
            xAxis=[{
                'label': 'Year',
                'tickLabelStyle': {'fontSize': 11},
            }],
            yAxis=[{
                'scaleType': 'log',
                'label': 'Density (units/mm\u00B2)',
                'width': 65,
                'tickLabelStyle': {'fontSize': 11},
            }],
            grid={'horizontal': True},
            voronoiMaxRadius=25,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""ScatterChart(
    series=[...],
    yAxis=[{
        'scaleType': 'log',
        'label': 'Density (units/mm\u00B2)',
    }],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 5. Click Events
    # ==========================================================================
    html.Div([
        html.H2("Click Events"),
        html.P(
            "Click on scatter points to capture event data in Dash callbacks. "
            "Uses voronoiMaxRadius to control interaction distance.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-click',
            height=300,
            series=[
                {
                    'id': 'series-a',
                    'label': 'A',
                    'data': [
                        {'x': 1, 'y': 5, 'id': 0},
                        {'x': 2, 'y': 3, 'id': 1},
                        {'x': 3, 'y': 8, 'id': 2},
                        {'x': 4, 'y': 2, 'id': 3},
                        {'x': 5, 'y': 7, 'id': 4},
                        {'x': 6, 'y': 4, 'id': 5},
                        {'x': 7, 'y': 9, 'id': 6},
                        {'x': 8, 'y': 1, 'id': 7},
                    ],
                    'color': '#7e57c2',
                    'markerSize': 8,
                    'highlightScope': {'highlight': 'item'},
                },
                {
                    'id': 'series-b',
                    'label': 'B',
                    'data': [
                        {'x': 1.5, 'y': 6, 'id': 0},
                        {'x': 2.5, 'y': 4, 'id': 1},
                        {'x': 3.5, 'y': 7, 'id': 2},
                        {'x': 4.5, 'y': 3, 'id': 3},
                        {'x': 5.5, 'y': 8, 'id': 4},
                        {'x': 6.5, 'y': 5, 'id': 5},
                        {'x': 7.5, 'y': 6, 'id': 6},
                    ],
                    'color': '#26a69a',
                    'markerSize': 8,
                    'highlightScope': {'highlight': 'item'},
                },
            ],
            grid={'horizontal': True},
            voronoiMaxRadius=50,
        ),
        html.H4("Click Data:", style={'marginTop': '15px'}),
        html.Pre(
            id='scatter-click-output',
            children="Click on a scatter point to see event data",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""@callback(
    Output('scatter-click-output', 'children'),
    Input('scatter-click', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    return json.dumps(click_data, indent=2)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 6. Dataset-Driven Scatter
    # ==========================================================================
    html.Div([
        html.H2("Dataset-Driven Scatter"),
        html.P(
            "Use the dataset prop with datasetKeys to map columns to x/y axes. "
            "This is useful when data comes from a shared table format.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-dataset',
            height=300,
            dataset=[
                {'x1': 373, 'y1': 434, 'x2': 304, 'y2': 349},
                {'x1': 173, 'y1': 437, 'x2': 208, 'y2': 347},
                {'x1': 68, 'y1': 292, 'x2': 151, 'y2': 280},
                {'x1': 121, 'y1': 116, 'x2': 185, 'y2': 176},
                {'x1': 322, 'y1': 61, 'x2': 278, 'y2': 170},
                {'x1': 466, 'y1': 210, 'x2': 346, 'y2': 246},
                {'x1': 418, 'y1': 403, 'x2': 326, 'y2': 333},
                {'x1': 224, 'y1': 449, 'x2': 235, 'y2': 352},
                {'x1': 87, 'y1': 335, 'x2': 158, 'y2': 311},
                {'x1': 104, 'y1': 167, 'x2': 166, 'y2': 218},
                {'x1': 262, 'y1': 70, 'x2': 251, 'y2': 161},
                {'x1': 421, 'y1': 167, 'x2': 335, 'y2': 199},
                {'x1': 442, 'y1': 352, 'x2': 341, 'y2': 302},
                {'x1': 294, 'y1': 474, 'x2': 264, 'y2': 366},
                {'x1': 101, 'y1': 386, 'x2': 174, 'y2': 318},
            ],
            series=[
                {
                    'id': 'ds-a',
                    'label': 'Series A',
                    'datasetKeys': {'x': 'x1', 'y': 'y1'},
                },
                {
                    'id': 'ds-b',
                    'label': 'Series B',
                    'datasetKeys': {'x': 'x2', 'y': 'y2'},
                },
            ],
            yAxis=[{'label': 'Rainfall (mm)', 'width': 60}],
            grid={'horizontal': True, 'vertical': True},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""ScatterChart(
    dataset=[
        {'x1': 373, 'y1': 434, 'x2': 304, 'y2': 349},
        {'x1': 173, 'y1': 437, 'x2': 208, 'y2': 347},
        ...
    ],
    series=[
        {'label': 'Series A', 'datasetKeys': {'x': 'x1', 'y': 'y1'}},
        {'label': 'Series B', 'datasetKeys': {'x': 'x2', 'y': 'y2'}},
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 7. Axis Styling
    # ==========================================================================
    html.Div([
        html.H2("Axis Styling (0.0.8)"),
        html.P(
            "Scatter charts support the full 0.0.8 axis API: tickLabelStyle, labelStyle, "
            "tickSize, domainLimit, disableLine, and more.",
            style=description_style
        ),
        ScatterChart(
            id='scatter-axis-styling',
            height=400,
            series=[
                {
                    'id': 'styled',
                    'label': 'Measurements',
                    'data': correlated[:40],
                    'markerSize': 6,
                    'color': '#00897b',
                    'highlightScope': {'highlight': 'item', 'fade': 'global'},
                },
            ],
            xAxis=[{
                'label': 'Independent Variable',
                'min': -5,
                'max': 105,
                'tickSize': 8,
                'tickNumber': 10,
                'tickLabelStyle': {
                    'fontSize': 11,
                    'fontWeight': 'bold',
                },
                'labelStyle': {
                    'fontSize': 14,
                    'fontWeight': 'bold',
                    'fill': '#00897b',
                },
                'domainLimit': 'nice',
            }],
            yAxis=[{
                'label': 'Dependent Variable',
                'width': 65,
                'tickSize': 8,
                'tickLabelStyle': {
                    'fontSize': 11,
                    'fontWeight': 'bold',
                },
                'labelStyle': {
                    'fontSize': 14,
                    'fontWeight': 'bold',
                    'fill': '#00897b',
                },
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True, 'vertical': True},
            margin={'left': 75, 'bottom': 50, 'right': 20, 'top': 20},
            voronoiMaxRadius=40,
        ),
    ], style=section_style),
])


@callback(
    Output('scatter-click-output', 'children'),
    Input('scatter-click', 'clickData'),
    prevent_initial_call=True
)
def display_scatter_click(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a scatter point to see event data"