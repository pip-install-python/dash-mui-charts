"""
LineChart Basics - Fundamental features and usage examples
"""

import os
import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/linechart-basic', name='LineChart Basics')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

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

layout = html.Div([
    html.H1("LineChart Basics"),
    html.P(
        "This page demonstrates the fundamental features of the LineChart component.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '40px'}
    ),

    # ==========================================================================
    # Basic Line Chart with Grid
    # ==========================================================================
    html.Div([
        html.H2("Basic Line Chart with Grid"),
        html.P(
            "A simple line chart with multiple series and grid lines. "
            "The grid prop accepts 'horizontal' and 'vertical' boolean options.",
            style=description_style
        ),
        LineChart(
            id='basic-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'data': [2, 5.5, 2, 8.5, 1.5, 5],
                    'label': 'Series A',
                    'showMark': True,
                },
                {
                    'data': [4, 3.5, 6, 2.5, 4.5, 3],
                    'label': 'Series B',
                },
            ],
            xAxis=[{
                'data': [1, 2, 3, 4, 5, 6],
                'scaleType': 'point',
            }],
            grid={'horizontal': True, 'vertical': True},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=350,
    series=[
        {'data': [2, 5.5, 2, 8.5, 1.5, 5], 'label': 'Series A', 'showMark': True},
        {'data': [4, 3.5, 6, 2.5, 4.5, 3], 'label': 'Series B'},
    ],
    xAxis=[{'data': [1, 2, 3, 4, 5, 6], 'scaleType': 'point'}],
    grid={'horizontal': True, 'vertical': True},
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Area Chart
    # ==========================================================================
    html.Div([
        html.H2("Area Chart"),
        html.P(
            "Set 'area': True on a series to fill the area under the line. "
            "The 'scaleType': 'band' creates evenly spaced categorical x-axis.",
            style=description_style
        ),
        LineChart(
            id='area-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=300,
            series=[
                {
                    'data': [2, 5.5, 2, 8.5, 1.5, 5],
                    'label': 'Revenue',
                    'area': True,
                    'color': '#1976d2',
                },
            ],
            xAxis=[{
                'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'scaleType': 'band',
            }],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=300,
    series=[{
        'data': [2, 5.5, 2, 8.5, 1.5, 5],
        'label': 'Revenue',
        'area': True,
        'color': '#1976d2',
    }],
    xAxis=[{'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'scaleType': 'band'}],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Stacked Area Chart
    # ==========================================================================
    html.Div([
        html.H2("Stacked Area Chart"),
        html.P(
            "Use the 'stack' property with a common identifier to stack multiple series. "
            "All series with the same stack ID will be stacked together.",
            style=description_style
        ),
        LineChart(
            id='stacked-area-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=300,
            series=[
                {
                    'data': [4, 3, 5, 4, 6, 3, 5],
                    'label': 'Product A',
                    'area': True,
                    'stack': 'total',
                },
                {
                    'data': [3, 4, 3, 5, 4, 6, 4],
                    'label': 'Product B',
                    'area': True,
                    'stack': 'total',
                },
                {
                    'data': [2, 2, 3, 2, 3, 2, 3],
                    'label': 'Product C',
                    'area': True,
                    'stack': 'total',
                },
            ],
            xAxis=[{
                'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'scaleType': 'point',
            }],
            colors=['#4e79a7', '#f28e2c', '#e15759'],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=300,
    series=[
        {'data': [4, 3, 5, 4, 6, 3, 5], 'label': 'Product A', 'area': True, 'stack': 'total'},
        {'data': [3, 4, 3, 5, 4, 6, 4], 'label': 'Product B', 'area': True, 'stack': 'total'},
        {'data': [2, 2, 3, 2, 3, 2, 3], 'label': 'Product C', 'area': True, 'stack': 'total'},
    ],
    xAxis=[{'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'scaleType': 'point'}],
    colors=['#4e79a7', '#f28e2c', '#e15759'],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Custom Colors and Curves
    # ==========================================================================
    html.Div([
        html.H2("Custom Colors and Curves"),
        html.P(
            "The 'curve' property controls line interpolation. Options include: "
            "'linear', 'monotoneX', 'monotoneY', 'natural', 'step', 'stepBefore', "
            "'stepAfter', 'catmullRom', 'bumpX', 'bumpY'.",
            style=description_style
        ),
        LineChart(
            id='custom-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=300,
            series=[
                {
                    'data': [1, 4, 2, 5, 7, 2, 4],
                    'label': 'Linear',
                    'curve': 'linear',
                },
                {
                    'data': [2, 3, 5, 4, 6, 3, 5],
                    'label': 'Monotone',
                    'curve': 'monotoneX',
                },
                {
                    'data': [3, 2, 4, 6, 5, 4, 3],
                    'label': 'Step',
                    'curve': 'step',
                },
            ],
            xAxis=[{
                'data': [0, 1, 2, 3, 4, 5, 6],
            }],
            colors=['#ff6384', '#36a2eb', '#ffce56'],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=300,
    series=[
        {'data': [1, 4, 2, 5, 7, 2, 4], 'label': 'Linear', 'curve': 'linear'},
        {'data': [2, 3, 5, 4, 6, 3, 5], 'label': 'Monotone', 'curve': 'monotoneX'},
        {'data': [3, 2, 4, 6, 5, 4, 3], 'label': 'Step', 'curve': 'step'},
    ],
    xAxis=[{'data': [0, 1, 2, 3, 4, 5, 6]}],
    colors=['#ff6384', '#36a2eb', '#ffce56'],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Biaxial Chart (Dual Y-Axes)
    # ==========================================================================
    html.Div([
        html.H2("Biaxial Chart (Dual Y-Axes)"),
        html.P(
            "Create charts with two Y-axes by defining multiple yAxis configs with unique IDs, "
            "then reference them in series using 'yAxisId'. Great for comparing metrics with different scales.",
            style=description_style
        ),
        LineChart(
            id='biaxial-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'unemployment',
                    'data': [4.0, 4.7, 5.8, 6.0, 5.5, 5.1, 4.6, 4.6, 5.8, 9.3, 9.6, 8.9],
                    'label': 'Unemployment Rate (%)',
                    'color': '#af3838',
                    'showMark': False,
                    'yAxisId': 'unemployment-axis',
                },
                {
                    'id': 'gdp',
                    'data': [36330, 37134, 37998, 39496, 41713, 44115, 46299, 48050, 48570, 47099, 48468, 50066],
                    'label': 'GDP per capita ($)',
                    'color': '#4caf50',
                    'showMark': False,
                    'yAxisId': 'gdp-axis',
                },
            ],
            xAxis=[{
                'data': list(range(2000, 2012)),
                'scaleType': 'point',
            }],
            yAxis=[
                {
                    'id': 'unemployment-axis',
                    'label': 'Unemployment (%)',
                    'position': 'left',
                    'width': 60,
                },
                {
                    'id': 'gdp-axis',
                    'label': 'GDP ($)',
                    'position': 'right',
                    'width': 80,
                },
            ],
            grid={'horizontal': True},
            margin={'left': 70, 'right': 90, 'top': 20, 'bottom': 30},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=350,
    series=[
        {'data': [...], 'label': 'Unemployment Rate (%)', 'yAxisId': 'unemployment-axis'},
        {'data': [...], 'label': 'GDP per capita ($)', 'yAxisId': 'gdp-axis'},
    ],
    xAxis=[{'data': list(range(2000, 2012)), 'scaleType': 'point'}],
    yAxis=[
        {'id': 'unemployment-axis', 'label': 'Unemployment (%)', 'position': 'left'},
        {'id': 'gdp-axis', 'label': 'GDP ($)', 'position': 'right'},
    ],
    margin={'left': 70, 'right': 90, 'top': 20, 'bottom': 30},
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Interactive Chart with Click Events
    # ==========================================================================
    html.Div([
        html.H2("Interactive Chart with Click Events"),
        html.P(
            "The LineChart fires click events that can be captured via Dash callbacks. "
            "The 'clickData' prop contains information about what was clicked, and "
            "'n_clicks' increments with each click.",
            style=description_style
        ),
        LineChart(
            id='interactive-linechart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'data': [2400, 1398, 9800, 3908, 4800, 3800, 4300],
                    'label': 'Sales',
                    'showMark': True,
                },
                {
                    'data': [4000, 3000, 2000, 2780, 1890, 2390, 3490],
                    'label': 'Expenses',
                    'showMark': True,
                },
            ],
            xAxis=[{
                'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'scaleType': 'point',
                'label': 'Day of Week',
            }],
            yAxis=[{
                'label': 'Amount ($)',
            }],
            grid={'horizontal': True},
        ),
        html.H4("Click Data:", style={'marginTop': '20px'}),
        html.Pre(
            id='click-output',
            children="Click on the chart to see event data",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='interactive-linechart',
    height=350,
    series=[
        {'data': [...], 'label': 'Sales', 'showMark': True},
        {'data': [...], 'label': 'Expenses', 'showMark': True},
    ],
    xAxis=[{'data': ['Mon', 'Tue', ...], 'scaleType': 'point', 'label': 'Day of Week'}],
    yAxis=[{'label': 'Amount ($)'}],
)

@callback(Output('click-output', 'children'), Input('interactive-linechart', 'clickData'))
def display_click(click_data):
    return json.dumps(click_data, indent=2) if click_data else "Click on the chart"
""", style=code_style),
        ]),
    ], style=section_style),
])


@callback(
    Output('click-output', 'children'),
    Input('interactive-linechart', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    """Display click event data."""
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on the chart to see event data"
