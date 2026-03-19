"""
LineChart 0.0.8 - Zoom Slider Preview & Enhanced Axis Configuration
"""

import os
import json
import math
import random
from datetime import datetime, timedelta

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/linechart-zoom-preview', name='Zoom Preview (0.0.8)')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# ---------------------------------------------------------------------------
# Generate 2 months of simulated hourly sensor data (Jan 1 - Feb 28, 2025)
# ---------------------------------------------------------------------------
random.seed(42)
start_date = datetime(2025, 1, 1)
hours = 24 * 59  # 59 days of hourly data

timestamps = []
temperature = []
humidity = []

for h in range(hours):
    dt = start_date + timedelta(hours=h)
    timestamps.append(int(dt.timestamp() * 1000))  # epoch ms for MUI time scale

    day_of_year = dt.timetuple().tm_yday
    hour = dt.hour

    # Temperature: seasonal base + daily cycle + noise
    seasonal = 2.0 + 8.0 * math.sin(2 * math.pi * (day_of_year - 30) / 365)
    daily_cycle = 4.0 * math.sin(2 * math.pi * (hour - 6) / 24)
    noise = random.gauss(0, 1.2)
    temp = seasonal + daily_cycle + noise
    temperature.append(round(temp, 1))

    # Humidity: inversely correlated with temperature + noise
    hum_base = 65 - 1.5 * (temp - 5)
    hum_noise = random.gauss(0, 3)
    humidity.append(round(max(20, min(95, hum_base + hum_noise)), 1))


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
        html.H1("Zoom Slider Preview", style={'display': 'inline'}),
        pro_badge,
        new_badge,
    ]),
    html.P(
        "New in 0.0.8: zoom.slider.preview shows a miniature of the full dataset "
        "inside the slider, enhanced axis configuration with tick styling, and "
        "zoomInteractionConfig for fine-grained zoom/pan control.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # ==========================================================================
    # Zoom Slider with Preview - Time Series
    # ==========================================================================
    html.Div([
        html.H2("Zoom Slider with Preview"),
        html.P(
            "Two months of simulated hourly sensor data (Jan-Feb 2025). "
            "The zoom slider shows a preview of the full dataset, making it easy to "
            "navigate to regions of interest. Scroll to zoom, drag to pan.",
            style=description_style
        ),
        LineChart(
            id='zoom-preview-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=450,
            series=[
                {
                    'id': 'temperature',
                    'data': temperature,
                    'label': 'Temperature',
                    'color': '#ef5350',
                    'showMark': False,
                    'area': True,
                    'curve': 'natural',
                },
            ],
            xAxis=[{
                'id': 'time-axis',
                'data': timestamps,
                'scaleType': 'time',
                'label': 'Date',
                'tickMinStep': 3600 * 1000 * 24,  # minimum 1 day between ticks
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 11,
                    'textAnchor': 'start',
                },
                'height': 50,
                'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
                'zoom': {
                    'minSpan': 2,
                    'panning': True,
                    'filterMode': 'discard',
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Temperature (C)',
                'width': 55,
                'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
                'tickLabelStyle': {'fontSize': 11},
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 70},
            initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 25}],
        ),
        html.P(
            "Source: Simulated hourly sensor data",
            style={'color': '#999', 'fontSize': '12px', 'marginTop': '5px'}
        ),
        html.H4("Zoom State:", style={'marginTop': '15px'}),
        html.Pre(
            id='zoom-preview-output',
            children="Interact with the chart to see zoom state",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=450,
    series=[{
        'data': temperature, 'label': 'Temperature',
        'color': '#ef5350', 'showMark': False,
        'area': True, 'curve': 'natural',
    }],
    xAxis=[{
        'id': 'time-axis',
        'data': timestamps,           # epoch ms values
        'scaleType': 'time',
        'label': 'Date',
        'tickMinStep': 3600 * 1000 * 24,  # min 1 day between ticks
        'tickLabelStyle': {'angle': 35, 'fontSize': 11, 'textAnchor': 'start'},
        'height': 50,                 # extra space for angled labels
        'zoom': {
            'minSpan': 2,
            'panning': True,
            'filterMode': 'discard',
            'slider': {
                'enabled': True,
                'preview': True,      # NEW in 0.0.8!
            },
        },
    }],
    yAxis=[{
        'label': 'Temperature (C)',
        'domainLimit': 'nice',        # rounds to friendly values
    }],
    initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 25}],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Biaxial with Preview - Temperature & Humidity
    # ==========================================================================
    html.Div([
        html.H2("Biaxial Chart with Slider Preview"),
        html.P(
            "Temperature and humidity on dual axes. The slider preview shows both "
            "series, and filterMode='discard' auto-adjusts the y-axis to the visible range.",
            style=description_style
        ),
        LineChart(
            id='zoom-preview-biaxial',
            licenseKey=MUI_LICENSE_KEY,
            height=450,
            series=[
                {
                    'id': 'temperature',
                    'data': temperature,
                    'label': 'Temperature (C)',
                    'color': '#ef5350',
                    'showMark': False,
                    'curve': 'natural',
                    'yAxisId': 'temp-axis',
                },
                {
                    'id': 'humidity',
                    'data': humidity,
                    'label': 'Humidity (%)',
                    'color': '#42a5f5',
                    'showMark': False,
                    'curve': 'natural',
                    'yAxisId': 'hum-axis',
                },
            ],
            xAxis=[{
                'id': 'biaxial-time-axis',
                'data': timestamps,
                'scaleType': 'time',
                'tickMinStep': 3600 * 1000 * 24,
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 11,
                    'textAnchor': 'start',
                },
                'height': 50,
                'zoom': {
                    'minSpan': 2,
                    'panning': True,
                    'filterMode': 'discard',
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[
                {
                    'id': 'temp-axis',
                    'label': 'Temperature (C)',
                    'position': 'left',
                    'width': 55,
                    'labelStyle': {'fontSize': 12, 'fill': '#ef5350'},
                    'tickLabelStyle': {'fontSize': 11},
                    'domainLimit': 'nice',
                },
                {
                    'id': 'hum-axis',
                    'label': 'Humidity (%)',
                    'position': 'right',
                    'width': 55,
                    'labelStyle': {'fontSize': 12, 'fill': '#42a5f5'},
                    'tickLabelStyle': {'fontSize': 11},
                    'domainLimit': 'nice',
                },
            ],
            grid={'horizontal': True},
            margin={'left': 65, 'right': 65, 'top': 20, 'bottom': 70},
            initialZoom=[{'axisId': 'biaxial-time-axis', 'start': 30, 'end': 60}],
        ),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Zoom Interaction Config
    # ==========================================================================
    html.Div([
        html.H2("Zoom Interaction Configuration"),
        html.P(
            "New in 0.0.8: zoomInteractionConfig gives fine-grained control over "
            "zoom and pan interactions. This chart uses brush zoom with double-tap reset, "
            "plus drag panning.",
            style=description_style
        ),
        LineChart(
            id='zoom-interaction-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'id': 'temperature',
                    'data': temperature,
                    'label': 'Temperature (C)',
                    'color': '#7e57c2',
                    'showMark': False,
                    'curve': 'natural',
                },
            ],
            xAxis=[{
                'id': 'interaction-x',
                'data': timestamps,
                'scaleType': 'time',
                'tickMinStep': 3600 * 1000 * 24,
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 11,
                    'textAnchor': 'start',
                },
                'height': 50,
                'zoom': {
                    'minSpan': 2,
                    'panning': True,
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Temperature (C)',
                'width': 55,
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 70},
            zoomInteractionConfig={
                'zoom': ['wheel', 'pinch', 'doubleTapReset'],
                'pan': ['drag', 'wheel'],
            },
        ),
        html.Div([
            html.H4("Interaction Config Reference:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                        html.Th("Interactions", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("zoom", style={'padding': '6px 8px', 'fontWeight': 'bold'}), html.Td("wheel", style={'padding': '6px 8px'}), html.Td("Scroll wheel zoom in/out", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("pinch", style={'padding': '6px 8px'}), html.Td("Pinch to zoom on touch devices", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("tapAndDrag", style={'padding': '6px 8px'}), html.Td("Double-tap then drag vertically", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("brush", style={'padding': '6px 8px'}), html.Td("Click-drag to select zoom area", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("doubleTapReset", style={'padding': '6px 8px'}), html.Td("Double-tap to reset zoom", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("pan", style={'padding': '6px 8px', 'fontWeight': 'bold', 'borderTop': '1px solid #eee'}), html.Td("drag", style={'padding': '6px 8px', 'borderTop': '1px solid #eee'}), html.Td("Drag to pan the chart", style={'padding': '6px 8px', 'borderTop': '1px solid #eee'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("pressAndDrag", style={'padding': '6px 8px'}), html.Td("Press-hold then drag to pan", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("", style={'padding': '6px 8px'}), html.Td("wheel", style={'padding': '6px 8px'}), html.Td("Trackpad two-finger scroll pan", style={'padding': '6px 8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '15px'}),
            html.Pre("""LineChart(
    ...
    zoomInteractionConfig={
        'zoom': ['wheel', 'pinch', 'doubleTapReset'],
        'pan': ['drag', 'wheel'],
    },
    # Advanced: use objects for key modifiers and pointer modes
    # zoomInteractionConfig={
    #     'zoom': [
    #         {'type': 'wheel', 'requiredKeys': ['Control']},
    #         'pinch',
    #     ],
    #     'pan': [
    #         {'type': 'drag', 'pointerMode': 'mouse', 'requiredKeys': ['Shift']},
    #         {'type': 'drag', 'pointerMode': 'touch'},
    #     ],
    # },
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Enhanced Axis Configuration
    # ==========================================================================
    html.Div([
        html.H2("Enhanced Axis Configuration"),
        html.P(
            "0.0.8 exposes the full MUI axis API: tickLabelStyle, labelStyle, "
            "tickMinStep, tickSize, domainLimit, disableLine, disableTicks, height, "
            "reverse, and more. This example uses styled axes with customized ticks.",
            style=description_style
        ),
        LineChart(
            id='axis-config-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'id': 'temp',
                    'data': temperature[:168],  # 1 week of hourly data
                    'label': 'Temperature (C)',
                    'color': '#ff7043',
                    'showMark': False,
                    'curve': 'natural',
                    'area': True,
                },
            ],
            xAxis=[{
                'id': 'week-axis',
                'data': timestamps[:168],
                'scaleType': 'time',
                'tickMinStep': 3600 * 1000 * 12,  # every 12 hours
                'tickSize': 8,
                'tickLabelStyle': {
                    'angle': 40,
                    'fontSize': 10,
                    'textAnchor': 'start',
                },
                'height': 55,
                'labelStyle': {'fontSize': 13},
                'label': 'One Week (12-hour tick intervals)',
                'zoom': {
                    'minSpan': 5,
                    'panning': True,
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Temperature (C)',
                'width': 50,
                'tickNumber': 6,
                'tickSize': 4,
                'tickLabelStyle': {'fontSize': 11},
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True, 'vertical': True},
            margin={'left': 60, 'right': 20, 'top': 20, 'bottom': 75},
            initialZoom=[{'axisId': 'week-axis', 'start': 0, 'end': 60}],
        ),
        html.Div([
            html.H4("New Axis Properties in 0.0.8:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Property", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("tickLabelStyle", style={'padding': '6px 8px'}), html.Td("dict", style={'padding': '6px 8px'}), html.Td("CSS for tick labels: angle, fontSize, textAnchor, fill", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("labelStyle", style={'padding': '6px 8px'}), html.Td("dict", style={'padding': '6px 8px'}), html.Td("CSS for axis label: fontSize, fontWeight, fill", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("tickMinStep", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Min step between ticks (ms for time axes)", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("tickMaxStep", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Max step between ticks", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("tickNumber", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Approximate tick count", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("tickSize", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Tick mark length in pixels", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("tickSpacing", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Min spacing between ticks (ordinal)", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("height / width", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Space reserved for axis (px)", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("domainLimit", style={'padding': '6px 8px'}), html.Td("string", style={'padding': '6px 8px'}), html.Td("'nice' or 'strict' axis range", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("disableLine", style={'padding': '6px 8px'}), html.Td("bool", style={'padding': '6px 8px'}), html.Td("Hide the axis line", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("disableTicks", style={'padding': '6px 8px'}), html.Td("bool", style={'padding': '6px 8px'}), html.Td("Hide tick marks", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("reverse", style={'padding': '6px 8px'}), html.Td("bool", style={'padding': '6px 8px'}), html.Td("Reverse axis direction", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("min / max", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Fixed axis domain bounds", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("categoryGapRatio", style={'padding': '6px 8px'}), html.Td("number", style={'padding': '6px 8px'}), html.Td("Gap between bands (0-1)", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("scaleType", style={'padding': '6px 8px'}), html.Td("string", style={'padding': '6px 8px'}), html.Td("Now includes 'symlog', 'sqrt', 'utc'", style={'padding': '6px 8px'})]),
                    html.Tr([html.Td("position", style={'padding': '6px 8px'}), html.Td("string", style={'padding': '6px 8px'}), html.Td("Now includes 'none' to hide axis", style={'padding': '6px 8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
    ], style=section_style),
])


@callback(
    Output('zoom-preview-output', 'children'),
    Input('zoom-preview-chart', 'zoomData'),
    prevent_initial_call=True
)
def display_zoom_preview(zoom_data):
    if zoom_data:
        return json.dumps(zoom_data, indent=2)
    return "Interact with the chart to see zoom state"