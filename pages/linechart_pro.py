"""
LineChart Pro - Advanced Pro license features
"""

import os
import json
import dash
from dash import html, callback, Input, Output, State

dash.register_page(__name__, path='/linechart-pro', name='LineChart Pro')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data
years = list(range(2000, 2024))
unemployment_rate = [
    4.0, 4.7, 5.8, 6.0, 5.5, 5.1, 4.6, 4.6, 5.8, 9.3,
    9.6, 8.9, 8.1, 7.4, 6.2, 5.3, 4.9, 4.4, 3.9, 3.7,
    8.1, 5.4, 3.6, 3.7
]
gdp_per_capita = [
    36330, 37134, 37998, 39496, 41713, 44115, 46299, 48050, 48570, 47099,
    48468, 50066, 51784, 53107, 55049, 56863, 58021, 60110, 63064, 65280,
    63544, 70249, 76343, 80035
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

layout = html.Div([
    html.Div([
        html.H1("LineChart Pro", style={'display': 'inline'}),
        pro_badge,
    ]),
    html.P(
        "This page demonstrates the advanced Pro features of LineChart including "
        "zoom, pan, zoom slider, and zoom state callbacks.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '20px'}
    ),
    html.Div([
        html.P(
            "These features require an MUI X Pro license key. "
            "Set your license key in the MUI_PRO_API_KEY environment variable.",
            style={
                'backgroundColor': '#fff3e0',
                'padding': '12px 16px',
                'borderRadius': '4px',
                'borderLeft': '4px solid #ff9800',
                'marginBottom': '40px',
            }
        ),
    ]) if not MUI_LICENSE_KEY else None,

    # ==========================================================================
    # Zoom with Slider
    # ==========================================================================
    html.Div([
        html.H2("Zoom with Slider"),
        html.P(
            "The zoom slider provides an intuitive way to zoom and pan through data. "
            "Set 'showSlider=True' to enable the slider below the chart. "
            "Drag the handles to zoom, or drag the selected region to pan.",
            style=description_style
        ),
        LineChart(
            id='zoom-slider-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'id': 'unemployment',
                    'data': unemployment_rate,
                    'label': 'Unemployment Rate (%)',
                    'color': '#1976d2',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'id': 'x-axis',
                'data': years,
                'scaleType': 'point',
                'label': 'Year',
                'zoom': {
                    'minSpan': 5,
                    'maxSpan': 100,
                    'panning': True,
                },
            }],
            yAxis=[{
                'label': 'Unemployment Rate (%)',
            }],
            grid={'horizontal': True},
            showSlider=True,
            initialZoom=[{'axisId': 'x-axis', 'start': 0, 'end': 50}],
        ),
        html.H4("Zoom State:", style={'marginTop': '20px'}),
        html.Pre(
            id='zoom-slider-output',
            children="Interact with the slider to see zoom state changes",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='zoom-slider-chart',
    height=400,
    series=[{'data': unemployment_rate, 'label': 'Unemployment Rate (%)'}],
    xAxis=[{
        'id': 'x-axis',
        'data': years,
        'scaleType': 'point',
        'zoom': {
            'minSpan': 5,      # Minimum zoom span
            'maxSpan': 100,    # Maximum zoom span (100 = full range)
            'panning': True,   # Enable panning
        },
    }],
    showSlider=True,  # Enable zoom slider
    initialZoom=[{'axisId': 'x-axis', 'start': 0, 'end': 50}],  # Start zoomed to first half
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Zoom Configuration Options
    # ==========================================================================
    html.Div([
        html.H2("Zoom Configuration Options"),
        html.P(
            "The zoom configuration supports several options to customize behavior. "
            "Here's a chart with different zoom constraints.",
            style=description_style
        ),
        LineChart(
            id='zoom-config-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'data': gdp_per_capita,
                    'label': 'GDP per Capita ($)',
                    'color': '#4caf50',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'id': 'gdp-x-axis',
                'data': years,
                'scaleType': 'point',
                'label': 'Year',
                'zoom': {
                    'minSpan': 10,     # Can't zoom in past 10 data points
                    'maxSpan': 100,    # Can zoom out to see all
                    'panning': True,
                },
            }],
            yAxis=[{
                'label': 'GDP per Capita ($)',
            }],
            grid={'horizontal': True},
            showSlider=True,
        ),
        html.Div([
            html.H4("Zoom Configuration Reference:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Option", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("minSpan", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Minimum zoom span (data points visible)", style={'padding': '8px'})]),
                    html.Tr([html.Td("maxSpan", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Maximum zoom span (100 = full range)", style={'padding': '8px'})]),
                    html.Tr([html.Td("panning", style={'padding': '8px'}), html.Td("boolean", style={'padding': '8px'}), html.Td("Enable drag panning", style={'padding': '8px'})]),
                    html.Tr([html.Td("minStart", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Minimum start position (0-100)", style={'padding': '8px'})]),
                    html.Tr([html.Td("maxEnd", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Maximum end position (0-100)", style={'padding': '8px'})]),
                    html.Tr([html.Td("step", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Zoom granularity", style={'padding': '8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Biaxial Chart with Zoom
    # ==========================================================================
    html.Div([
        html.H2("Biaxial Chart with Zoom"),
        html.P(
            "Combine dual Y-axes with zoom functionality for powerful data exploration. "
            "This example shows unemployment rate and GDP per capita with a zoom slider.",
            style=description_style
        ),
        LineChart(
            id='biaxial-zoom-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'id': 'unemployment',
                    'data': unemployment_rate,
                    'label': 'Unemployment Rate',
                    'color': '#af3838',
                    'showMark': False,
                    'yAxisId': 'unemployment-axis',
                },
                {
                    'id': 'gdp',
                    'data': gdp_per_capita,
                    'label': 'GDP per Capita',
                    'color': '#4caf50',
                    'showMark': False,
                    'yAxisId': 'gdp-axis',
                },
            ],
            xAxis=[{
                'id': 'biaxial-x-axis',
                'data': years,
                'scaleType': 'point',
                'zoom': {
                    'minSpan': 5,
                    'maxSpan': 100,
                    'panning': True,
                },
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
            showSlider=True,
        ),
        html.P(
            "Source: Sample data based on FRED",
            style={'color': '#999', 'fontSize': '12px', 'marginTop': '10px'}
        ),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Controlled vs Uncontrolled Zoom
    # ==========================================================================
    html.Div([
        html.H2("Controlled vs Uncontrolled Zoom"),
        html.P(
            "LineChart supports both controlled and uncontrolled zoom patterns:",
            style=description_style
        ),
        html.Ul([
            html.Li([
                html.Strong("initialZoom"),
                " - Sets the initial zoom state. The chart manages its own state after that (uncontrolled)."
            ]),
            html.Li([
                html.Strong("zoom"),
                " - Fully controlled zoom state. Use with callbacks to programmatically control zoom."
            ]),
            html.Li([
                html.Strong("zoomData"),
                " - Output prop that reports the current zoom state whenever it changes."
            ]),
        ], style={'color': '#666', 'marginBottom': '20px'}),

        html.Div([
            html.Button(
                "Reset Zoom",
                id='reset-zoom-btn',
                style={
                    'backgroundColor': '#1976d2',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'marginRight': '10px',
                }
            ),
            html.Button(
                "Zoom to 2010-2020",
                id='zoom-decade-btn',
                style={
                    'backgroundColor': '#4caf50',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                }
            ),
        ], style={'marginBottom': '20px'}),

        LineChart(
            id='controlled-zoom-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'data': unemployment_rate,
                    'label': 'Unemployment Rate (%)',
                    'color': '#9c27b0',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'id': 'controlled-x-axis',
                'data': years,
                'scaleType': 'point',
                'label': 'Year',
                'zoom': {
                    'minSpan': 3,
                    'maxSpan': 100,
                    'panning': True,
                },
            }],
            grid={'horizontal': True},
            showSlider=True,
            zoom=[{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}],
        ),
        html.H4("Current Zoom State:", style={'marginTop': '20px'}),
        html.Pre(
            id='controlled-zoom-output',
            children="Interact with the chart or buttons to see zoom state",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Controlled zoom with buttons
LineChart(
    id='controlled-zoom-chart',
    zoom=[{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}],
    showSlider=True,
    ...
)

@callback(
    Output('controlled-zoom-chart', 'zoom'),
    Input('reset-zoom-btn', 'n_clicks'),
    Input('zoom-decade-btn', 'n_clicks'),
    Input('controlled-zoom-chart', 'zoomData'),
)
def control_zoom(reset_clicks, decade_clicks, zoom_data):
    triggered = ctx.triggered_id
    if triggered == 'reset-zoom-btn':
        return [{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}]
    elif triggered == 'zoom-decade-btn':
        # Calculate positions for 2010-2020 (indices 10-20 out of 24)
        return [{'axisId': 'controlled-x-axis', 'start': 41.67, 'end': 83.33}]
    return zoom_data or [{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}]
""", style=code_style),
        ]),
    ], style=section_style),
])


@callback(
    Output('zoom-slider-output', 'children'),
    Input('zoom-slider-chart', 'zoomData'),
    prevent_initial_call=True
)
def display_zoom_slider(zoom_data):
    """Display zoom state from slider chart."""
    if zoom_data:
        return json.dumps(zoom_data, indent=2)
    return "Interact with the slider to see zoom state changes"


@callback(
    Output('controlled-zoom-chart', 'zoom'),
    Output('controlled-zoom-output', 'children'),
    Input('reset-zoom-btn', 'n_clicks'),
    Input('zoom-decade-btn', 'n_clicks'),
    Input('controlled-zoom-chart', 'zoomData'),
    prevent_initial_call=True
)
def control_zoom(reset_clicks, decade_clicks, zoom_data):
    """Control zoom with buttons."""
    from dash import ctx
    triggered = ctx.triggered_id

    if triggered == 'reset-zoom-btn':
        new_zoom = [{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}]
        return new_zoom, json.dumps(new_zoom, indent=2)
    elif triggered == 'zoom-decade-btn':
        # 2010 is index 10, 2020 is index 20, out of 24 total years
        # Calculate as percentage: 10/24 * 100 = 41.67, 20/24 * 100 = 83.33
        new_zoom = [{'axisId': 'controlled-x-axis', 'start': 41.67, 'end': 83.33}]
        return new_zoom, json.dumps(new_zoom, indent=2)

    # Return current zoom data from chart interaction
    if zoom_data:
        return zoom_data, json.dumps(zoom_data, indent=2)

    return [{'axisId': 'controlled-x-axis', 'start': 0, 'end': 100}], "Full range"
