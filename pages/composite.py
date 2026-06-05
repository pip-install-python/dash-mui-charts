"""
CompositeChart Demo - 0.0.8
Showcases layering scatter and line charts together using the composition API.
"""

import os
import json
import math
import random

import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/composite', name='Composite Chart (0.0.8)')

from dash_mui_charts import CompositeChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# ---------------------------------------------------------------------------
# Generate datasets
# ---------------------------------------------------------------------------
random.seed(99)

# Dataset 1: Scatter + Trend Line (hourly temperature over 3 days)
# Scatter: individual sensor readings with noise
hourly_readings = []
for i in range(72):  # 3 days * 24 hours
    temp = 20 + 8 * math.sin(2 * math.pi * (i - 6) / 24) + random.gauss(0, 2)
    hourly_readings.append({'x': i, 'y': round(temp, 1), 'id': i})
# Line: smoothed expected curve (no noise)
expected_temps = [round(20 + 8 * math.sin(2 * math.pi * (i - 6) / 24), 1) for i in range(72)]
# X-axis data for line positioning
hours_3days = list(range(72))

# Dataset 2: Scatter + Line + Reference (temperature monitoring)
hours_in_week = list(range(168))
sensor_readings = [
    {'x': h, 'y': round(22 + 3 * math.sin(2 * math.pi * h / 24) + random.gauss(0, 1.5), 1), 'id': h}
    for h in hours_in_week
]
hourly_average = [
    round(22 + 3 * math.sin(2 * math.pi * h / 24), 1)
    for h in hours_in_week
]

# Dataset 3: Multi-axis (pressure vs temperature)
pressure_scatter = [
    {'x': random.uniform(10, 35), 'y': round(900 + random.gauss(0, 30), 1), 'id': i}
    for i in range(60)
]
# Sort for line plot
pressure_sorted_x = sorted(set(round(p['x']) for p in pressure_scatter))
pressure_trend = [round(1050 - 5 * x + random.gauss(0, 5), 1) for x in range(10, 36)]
temp_range = list(range(10, 36))

# Dataset 4: Time series with scatter overlay (for zoom demo)
random.seed(42)
ts_hours = 24 * 30  # 30 days
timestamps = [int((1704067200 + h * 3600) * 1000) for h in range(ts_hours)]  # epoch ms from Jan 1 2024
baseline = [round(50 + 20 * math.sin(2 * math.pi * h / 168) + random.gauss(0, 3), 1) for h in range(ts_hours)]
# Anomaly scatter points - unusual readings, split into red/yellow groups randomly
anomalies_red = []
anomalies_yellow = []
for i in range(ts_hours):
    if random.random() < 0.02:  # 2% chance of anomaly
        point = {
            'x': timestamps[i],
            'y': round(baseline[i] + random.choice([-1, 1]) * random.uniform(15, 30), 1),
        }
        if random.random() < 0.5:
            point['id'] = len(anomalies_red)
            anomalies_red.append(point)
        else:
            point['id'] = len(anomalies_yellow)
            anomalies_yellow.append(point)


