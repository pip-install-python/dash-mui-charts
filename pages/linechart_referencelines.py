"""
LineChart Reference Lines - Horizontal and vertical reference markers
"""

import os
import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State

dash.register_page(__name__, path='/linechart-referencelines', name='LineChart Reference Lines')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data - Monthly sales with targets
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales_data = [65, 72, 68, 85, 92, 88, 95, 110, 105, 98, 115, 125]
target = 90
warning_threshold = 75

# Stock price data for date examples
stock_prices = [152.3, 148.7, 155.2, 160.1, 158.4, 165.8, 172.3, 168.9, 175.2, 180.5]
stock_dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01',
               '2024-06-01', '2024-07-01', '2024-08-01', '2024-09-01', '2024-10-01']

# Temperature data for biaxial example
temp_celsius = [5, 8, 12, 18, 22, 26, 28, 27, 23, 17, 10, 6]
humidity = [85, 80, 75, 65, 60, 55, 58, 62, 68, 75, 82, 88]

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
    html.H1("LineChart Reference Lines"),
    html.P(
        "Reference lines are horizontal or vertical markers that help highlight specific values, "
        "thresholds, targets, or important dates on a chart. They provide visual context for "
        "interpreting data.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # ==========================================================================
    # Basic Horizontal Reference Lines
    # ==========================================================================
    html.Div([
        html.H2("Horizontal Reference Lines"),
        html.P(
            "Use the 'y' prop to create horizontal reference lines. These are useful for showing "
            "targets, thresholds, averages, or any significant Y-axis value.",
            style=description_style
        ),
        LineChart(
            id='horizontal-ref-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': sales_data,
                'label': 'Monthly Sales',
                'color': '#1976d2',
                'showMark': True,
            }],
            xAxis=[{
                'data': months,
                'scaleType': 'point',
                'label': 'Month',
            }],
            yAxis=[{
                'label': 'Sales ($K)',
                'min': 50,
                'max': 140,
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': target,
                    'label': 'Target',
                    'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#4caf50', 'fontWeight': 'bold'},
                },
                {
                    'y': warning_threshold,
                    'label': 'Warning',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""LineChart(
    series=[{'data': sales_data, 'label': 'Monthly Sales'}],
    xAxis=[{'data': months, 'scaleType': 'point'}],
    referenceLines=[
        {
            'y': 90,  # Target line
            'label': 'Target',
            'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2},
            'labelStyle': {'fill': '#4caf50', 'fontWeight': 'bold'},
        },
        {
            'y': 75,  # Warning threshold
            'label': 'Warning',
            'lineStyle': {'stroke': '#ff9800', 'strokeDasharray': '5 5'},
            'labelStyle': {'fill': '#ff9800'},
        },
    ],
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Vertical Reference Lines
    # ==========================================================================
    html.Div([
        html.H2("Vertical Reference Lines"),
        html.P(
            "Use the 'x' prop to create vertical reference lines. These are useful for marking "
            "specific dates, events, or X-axis values of interest.",
            style=description_style
        ),
        LineChart(
            id='vertical-ref-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': sales_data,
                'label': 'Monthly Sales',
                'color': '#9c27b0',
                'area': True,
                'showMark': False,
            }],
            xAxis=[{
                'data': months,
                'scaleType': 'point',
                'label': 'Month',
            }],
            yAxis=[{
                'label': 'Sales ($K)',
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'x': 'Apr',
                    'label': 'Q1 End',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#f44336'},
                    'labelAlign': 'start',
                },
                {
                    'x': 'Jul',
                    'label': 'Q2 End',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#f44336'},
                    'labelAlign': 'start',
                },
                {
                    'x': 'Oct',
                    'label': 'Q3 End',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#f44336'},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""LineChart(
    series=[{'data': sales_data, 'label': 'Monthly Sales', 'area': True}],
    xAxis=[{'data': months, 'scaleType': 'point'}],
    referenceLines=[
        {
            'x': 'Apr',  # Match x-axis value
            'label': 'Q1 End',
            'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
            'labelAlign': 'start',  # Position label at top
        },
        {
            'x': 'Jul',
            'label': 'Q2 End',
            ...
        },
    ],
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Combined Reference Lines
    # ==========================================================================
    html.Div([
        html.H2("Combined Horizontal & Vertical Lines"),
        html.P(
            "Combine both horizontal and vertical reference lines to create rich annotations "
            "that highlight both X and Y values of significance.",
            style=description_style
        ),
        LineChart(
            id='combined-ref-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[{
                'data': sales_data,
                'label': 'Monthly Sales',
                'color': '#2196f3',
                'showMark': True,
            }],
            xAxis=[{
                'data': months,
                'scaleType': 'point',
            }],
            yAxis=[{
                'label': 'Sales ($K)',
                'min': 50,
                'max': 140,
            }],
            grid={'horizontal': True, 'vertical': True},
            referenceLines=[
                # Horizontal lines
                {
                    'y': 100,
                    'label': '100K Goal',
                    'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#4caf50', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
                {
                    'y': 80,
                    'label': 'Minimum',
                    'lineStyle': {'stroke': '#ff5722', 'strokeDasharray': '3 3'},
                    'labelStyle': {'fill': '#ff5722'},
                    'labelAlign': 'end',
                },
                # Vertical lines
                {
                    'x': 'Aug',
                    'label': 'Peak Month',
                    'lineStyle': {'stroke': '#673ab7', 'strokeWidth': 2, 'strokeDasharray': '8 4'},
                    'labelStyle': {'fill': '#673ab7', 'fontWeight': 'bold'},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""referenceLines=[
    # Horizontal reference lines (y prop)
    {
        'y': 100,
        'label': '100K Goal',
        'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2},
        'labelAlign': 'end',  # Position at right
    },
    # Vertical reference lines (x prop)
    {
        'x': 'Aug',
        'label': 'Peak Month',
        'lineStyle': {'stroke': '#673ab7', 'strokeDasharray': '8 4'},
        'labelAlign': 'start',  # Position at top
    },
]""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Label Alignment Options
    # ==========================================================================
    html.Div([
        html.H2("Label Alignment"),
        html.P(
            "The 'labelAlign' prop controls where the label appears along the reference line. "
            "Options are 'start', 'middle' (default), and 'end'.",
            style=description_style
        ),
        LineChart(
            id='label-align-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': [30, 40, 35, 50, 49, 60, 70, 65, 75],
                'label': 'Data',
                'showMark': False,
            }],
            xAxis=[{
                'data': list(range(1, 10)),
                'scaleType': 'point',
            }],
            yAxis=[{
                'min': 20,
                'max': 85,
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': 40,
                    'label': "labelAlign='start'",
                    'labelAlign': 'start',
                    'lineStyle': {'stroke': '#e91e63', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#e91e63', 'fontSize': 12},
                },
                {
                    'y': 55,
                    'label': "labelAlign='middle' (default)",
                    'labelAlign': 'middle',
                    'lineStyle': {'stroke': '#9c27b0', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#9c27b0', 'fontSize': 12},
                },
                {
                    'y': 70,
                    'label': "labelAlign='end'",
                    'labelAlign': 'end',
                    'lineStyle': {'stroke': '#3f51b5', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#3f51b5', 'fontSize': 12},
                },
            ],
        ),
        html.Div([
            html.H4("labelAlign Options:", style={'marginTop': '20px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Value", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Horizontal Line", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                        html.Th("Vertical Line", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("'start'", style={'padding': '8px'}), html.Td("Left side", style={'padding': '8px'}), html.Td("Top", style={'padding': '8px'})]),
                    html.Tr([html.Td("'middle'", style={'padding': '8px'}), html.Td("Center (default)", style={'padding': '8px'}), html.Td("Center (default)", style={'padding': '8px'})]),
                    html.Tr([html.Td("'end'", style={'padding': '8px'}), html.Td("Right side", style={'padding': '8px'}), html.Td("Bottom", style={'padding': '8px'})]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Line Styling
    # ==========================================================================
    html.Div([
        html.H2("Line Styling"),
        html.P(
            "Use the 'lineStyle' prop to customize the appearance of reference lines. "
            "You can set stroke color, width, dash patterns, and opacity.",
            style=description_style
        ),
        LineChart(
            id='line-style-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': [20, 35, 30, 45, 40, 55, 50, 65, 60],
                'label': 'Data',
                'showMark': False,
                'color': '#607d8b',
            }],
            xAxis=[{
                'data': list(range(1, 10)),
                'scaleType': 'point',
            }],
            yAxis=[{
                'min': 10,
                'max': 75,
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': 25,
                    'label': 'Solid (default)',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#f44336'},
                    'labelAlign': 'end',
                },
                {
                    'y': 40,
                    'label': 'Dashed',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
                {
                    'y': 55,
                    'label': 'Dotted',
                    'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2, 'strokeDasharray': '2 3'},
                    'labelStyle': {'fill': '#4caf50'},
                    'labelAlign': 'end',
                },
                {
                    'y': 70,
                    'label': 'Thick dashed',
                    'lineStyle': {'stroke': '#2196f3', 'strokeWidth': 4, 'strokeDasharray': '10 5'},
                    'labelStyle': {'fill': '#2196f3'},
                    'labelAlign': 'end',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""# Line style examples
referenceLines=[
    {
        'y': 25,
        'label': 'Solid',
        'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2},
    },
    {
        'y': 40,
        'label': 'Dashed',
        'lineStyle': {
            'stroke': '#ff9800',
            'strokeWidth': 2,
            'strokeDasharray': '5 5',  # 5px dash, 5px gap
        },
    },
    {
        'y': 55,
        'label': 'Dotted',
        'lineStyle': {
            'stroke': '#4caf50',
            'strokeDasharray': '2 3',  # 2px dash, 3px gap
        },
    },
]""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Label Spacing
    # ==========================================================================
    html.Div([
        html.H2("Label Spacing"),
        html.P(
            "The 'spacing' prop adds space between the label and the reference line or axes. "
            "It can be a number (applied to both x and y) or an object with x and y values.",
            style=description_style
        ),
        LineChart(
            id='spacing-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': [30, 40, 35, 50, 49, 60, 55],
                'label': 'Data',
                'showMark': True,
            }],
            xAxis=[{
                'data': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': 45,
                    'label': 'Default spacing',
                    'lineStyle': {'stroke': '#9c27b0'},
                    'labelStyle': {'fill': '#9c27b0'},
                    'labelAlign': 'end',
                },
                {
                    'y': 55,
                    'label': 'spacing=20',
                    'lineStyle': {'stroke': '#2196f3'},
                    'labelStyle': {'fill': '#2196f3'},
                    'labelAlign': 'end',
                    'spacing': 20,
                },
                {
                    'x': 'D',
                    'label': 'Custom spacing',
                    'lineStyle': {'stroke': '#4caf50'},
                    'labelStyle': {'fill': '#4caf50'},
                    'labelAlign': 'start',
                    'spacing': {'x': 10, 'y': 15},
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""referenceLines=[
    {
        'y': 55,
        'label': 'spacing=20',
        'spacing': 20,  # 20px spacing in both directions
    },
    {
        'x': 'D',
        'label': 'Custom spacing',
        'spacing': {'x': 10, 'y': 15},  # Different x and y spacing
    },
]""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # With Multiple Y-Axes (axisId)
    # ==========================================================================
    html.Div([
        html.H2("Reference Lines with Multiple Axes"),
        html.P(
            "When using multiple Y-axes, use the 'axisId' prop to specify which axis "
            "the reference line's value corresponds to.",
            style=description_style
        ),
        LineChart(
            id='multiaxis-ref-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'id': 'temp',
                    'data': temp_celsius,
                    'label': 'Temperature (C)',
                    'color': '#f44336',
                    'yAxisId': 'temp-axis',
                    'showMark': False,
                },
                {
                    'id': 'humidity',
                    'data': humidity,
                    'label': 'Humidity (%)',
                    'color': '#2196f3',
                    'yAxisId': 'humidity-axis',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'data': months,
                'scaleType': 'point',
            }],
            yAxis=[
                {
                    'id': 'temp-axis',
                    'label': 'Temperature (C)',
                    'position': 'left',
                    'min': 0,
                    'max': 35,
                },
                {
                    'id': 'humidity-axis',
                    'label': 'Humidity (%)',
                    'position': 'right',
                    'min': 50,
                    'max': 95,
                },
            ],
            margin={'left': 50, 'right': 60},
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': 20,
                    'axisId': 'temp-axis',
                    'label': 'Comfortable temp',
                    'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#f44336'},
                    'labelAlign': 'start',
                },
                {
                    'y': 70,
                    'axisId': 'humidity-axis',
                    'label': 'Ideal humidity',
                    'lineStyle': {'stroke': '#2196f3', 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#2196f3'},
                    'labelAlign': 'end',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""# Reference lines on different axes
yAxis=[
    {'id': 'temp-axis', 'label': 'Temperature', 'position': 'left'},
    {'id': 'humidity-axis', 'label': 'Humidity', 'position': 'right'},
]

referenceLines=[
    {
        'y': 20,
        'axisId': 'temp-axis',  # Use temperature scale
        'label': 'Comfortable temp',
        'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '5 5'},
    },
    {
        'y': 70,
        'axisId': 'humidity-axis',  # Use humidity scale
        'label': 'Ideal humidity',
        'lineStyle': {'stroke': '#2196f3', 'strokeDasharray': '5 5'},
    },
]""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Dynamic Reference Lines
    # ==========================================================================
    html.Div([
        html.H2("Dynamic Reference Lines"),
        html.P(
            "Reference lines can be updated dynamically via callbacks. Use this to show "
            "user-selected thresholds or computed values like averages.",
            style=description_style
        ),
        html.Div([
            html.Label("Threshold Value: ", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Input(
                id='threshold-input',
                type='number',
                value=80,
                min=50,
                max=130,
                style={'width': '80px', 'marginRight': '20px', 'padding': '5px'}
            ),
            html.Button(
                "Show Average",
                id='show-avg-btn',
                n_clicks=0,
                style={'padding': '8px 16px', 'marginRight': '10px'}
            ),
            html.Button(
                "Hide Average",
                id='hide-avg-btn',
                n_clicks=0,
                style={'padding': '8px 16px'}
            ),
        ], style={'marginBottom': '20px'}),
        LineChart(
            id='dynamic-ref-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': sales_data,
                'label': 'Monthly Sales',
                'color': '#009688',
                'showMark': True,
            }],
            xAxis=[{
                'data': months,
                'scaleType': 'point',
            }],
            yAxis=[{
                'label': 'Sales ($K)',
                'min': 50,
                'max': 140,
            }],
            grid={'horizontal': True},
            referenceLines=[
                {
                    'y': 80,
                    'label': 'Threshold: 80',
                    'lineStyle': {'stroke': '#ff5722', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#ff5722', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""@callback(
    Output('dynamic-ref-chart', 'referenceLines'),
    Input('threshold-input', 'value'),
    Input('show-avg-btn', 'n_clicks'),
    Input('hide-avg-btn', 'n_clicks'),
)
def update_reference_lines(threshold, show_clicks, hide_clicks):
    lines = [{
        'y': threshold,
        'label': f'Threshold: {threshold}',
        'lineStyle': {'stroke': '#ff5722', 'strokeWidth': 2},
    }]

    # Add average line if requested
    if show_clicks > hide_clicks:
        avg = sum(sales_data) / len(sales_data)
        lines.append({
            'y': avg,
            'label': f'Average: {avg:.1f}',
            'lineStyle': {'stroke': '#4caf50', 'strokeDasharray': '5 5'},
        })

    return lines""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # API Reference
    # ==========================================================================
    html.Div([
        html.H2("Reference Line Props"),
        html.P(
            "Complete reference for all available props on reference line objects.",
            style=description_style
        ),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Prop", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                    html.Th("Type", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                    html.Th("Default", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                    html.Th("Description", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                ]),
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("x", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("string | number | Date", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("-", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("X-axis value for a vertical reference line", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("y", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("string | number | Date", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("-", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("Y-axis value for a horizontal reference line", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("axisId", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("string | number", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("First axis", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("ID of the axis for the reference value (for multi-axis charts)", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("label", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("string", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("-", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("Label text displayed along the reference line", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("labelAlign", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("'start' | 'middle' | 'end'", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("'middle'", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("Position of the label along the line", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("lineStyle", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("object", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("-", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("CSS style for the line (stroke, strokeWidth, strokeDasharray, etc.)", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("labelStyle", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("object", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("-", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("CSS style for the label (fill, fontSize, fontWeight, etc.)", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
                html.Tr([
                    html.Td("spacing", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("number | {x: number, y: number}", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("{x: 5, y: 0} or {x: 0, y: 5}", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                    html.Td("Space around the label in pixels", style={'padding': '10px', 'borderBottom': '1px solid #eee'}),
                ]),
            ]),
        ], style={'width': '100%', 'borderCollapse': 'collapse'}),
    ], style=section_style),
])


@callback(
    Output('dynamic-ref-chart', 'referenceLines'),
    Input('threshold-input', 'value'),
    Input('show-avg-btn', 'n_clicks'),
    Input('hide-avg-btn', 'n_clicks'),
)
def update_reference_lines(threshold, show_clicks, hide_clicks):
    """Update reference lines dynamically based on user input."""
    threshold = threshold or 80

    lines = [{
        'y': threshold,
        'label': f'Threshold: {threshold}',
        'lineStyle': {'stroke': '#ff5722', 'strokeWidth': 2},
        'labelStyle': {'fill': '#ff5722', 'fontWeight': 'bold'},
        'labelAlign': 'end',
    }]

    # Add average line if show button clicked more times than hide
    if show_clicks > hide_clicks:
        avg = sum(sales_data) / len(sales_data)
        lines.append({
            'y': avg,
            'label': f'Average: {avg:.1f}',
            'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
            'labelStyle': {'fill': '#4caf50', 'fontWeight': 'bold'},
            'labelAlign': 'start',
        })

    return lines
