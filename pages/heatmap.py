"""
Heatmap - Matrix Visualization with Color Intensity

This page demonstrates the Heatmap component for creating
matrix visualizations where color intensity represents values.
This is a Pro feature - requires MUI X Pro license key.
"""

import os
import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/heatmap', name='Heatmap')

from dash_mui_charts import Heatmap

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data - Weekly activity (7 days x 4 weeks)
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']

# Generate activity data as [x_index, y_index, value]
activity_data = [
    # Week 1
    [0, 0, 8], [1, 0, 7], [2, 0, 9], [3, 0, 6], [4, 0, 5], [5, 0, 2], [6, 0, 1],
    # Week 2
    [0, 1, 7], [1, 1, 8], [2, 1, 8], [3, 1, 9], [4, 1, 6], [5, 1, 3], [6, 1, 2],
    # Week 3
    [0, 2, 9], [1, 2, 8], [2, 2, 7], [3, 2, 8], [4, 2, 7], [5, 2, 4], [6, 2, 3],
    # Week 4
    [0, 3, 6], [1, 3, 7], [2, 3, 8], [3, 3, 9], [4, 3, 8], [5, 3, 5], [6, 3, 2],
]

# Correlation matrix data
variables = ['Revenue', 'Users', 'Sessions', 'Conversion', 'Bounce Rate']
correlation_data = [
    [0, 0, 1.00], [1, 0, 0.85], [2, 0, 0.78], [3, 0, 0.65], [4, 0, -0.42],
    [0, 1, 0.85], [1, 1, 1.00], [2, 1, 0.92], [3, 1, 0.58], [4, 1, -0.55],
    [0, 2, 0.78], [1, 2, 0.92], [2, 2, 1.00], [3, 2, 0.48], [4, 2, -0.62],
    [0, 3, 0.65], [1, 3, 0.58], [2, 3, 0.48], [3, 3, 1.00], [4, 3, -0.38],
    [0, 4, -0.42], [1, 4, -0.55], [2, 4, -0.62], [3, 4, -0.38], [4, 4, 1.00],
]

