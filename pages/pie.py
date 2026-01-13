"""
Pie Chart - Circular Data Visualization

This page demonstrates the PieChart component for creating pie and donut charts
that express portions of a whole using arcs within a circle.
This is a free feature - no MUI X Pro license required.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/pie', name='Pie Chart')

from dash_mui_charts import PieChart

# Sample data - Budget allocation
budget_data = [
    {'id': 0, 'value': 35, 'label': 'Marketing'},
    {'id': 1, 'value': 25, 'label': 'Engineering'},
    {'id': 2, 'value': 20, 'label': 'Sales'},
    {'id': 3, 'value': 15, 'label': 'Support'},
    {'id': 4, 'value': 5, 'label': 'Other'},
]

# Browser market share data
browser_data = [
    {'id': 0, 'value': 63.5, 'label': 'Chrome'},
    {'id': 1, 'value': 19.2, 'label': 'Safari'},
    {'id': 2, 'value': 4.3, 'label': 'Firefox'},
    {'id': 3, 'value': 3.9, 'label': 'Edge'},
    {'id': 4, 'value': 9.1, 'label': 'Other'},
]

# Task completion data (for half-pie gauge)
task_data = [
    {'id': 0, 'value': 72, 'label': 'Completed'},
    {'id': 1, 'value': 28, 'label': 'Remaining'},
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

layout = html.Div([
    html.H1("Pie Chart"),
    html.P(
        "Pie charts express portions of a whole using arcs within a circle. "
        "Create standard pies, donuts, or gauge-style visualizations with customizable styling.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # Section 1: Basic Pie Chart
    html.Div([
        html.H2("Basic Pie Chart"),
        html.P(
            "A simple pie chart showing budget allocation by department. "
            "Hover over slices to see values, click to interact.",
            style=description_style
        ),
        html.Div([
            PieChart(
                id='basic-pie',
                data=budget_data,
                height=300,
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Pre(
            '''PieChart(
    data=[
        {'id': 0, 'value': 35, 'label': 'Marketing'},
        {'id': 1, 'value': 25, 'label': 'Engineering'},
        {'id': 2, 'value': 20, 'label': 'Sales'},
        {'id': 3, 'value': 15, 'label': 'Support'},
        {'id': 4, 'value': 5, 'label': 'Other'},
    ],
    height=300,
)''',
            style=code_style
        ),
    ], style=section_style),

    # Section 2: Donut Chart
    html.Div([
        html.H2("Donut Chart"),
        html.P(
            "Set innerRadius to create a donut chart. The hollow center can "
            "be used for additional information or just aesthetic appeal.",
            style=description_style
        ),
        html.Div([
            PieChart(
                id='donut-pie',
                data=browser_data,
                innerRadius=60,
                height=300,
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Pre(
            '''PieChart(
    data=browser_data,
    innerRadius=60,  # Creates the donut hole
    height=300,
)''',
            style=code_style
        ),
    ], style=section_style),

    # Section 3: Pie with Arc Labels
    html.Div([
        html.H2("Arc Labels"),
        html.P(
            "Display values directly on the arcs. Use arcLabelMinAngle to hide "
            "labels on small slices that would be too crowded.",
            style=description_style
        ),
        html.Div([
            PieChart(
                id='labeled-pie',
                data=budget_data,
                arcLabel='value',
                arcLabelMinAngle=30,
                height=300,
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Pre(
            '''PieChart(
    data=budget_data,
    arcLabel='value',      # Options: 'value', 'label', 'formattedValue'
    arcLabelMinAngle=30,   # Hide labels on slices < 30 degrees
    height=300,
)''',
            style=code_style
        ),
    ], style=section_style),

    # Section 4: Styled Pie
    html.Div([
        html.H2("Styled Pie"),
        html.P(
            "Customize the appearance with padding between slices, rounded corners, "
            "and custom color palettes.",
            style=description_style
        ),
        html.Div([
            PieChart(
                id='styled-pie',
                data=budget_data,
                paddingAngle=3,
                cornerRadius=8,
                colors=['#1976d2', '#dc004e', '#ff9800', '#4caf50', '#9c27b0'],
                height=300,
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Pre(
            '''PieChart(
    data=budget_data,
    paddingAngle=3,     # Gap between slices in degrees
    cornerRadius=8,     # Rounded corners on slices
    colors=['#1976d2', '#dc004e', '#ff9800', '#4caf50', '#9c27b0'],
    height=300,
)''',
            style=code_style
        ),
    ], style=section_style),

    # Section 5: Half Pie / Gauge
    html.Div([
        html.H2("Half Pie / Gauge"),
        html.P(
            "Create gauge-style visualizations by adjusting startAngle and endAngle. "
            "Perfect for progress indicators or completion metrics.",
            style=description_style
        ),
        html.Div([
            PieChart(
                id='gauge-pie',
                data=task_data,
                startAngle=-90,
                endAngle=90,
                innerRadius=50,
                colors=['#4caf50', '#e0e0e0'],
                height=200,
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Pre(
            '''PieChart(
    data=[
        {'id': 0, 'value': 72, 'label': 'Completed'},
        {'id': 1, 'value': 28, 'label': 'Remaining'},
    ],
    startAngle=-90,    # Start at 12 o'clock
    endAngle=90,       # End at 6 o'clock (half circle)
    innerRadius=50,    # Donut style
    colors=['#4caf50', '#e0e0e0'],
    height=200,
)''',
            style=code_style
        ),
    ], style=section_style),

    # Section 6: Interactive Example
    html.Div([
        html.H2("Interactive Example"),
        html.P(
            "Click on slices to see detailed click data. Hover to highlight slices "
            "and see the highlight state update in real-time.",
            style=description_style
        ),
        html.Div([
            html.Div([
                PieChart(
                    id='interactive-pie',
                    data=budget_data,
                    innerRadius=40,
                    paddingAngle=2,
                    cornerRadius=4,
                    highlightScope={'highlight': 'item', 'fade': 'global'},
                    height=300,
                ),
            ], style={'flex': '1'}),
            html.Div([
                html.Div([
                    html.H4("Click Data", style={'marginTop': 0, 'marginBottom': '10px'}),
                    html.Pre(
                        id='pie-click-data',
                        children='Click on a slice',
                        style={
                            'backgroundColor': '#e3f2fd',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'minHeight': '80px',
                            'fontSize': '13px',
                            'margin': 0,
                        }
                    ),
                ], style={'marginBottom': '20px'}),
                html.Div([
                    html.H4("Highlighted Item", style={'marginTop': 0, 'marginBottom': '10px'}),
                    html.Pre(
                        id='pie-highlight-data',
                        children='Hover over a slice',
                        style={
                            'backgroundColor': '#e8f5e9',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'minHeight': '80px',
                            'fontSize': '13px',
                            'margin': 0,
                        }
                    ),
                ]),
            ], style={'flex': '1', 'paddingLeft': '30px'}),
        ], style={'display': 'flex', 'alignItems': 'flex-start'}),
        html.Pre(
            '''PieChart(
    id='interactive-pie',
    data=budget_data,
    innerRadius=40,
    paddingAngle=2,
    cornerRadius=4,
    highlightScope={'highlight': 'item', 'fade': 'global'},
    height=300,
)

# Callbacks receive clickData and highlightedItem
@callback(
    Output('pie-click-data', 'children'),
    Input('interactive-pie', 'clickData')
)
def display_click(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return 'Click on a slice'
''',
            style=code_style
        ),
    ], style=section_style),

], style={'maxWidth': '900px', 'margin': '0 auto', 'padding': '20px'})


@callback(
    Output('pie-click-data', 'children'),
    Input('interactive-pie', 'clickData'),
    prevent_initial_call=True
)
def display_click_data(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return 'Click on a slice'


@callback(
    Output('pie-highlight-data', 'children'),
    Input('interactive-pie', 'highlightedItem'),
    prevent_initial_call=True
)
def display_highlight_data(highlighted_item):
    if highlighted_item:
        return json.dumps(highlighted_item, indent=2)
    return 'Hover over a slice'
