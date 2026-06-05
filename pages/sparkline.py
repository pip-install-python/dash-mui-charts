"""
SparklineChart - Compact Inline Charts

This page demonstrates the SparklineChart component for creating
compact, inline visualizations perfect for dashboards and tables.
This is a Community feature - no license key required.
"""

import json
import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, dcc

dash.register_page(__name__, path='/sparkline', name='Sparkline')

from dash_mui_charts import SparklineChart

# Sample data
sales_trend = [10, 15, 8, 22, 18, 25, 30, 28, 35, 40, 38, 45]
stock_prices = [142.5, 145.2, 143.8, 148.9, 151.2, 149.5, 155.8, 158.2, 154.3, 160.1]
temperature_week = [72, 75, 78, 82, 79, 74, 71]
server_load = [45, 52, 48, 65, 72, 58, 42, 55, 61, 48]
error_rates = [2, 5, 3, 8, 4, 2, 1, 3, 2, 4]

# Weekly downloads data (like npm)
weekly_downloads = [
    125430, 142350, 138200, 156780, 162340, 158900, 171200,
    168500, 175600, 182300, 178900, 195400
]
weeks = [
    'Dec 1-7', 'Dec 8-14', 'Dec 15-21', 'Dec 22-28',
    'Dec 29-Jan 4', 'Jan 5-11', 'Jan 12-18',
    'Jan 19-25', 'Jan 26-Feb 1', 'Feb 2-8', 'Feb 9-15', 'Feb 16-22'
]

# Multiple metrics for synced hover
revenue_data = [42, 45, 48, 52, 49, 55, 58, 62, 60, 65]
users_data = [1200, 1350, 1420, 1580, 1520, 1680, 1750, 1890, 1820, 1950]
sessions_data = [3500, 3800, 4100, 4500, 4200, 4800, 5100, 5400, 5200, 5600]
metric_labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10']

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

# KPI Card style
kpi_card_style = {
    'backgroundColor': 'white',
    'borderRadius': '8px',
    'padding': '20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'width': '280px',
}

