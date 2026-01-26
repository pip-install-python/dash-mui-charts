"""
LineChart Brush - Range selection with visual overlays
"""

import os
import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/linechart-brush', name='LineChart Brush')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample market-like data
market_data = [
    100, 96.56, 97.04, 98.95, 102.66, 106.18, 107.76, 109.78, 113.57,
    111.54, 107.69, 104.58, 106.62, 103.81, 104.46, 105.14, 108.94
]
dates = [f'Jan {i+1}' for i in range(len(market_data))]

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
        html.H1("LineChart Brush", style={'display': 'inline'}),
        pro_badge,
    ]),
    html.P(
        "The brush interaction enables users to select chart regions by clicking and dragging. "
        "It captures start and current positions of the selection for highlighting trends, "
        "selecting data points, or triggering callbacks based on the selection area.",
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
    # Brush with Values Overlay
    # ==========================================================================
    html.Div([
        html.H2("Brush with Values Overlay"),
        html.P(
            "The 'values' overlay shows start and end values with calculated difference and percentage change. "
            "Click and drag on the chart to select a region. This is useful for comparing values across time periods.",
            style=description_style
        ),
        LineChart(
            id='brush-values-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[{
                'id': 'market',
                'data': market_data,
                'label': 'Market Value',
                'color': '#1976d2',
                'showMark': False,
            }],
            xAxis=[{
                'data': dates,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            brushConfig={'enabled': True},
            brushOverlay='values',
            brushSeriesId='market',
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='brush-values-chart',
    series=[{
        'id': 'market',  # Important: provide ID for brush overlay
        'data': market_data,
        'label': 'Market Value',
    }],
    xAxis=[{'data': dates, 'scaleType': 'point'}],
    brushConfig={'enabled': True},
    brushOverlay='values',  # Shows start/end values with % change
    brushSeriesId='market',  # Which series to use for value calculations
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Brush Overlay Types
    # ==========================================================================
    html.Div([
        html.H2("Brush Overlay Types"),
        html.P(
            "Choose between different overlay types: 'none' (no visual feedback), "
            "'default' (standard selection rectangle), or 'values' (shows values with difference).",
            style=description_style
        ),

        html.Div([
            html.Label("Overlay Type: ", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Button("None", id='overlay-none-btn', n_clicks=0,
                       style={'marginRight': '5px', 'padding': '8px 16px'}),
            html.Button("Default", id='overlay-default-btn', n_clicks=0,
                       style={'marginRight': '5px', 'padding': '8px 16px'}),
            html.Button("Values", id='overlay-values-btn', n_clicks=0,
                       style={'padding': '8px 16px', 'backgroundColor': '#1976d2', 'color': 'white', 'border': 'none'}),
        ], style={'marginBottom': '20px'}),

        LineChart(
            id='brush-toggle-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'id': 'data',
                'data': [65, 59, 80, 81, 56, 55, 70, 75, 68, 72],
                'label': 'Monthly Data',
                'color': '#4caf50',
                'showMark': True,
            }],
            xAxis=[{
                'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            brushConfig={'enabled': True},
            brushOverlay='values',
            brushSeriesId='data',
        ),
        html.Div([
            html.H4("Overlay Types Reference:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("'none'", style={'padding': '8px'}), html.Td("No visual overlay, brush interaction still works", style={'padding': '8px'})]),
                    html.Tr([html.Td("'default'", style={'padding': '8px'}), html.Td("Standard MUI selection rectangle", style={'padding': '8px'})]),
                    html.Tr([html.Td("'values'", style={'padding': '8px'}), html.Td("Custom overlay showing start/end values with difference and percentage change", style={'padding': '8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Brush Configuration Options
    # ==========================================================================
    html.Div([
        html.H2("Brush Configuration"),
        html.P(
            "The brushConfig prop controls brush behavior. You can enable/disable tooltip "
            "and highlight interactions during brush selection.",
            style=description_style
        ),
        html.Div([
            html.H4("brushConfig Options:", style={'marginTop': '10px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Option", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Default", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td("enabled", style={'padding': '8px'}),
                        html.Td("boolean", style={'padding': '8px'}),
                        html.Td("false", style={'padding': '8px'}),
                        html.Td("Whether brush interaction is enabled", style={'padding': '8px'})
                    ]),
                    html.Tr([
                        html.Td("preventTooltip", style={'padding': '8px'}),
                        html.Td("boolean", style={'padding': '8px'}),
                        html.Td("true", style={'padding': '8px'}),
                        html.Td("Prevent tooltip from showing during brush", style={'padding': '8px'})
                    ]),
                    html.Tr([
                        html.Td("preventHighlight", style={'padding': '8px'}),
                        html.Td("boolean", style={'padding': '8px'}),
                        html.Td("true", style={'padding': '8px'}),
                        html.Td("Prevent highlight during brush", style={'padding': '8px'})
                    ]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '20px'}),
            html.Pre("""# Basic brush configuration
LineChart(
    brushConfig={
        'enabled': True,
        'preventTooltip': True,   # No tooltip during brush
        'preventHighlight': True,  # No highlight during brush
    },
    brushOverlay='values',
    brushSeriesId='my-series',
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Axis Highlight Configuration
    # ==========================================================================
    html.Div([
        html.H2("Axis Highlight Configuration"),
        html.P(
            "The axisHighlight prop controls how axes are highlighted on hover. "
            "You can configure both x and y axis highlighting independently.",
            style=description_style
        ),
        LineChart(
            id='axis-highlight-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=300,
            series=[{
                'data': [30, 40, 35, 50, 49, 60, 70, 91, 125],
                'label': 'Sales',
                'showMark': True,
            }],
            xAxis=[{
                'data': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'],
                'scaleType': 'point',
            }],
            grid={'horizontal': True, 'vertical': True},
            axisHighlight={'x': 'band', 'y': 'line'},
        ),
        html.Div([
            html.H4("axisHighlight Options:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Axis", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Values", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td("x", style={'padding': '8px'}),
                        html.Td("'none', 'line', 'band'", style={'padding': '8px'}),
                        html.Td("Highlight style for x-axis (default: 'line')", style={'padding': '8px'})
                    ]),
                    html.Tr([
                        html.Td("y", style={'padding': '8px'}),
                        html.Td("'none', 'line'", style={'padding': '8px'}),
                        html.Td("Highlight style for y-axis (default: 'none')", style={'padding': '8px'})
                    ]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '20px'}),
            html.Pre("""LineChart(
    series=[...],
    xAxis=[...],
    # Configure axis highlighting
    axisHighlight={
        'x': 'band',  # Shows a band highlight on x-axis
        'y': 'line',  # Shows a line highlight on y-axis
    },
)""", style=code_style),
        ]),
    ], style=section_style),
])


@callback(
    Output('brush-toggle-chart', 'brushOverlay'),
    Input('overlay-none-btn', 'n_clicks'),
    Input('overlay-default-btn', 'n_clicks'),
    Input('overlay-values-btn', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_overlay(none_clicks, default_clicks, values_clicks):
    """Toggle between overlay types."""
    from dash import ctx
    triggered = ctx.triggered_id

    if triggered == 'overlay-none-btn':
        return 'none'
    elif triggered == 'overlay-default-btn':
        return 'default'
    elif triggered == 'overlay-values-btn':
        return 'values'
    return 'values'
