"""
CompositeChart v1.2.0 Changes Demo
Demonstrates: axis tooltip fix, highlightedAxis, syncedTooltipIndex cross-chart sync.
"""

import os
import json
import math
import random
from datetime import datetime, timedelta

import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, ctx, no_update

dash.register_page(__name__, path='/composite-v120', name='CompositeChart v1.2.0')

from dash_mui_charts import CompositeChart

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# ---------------------------------------------------------------------------
# Shared data
# ---------------------------------------------------------------------------
random.seed(42)

# 48 hours of data (every 30 min = 96 points)
N = 96
x_data = list(range(N))

# Line series: temperature curve
temp_line = [round(22 + 5 * math.sin(2 * math.pi * i / 48) + random.gauss(0, 0.5), 1) for i in range(N)]

# Scatter series: sensor alerts (sparse events on the same x-axis)
alerts = [
    {'x': i, 'y': round(temp_line[i] + random.choice([-1, 1]) * random.uniform(4, 8), 1), 'id': j}
    for j, i in enumerate(sorted(random.sample(range(N), 12)))
]

# Second metric: humidity
humidity_line = [round(55 + 10 * math.cos(2 * math.pi * i / 48) + random.gauss(0, 1), 1) for i in range(N)]

# Third metric: pressure
pressure_line = [round(1013 + 3 * math.sin(2 * math.pi * i / 96) + random.gauss(0, 0.3), 1) for i in range(N)]

# ---------------------------------------------------------------------------
# Section 4 data: 90 days of daily readings with epoch-ms timestamps
# ---------------------------------------------------------------------------
S4_N = 90
s4_base = datetime(2025, 10, 1)
s4_timestamps = [int((s4_base + timedelta(days=i)).timestamp()) * 1000 for i in range(S4_N)]

random.seed(77)
s4_temp = [round(18 + 8 * math.sin(2 * math.pi * i / 90) + random.gauss(0, 1), 1) for i in range(S4_N)]
s4_humidity = [round(60 + 15 * math.cos(2 * math.pi * i / 90) + random.gauss(0, 2), 1) for i in range(S4_N)]
s4_pressure = [round(1013 + 5 * math.sin(2 * math.pi * i / 45) + random.gauss(0, 0.5), 1) for i in range(S4_N)]

# Scatter events: sparse alerts across the 90 days
s4_alert_indices = sorted(random.sample(range(S4_N), 10))
s4_alerts = [
    {'x': s4_timestamps[i], 'y': round(s4_pressure[i] + random.choice([-1, 1]) * random.uniform(3, 6), 1), 'id': j}
    for j, i in enumerate(s4_alert_indices)
]

# Styles
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
badge_style = {
    'backgroundColor': '#1565c0',
    'color': 'white',
    'padding': '2px 8px',
    'borderRadius': '4px',
    'fontSize': '10px',
    'fontWeight': 'bold',
    'marginLeft': '8px',
    'verticalAlign': 'middle',
}

