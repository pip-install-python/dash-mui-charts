"""
Highlighting Sync - Synchronized highlights across multiple charts
"""

import os
import json
import dash
from dash import html, callback, Input, Output, ctx

dash.register_page(__name__, path='/highlighting-sync', name='Highlighting Sync')

from dash_mui_charts import LineChart, PieChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data - Product categories across months
categories = ['Electronics', 'Clothing', 'Food', 'Home', 'Sports']
category_colors = ['#1976d2', '#4caf50', '#ff9800', '#9c27b0', '#f44336']

# Monthly data for each category (indexed to match)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
electronics_data = [150, 165, 180, 175, 190, 200]
clothing_data = [80, 95, 110, 105, 120, 130]
food_data = [200, 210, 205, 220, 215, 230]
home_data = [60, 75, 85, 80, 90, 95]
sports_data = [40, 55, 70, 65, 80, 90]

# Pie chart data using totals
pie_data = [
    {'id': 'electronics', 'value': sum(electronics_data), 'label': 'Electronics', 'color': '#1976d2'},
    {'id': 'clothing', 'value': sum(clothing_data), 'label': 'Clothing', 'color': '#4caf50'},
    {'id': 'food', 'value': sum(food_data), 'label': 'Food', 'color': '#ff9800'},
    {'id': 'home', 'value': sum(home_data), 'label': 'Home', 'color': '#9c27b0'},
    {'id': 'sports', 'value': sum(sports_data), 'label': 'Sports', 'color': '#f44336'},
]

# Revenue and Expenses data for Two LineCharts sync demo
revenue_data = [100, 120, 140, 130, 150, 170]
expenses_data = [80, 85, 95, 90, 100, 110]

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
chart_container_style = {
    'display': 'flex',
    'gap': '20px',
    'flexWrap': 'wrap',
    'alignItems': 'flex-start',
}

# Custom tooltip base style (hidden by default)
custom_tooltip_style = {
    'position': 'absolute',
    'backgroundColor': 'var(--mantine-color-body)',
    'border': '1px solid var(--mantine-color-default-border)',
    'borderRadius': '4px',
    'padding': '8px 12px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
    'pointerEvents': 'none',
    'zIndex': 1000,
    'transform': 'translateX(-50%)',
    'display': 'none',
    'whiteSpace': 'nowrap',
    'fontSize': '13px',
    'color': 'var(--mantine-color-text)',
}