# Common styles
section_style = {'marginBottom': '50px'}
description_style = {'color': 'var(--mantine-color-dimmed)', 'marginBottom': '15px'}
code_style = {
    'backgroundColor': 'var(--mantine-color-default)',
    'padding': '15px',
    'borderRadius': '5px',
    'whiteSpace': 'pre-wrap',
    'fontSize': '12px',
    'overflow': 'auto',
}
pro_badge = html.Span(
    "PRO",
    style={
        'backgroundColor': '#ff9800',
        'color': 'white',
        'padding': '2px 8px',
        'borderRadius': '4px',
        'fontSize': '10px',
        'fontWeight': 'bold',
        'marginLeft': '10px',
        'verticalAlign': 'middle',
    }
)
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
        html.H1("Composite Chart", style={'display': 'inline'}),
        new_badge,
    ]),
    html.P(
        "New in 0.0.8: CompositeChart layers scatter and line plots on a single surface. "
        "Each series specifies its type ('scatter' or 'line'). Supports zoom, reference lines, "
        "and multi-axis configurations.",
        style={'fontSize': '16px', 'color': 'var(--mantine-color-dimmed)', 'marginBottom': '30px'}
    ),

    # ==========================================================================
    # 1. Scatter + Trend Line
    # ==========================================================================
    html.Div([
        html.H2("Scatter + Trend Line"),
        html.P(
            "Individual sensor readings (scatter) overlaid with the expected temperature "
            "curve (line). The scatter points show actual variance while the line shows "
            "the theoretical model. Hover to see both data layers.",
            style=description_style
        ),
        CompositeChart(
            id='composite-trend',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'type': 'scatter',
                    'id': 'readings',
                    'label': 'Sensor Readings',
                    'data': hourly_readings,
                    'color': '#90caf9',
                    'markerSize': 4,
                },
                {
                    'type': 'line',
                    'id': 'expected-curve',
                    'label': 'Expected Curve',
                    'data': expected_temps,
                    'color': '#1565c0',
                    'curve': 'natural',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'data': hours_3days,
                'scaleType': 'linear',
                'label': 'Hour',
                'tickNumber': 12,
                'min': 0,
                'max': 71,
            }],
            yAxis=[{
                'label': 'Temperature (\u00B0C)',
                'width': 55,
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            voronoiMaxRadius=20,
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 50},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""CompositeChart(
    series=[
        {
            'type': 'scatter',        # Scatter for actual readings
            'label': 'Sensor Readings',
            'data': [{'x': 0, 'y': 18.5, 'id': 0}, ...],
            'markerSize': 4,
        },
        {
            'type': 'line',           # Line for expected curve
            'label': 'Expected Curve',
            'data': [20.0, 22.1, ...],  # positional values
            'curve': 'natural',
            'showMark': False,
        },
    ],
    xAxis=[{
        'data': [0, 1, 2, ...],       # linear axis for both types
        'scaleType': 'linear',
    }],
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 2. Scatter + Line + Reference Lines
    # ==========================================================================
    html.Div([
        html.H2("Scatter + Line + Reference Lines"),
        html.P(
            "Temperature sensor readings (scatter) with expected curve (line) and "
            "upper/lower threshold reference lines. Points outside thresholds indicate issues.",
            style=description_style
        ),
        CompositeChart(
            id='composite-reference',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'type': 'scatter',
                    'id': 'readings',
                    'label': 'Sensor Readings',
                    'data': sensor_readings,
                    'color': '#42a5f5',
                    'markerSize': 2,
                },
                {
                    'type': 'line',
                    'id': 'expected',
                    'label': 'Expected Curve',
                    'data': hourly_average,
                    'color': '#ff7043',
                    'curve': 'natural',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'label': 'Hour of Week',
                'tickLabelStyle': {'fontSize': 11},
            }],
            yAxis=[{
                'label': 'Temperature (\u00B0C)',
                'width': 50,
                'domainLimit': 'nice',
            }],
            referenceLines=[
                {
                    'y': 28,
                    'label': 'Upper Limit',
                    'lineStyle': {'stroke': '#e53935', 'strokeDasharray': '5 5', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#e53935', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
                {
                    'y': 16,
                    'label': 'Lower Limit',
                    'lineStyle': {'stroke': '#e53935', 'strokeDasharray': '5 5', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#e53935', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
            ],
            grid={'horizontal': True},
            voronoiMaxRadius=15,
            margin={'left': 60, 'right': 20, 'top': 20, 'bottom': 50},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""CompositeChart(
    series=[
        {'type': 'scatter', 'label': 'Readings', 'data': [...], 'markerSize': 2},
        {'type': 'line', 'label': 'Expected', 'data': [...], 'curve': 'natural'},
    ],
    referenceLines=[
        {'y': 28, 'label': 'Upper Limit',
         'lineStyle': {'stroke': '#e53935', 'strokeDasharray': '5 5'}},
        {'y': 16, 'label': 'Lower Limit',
         'lineStyle': {'stroke': '#e53935', 'strokeDasharray': '5 5'}},
    ],
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 3. Multi-Axis Composite
    # ==========================================================================
    html.Div([
        html.H2("Multi-Axis Composite"),
        html.P(
            "Scatter data on the left axis and a line trend on the right axis. "
            "Useful for showing correlated variables with different scales.",
            style=description_style
        ),
        CompositeChart(
            id='composite-multiaxis',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'type': 'scatter',
                    'id': 'pressure-scatter',
                    'label': 'Pressure Readings',
                    'data': pressure_scatter,
                    'color': '#5c6bc0',
                    'markerSize': 4,
                    'yAxisId': 'pressure-axis',
                    'highlightScope': {'highlight': 'item', 'fade': 'global'},
                },
                {
                    'type': 'line',
                    'id': 'pressure-trend',
                    'label': 'Pressure Model',
                    'data': pressure_trend,
                    'color': '#ef5350',
                    'curve': 'natural',
                    'showMark': False,
                    'yAxisId': 'model-axis',
                },
            ],
            xAxis=[{
                'data': temp_range,
                'scaleType': 'linear',
                'label': 'Temperature (\u00B0C)',
                'min': 8,
                'max': 37,
            }],
            yAxis=[
                {
                    'id': 'pressure-axis',
                    'label': 'Pressure (hPa)',
                    'position': 'left',
                    'width': 60,
                    'labelStyle': {'fill': '#5c6bc0'},
                    'tickLabelStyle': {'fontSize': 11},
                    'domainLimit': 'nice',
                },
                {
                    'id': 'model-axis',
                    'label': 'Modeled Pressure (hPa)',
                    'position': 'right',
                    'width': 60,
                    'labelStyle': {'fill': '#ef5350'},
                    'tickLabelStyle': {'fontSize': 11},
                    'domainLimit': 'nice',
                },
            ],
            grid={'horizontal': True},
            voronoiMaxRadius=30,
            margin={'left': 70, 'right': 70, 'top': 20, 'bottom': 50},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""CompositeChart(
    series=[
        {'type': 'scatter', 'yAxisId': 'pressure-axis', ...},
        {'type': 'line', 'yAxisId': 'model-axis', ...},
    ],
    yAxis=[
        {'id': 'pressure-axis', 'position': 'left', ...},
        {'id': 'model-axis', 'position': 'right', ...},
    ],
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # 4. Zoom-Enabled Composite (Pro)
    # ==========================================================================
    html.Div([
        html.H2([
            "Zoom-Enabled Composite",
            pro_badge,
        ]),
        html.P(
            "Time series baseline with scatter anomaly overlay. Zoom and pan to "
            "investigate anomalies. The tooltip shows both Baseline and Anomaly "
            "data when hovering near an anomaly point. Use the sliders to adjust "
            "chart and preview marker sizes.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Label("Chart Marker Size", style={
                    'fontWeight': 500, 'marginBottom': '5px', 'display': 'block',
                }),
                dmc.Slider(
                    id='anomaly-marker-slider',
                    value=6,
                    min=2,
                    max=20,
                    step=1,
                    marks=[
                        {'value': 2, 'label': '2'},
                        {'value': 6, 'label': '6'},
                        {'value': 10, 'label': '10'},
                        {'value': 15, 'label': '15'},
                        {'value': 20, 'label': '20'},
                    ],
                    style={'maxWidth': '400px'},
                ),
            ], style={'flex': '1'}),
            html.Div([
                html.Label("Preview Marker Size", style={
                    'fontWeight': 500, 'marginBottom': '5px', 'display': 'block',
                }),
                dmc.Slider(
                    id='preview-marker-slider',
                    value=2,
                    min=1,
                    max=10,
                    step=1,
                    marks=[
                        {'value': 1, 'label': '1'},
                        {'value': 2, 'label': '2'},
                        {'value': 5, 'label': '5'},
                        {'value': 10, 'label': '10'},
                    ],
                    style={'maxWidth': '400px'},
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'gap': '40px', 'marginBottom': '20px'}),
        CompositeChart(
            id='composite-zoom',
            licenseKey=MUI_LICENSE_KEY,
            height=450,
            series=[
                {
                    'type': 'line',
                    'id': 'baseline',
                    'label': 'Baseline',
                    'data': baseline,
                    'color': '#66bb6a',
                    'curve': 'natural',
                    'showMark': False,
                    'area': True,
                },
                {
                    'type': 'scatter',
                    'id': 'anomalies-red',
                    'label': 'Anomalies (Critical)',
                    'data': anomalies_red,
                    'color': '#e53935',
                    'markerSize': 6,
                    'highlightScope': {'highlight': 'item'},
                },
                {
                    'type': 'scatter',
                    'id': 'anomalies-yellow',
                    'label': 'Anomalies (Warning)',
                    'data': anomalies_yellow,
                    'color': '#fdd835',
                    'markerSize': 6,
                    'highlightScope': {'highlight': 'item'},
                },
            ],
            xAxis=[{
                'id': 'time-axis',
                'data': timestamps,
                'scaleType': 'time',
                'label': 'Date',
                'tickMinStep': 3600 * 1000 * 24,
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 11,
                    'textAnchor': 'start',
                },
                'height': 60,
                'zoom': {
                    'minSpan': 5,
                    'panning': True,
                    'filterMode': 'discard',
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Value',
                'width': 50,
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            voronoiMaxRadius=20,
            margin={'left': 60, 'right': 20, 'top': 20, 'bottom': 90},
            initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 30}],
        ),
        html.H4("Click Data:", style={'marginTop': '15px'}),
        html.Pre(
            id='composite-zoom-output',
            children="Click on a point to see event data",
            style=code_style,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""CompositeChart(
    licenseKey=MUI_LICENSE_KEY,
    series=[
        {
            'type': 'line',
            'label': 'Baseline',
            'data': baseline,
            'area': True,
            'curve': 'natural',
        },
        {
            'type': 'scatter',
            'label': 'Anomalies',
            'data': [{'x': timestamp, 'y': value, 'id': i}, ...],
            'markerSize': 6,  # adjustable via DMC slider
        },
    ],
    xAxis=[{
        'data': timestamps,
        'scaleType': 'time',
        'zoom': {
            'slider': {'enabled': True, 'preview': True},
        },
    }],
    initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 30}],
)""", language="python"),
        ]),
    ], style=section_style),
])


@callback(
    Output('composite-zoom', 'series'),
    Input('anomaly-marker-slider', 'value'),
    Input('preview-marker-slider', 'value'),
)
def update_anomaly_marker_size(marker_size, preview_size):
    ms = marker_size or 6
    ps = preview_size or 2
    return [
        {
            'type': 'line',
            'id': 'baseline',
            'label': 'Baseline',
            'data': baseline,
            'color': '#66bb6a',
            'curve': 'natural',
            'showMark': False,
            'area': True,
        },
        {
            'type': 'scatter',
            'id': 'anomalies-red',
            'label': 'Anomalies (Critical)',
            'data': anomalies_red,
            'color': '#e53935',
            'markerSize': ms,
            'preview': {'markerSize': ps},
            'highlightScope': {'highlight': 'item'},
        },
        {
            'type': 'scatter',
            'id': 'anomalies-yellow',
            'label': 'Anomalies (Warning)',
            'data': anomalies_yellow,
            'color': '#fdd835',
            'markerSize': ms,
            'preview': {'markerSize': ps},
            'highlightScope': {'highlight': 'item'},
        },
    ]


@callback(
    Output('composite-zoom-output', 'children'),
    Input('composite-zoom', 'clickData'),
    prevent_initial_call=True
)
def display_composite_click(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a point to see event data"