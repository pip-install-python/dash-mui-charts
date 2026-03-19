"""
LineChart Highlighting - Controlled axis/item highlights and per-series highlightScope
"""

import os
import json
import dash
from dash import html, callback, Input, Output, State, ctx

dash.register_page(__name__, path='/linechart-highlighting', name='LineChart Highlighting')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales_2023 = [120, 135, 150, 145, 160, 175, 190, 185, 200, 210, 195, 220]
sales_2024 = [130, 145, 165, 160, 180, 195, 210, 205, 225, 235, 220, 250]

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
button_style = {
    'backgroundColor': '#1976d2',
    'color': 'white',
    'border': 'none',
    'padding': '8px 16px',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'marginRight': '8px',
    'marginBottom': '8px',
}

layout = html.Div([
    html.H1("LineChart Highlighting"),
    html.P(
        "This page demonstrates controlled highlighting features including "
        "axis highlights, item highlights, and per-series highlight scopes.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '20px'}
    ),

    # ==========================================================================
    # Controlled Item Highlight
    # ==========================================================================
    html.Div([
        html.H2("Controlled Item Highlight"),
        html.P(
            "Use highlightedItem to programmatically control which data point is highlighted. "
            "Hover over the chart to see the highlight state update, or use the buttons below "
            "to set highlights programmatically.",
            style=description_style
        ),
        html.Div([
            html.Button("Highlight Jan 2023", id='highlight-jan-btn', style=button_style),
            html.Button("Highlight Jun 2024", id='highlight-jun-btn', style=button_style),
            html.Button("Clear Highlight", id='clear-highlight-btn', style={**button_style, 'backgroundColor': '#666'}),
        ], style={'marginBottom': '15px'}),
        LineChart(
            id='item-highlight-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'sales-2023',
                    'data': sales_2023,
                    'label': 'Sales 2023',
                    'color': '#1976d2',
                    'showMark': True,
                    'highlightScope': {'highlight': 'item', 'fade': 'global'},
                },
                {
                    'id': 'sales-2024',
                    'data': sales_2024,
                    'label': 'Sales 2024',
                    'color': '#4caf50',
                    'showMark': True,
                    'highlightScope': {'highlight': 'item', 'fade': 'global'},
                },
            ],
            xAxis=[{
                'id': 'x-axis',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            tooltip={'trigger': 'item'},
        ),
        html.H4("Highlighted Item:", style={'marginTop': '20px'}),
        html.Pre(
            id='item-highlight-output',
            children="Hover over data points or click buttons to see highlight state",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='item-highlight-chart',
    series=[
        {
            'id': 'sales-2023',
            'data': sales_2023,
            'label': 'Sales 2023',
            'showMark': True,  # Required for item hover
            'highlightScope': {'highlight': 'item', 'fade': 'global'},
        },
        {
            'id': 'sales-2024',
            'data': sales_2024,
            'label': 'Sales 2024',
            'showMark': True,
            'highlightScope': {'highlight': 'item', 'fade': 'global'},
        },
    ],
    xAxis=[{'data': months, 'scaleType': 'point'}],
    tooltip={'trigger': 'item'},  # Use item trigger for item-level interaction
)

# Callback to control highlight
@callback(
    Output('item-highlight-chart', 'highlightedItem'),
    Output('item-highlight-output', 'children'),
    Input('highlight-jan-btn', 'n_clicks'),
    Input('item-highlight-chart', 'highlightedItem'),
)
def control_highlight(jan_clicks, current_highlight):
    if ctx.triggered_id == 'highlight-jan-btn':
        return {'seriesId': 'sales-2023', 'dataIndex': 0}, json.dumps(...)
    return current_highlight, json.dumps(current_highlight)
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Controlled Axis Highlight
    # ==========================================================================
    html.Div([
        html.H2("Controlled Axis Highlight"),
        html.P(
            "Use highlightedAxis to control which axis position is highlighted. "
            "This is useful for synchronizing highlights across charts or highlighting "
            "specific time periods.",
            style=description_style
        ),
        html.Div([
            html.Button("Highlight March", id='highlight-mar-axis-btn', style=button_style),
            html.Button("Highlight September", id='highlight-sep-axis-btn', style=button_style),
            html.Button("Clear Axis Highlight", id='clear-axis-btn', style={**button_style, 'backgroundColor': '#666'}),
        ], style={'marginBottom': '15px'}),
        LineChart(
            id='axis-highlight-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'sales',
                    'data': sales_2024,
                    'label': 'Sales 2024',
                    'color': '#9c27b0',
                    'showMark': True,
                },
            ],
            xAxis=[{
                'id': 'month-axis',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'band', 'y': 'none'},
        ),
        html.H4("Highlighted Axis:", style={'marginTop': '20px'}),
        html.Pre(
            id='axis-highlight-output',
            children="Hover over the chart or click buttons to see axis highlight state",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='axis-highlight-chart',
    series=[{'id': 'sales', 'data': sales_2024}],
    xAxis=[{'id': 'month-axis', 'data': months, 'scaleType': 'point'}],
    axisHighlight={'x': 'band', 'y': 'none'},  # Show band highlight on x-axis
    highlightedAxis=[{'axisId': 'month-axis', 'dataIndex': 2}],  # Highlight March
)
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Per-Series Highlight Scope
    # ==========================================================================
    html.Div([
        html.H2("Per-Series Highlight Scope"),
        html.P(
            "Each series can have its own highlightScope configuration. "
            "This allows different highlight/fade behaviors per series. "
            "In this example, Sales 2023 highlights the whole series while Sales 2024 highlights individual items.",
            style=description_style
        ),
        LineChart(
            id='highlight-scope-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'sales-2023-scope',
                    'data': sales_2023,
                    'label': 'Sales 2023 (series highlight)',
                    'color': '#ff5722',
                    'showMark': True,
                    'highlightScope': {
                        'highlight': 'series',  # Highlight entire series
                        'fade': 'global',       # Fade all other series
                    },
                },
                {
                    'id': 'sales-2024-scope',
                    'data': sales_2024,
                    'label': 'Sales 2024 (item highlight)',
                    'showMark': True,
                    'color': '#00bcd4',
                    'highlightScope': {
                        'highlight': 'item',    # Highlight single item
                        'fade': 'series',       # Fade other items in same series
                    },
                },
            ],
            xAxis=[{
                'id': 'x-axis-scope',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            tooltip={'trigger': 'item'},
        ),
        html.P(
            "Hover over each line to see the different highlight behaviors.",
            style={'color': '#666', 'fontStyle': 'italic', 'marginTop': '10px'}
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    series=[
        {
            'id': 'sales-2023',
            'data': sales_2023,
            'label': 'Sales 2023 (series highlight)',
            'highlightScope': {
                'highlight': 'series',  # Highlight entire series on hover
                'fade': 'global',       # Fade all other series
            },
        },
        {
            'id': 'sales-2024',
            'data': sales_2024,
            'label': 'Sales 2024 (item highlight)',
            'highlightScope': {
                'highlight': 'item',    # Highlight single data point
                'fade': 'series',       # Fade other items in same series
            },
        },
    ],
    tooltip={'trigger': 'item'},  # Show tooltip on item hover
)
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Highlight Scope Reference
    # ==========================================================================
    html.Div([
        html.H2("Highlight Scope Reference"),
        html.P(
            "The highlightScope configuration controls how items are highlighted and how other items fade.",
            style=description_style
        ),
        html.Div([
            html.H4("highlight options:", style={'marginTop': '10px'}),
            html.Table([
                html.Tbody([
                    html.Tr([html.Td("'none'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("No highlighting", style={'padding': '8px'})]),
                    html.Tr([html.Td("'item'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("Highlight single data point on hover", style={'padding': '8px'})]),
                    html.Tr([html.Td("'series'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("Highlight entire series on hover", style={'padding': '8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginBottom': '20px'}),

            html.H4("fade options:", style={'marginTop': '10px'}),
            html.Table([
                html.Tbody([
                    html.Tr([html.Td("'none'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("No fading", style={'padding': '8px'})]),
                    html.Tr([html.Td("'series'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("Fade other items in the same series", style={'padding': '8px'})]),
                    html.Tr([html.Td("'global'", style={'padding': '8px', 'fontFamily': 'monospace'}), html.Td("Fade all items in all series", style={'padding': '8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse'}),
        ]),
    ], style=section_style),
])


# ==========================================================================
# Callbacks
# ==========================================================================

# Separate callback for button-triggered highlights
@callback(
    Output('item-highlight-chart', 'highlightedItem'),
    Input('highlight-jan-btn', 'n_clicks'),
    Input('highlight-jun-btn', 'n_clicks'),
    Input('clear-highlight-btn', 'n_clicks'),
    prevent_initial_call=True
)
def set_item_highlight(jan_clicks, jun_clicks, clear_clicks):
    """Set item highlight via buttons."""
    triggered = ctx.triggered_id

    if triggered == 'highlight-jan-btn':
        return {'seriesId': 'sales-2023', 'dataIndex': 0}
    elif triggered == 'highlight-jun-btn':
        return {'seriesId': 'sales-2024', 'dataIndex': 5}
    elif triggered == 'clear-highlight-btn':
        return None
    return dash.no_update


# Separate callback for displaying current highlight state
@callback(
    Output('item-highlight-output', 'children'),
    Input('item-highlight-chart', 'highlightedItem'),
)
def display_item_highlight(current_highlight):
    """Display current highlight state (from hover or buttons)."""
    if current_highlight:
        return json.dumps(current_highlight, indent=2)
    return "null (no highlight)"


# Separate callback for button-triggered axis highlights
@callback(
    Output('axis-highlight-chart', 'highlightedAxis'),
    Input('highlight-mar-axis-btn', 'n_clicks'),
    Input('highlight-sep-axis-btn', 'n_clicks'),
    Input('clear-axis-btn', 'n_clicks'),
    prevent_initial_call=True
)
def set_axis_highlight(mar_clicks, sep_clicks, clear_clicks):
    """Set axis highlight via buttons."""
    triggered = ctx.triggered_id

    if triggered == 'highlight-mar-axis-btn':
        return [{'axisId': 'month-axis', 'dataIndex': 2}]  # March is index 2
    elif triggered == 'highlight-sep-axis-btn':
        return [{'axisId': 'month-axis', 'dataIndex': 8}]  # September is index 8
    elif triggered == 'clear-axis-btn':
        return []
    return dash.no_update


# Separate callback for displaying current axis highlight state
@callback(
    Output('axis-highlight-output', 'children'),
    Input('axis-highlight-chart', 'highlightedAxis'),
)
def display_axis_highlight(current_highlight):
    """Display current axis highlight state."""
    if current_highlight:
        return json.dumps(current_highlight, indent=2)
    return "[] (no highlight)"