layout = html.Div([
    html.Div([
        html.H1("CompositeChart v1.2.0", style={'display': 'inline'}),
        html.Span("1.2.0", style=badge_style),
    ]),
    html.P(
        "v1.2.0 fixes axis tooltip behavior for mixed series (line + scatter) and adds "
        "highlightedAxis / syncedTooltipIndex controlled props for cross-chart synchronization.",
        style={'fontSize': '16px', 'color': 'var(--mantine-color-dimmed)', 'marginBottom': '30px'},
    ),

    # ======================================================================
    # 1. Axis Tooltip Fix (the core bug fix)
    # ======================================================================
    html.Div([
        html.H2("1. Axis Tooltip Fix"),
        html.P(
            "Before v1.2.0, tooltip={'trigger': 'axis'} on a CompositeChart with mixed "
            "line + scatter series only showed a tooltip when hovering directly on a data "
            "mark. Now it shows at any x-position, matching LineChart behavior. "
            "Hover anywhere on the chart below to see the tooltip.",
            style=description_style,
        ),
        CompositeChart(
            id='v120-axis-tooltip',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'type': 'line',
                    'id': 'temperature',
                    'label': 'Temperature',
                    'data': temp_line,
                    'color': '#1976d2',
                    'curve': 'monotoneX',
                    'showMark': False,
                },
                {
                    'type': 'scatter',
                    'id': 'alerts',
                    'label': 'Alerts',
                    'data': alerts,
                    'color': '#e53935',
                    'markerSize': 7,
                },
            ],
            xAxis=[{
                'data': x_data,
                'scaleType': 'linear',
                'label': 'Time (half-hours)',
                'tickNumber': 12,
            }],
            yAxis=[{'label': 'Temp (C)', 'width': 50, 'domainLimit': 'nice'}],
            tooltip={'trigger': 'axis'},
            axisHighlight={'x': 'line'},
            grid={'horizontal': True},
            margin={'left': 60, 'right': 20, 'top': 20, 'bottom': 50},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""CompositeChart(
    series=[
        {'type': 'line', 'id': 'temperature', 'label': 'Temperature', ...},
        {'type': 'scatter', 'id': 'alerts', 'label': 'Alerts', ...},
    ],
    tooltip={'trigger': 'axis'},   # <-- now works at any x-position
    axisHighlight={'x': 'line'},
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 2. highlightedAxis output
    # ======================================================================
    html.Div([
        html.H2("2. highlightedAxis Output"),
        html.P(
            "The highlightedAxis prop now fires on any x-position hover, returning the "
            "axisId and dataIndex. Hover the chart to see the callback output update.",
            style=description_style,
        ),
        CompositeChart(
            id='v120-highlighted-axis',
            licenseKey=MUI_LICENSE_KEY,
            height=300,
            series=[
                {
                    'type': 'line',
                    'id': 'humidity',
                    'label': 'Humidity (%)',
                    'data': humidity_line,
                    'color': '#43a047',
                    'showMark': False,
                },
                {
                    'type': 'scatter',
                    'id': 'alerts',
                    'label': 'Alerts',
                    'data': alerts,
                    'color': '#ff9800',
                    'markerSize': 6,
                },
            ],
            xAxis=[{
                'id': 'x-axis',
                'data': x_data,
                'scaleType': 'linear',
                'label': 'Time (half-hours)',
                'tickNumber': 12,
            }],
            yAxis=[{'label': 'Humidity (%)', 'width': 50, 'domainLimit': 'nice'}],
            tooltip={'trigger': 'axis'},
            axisHighlight={'x': 'line'},
            grid={'horizontal': True},
            margin={'left': 60, 'right': 20, 'top': 20, 'bottom': 50},
        ),
        html.Pre(
            id='v120-axis-output',
            children="Hover the chart to see highlightedAxis data",
            style=code_style,
        ),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 3. Cross-Chart Sync (highlightedAxis + syncedTooltipIndex)
    # ======================================================================
    html.Div([
        html.H2("3. Cross-Chart Sync via highlightedAxis"),
        html.P(
            "Hover either chart. The highlightedAxis value from the hovered chart syncs "
            "the crosshair and tooltip on the other chart via syncedTooltipIndex.",
            style=description_style,
        ),
        html.Div([
            html.Div([
                html.H4("Temperature", style={'margin': '0 0 5px'}),
                CompositeChart(
                    id='v120-sync-temp',
                    licenseKey=MUI_LICENSE_KEY,
                    height=280,
                    series=[
                        {
                            'type': 'line',
                            'id': 'temp',
                            'label': 'Temperature',
                            'data': temp_line,
                            'color': '#1976d2',
                            'showMark': False,
                        },
                        {
                            'type': 'scatter',
                            'id': 'alerts',
                            'label': 'Alerts',
                            'data': alerts,
                            'color': '#e53935',
                            'markerSize': 5,
                        },
                    ],
                    xAxis=[{
                        'id': 'x-axis',
                        'data': x_data,
                        'scaleType': 'linear',
                        'tickNumber': 10,
                    }],
                    yAxis=[{'label': 'Temp (C)', 'width': 50, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'},
                    axisHighlight={'x': 'line'},
                    grid={'horizontal': True},
                    margin={'left': 55, 'right': 15, 'top': 15, 'bottom': 30},
                ),
            ], style={'flex': '1', 'minWidth': '400px'}),
            html.Div([
                html.H4("Humidity", style={'margin': '0 0 5px'}),
                CompositeChart(
                    id='v120-sync-humidity',
                    licenseKey=MUI_LICENSE_KEY,
                    height=280,
                    series=[
                        {
                            'type': 'line',
                            'id': 'humidity',
                            'label': 'Humidity',
                            'data': humidity_line,
                            'color': '#43a047',
                            'showMark': False,
                        },
                    ],
                    xAxis=[{
                        'id': 'x-axis',
                        'data': x_data,
                        'scaleType': 'linear',
                        'tickNumber': 10,
                    }],
                    yAxis=[{'label': 'Humidity (%)', 'width': 50, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'},
                    axisHighlight={'x': 'line'},
                    grid={'horizontal': True},
                    margin={'left': 55, 'right': 15, 'top': 15, 'bottom': 30},
                ),
            ], style={'flex': '1', 'minWidth': '400px'}),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),
        html.Pre(
            id='v120-sync-output',
            children="Hover either chart to see sync data",
            style=code_style,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Single callback avoids circular dependency.
# highlightedAxis syncs crosshair; syncedTooltipIndex shows tooltip overlay.
@callback(
    Output('chart-a', 'highlightedAxis'),
    Output('chart-b', 'highlightedAxis'),
    Output('chart-a', 'syncedTooltipIndex'),
    Output('chart-b', 'syncedTooltipIndex'),
    Input('chart-a', 'highlightedAxis'),
    Input('chart-b', 'highlightedAxis'),
    prevent_initial_call=True,
)
def sync_charts(axis_a, axis_b):
    source = ctx.triggered_id
    axis = axis_a if source == 'chart-a' else axis_b
    idx = axis[0]['dataIndex'] if axis else -1
    # Only show synced tooltip on the OTHER chart
    if source == 'chart-a':
        return axis, axis, -1, idx
    else:
        return axis, axis, idx, -1""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 4. Three stacked charts with synced tooltips (the dashboard use case)
    # ======================================================================
    html.Div([
        html.H2("4. Stacked Dashboard (3-Chart Sync)"),
        html.P(
            "Three vertically stacked CompositeCharts sharing a time-scale x-axis with "
            "dd/MM/YY date formatting and angled tick labels. "
            "Toggle Sync to show tooltips on all charts simultaneously. "
            "Toggle Compact to hide x-axis on the top two charts.",
            style=description_style,
        ),
        html.Div([
            dmc.Switch(
                id='v120-sync-switch',
                label='Sync tooltips across all charts',
                checked=True,
                size='md',
            ),
            dmc.Switch(
                id='v120-compact-switch',
                label='Compact mode (shared x-axis)',
                checked=True,
                size='md',
            ),
        ], style={'display': 'flex', 'gap': '30px', 'marginBottom': '15px'}),
        html.Div(id='v120-stack-container', children=[
            html.Div([
                html.H4("Temperature", style={'margin': '0 0 2px', 'fontSize': '14px'}),
                CompositeChart(
                    id='v120-stack-temp',
                    licenseKey=MUI_LICENSE_KEY,
                    height=200,
                    series=[
                        {
                            'type': 'line', 'id': 'temp', 'label': 'Temp',
                            'data': s4_temp, 'color': '#1976d2',
                            'showMark': False, 'area': True,
                        },
                    ],
                    xAxis=[{
                        'id': 'x', 'data': s4_timestamps, 'scaleType': 'time',
                        'tickNumber': 8,
                        'tickMinStep': 86400 * 1000 * 7,
                        'dateFormat': 'dd/MM/YYYY',
                        'dateTickFormat': 'dd/MM/YY',
                        'position': 'none',
                        'tickLabelStyle': {
                            'angle': 35, 'fontSize': 11, 'textAnchor': 'start',
                        },
                    }],
                    yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'},
                    axisHighlight={'x': 'line'},
                    hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 5},
                ),
            ]),
            html.Div([
                html.H4("Humidity", style={'margin': '0 0 2px', 'fontSize': '14px'}),
                CompositeChart(
                    id='v120-stack-humidity',
                    licenseKey=MUI_LICENSE_KEY,
                    height=200,
                    series=[
                        {
                            'type': 'line', 'id': 'humidity', 'label': 'Humidity',
                            'data': s4_humidity, 'color': '#43a047',
                            'showMark': False, 'area': True,
                        },
                    ],
                    xAxis=[{
                        'id': 'x', 'data': s4_timestamps, 'scaleType': 'time',
                        'tickNumber': 8,
                        'tickMinStep': 86400 * 1000 * 7,
                        'dateFormat': 'dd/MM/YYYY',
                        'dateTickFormat': 'dd/MM/YY',
                        'position': 'none',
                        'tickLabelStyle': {
                            'angle': 35, 'fontSize': 11, 'textAnchor': 'start',
                        },
                    }],
                    yAxis=[{'label': '%', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'},
                    axisHighlight={'x': 'line'},
                    hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 5},
                ),
            ]),
            html.Div([
                html.H4("Pressure", style={'margin': '0 0 2px', 'fontSize': '14px'}),
                CompositeChart(
                    id='v120-stack-pressure',
                    licenseKey=MUI_LICENSE_KEY,
                    height=250,
                    series=[
                        {
                            'type': 'line', 'id': 'pressure', 'label': 'Pressure',
                            'data': s4_pressure, 'color': '#7b1fa2',
                            'showMark': False, 'area': True,
                        },
                        {
                            'type': 'scatter', 'id': 'events', 'label': 'Events',
                            'data': s4_alerts, 'color': '#e53935', 'markerSize': 5,
                        },
                    ],
                    xAxis=[{
                        'id': 'x', 'data': s4_timestamps, 'scaleType': 'time',
                        'label': 'Date',
                        'height': 60,
                        'tickNumber': 8,
                        'tickMinStep': 86400 * 1000 * 7,
                        'dateFormat': 'dd/MM/YYYY',
                        'dateTickFormat': 'dd/MM/YY',
                        'tickLabelStyle': {
                            'angle': 35, 'fontSize': 11, 'textAnchor': 'start',
                        },
                        'labelStyle': {'fontSize': 12},
                    }],
                    yAxis=[{'label': 'hPa', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'},
                    axisHighlight={'x': 'line'},
                    hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 70},
                ),
            ]),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Time-scale x-axis with dd/MM/YY formatting and angled labels.
# Compact mode: top charts use position='none' to hide x-axis,
# bottom chart shows the shared axis.
xAxis=[{
    'data': timestamps,
    'scaleType': 'time',
    'dateFormat': 'dd/MM/YYYY',         # tooltip format
    'dateTickFormat': 'dd/MM/YY',       # tick label format
    'tickNumber': 8,
    'tickMinStep': 86400 * 1000 * 7,    # min 7 days between ticks
    'position': 'none',                  # hide on top charts (compact)
    'tickLabelStyle': {'angle': 35, 'fontSize': 11, 'textAnchor': 'start'},
}]""", style=code_style),
        ]),
    ], style=section_style),
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


# ===========================================================================
# Callbacks
# ===========================================================================

# --- Section 2: highlightedAxis output display ---
@callback(
    Output('v120-axis-output', 'children'),
    Input('v120-highlighted-axis', 'highlightedAxis'),
    prevent_initial_call=True,
)
def show_highlighted_axis(axis):
    return json.dumps(axis, indent=2) if axis else "[]"


# --- Section 3: Two-chart sync (single callback to avoid circular deps) ---
@callback(
    Output('v120-sync-temp', 'highlightedAxis'),
    Output('v120-sync-humidity', 'highlightedAxis'),
    Output('v120-sync-temp', 'syncedTooltipIndex'),
    Output('v120-sync-humidity', 'syncedTooltipIndex'),
    Output('v120-sync-output', 'children'),
    Input('v120-sync-temp', 'highlightedAxis'),
    Input('v120-sync-humidity', 'highlightedAxis'),
    prevent_initial_call=True,
)
def sync_two_charts(axis_temp, axis_humidity):
    source = ctx.triggered_id
    axis = axis_temp if source == 'v120-sync-temp' else axis_humidity
    idx = axis[0]['dataIndex'] if axis and len(axis) > 0 else -1

    # Native tooltip shows on the hovered chart; syncedTooltipIndex on the other
    if source == 'v120-sync-temp':
        tip_temp, tip_humidity = -1, idx
    else:
        tip_temp, tip_humidity = idx, -1

    info = json.dumps({'source': source, 'dataIndex': idx}, indent=2)
    return axis, axis, tip_temp, tip_humidity, info


# --- Section 4: Three-chart stacked sync (axis + synced tooltip overlay) ---
@callback(
    Output('v120-stack-temp', 'highlightedAxis'),
    Output('v120-stack-humidity', 'highlightedAxis'),
    Output('v120-stack-pressure', 'highlightedAxis'),
    Output('v120-stack-temp', 'syncedTooltipIndex'),
    Output('v120-stack-humidity', 'syncedTooltipIndex'),
    Output('v120-stack-pressure', 'syncedTooltipIndex'),
    Input('v120-stack-temp', 'highlightedAxis'),
    Input('v120-stack-humidity', 'highlightedAxis'),
    Input('v120-stack-pressure', 'highlightedAxis'),
    State('v120-sync-switch', 'checked'),
    prevent_initial_call=True,
)
def stack_sync_all(axis_temp, axis_humidity, axis_pressure, synced):
    source = ctx.triggered_id
    axes = {
        'v120-stack-temp': axis_temp,
        'v120-stack-humidity': axis_humidity,
        'v120-stack-pressure': axis_pressure,
    }
    axis = axes.get(source, axis_temp)
    idx = axis[0]['dataIndex'] if axis and len(axis) > 0 else -1

    if not synced:
        # Sync only crosshair, no synced tooltip overlay
        return axis, axis, axis, -1, -1, -1

    # Sync crosshair on all charts + show synced tooltip on non-hovered charts.
    # The hovered chart already shows its native tooltip from MUI.
    chart_ids = ['v120-stack-temp', 'v120-stack-humidity', 'v120-stack-pressure']
    tips = [idx if cid != source else -1 for cid in chart_ids]

    return axis, axis, axis, tips[0], tips[1], tips[2]


# Shared x-axis config pieces for compact toggle
_s4_xaxis_base = {
    'id': 'x',
    'data': s4_timestamps,
    'scaleType': 'time',
    'tickNumber': 8,
    'tickMinStep': 86400 * 1000 * 7,
    'dateFormat': 'dd/MM/YYYY',
    'dateTickFormat': 'dd/MM/YY',
    'tickLabelStyle': {'angle': 35, 'fontSize': 11, 'textAnchor': 'start'},
}


# --- Section 4: Compact mode toggle ---
@callback(
    Output('v120-stack-temp', 'xAxis'),
    Output('v120-stack-humidity', 'xAxis'),
    Output('v120-stack-pressure', 'xAxis'),
    Output('v120-stack-temp', 'margin'),
    Output('v120-stack-humidity', 'margin'),
    Output('v120-stack-pressure', 'margin'),
    Output('v120-stack-temp', 'height'),
    Output('v120-stack-humidity', 'height'),
    Output('v120-stack-pressure', 'height'),
    Input('v120-compact-switch', 'checked'),
)
def toggle_compact(compact):
    if compact:
        # Hide x-axis on top two charts, show only on bottom
        top_axis = [{**_s4_xaxis_base, 'position': 'none'}]
        bottom_axis = [{
            **_s4_xaxis_base,
            'label': 'Date',
            'height': 60,
            'labelStyle': {'fontSize': 12},
        }]
        top_margin = {'left': 65, 'right': 15, 'top': 10, 'bottom': 5}
        bottom_margin = {'left': 65, 'right': 15, 'top': 10, 'bottom': 70}
        return (top_axis, top_axis, bottom_axis,
                top_margin, top_margin, bottom_margin,
                200, 200, 250)
    else:
        # All charts show their own x-axis
        all_axis = [{
            **_s4_xaxis_base,
            'label': 'Date',
            'height': 60,
            'labelStyle': {'fontSize': 12},
        }]
        margin = {'left': 65, 'right': 15, 'top': 10, 'bottom': 70}
        return (all_axis, all_axis, all_axis,
                margin, margin, margin,
                280, 280, 280)