layout = html.Div([
    html.H1("SparklineChart"),
    html.P(
        "Sparklines are compact, inline charts that show data trends without axes or labels. "
        "Perfect for dashboards, KPI cards, and tables. This is a Community feature - no license required.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # ==========================================================================
    # Basic Line Sparkline
    # ==========================================================================
    html.Div([
        html.H2("Basic Line Sparkline"),
        html.P(
            "The simplest sparkline - just pass an array of numbers. "
            "Great for showing trends at a glance.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Span("Sales Trend: ", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                SparklineChart(
                    data=sales_trend,
                    width=150,
                    height=30,
                    color='#1976d2',
                ),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'}),
            html.Div([
                html.Span("Stock Price: ", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                SparklineChart(
                    data=stock_prices,
                    width=150,
                    height=30,
                    color='#4caf50',
                ),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""SparklineChart(
    data=[10, 15, 8, 22, 18, 25, 30, 28, 35, 40],
    width=150,
    height=30,
    color='#1976d2',
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # NPM-Style Downloads Sparkline
    # ==========================================================================
    html.Div([
        html.H2("NPM-Style Downloads Sparkline"),
        html.P(
            "A rich interactive sparkline like npm's package download chart. "
            "Hover over the chart to see weekly download counts update in real-time.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Span("📦 ", style={'marginRight': '5px'}),
                    html.Span(
                        id='npm-week-label',
                        children="Weekly Downloads",
                        style={'color': '#666', 'fontSize': '14px'}
                    ),
                ], style={'marginBottom': '8px'}),
                html.Div([
                    html.Span(
                        id='npm-download-count',
                        children=f"{weekly_downloads[-1]:,}",
                        style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#333'}
                    ),
                    html.Div([
                        SparklineChart(
                            id='npm-sparkline',
                            data=weekly_downloads,
                            width=200,
                            height=45,
                            color='rgb(137, 86, 255)',
                            area=True,
                            showHighlight=True,
                            baseline='min',
                            margin={'top': 5, 'right': 0, 'bottom': 0, 'left': 4},
                            xAxis={'id': 'week-axis', 'data': weeks},
                            axisHighlight={'x': 'line'},
                            slotProps={'lineHighlight': {'r': 4}},
                            clipAreaOffset={'top': 2, 'bottom': 2},
                        ),
                    ], style={'marginLeft': 'auto'}),
                ], style={
                    'display': 'flex',
                    'alignItems': 'flex-end',
                    'justifyContent': 'space-between',
                    'borderBottom': '2px solid rgba(137, 86, 255, 0.2)',
                    'paddingBottom': '5px',
                }),
            ], style={
                'width': '350px',
                'backgroundColor': 'white',
                'padding': '15px 20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            }),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""SparklineChart(
    id='npm-sparkline',
    data=weekly_downloads,
    width=200,
    height=45,
    color='rgb(137, 86, 255)',
    area=True,
    showHighlight=True,
    baseline='min',  # Area fills from minimum value
    margin={'top': 5, 'right': 0, 'bottom': 0, 'left': 4},
    xAxis={'id': 'week-axis', 'data': weeks},
    axisHighlight={'x': 'line'},  # Show vertical line on hover
    slotProps={'lineHighlight': {'r': 4}},  # Smaller highlight dot
    clipAreaOffset={'top': 2, 'bottom': 2},
)

@callback(
    Output('npm-download-count', 'children'),
    Output('npm-week-label', 'children'),
    Input('npm-sparkline', 'hoverIndex'),
    Input('npm-sparkline', 'hoverValue'),
)
def update_npm_display(hover_index, hover_value):
    if hover_index is not None and hover_value is not None:
        return f"{int(hover_value):,}", weeks[hover_index]
    return f"{weekly_downloads[-1]:,}", "Weekly Downloads"
""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Synchronized Multi-Metric Dashboard
    # ==========================================================================
    html.Div([
        html.H2("Synchronized Multi-Metric Dashboard"),
        html.P(
            "Multiple sparklines that sync their hover state. "
            "Hover over any chart to see all metrics for that time period.",
            style=description_style
        ),
        # Store for shared hover index
        dcc.Store(id='shared-hover-index', data=None),

        html.Div([
            # Revenue Card
            html.Div([
                html.Div("Revenue", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div([
                    html.Span(id='sync-revenue-value', children=f"${revenue_data[-1]}K", style={'fontSize': '24px', 'fontWeight': 'bold'}),
                    html.Span(id='sync-revenue-label', children="", style={'fontSize': '11px', 'color': '#999', 'marginLeft': '8px'}),
                ]),
                SparklineChart(
                    id='sync-revenue-spark',
                    data=revenue_data,
                    width=200,
                    height=35,
                    color='#4caf50',
                    area=True,
                    showHighlight=True,
                    xAxis={'id': 'rev-axis', 'data': metric_labels},
                ),
            ], style={**kpi_card_style, 'borderTop': '3px solid #4caf50'}),

            # Users Card
            html.Div([
                html.Div("Active Users", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div([
                    html.Span(id='sync-users-value', children=f"{users_data[-1]:,}", style={'fontSize': '24px', 'fontWeight': 'bold'}),
                    html.Span(id='sync-users-label', children="", style={'fontSize': '11px', 'color': '#999', 'marginLeft': '8px'}),
                ]),
                SparklineChart(
                    id='sync-users-spark',
                    data=users_data,
                    width=200,
                    height=35,
                    color='#2196f3',
                    area=True,
                    showHighlight=True,
                    xAxis={'id': 'users-axis', 'data': metric_labels},
                ),
            ], style={**kpi_card_style, 'borderTop': '3px solid #2196f3'}),

            # Sessions Card
            html.Div([
                html.Div("Sessions", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div([
                    html.Span(id='sync-sessions-value', children=f"{sessions_data[-1]:,}", style={'fontSize': '24px', 'fontWeight': 'bold'}),
                    html.Span(id='sync-sessions-label', children="", style={'fontSize': '11px', 'color': '#999', 'marginLeft': '8px'}),
                ]),
                SparklineChart(
                    id='sync-sessions-spark',
                    data=sessions_data,
                    width=200,
                    height=35,
                    color='#ff9800',
                    area=True,
                    showHighlight=True,
                    xAxis={'id': 'sessions-axis', 'data': metric_labels},
                ),
            ], style={**kpi_card_style, 'borderTop': '3px solid #ff9800'}),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),

        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '15px'}),
            dmc.CodeHighlight(code="""# Three sparklines with synchronized hover
SparklineChart(
    id='sync-revenue-spark',
    data=revenue_data,
    showHighlight=True,
    xAxis={'id': 'rev-axis', 'data': metric_labels},
    ...
)

# Callback to sync hover across all sparklines
@callback(
    Output('sync-revenue-value', 'children'),
    Output('sync-users-value', 'children'),
    Output('sync-sessions-value', 'children'),
    Input('sync-revenue-spark', 'hoverIndex'),
    Input('sync-users-spark', 'hoverIndex'),
    Input('sync-sessions-spark', 'hoverIndex'),
)
def sync_hover(rev_idx, users_idx, sessions_idx):
    # Find which chart triggered the callback
    idx = rev_idx or users_idx or sessions_idx
    if idx is not None:
        return f"${revenue_data[idx]}K", f"{users_data[idx]:,}", f"{sessions_data[idx]:,}"
    return f"${revenue_data[-1]}K", f"{users_data[-1]:,}", f"{sessions_data[-1]:,}"
""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Area Sparkline
    # ==========================================================================
    html.Div([
        html.H2("Area Sparkline"),
        html.P(
            "Add 'area=True' to fill the area under the line. "
            "Use 'baseline' to control where the fill starts.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Span("baseline='min': ", style={'width': '120px', 'display': 'inline-block'}),
                SparklineChart(
                    data=temperature_week,
                    width=150,
                    height=40,
                    color='#ff9800',
                    area=True,
                    baseline='min',
                ),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("baseline='max': ", style={'width': '120px', 'display': 'inline-block'}),
                SparklineChart(
                    data=temperature_week,
                    width=150,
                    height=40,
                    color='#2196f3',
                    area=True,
                    baseline='max',
                ),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("baseline=75: ", style={'width': '120px', 'display': 'inline-block'}),
                SparklineChart(
                    data=temperature_week,
                    width=150,
                    height=40,
                    color='#9c27b0',
                    area=True,
                    baseline=75,
                ),
            ]),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""# baseline='min' - fills from minimum (default)
SparklineChart(data=data, area=True, baseline='min')

# baseline='max' - fills from maximum (inverted)
SparklineChart(data=data, area=True, baseline='max')

# baseline=75 - fills from a specific value
SparklineChart(data=data, area=True, baseline=75)
""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Bar Sparkline
    # ==========================================================================
    html.Div([
        html.H2("Bar Sparkline"),
        html.P(
            "Use 'plotType=\"bar\"' for a bar chart sparkline. "
            "Good for discrete values or comparing magnitudes.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Span("Daily Errors: ", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                SparklineChart(
                    data=error_rates,
                    width=150,
                    height=40,
                    plotType='bar',
                    color='#f44336',
                ),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'}),
            html.Div([
                html.Span("Weekly Sales: ", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                SparklineChart(
                    data=[120, 145, 132, 168, 155, 142, 178],
                    width=150,
                    height=40,
                    plotType='bar',
                    color='#2196f3',
                ),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""SparklineChart(
    data=[2, 5, 3, 8, 4, 2, 1, 3, 2, 4],
    width=150,
    height=40,
    plotType='bar',  # Bar chart instead of line
    color='#f44336',
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Sparklines in a Table
    # ==========================================================================
    html.Div([
        html.H2("Sparklines in a Table"),
        html.P(
            "Sparklines are perfect for embedding in data tables to show trends "
            "alongside other metrics.",
            style=description_style
        ),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Metric", style={'textAlign': 'left', 'padding': '12px', 'borderBottom': '2px solid #ddd'}),
                    html.Th("Current", style={'textAlign': 'right', 'padding': '12px', 'borderBottom': '2px solid #ddd'}),
                    html.Th("Trend (7 days)", style={'textAlign': 'center', 'padding': '12px', 'borderBottom': '2px solid #ddd'}),
                    html.Th("Change", style={'textAlign': 'right', 'padding': '12px', 'borderBottom': '2px solid #ddd'}),
                ]),
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("Revenue", style={'padding': '12px'}),
                    html.Td("$45,230", style={'textAlign': 'right', 'padding': '12px', 'fontWeight': 'bold'}),
                    html.Td(
                        SparklineChart(data=[38, 42, 40, 44, 43, 45, 45], width=100, height=25, color='#4caf50', area=True),
                        style={'textAlign': 'center', 'padding': '12px'}
                    ),
                    html.Td("+12%", style={'textAlign': 'right', 'padding': '12px', 'color': '#4caf50'}),
                ]),
                html.Tr([
                    html.Td("Users", style={'padding': '12px'}),
                    html.Td("2,847", style={'textAlign': 'right', 'padding': '12px', 'fontWeight': 'bold'}),
                    html.Td(
                        SparklineChart(data=[2200, 2350, 2400, 2500, 2650, 2750, 2847], width=100, height=25, color='#2196f3', area=True),
                        style={'textAlign': 'center', 'padding': '12px'}
                    ),
                    html.Td("+29%", style={'textAlign': 'right', 'padding': '12px', 'color': '#4caf50'}),
                ]),
                html.Tr([
                    html.Td("Errors", style={'padding': '12px'}),
                    html.Td("23", style={'textAlign': 'right', 'padding': '12px', 'fontWeight': 'bold'}),
                    html.Td(
                        SparklineChart(data=[45, 38, 42, 35, 30, 28, 23], width=100, height=25, color='#f44336'),
                        style={'textAlign': 'center', 'padding': '12px'}
                    ),
                    html.Td("-49%", style={'textAlign': 'right', 'padding': '12px', 'color': '#4caf50'}),
                ]),
                html.Tr([
                    html.Td("Response Time", style={'padding': '12px'}),
                    html.Td("245ms", style={'textAlign': 'right', 'padding': '12px', 'fontWeight': 'bold'}),
                    html.Td(
                        SparklineChart(data=[220, 235, 242, 238, 250, 248, 245], width=100, height=25, color='#ff9800'),
                        style={'textAlign': 'center', 'padding': '12px'}
                    ),
                    html.Td("+11%", style={'textAlign': 'right', 'padding': '12px', 'color': '#f44336'}),
                ]),
            ]),
        ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'}),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Callback-Triggered Data Changes
    # ==========================================================================
    html.Div([
        html.H2("Callback-Triggered Data Changes"),
        html.P(
            "Change the sparkline data dynamically using callbacks. "
            "Select a metric to see different trend data.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Label("Select Metric:", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='metric-selector',
                    options=[
                        {'label': 'Revenue', 'value': 'revenue'},
                        {'label': 'Users', 'value': 'users'},
                        {'label': 'Sessions', 'value': 'sessions'},
                        {'label': 'Errors', 'value': 'errors'},
                    ],
                    value='revenue',
                    style={'width': '200px'},
                    clearable=False,
                ),
            ], style={'marginBottom': '20px'}),
            html.Div([
                html.Div(id='dynamic-metric-label', children="Revenue Trend", style={'fontSize': '14px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div(id='dynamic-metric-value', children="$65K", style={'fontSize': '32px', 'fontWeight': 'bold', 'marginBottom': '10px'}),
                html.Div(id='dynamic-sparkline-container'),
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '300px',
            }),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '15px'}),
            dmc.CodeHighlight(code="""@callback(
    Output('dynamic-sparkline-container', 'children'),
    Output('dynamic-metric-label', 'children'),
    Output('dynamic-metric-value', 'children'),
    Input('metric-selector', 'value')
)
def update_sparkline(metric):
    data_map = {
        'revenue': (revenue_data, '#4caf50', 'Revenue Trend', f"${revenue_data[-1]}K"),
        'users': (users_data, '#2196f3', 'Active Users', f"{users_data[-1]:,}"),
        'sessions': (sessions_data, '#ff9800', 'Sessions', f"{sessions_data[-1]:,}"),
        'errors': (error_rates, '#f44336', 'Error Rate', f"{error_rates[-1]}"),
    }
    data, color, label, value = data_map[metric]

    return SparklineChart(
        data=data,
        width=260,
        height=50,
        color=color,
        area=True,
        showHighlight=True,
        showTooltip=True,
    ), label, value
""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Custom Curves
    # ==========================================================================
    html.Div([
        html.H2("Custom Curves"),
        html.P(
            "Use different curve interpolation methods for different visual effects.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Span("Linear: ", style={'width': '100px', 'display': 'inline-block'}),
                SparklineChart(data=sales_trend, width=120, height=30, color='#1976d2', curve='linear'),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("Natural: ", style={'width': '100px', 'display': 'inline-block'}),
                SparklineChart(data=sales_trend, width=120, height=30, color='#4caf50', curve='natural'),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("Step: ", style={'width': '100px', 'display': 'inline-block'}),
                SparklineChart(data=sales_trend, width=120, height=30, color='#ff9800', curve='step'),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Span("MonotoneX: ", style={'width': '100px', 'display': 'inline-block'}),
                SparklineChart(data=sales_trend, width=120, height=30, color='#9c27b0', curve='monotoneX'),
            ], style={'marginBottom': '10px'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""# Available curves: 'linear', 'natural', 'step', 'stepBefore',
# 'stepAfter', 'monotoneX', 'monotoneY', 'catmullRom', 'bumpX', 'bumpY'

SparklineChart(
    data=sales_trend,
    width=120,
    height=30,
    color='#4caf50',
    curve='natural',  # Smooth natural curve
)""", language="python"),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==========================================================================
    # Interactive Sparkline with Hover Details
    # ==========================================================================
    html.Div([
        html.H2("Interactive Sparkline with Hover Details"),
        html.P(
            "Enable tooltips and highlighting to make sparklines interactive. "
            "Hover over the chart to see detailed information.",
            style=description_style
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Span("Stock Price: ", style={'fontWeight': 'bold'}),
                    html.Span(id='stock-price-display', children=f"${stock_prices[-1]:.2f}"),
                ], style={'marginBottom': '10px'}),
                SparklineChart(
                    id='interactive-stock-sparkline',
                    data=stock_prices,
                    width=300,
                    height=60,
                    color='#1976d2',
                    area=True,
                    showTooltip=True,
                    showHighlight=True,
                    xAxis={'id': 'stock-axis', 'data': ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10']},
                    axisHighlight={'x': 'line'},
                ),
            ]),
            html.Div([
                html.Strong("Hover Data:"),
                html.Pre(
                    id='stock-hover-output',
                    children="Hover over the chart to see details",
                    style={**code_style, 'marginTop': '10px', 'minHeight': '60px'}
                ),
            ], style={'marginTop': '15px'}),
        ]),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            dmc.CodeHighlight(code="""SparklineChart(
    id='interactive-stock-sparkline',
    data=stock_prices,
    width=300,
    height=60,
    color='#1976d2',
    area=True,
    showTooltip=True,
    showHighlight=True,
    xAxis={'id': 'stock-axis', 'data': day_labels},
    axisHighlight={'x': 'line'},  # Vertical line on hover
)

@callback(
    Output('stock-price-display', 'children'),
    Output('stock-hover-output', 'children'),
    Input('interactive-stock-sparkline', 'hoverIndex'),
    Input('interactive-stock-sparkline', 'hoverValue'),
)
def update_stock_display(index, value):
    if index is not None and value is not None:
        return f"${value:.2f}", json.dumps({
            'index': index,
            'value': value,
            'day': f'Day {index + 1}'
        }, indent=2)
    return f"${stock_prices[-1]:.2f}", "Hover over the chart"
""", language="python"),
        ]),
    ], style=section_style),
])


# ==========================================================================
# Callbacks
# ==========================================================================

@callback(
    Output('npm-download-count', 'children'),
    Output('npm-week-label', 'children'),
    Input('npm-sparkline', 'hoverIndex'),
    Input('npm-sparkline', 'hoverValue'),
    prevent_initial_call=True
)
def update_npm_display(hover_index, hover_value):
    """Update npm-style display based on hover."""
    if hover_index is not None and hover_value is not None:
        return f"{int(hover_value):,}", weeks[hover_index]
    return f"{weekly_downloads[-1]:,}", "Weekly Downloads"


@callback(
    Output('sync-revenue-value', 'children'),
    Output('sync-revenue-label', 'children'),
    Output('sync-users-value', 'children'),
    Output('sync-users-label', 'children'),
    Output('sync-sessions-value', 'children'),
    Output('sync-sessions-label', 'children'),
    Input('sync-revenue-spark', 'hoverIndex'),
    Input('sync-users-spark', 'hoverIndex'),
    Input('sync-sessions-spark', 'hoverIndex'),
    prevent_initial_call=True
)
def sync_hover(rev_idx, users_idx, sessions_idx):
    """Sync hover state across multiple sparklines."""
    # Find which index to use (any non-None value)
    idx = None
    for i in [rev_idx, users_idx, sessions_idx]:
        if i is not None:
            idx = i
            break

    if idx is not None:
        label = metric_labels[idx]
        return (
            f"${revenue_data[idx]}K", label,
            f"{users_data[idx]:,}", label,
            f"{sessions_data[idx]:,}", label,
        )
    return (
        f"${revenue_data[-1]}K", "",
        f"{users_data[-1]:,}", "",
        f"{sessions_data[-1]:,}", "",
    )


@callback(
    Output('dynamic-sparkline-container', 'children'),
    Output('dynamic-metric-label', 'children'),
    Output('dynamic-metric-value', 'children'),
    Input('metric-selector', 'value')
)
def update_dynamic_sparkline(metric):
    """Update sparkline based on selected metric."""
    data_map = {
        'revenue': (revenue_data, '#4caf50', 'Revenue Trend', f"${revenue_data[-1]}K"),
        'users': (users_data, '#2196f3', 'Active Users', f"{users_data[-1]:,}"),
        'sessions': (sessions_data, '#ff9800', 'Sessions', f"{sessions_data[-1]:,}"),
        'errors': (error_rates, '#f44336', 'Error Rate', str(error_rates[-1])),
    }
    data, color, label, value = data_map[metric]

    return SparklineChart(
        data=data,
        width=260,
        height=50,
        color=color,
        area=True,
        showHighlight=True,
        showTooltip=True,
    ), label, value


@callback(
    Output('stock-price-display', 'children'),
    Output('stock-hover-output', 'children'),
    Input('interactive-stock-sparkline', 'hoverIndex'),
    Input('interactive-stock-sparkline', 'hoverValue'),
    prevent_initial_call=True
)
def update_stock_display(index, value):
    """Update stock price display based on hover."""
    if index is not None and value is not None:
        return f"${value:.2f}", json.dumps({
            'index': index,
            'value': value,
            'day': f'Day {index + 1}'
        }, indent=2)
    return f"${stock_prices[-1]:.2f}", "Hover over the chart to see details"