# Temperature data (hours x days)
hours = ['6am', '9am', '12pm', '3pm', '6pm', '9pm']
temp_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
temperature_data = [
    # Monday
    [0, 0, 58], [0, 1, 65], [0, 2, 72], [0, 3, 75], [0, 4, 70], [0, 5, 62],
    # Tuesday
    [1, 0, 55], [1, 1, 62], [1, 2, 70], [1, 3, 73], [1, 4, 68], [1, 5, 60],
    # Wednesday
    [2, 0, 60], [2, 1, 68], [2, 2, 78], [2, 3, 82], [2, 4, 76], [2, 5, 65],
    # Thursday
    [3, 0, 62], [3, 1, 70], [3, 2, 80], [3, 3, 85], [3, 4, 78], [3, 5, 68],
    # Friday
    [4, 0, 58], [4, 1, 66], [4, 2, 74], [4, 3, 78], [4, 4, 72], [4, 5, 64],
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
        html.H1("Heatmap", style={'display': 'inline'}),
        pro_badge,
    ]),
    html.P(
        "Heatmaps display data as a matrix where color intensity represents values. "
        "Perfect for correlation matrices, activity tracking, and multi-dimensional data.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '20px'}
    ),
    html.Div([
        html.P(
            "This feature requires an MUI X Pro license key. "
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
    # Basic Heatmap
    # ==========================================================================
    html.Div([
        html.H2("Basic Heatmap"),
        html.P(
            "A simple heatmap showing weekly activity levels. "
            "Data is provided as [x_index, y_index, value] tuples.",
            style=description_style
        ),
        Heatmap(
            id='basic-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days, 'label': 'Day of Week'},
            yAxis={'data': weeks, 'label': 'Week'},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#e3f2fd', '#1565c0'],
            },
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""Heatmap(
    licenseKey=MUI_LICENSE_KEY,
    data=[
        [0, 0, 8], [1, 0, 7], [2, 0, 9], ...  # [x, y, value]
    ],
    xAxis={'data': ['Mon', 'Tue', 'Wed', ...], 'label': 'Day of Week'},
    yAxis={'data': ['Week 1', 'Week 2', ...], 'label': 'Week'},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 10,
        'colors': ['#e3f2fd', '#1565c0'],  # Light blue to dark blue
    },
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Correlation Matrix
    # ==========================================================================
    html.Div([
        html.H2("Correlation Matrix"),
        html.P(
            "Heatmaps are ideal for displaying correlation matrices. "
            "Use a diverging color scale to show positive and negative correlations.",
            style=description_style
        ),
        Heatmap(
            id='correlation-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=correlation_data,
            xAxis={'data': variables},
            yAxis={'data': variables},
            height=400,
            colorScale={
                'type': 'continuous',
                'min': -1,
                'max': 1,
                'colors': ['#d32f2f', '#fff', '#1976d2'],  # Red to White to Blue
            },
            margin={'left': 100, 'right': 20, 'top': 20, 'bottom': 80},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Correlation values range from -1 to 1
Heatmap(
    data=correlation_data,  # [[0, 0, 1.00], [1, 0, 0.85], ...]
    xAxis={'data': ['Revenue', 'Users', 'Sessions', ...]},
    yAxis={'data': ['Revenue', 'Users', 'Sessions', ...]},
    height=400,
    colorScale={
        'type': 'continuous',
        'min': -1,
        'max': 1,
        'colors': ['#d32f2f', '#fff', '#1976d2'],  # Diverging: red-white-blue
    },
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Temperature Heatmap
    # ==========================================================================
    html.Div([
        html.H2("Temperature Heatmap"),
        html.P(
            "A practical example showing hourly temperatures across the week. "
            "Uses a warm color scale from cool (blue) to hot (red).",
            style=description_style
        ),
        Heatmap(
            id='temperature-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=temperature_data,
            xAxis={'data': temp_days, 'label': 'Day'},
            yAxis={'data': hours, 'label': 'Time'},
            height=350,
            colorScale={
                'type': 'continuous',
                'min': 50,
                'max': 90,
                'colors': ['#42a5f5', '#ffeb3b', '#f44336'],  # Blue-Yellow-Red
            },
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""Heatmap(
    data=temperature_data,
    xAxis={'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'label': 'Day'},
    yAxis={'data': ['6am', '9am', '12pm', '3pm', '6pm', '9pm'], 'label': 'Time'},
    height=350,
    colorScale={
        'type': 'continuous',
        'min': 50,
        'max': 90,
        'colors': ['#42a5f5', '#ffeb3b', '#f44336'],  # Blue-Yellow-Red
    },
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Custom Rounded Cells
    # ==========================================================================
    html.Div([
        html.H2("Custom Rounded Cells"),
        html.P(
            "Use cellStyle='rounded' for cells with gaps, rounded corners, and value labels. "
            "Customize gap, borderRadius, fontSize, and text color.",
            style=description_style
        ),
        Heatmap(
            id='rounded-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days, 'label': 'Day of Week'},
            yAxis={'data': weeks, 'label': 'Week'},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#e8f5e9', '#2e7d32'],
            },
            cellStyle='rounded',
            highlightScope={'highlight': 'item'},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Simple rounded cells with default settings
Heatmap(
    data=activity_data,
    xAxis={'data': days, 'label': 'Day of Week'},
    yAxis={'data': weeks, 'label': 'Week'},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 10,
        'colors': ['#e8f5e9', '#2e7d32'],
    },
    cellStyle='rounded',  # Enable rounded corners with gap
    highlightScope={'highlight': 'item'},  # Highlight on hover
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Custom Cell Configuration
    # ==========================================================================
    html.Div([
        html.H2("Custom Cell Configuration"),
        html.P(
            "Fine-tune cell appearance with custom gap, border radius, font size, and colors.",
            style=description_style
        ),
        Heatmap(
            id='custom-cell-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days},
            yAxis={'data': weeks},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#fce4ec', '#c2185b'],
            },
            cellStyle={
                'gap': 6,
                'borderRadius': 8,
                'showValue': True,
                'fontSize': 14,
                'fontWeight': 600,
                'textColor': '#ffffff',
            },
            highlightScope={'highlight': 'item'},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Detailed cell customization
Heatmap(
    data=activity_data,
    xAxis={'data': days},
    yAxis={'data': weeks},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 10,
        'colors': ['#fce4ec', '#c2185b'],  # Pink gradient
    },
    cellStyle={
        'gap': 6,              # Space between cells
        'borderRadius': 8,     # Rounded corners
        'showValue': True,     # Display value in cell
        'fontSize': 14,        # Text size
        'fontWeight': 600,     # Text weight
        'textColor': '#ffffff', # Text color
    },
    highlightScope={'highlight': 'item'},
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Piecewise Color Scale
    # ==========================================================================
    html.Div([
        html.H2("Piecewise Color Scale"),
        html.P(
            "Use a piecewise color scale for discrete color bands. "
            "Useful for categorizing values into ranges (e.g., Low, Medium, High).",
            style=description_style
        ),
        Heatmap(
            id='piecewise-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days},
            yAxis={'data': weeks},
            height=300,
            colorScale={
                'type': 'piecewise',
                'thresholds': [3, 5, 7],
                'colors': ['#e8f5e9', '#81c784', '#43a047', '#1b5e20'],  # Light to dark green
            },
        ),
        html.Div([
            html.Span("Legend: ", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Span("0-2 (Low) ", style={'backgroundColor': '#e8f5e9', 'padding': '2px 8px', 'marginRight': '5px'}),
            html.Span("3-4 ", style={'backgroundColor': '#81c784', 'padding': '2px 8px', 'marginRight': '5px'}),
            html.Span("5-6 ", style={'backgroundColor': '#43a047', 'padding': '2px 8px', 'marginRight': '5px', 'color': 'white'}),
            html.Span("7+ (High)", style={'backgroundColor': '#1b5e20', 'padding': '2px 8px', 'color': 'white'}),
        ], style={'marginTop': '15px'}),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""Heatmap(
    data=activity_data,
    xAxis={'data': days},
    yAxis={'data': weeks},
    height=300,
    colorScale={
        'type': 'piecewise',
        'thresholds': [3, 5, 7],  # Creates 4 color bands
        'colors': ['#e8f5e9', '#81c784', '#43a047', '#1b5e20'],  # Need n+1 colors
    },
)

# Thresholds [3, 5, 7] create bands:
# - 0-2: color[0]
# - 3-4: color[1]
# - 5-6: color[2]
# - 7+:  color[3]
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Interactive Heatmap
    # ==========================================================================
    html.Div([
        html.H2("Interactive Heatmap"),
        html.P(
            "Click on cells to see their data. "
            "The heatmap reports click events with x, y coordinates and value.",
            style=description_style
        ),
        Heatmap(
            id='interactive-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days, 'label': 'Day'},
            yAxis={'data': weeks, 'label': 'Week'},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#fff3e0', '#ff9800'],
            },
        ),
        html.Div([
            html.H4("Click Data:", style={'marginTop': '20px'}),
            html.Pre(
                id='heatmap-click-output',
                children="Click on a cell to see its data",
                style=code_style
            ),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""Heatmap(
    id='interactive-heatmap',
    data=activity_data,
    xAxis={'data': days, 'label': 'Day'},
    yAxis={'data': weeks, 'label': 'Week'},
    height=300,
    colorScale={...},
)

@callback(
    Output('heatmap-click-output', 'children'),
    Input('interactive-heatmap', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a cell to see its data"
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Color Scale Reference
    # ==========================================================================
    html.Div([
        html.H2("Color Scale Reference"),
        html.P(
            "Quick reference for configuring color scales.",
            style=description_style
        ),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    html.Th("Configuration", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    html.Th("Use Case", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                ]),
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("Continuous", style={'padding': '8px', 'verticalAlign': 'top'}),
                    html.Td(html.Pre("{'type': 'continuous', 'min': 0, 'max': 100, 'colors': ['#low', '#high']}", style={'margin': 0, 'fontSize': '11px'}), style={'padding': '8px'}),
                    html.Td("Smooth gradient for numerical data", style={'padding': '8px'}),
                ]),
                html.Tr([
                    html.Td("Diverging", style={'padding': '8px', 'verticalAlign': 'top'}),
                    html.Td(html.Pre("{'type': 'continuous', 'min': -1, 'max': 1, 'colors': ['#neg', '#mid', '#pos']}", style={'margin': 0, 'fontSize': '11px'}), style={'padding': '8px'}),
                    html.Td("Correlations, deviations from center", style={'padding': '8px'}),
                ]),
                html.Tr([
                    html.Td("Piecewise", style={'padding': '8px', 'verticalAlign': 'top'}),
                    html.Td(html.Pre("{'type': 'piecewise', 'thresholds': [a, b, c], 'colors': ['#1', '#2', '#3', '#4']}", style={'margin': 0, 'fontSize': '11px'}), style={'padding': '8px'}),
                    html.Td("Categorical ranges (Low/Med/High)", style={'padding': '8px'}),
                ]),
            ]),
        ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
    ], style=section_style),
])


@callback(
    Output('heatmap-click-output', 'children'),
    Input('interactive-heatmap', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    """Display clicked cell data from heatmap."""
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a cell to see its data"
