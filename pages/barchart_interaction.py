"""
BarChart Demo - Interaction
Click events, highlighting, axis highlight, and tooltip modes.
"""

import json
import random

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/barchart-interaction', name='Bar Chart - Interaction')

from dash_mui_charts import BarChart

random.seed(42)

CARD = 'page-card'

PRE_STYLE = {
    'fontSize': '12px',
    'margin': 0,
    'padding': '10px 14px',
    'borderRadius': '6px',
    'background': 'var(--mantine-color-body)',
    'border': '1px solid var(--mantine-color-default-border)',
    'maxHeight': '120px',
    'overflow': 'auto',
    'color': 'var(--mantine-color-text)',
}

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [random.randint(30, 90) for _ in months]
expenses = [random.randint(20, 65) for _ in months]

layout = html.Div([
    html.H2("Bar Chart — Interaction"),
    html.P("Click events, highlighting, axis highlight modes, and tooltip triggers.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Click Events ---
    html.Div([
        html.H4("Click Events"),
        html.P("Click any bar to capture seriesId and dataIndex.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-int-click',
            series=[
                {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
        html.P("clickData:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='bar-int-click-out', children='Click a bar...', style=PRE_STYLE),
    ], className=CARD),

    # --- 2. Axis Click ---
    html.Div([
        html.H4("Axis Click"),
        html.P("Click on the chart area to capture the axis value and all series values at that point.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-int-axis-click',
            series=[
                {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
        html.P("axisClickData:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='bar-int-axis-click-out', children='Click on the chart...', style=PRE_STYLE),
    ], className=CARD),

    # --- 3. Series Highlighting ---
    html.Div([
        html.H4("Series Highlighting"),
        html.P("Hover over a bar to highlight the entire series and fade others.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-int-highlight',
            series=[
                {'data': [4, 3, 5, 7, 6], 'label': 'Alpha',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'}, 'color': '#5c6bc0'},
                {'data': [2, 5, 6, 3, 4], 'label': 'Beta',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'}, 'color': '#26a69a'},
                {'data': [3, 4, 2, 5, 3], 'label': 'Gamma',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'}, 'color': '#ef5350'},
            ],
            xAxis=[{'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
        html.P("highlightedItem:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='bar-int-highlight-out', children='Hover over a bar...', style=PRE_STYLE),
    ], className=CARD),

    # --- 4. Axis Highlight Modes ---
    html.Div([
        html.H4("Axis Highlight: Band vs Line vs None"),
        html.P("Control the hover band/line on each axis.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        html.Div([
            html.Div([
                html.P("x: 'band' (default)", style={'fontWeight': 600, 'fontSize': '13px'}),
                BarChart(
                    id='bar-int-ax-band',
                    series=[{'data': revenue, 'label': 'Revenue', 'color': '#1976d2'}],
                    xAxis=[{'data': months, 'scaleType': 'band'}],
                    axisHighlight={'x': 'band', 'y': 'none'},
                    height=200,
                ),
            ], style={'flex': 1}),
            html.Div([
                html.P("x: 'line'", style={'fontWeight': 600, 'fontSize': '13px'}),
                BarChart(
                    id='bar-int-ax-line',
                    series=[{'data': revenue, 'label': 'Revenue', 'color': '#f57c00'}],
                    xAxis=[{'data': months, 'scaleType': 'band'}],
                    axisHighlight={'x': 'line', 'y': 'none'},
                    height=200,
                ),
            ], style={'flex': 1}),
            html.Div([
                html.P("x: 'none'", style={'fontWeight': 600, 'fontSize': '13px'}),
                BarChart(
                    id='bar-int-ax-none',
                    series=[{'data': revenue, 'label': 'Revenue', 'color': '#388e3c'}],
                    xAxis=[{'data': months, 'scaleType': 'band'}],
                    axisHighlight={'x': 'none', 'y': 'none'},
                    height=200,
                ),
            ], style={'flex': 1}),
        ], style={'display': 'flex', 'gap': '16px'}),
    ], className=CARD),

    # --- 5. Tooltip Modes ---
    html.Div([
        html.H4("Tooltip Triggers"),
        html.P("'axis' shows all series at hover position; 'item' shows only the hovered bar.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        html.Div([
            html.Div([
                html.P("trigger: 'axis' (default)", style={'fontWeight': 600, 'fontSize': '13px'}),
                BarChart(
                    id='bar-int-tt-axis',
                    series=[
                        {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                        {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
                    ],
                    xAxis=[{'data': months, 'scaleType': 'band'}],
                    tooltip={'trigger': 'axis'},
                    height=250,
                ),
            ], style={'flex': 1}),
            html.Div([
                html.P("trigger: 'item'", style={'fontWeight': 600, 'fontSize': '13px'}),
                BarChart(
                    id='bar-int-tt-item',
                    series=[
                        {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                        {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
                    ],
                    xAxis=[{'data': months, 'scaleType': 'band'}],
                    tooltip={'trigger': 'item'},
                    height=250,
                ),
            ], style={'flex': 1}),
        ], style={'display': 'flex', 'gap': '16px'}),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})


@callback(
    Output('bar-int-click-out', 'children'),
    Input('bar-int-click', 'clickData'),
    prevent_initial_call=True,
)
def show_click(data):
    if not data:
        return 'Click a bar...'
    return json.dumps(data, indent=2)


@callback(
    Output('bar-int-axis-click-out', 'children'),
    Input('bar-int-axis-click', 'axisClickData'),
    prevent_initial_call=True,
)
def show_axis_click(data):
    if not data:
        return 'Click on the chart...'
    return json.dumps(data, indent=2)


@callback(
    Output('bar-int-highlight-out', 'children'),
    Input('bar-int-highlight', 'highlightedItem'),
    prevent_initial_call=True,
)
def show_highlight(data):
    if not data:
        return 'Hover over a bar...'
    return json.dumps(data, indent=2)