layout = html.Div([
    html.H1("Synchronized Highlighting"),
    html.P(
        "This page demonstrates synchronized highlights across multiple charts. "
        "Hovering over one chart highlights the corresponding data in other charts.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '20px'}
    ),

    # ==========================================================================
    # LineChart + PieChart Sync
    # ==========================================================================
    html.Div([
        html.H2("LineChart + PieChart Synchronization"),
        html.P(
            "Hover over either chart to see the same category highlighted in both. "
            "The LineChart and PieChart share highlightedItem state through a callback.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.H4("Sales Trend by Category", style={'marginBottom': '10px'}),
                LineChart(
                    id='sync-line-chart',
                    licenseKey=MUI_LICENSE_KEY,
                    height=300,
                    width=500,
                    series=[
                        {
                            'id': 'electronics',
                            'data': electronics_data,
                            'label': 'Electronics',
                            'color': '#1976d2',
                            'showMark': True,
                            'highlightScope': {'highlight': 'series', 'fade': 'global'},
                        },
                        {
                            'id': 'clothing',
                            'data': clothing_data,
                            'label': 'Clothing',
                            'color': '#4caf50',
                            'showMark': True,
                            'highlightScope': {'highlight': 'series', 'fade': 'global'},
                        },
                        {
                            'id': 'food',
                            'data': food_data,
                            'label': 'Food',
                            'color': '#ff9800',
                            'showMark': True,
                            'highlightScope': {'highlight': 'series', 'fade': 'global'},
                        },
                        {
                            'id': 'home',
                            'data': home_data,
                            'label': 'Home',
                            'color': '#9c27b0',
                            'showMark': True,
                            'highlightScope': {'highlight': 'series', 'fade': 'global'},
                        },
                        {
                            'id': 'sports',
                            'data': sports_data,
                            'label': 'Sports',
                            'color': '#f44336',
                            'showMark': True,
                            'highlightScope': {'highlight': 'series', 'fade': 'global'},
                        },
                    ],
                    xAxis=[{
                        'id': 'months',
                        'data': months,
                        'scaleType': 'point',
                    }],
                    grid={'horizontal': True},
                    tooltip={'trigger': 'item'},
                ),
            ], style={'flex': '1', 'minWidth': '400px'}),
            html.Div([
                html.H4("Total Sales by Category", style={'marginBottom': '10px'}),
                PieChart(
                    id='sync-pie-chart',
                    data=pie_data,
                    height=300,
                    width=350,
                    innerRadius=60,
                    highlightScope={'highlight': 'item', 'fade': 'global'},
                ),
            ], style={'flex': '0 0 auto'}),
        ], style=chart_container_style),
        html.H4("Shared Highlight State:", style={'marginTop': '20px'}),
        html.Pre(
            id='sync-highlight-output',
            children="Hover over either chart to see synchronized highlighting",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Both charts use the same series IDs for categories
LineChart(
    id='sync-line-chart',
    series=[
        {'id': 'electronics', 'data': electronics_data, 'label': 'Electronics'},
        {'id': 'clothing', 'data': clothing_data, 'label': 'Clothing'},
        # ...
    ],
)

PieChart(
    id='sync-pie-chart',
    data=[
        {'id': 'electronics', 'value': 1060, 'label': 'Electronics'},
        {'id': 'clothing', 'value': 640, 'label': 'Clothing'},
        # ...
    ],
)

@callback(
    Output('sync-line-chart', 'highlightedItem'),
    Output('sync-pie-chart', 'highlightedItem'),
    Input('sync-line-chart', 'highlightedItem'),
    Input('sync-pie-chart', 'highlightedItem'),
)
def sync_highlights(line_highlight, pie_highlight):
    triggered = ctx.triggered_id
    if triggered == 'sync-line-chart' and line_highlight:
        # Map line series to pie (pie uses 'auto-generated-id-0' as default series)
        return line_highlight, {'seriesId': 'auto-generated-id-0', 'dataIndex': get_index(line_highlight['seriesId'])}
    elif triggered == 'sync-pie-chart' and pie_highlight:
        return {'seriesId': categories[pie_highlight['dataIndex']]}, pie_highlight
    return None, None
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Two LineCharts Sync
    # ==========================================================================
    html.Div([
        html.H2("Two LineCharts Synchronization"),
        html.P(
            "Synchronize highlights between two LineCharts showing related data. "
            "Hovering over one chart highlights the corresponding month in both charts, "
            "with tooltips appearing simultaneously on both.",
            style=description_style
        ),
        html.Div([
            # Chart A wrapper with custom tooltip
            html.Div([
                html.H4("Revenue", style={'marginBottom': '10px', 'color': '#1976d2'}),
                html.Div([
                    LineChart(
                        id='sync-line-a',
                        licenseKey=MUI_LICENSE_KEY,
                        height=280,
                        series=[
                            {
                                'id': 'revenue',
                                'data': [100, 120, 140, 130, 150, 170],
                                'label': 'Revenue ($K)',
                                'color': '#1976d2',
                                'area': True,
                                'showMark': True,
                                'highlightScope': {'highlight': 'item', 'fade': 'global'},
                            },
                        ],
                        xAxis=[{
                            'id': 'x-axis-a',
                            'data': months,
                            'scaleType': 'point',
                            'label': 'Month',
                        }],
                        yAxis=[{
                            'label': 'Revenue ($K)',
                            'min': 0,
                            'max': 200,
                        }],
                        grid={'horizontal': True},
                        axisHighlight={'x': 'band', 'y': 'none'},
                        tooltip={'trigger': 'none'},  # Disable MUI tooltip
                    ),
                    # Custom tooltip overlay for Chart A
                    html.Div(
                        id='custom-tooltip-a',
                        style=custom_tooltip_style,
                    ),
                ], style={'position': 'relative'}),
            ], id='chart-wrapper-a', style={'flex': '1', 'minWidth': '350px'}),
            # Chart B wrapper with custom tooltip
            html.Div([
                html.H4("Expenses", style={'marginBottom': '10px', 'color': '#f44336'}),
                html.Div([
                    LineChart(
                        id='sync-line-b',
                        licenseKey=MUI_LICENSE_KEY,
                        height=280,
                        series=[
                            {
                                'id': 'expenses',
                                'data': [80, 85, 95, 90, 100, 110],
                                'label': 'Expenses ($K)',
                                'color': '#f44336',
                                'area': True,
                                'showMark': True,
                                'highlightScope': {'highlight': 'item', 'fade': 'global'},
                            },
                        ],
                        xAxis=[{
                            'id': 'x-axis-b',
                            'data': months,
                            'scaleType': 'point',
                            'label': 'Month',
                        }],
                        yAxis=[{
                            'label': 'Expenses ($K)',
                            'min': 0,
                            'max': 200,
                        }],
                        grid={'horizontal': True},
                        axisHighlight={'x': 'band', 'y': 'none'},
                        tooltip={'trigger': 'none'},  # Disable MUI tooltip
                    ),
                    # Custom tooltip overlay for Chart B
                    html.Div(
                        id='custom-tooltip-b',
                        style=custom_tooltip_style,
                    ),
                ], style={'position': 'relative'}),
            ], id='chart-wrapper-b', style={'flex': '1', 'minWidth': '350px'}),
        ], style=chart_container_style),

        # Profit summary card
        html.Div([
            html.Div([
                html.H4("Profit Summary", style={'margin': '0 0 10px 0'}),
                html.Div(id='profit-display', children=[
                    html.P("Hover over either chart to see monthly profit calculation",
                           style={'color': '#666', 'margin': 0})
                ]),
            ], style={
                'backgroundColor': '#f5f5f5',
                'padding': '15px 20px',
                'borderRadius': '8px',
                'marginTop': '15px',
            }),
        ]),

        html.H4("Synchronized State:", style={'marginTop': '20px'}),
        html.Pre(
            id='sync-axis-output',
            children="Hover over either chart to see synchronized data",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Charts with MUI tooltips disabled, using custom tooltip overlays
LineChart(
    id='sync-line-a',
    series=[{
        'id': 'revenue',
        'data': revenue_data,
        'showMark': True,
        'highlightScope': {'highlight': 'item', 'fade': 'global'},
    }],
    tooltip={'trigger': 'none'},  # Disable MUI tooltip
)

# Custom tooltip div positioned over chart
html.Div(id='custom-tooltip-a', style={'position': 'absolute', ...})

# Synchronize highlights AND custom tooltips between two charts
@callback(
    Output('sync-line-a', 'highlightedItem'),
    Output('sync-line-b', 'highlightedItem'),
    Output('custom-tooltip-a', 'style'),
    Output('custom-tooltip-a', 'children'),
    Output('custom-tooltip-b', 'style'),
    Output('custom-tooltip-b', 'children'),
    Input('sync-line-a', 'highlightedItem'),
    Input('sync-line-b', 'highlightedItem'),
)
def sync_charts_with_custom_tooltips(highlight_a, highlight_b):
    # Determine which chart triggered
    triggered = ctx.triggered_id
    # Get dataIndex from the triggered chart
    # Calculate x position based on chart margins and data index
    # Return highlight items for BOTH charts + visible tooltips for BOTH
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Use Cases
    # ==========================================================================
    html.Div([
        html.H2("Use Cases for Synchronized Highlighting"),
        html.Div([
            html.Div([
                html.H4("Dashboard Coordination"),
                html.P(
                    "In a dashboard with multiple charts showing different aspects of the same data, "
                    "synchronized highlighting helps users understand relationships across visualizations.",
                    style={'color': '#666'}
                ),
            ], style={'flex': '1', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px', 'margin': '5px'}),
            html.Div([
                html.H4("Comparison Views"),
                html.P(
                    "When comparing two datasets side-by-side (like revenue vs expenses, or year-over-year), "
                    "synchronized axis highlights make it easy to compare values at the same point in time.",
                    style={'color': '#666'}
                ),
            ], style={'flex': '1', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px', 'margin': '5px'}),
            html.Div([
                html.H4("Drill-down Navigation"),
                html.P(
                    "Highlight a category in an overview chart (like a pie chart) to show corresponding "
                    "detail in a line chart. This pattern enables intuitive data exploration.",
                    style={'color': '#666'}
                ),
            ], style={'flex': '1', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px', 'margin': '5px'}),
        ], style={'display': 'flex', 'gap': '10px', 'flexWrap': 'wrap'}),
    ], style=section_style),
])


# ==========================================================================
# Callbacks
# ==========================================================================

# Map category names to indices for pie chart
CATEGORY_TO_INDEX = {cat.lower(): i for i, cat in enumerate(categories)}

@callback(
    Output('sync-line-chart', 'highlightedItem'),
    Output('sync-pie-chart', 'highlightedItem'),
    Output('sync-highlight-output', 'children'),
    Input('sync-line-chart', 'highlightedItem'),
    Input('sync-pie-chart', 'highlightedItem'),
    prevent_initial_call=True
)
def sync_line_pie_highlights(line_highlight, pie_highlight):
    """Synchronize highlights between LineChart and PieChart."""
    triggered = ctx.triggered_id

    if triggered == 'sync-line-chart':
        if line_highlight and line_highlight.get('seriesId'):
            # Map line series ID to pie data index
            series_id = line_highlight['seriesId']
            pie_index = CATEGORY_TO_INDEX.get(series_id)
            if pie_index is not None:
                # PieChart uses 'auto-generated-id-0' as the default series ID
                pie_item = {'seriesId': 'auto-generated-id-0', 'dataIndex': pie_index}
                output = {
                    'source': 'LineChart',
                    'lineHighlight': line_highlight,
                    'pieHighlight': pie_item,
                }
                # Use no_update for the source chart to avoid echo
                return dash.no_update, pie_item, json.dumps(output, indent=2)
        return dash.no_update, None, "null (no highlight)"

    elif triggered == 'sync-pie-chart':
        if pie_highlight and pie_highlight.get('dataIndex') is not None:
            # Map pie data index back to line series ID
            data_index = pie_highlight['dataIndex']
            if 0 <= data_index < len(categories):
                series_id = categories[data_index].lower()
                line_item = {'seriesId': series_id}
                output = {
                    'source': 'PieChart',
                    'pieHighlight': pie_highlight,
                    'lineHighlight': line_item,
                }
                # Use no_update for the source chart to avoid echo
                return line_item, dash.no_update, json.dumps(output, indent=2)
        return None, dash.no_update, "null (no highlight)"

    return dash.no_update, dash.no_update, "null (no highlight)"


@callback(
    Output('sync-line-a', 'highlightedItem'),
    Output('sync-line-b', 'highlightedItem'),
    Output('custom-tooltip-a', 'style'),
    Output('custom-tooltip-a', 'children'),
    Output('custom-tooltip-b', 'style'),
    Output('custom-tooltip-b', 'children'),
    Output('sync-axis-output', 'children'),
    Output('profit-display', 'children'),
    Input('sync-line-a', 'highlightedItem'),
    Input('sync-line-b', 'highlightedItem'),
    prevent_initial_call=True
)
def sync_dual_line_with_custom_tooltips(highlight_a, highlight_b):
    """Synchronize highlights and custom tooltips between two LineCharts."""
    triggered = ctx.triggered_id

    # Chart layout constants (MUI X Charts defaults)
    LEFT_MARGIN = 80
    RIGHT_MARGIN = 20
    TOP_MARGIN = 20
    NUM_POINTS = len(months)

    def get_tooltip_style_for_index(data_index):
        """Get tooltip style positioned at the given data index using calc()."""
        if data_index is None:
            return {**custom_tooltip_style, 'display': 'none'}

        # Calculate position using percentage of plot area
        # Plot area starts at LEFT_MARGIN and ends at (100% - RIGHT_MARGIN)
        # For point scale with N points, point i is at position i/(N-1) within plot area
        if NUM_POINTS > 1:
            position_fraction = data_index / (NUM_POINTS - 1)
        else:
            position_fraction = 0.5

        return {
            **custom_tooltip_style,
            'display': 'block',
            # Position using calc: left_margin + fraction * (available_width)
            # available_width = 100% - left_margin - right_margin
            'left': f'calc({LEFT_MARGIN}px + {position_fraction} * (100% - {LEFT_MARGIN + RIGHT_MARGIN}px))',
            'top': f'{TOP_MARGIN + 15}px',
        }

    def get_tooltip_content_a(data_index):
        """Generate tooltip content for Revenue chart."""
        if data_index is None or data_index < 0 or data_index >= len(months):
            return ""
        month = months[data_index]
        revenue = revenue_data[data_index]
        return html.Div([
            html.Div(month, style={'fontWeight': 'bold', 'marginBottom': '4px', 'color': 'var(--mantine-color-text)'}),
            html.Div([
                html.Span("Revenue: ", style={'color': '#666'}),
                html.Span(f"${revenue}K", style={'color': '#1976d2', 'fontWeight': 'bold'}),
            ]),
        ])

    def get_tooltip_content_b(data_index):
        """Generate tooltip content for Expenses chart."""
        if data_index is None or data_index < 0 or data_index >= len(months):
            return ""
        month = months[data_index]
        expenses = expenses_data[data_index]
        return html.Div([
            html.Div(month, style={'fontWeight': 'bold', 'marginBottom': '4px', 'color': 'var(--mantine-color-text)'}),
            html.Div([
                html.Span("Expenses: ", style={'color': '#666'}),
                html.Span(f"${expenses}K", style={'color': '#f44336', 'fontWeight': 'bold'}),
            ]),
        ])

    def get_profit_display(data_index):
        """Generate profit display for a given data index."""
        if data_index is None or data_index < 0 or data_index >= len(months):
            return html.P("Hover over either chart to see monthly profit calculation",
                         style={'color': '#666', 'margin': 0})

        month = months[data_index]
        revenue = revenue_data[data_index]
        expenses = expenses_data[data_index]
        profit = revenue - expenses
        margin = (profit / revenue * 100) if revenue > 0 else 0

        profit_color = '#4caf50' if profit >= 0 else '#f44336'

        return html.Div([
            html.Div([
                html.Span(f"{month}", style={'fontWeight': 'bold', 'fontSize': '18px'}),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Div([
                    html.Span("Revenue: ", style={'color': '#666'}),
                    html.Span(f"${revenue}K", style={'color': '#1976d2', 'fontWeight': 'bold'}),
                ], style={'display': 'inline-block', 'marginRight': '20px'}),
                html.Div([
                    html.Span("Expenses: ", style={'color': '#666'}),
                    html.Span(f"${expenses}K", style={'color': '#f44336', 'fontWeight': 'bold'}),
                ], style={'display': 'inline-block', 'marginRight': '20px'}),
                html.Div([
                    html.Span("Profit: ", style={'color': '#666'}),
                    html.Span(f"${profit}K", style={'color': profit_color, 'fontWeight': 'bold'}),
                    html.Span(f" ({margin:.1f}% margin)", style={'color': '#666', 'fontSize': '12px'}),
                ], style={'display': 'inline-block'}),
            ]),
        ])

    # Hidden tooltip style
    hidden_tooltip_style = {**custom_tooltip_style, 'display': 'none'}
    default_profit = html.P("Hover over either chart to see monthly profit calculation",
                            style={'color': '#666', 'margin': 0})

    # Determine which chart triggered and get data index
    data_index = None
    source_chart = None

    if triggered == 'sync-line-a' and highlight_a and highlight_a.get('dataIndex') is not None:
        data_index = highlight_a['dataIndex']
        source_chart = 'A'
    elif triggered == 'sync-line-b' and highlight_b and highlight_b.get('dataIndex') is not None:
        data_index = highlight_b['dataIndex']
        source_chart = 'B'

    # If no valid highlight, hide tooltips and clear highlights
    if data_index is None:
        return (
            None,  # highlight_a
            None,  # highlight_b
            hidden_tooltip_style,  # tooltip_a style
            "",  # tooltip_a content
            hidden_tooltip_style,  # tooltip_b style
            "",  # tooltip_b content
            "null (no highlight)",  # sync output
            default_profit,  # profit display
        )

    # Valid highlight - sync both charts and show both tooltips
    highlight_for_a = {'seriesId': 'revenue', 'dataIndex': data_index}
    highlight_for_b = {'seriesId': 'expenses', 'dataIndex': data_index}

    tooltip_style = get_tooltip_style_for_index(data_index)
    tooltip_content_a = get_tooltip_content_a(data_index)
    tooltip_content_b = get_tooltip_content_b(data_index)
    profit_display = get_profit_display(data_index)

    output = {
        'source': f'Chart {source_chart} ({"Revenue" if source_chart == "A" else "Expenses"})',
        'dataIndex': data_index,
        'month': months[data_index] if 0 <= data_index < len(months) else 'unknown',
        'revenue': revenue_data[data_index] if 0 <= data_index < len(revenue_data) else None,
        'expenses': expenses_data[data_index] if 0 <= data_index < len(expenses_data) else None,
    }

    # Use no_update for the source chart's highlight to avoid feedback loop
    if source_chart == 'A':
        return (
            dash.no_update,  # Don't update source chart's highlight
            highlight_for_b,  # Sync to chart B
            tooltip_style,
            tooltip_content_a,
            tooltip_style,
            tooltip_content_b,
            json.dumps(output, indent=2),
            profit_display,
        )
    else:
        return (
            highlight_for_a,  # Sync to chart A
            dash.no_update,  # Don't update source chart's highlight
            tooltip_style,
            tooltip_content_a,
            tooltip_style,
            tooltip_content_b,
            json.dumps(output, indent=2),
            profit_display,
        )
