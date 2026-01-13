"""
Dash MUI Charts - LineChart Usage Example

This example demonstrates the basic usage of the LineChart component,
including multiple series, axis configuration, grid, click callbacks,
biaxial charts (dual Y-axes), and Pro features like zoom and pan.
"""

import os
from dash import Dash, html, callback, Input, Output
import json

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import the LineChart component
from dash_mui_charts import LineChart

# Load MUI X Pro license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

app = Dash(__name__)

# =============================================================================
# Sample Data: US Unemployment Rate and GDP Per Capita (2000-2023)
# Similar to the MUI X Charts Pro example
# =============================================================================
years = list(range(2000, 2024))

# Unemployment rate data (%)
unemployment_rate = [
    4.0, 4.7, 5.8, 6.0, 5.5, 5.1, 4.6, 4.6, 5.8, 9.3,
    9.6, 8.9, 8.1, 7.4, 6.2, 5.3, 4.9, 4.4, 3.9, 3.7,
    8.1, 5.4, 3.6, 3.7
]

# GDP per capita data ($)
gdp_per_capita = [
    36330, 37134, 37998, 39496, 41713, 44115, 46299, 48050, 48570, 47099,
    48468, 50066, 51784, 53107, 55049, 56863, 58021, 60110, 63064, 65280,
    63544, 70249, 76343, 80035
]

app.layout = html.Div([
    html.H1("Dash MUI Charts - LineChart Demo"),

    # ==========================================================================
    # Biaxial Chart: Unemployment Rate vs GDP Per Capita
    # Inspired by MUI X Charts Pro LineOverview example
    # ==========================================================================
    html.H2("Biaxial Chart: US Unemployment Rate vs GDP Per Capita"),
    html.P(
        "This chart demonstrates dual Y-axes (biaxial) with different scales, "
        "similar to the MUI X Charts Pro example.",
        style={'color': '#666', 'marginBottom': '10px'}
    ),
    LineChart(
        id='biaxial-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=350,
        series=[
            {
                'id': 'unemployment',
                'data': unemployment_rate,
                'label': 'Unemployment rate',
                'color': '#af3838',
                'showMark': False,
                'yAxisId': 'unemployment-axis',
            },
            {
                'id': 'gdp',
                'data': gdp_per_capita,
                'label': 'GDP per capita',
                'color': '#4caf50',
                'showMark': False,
                'yAxisId': 'gdp-axis',
                'connectNulls': True,
            },
        ],
        xAxis=[{
            'data': years,
            'scaleType': 'point',
        }],
        yAxis=[
            {
                'id': 'unemployment-axis',
                'label': 'Unemployment Rate (%)',
                'position': 'left',
                'width': 60,
            },
            {
                'id': 'gdp-axis',
                'label': 'GDP per capita ($)',
                'position': 'right',
                'width': 80,
            },
        ],
        grid={'horizontal': True},
        margin={'left': 70, 'right': 90, 'top': 20, 'bottom': 30},
    ),
    html.P(
        "Source: Sample data based on FRED",
        style={'color': '#999', 'fontSize': '12px', 'marginTop': '5px'}
    ),

    html.Hr(),

    # ==========================================================================
    # Pro Feature: Zoom and Pan
    # ==========================================================================
    html.H2("Pro Feature: Zoom and Pan"),
    html.P(
        "Use the slider below the chart to select a range, or drag the handles to zoom. "
        "The slider provides intuitive control for exploring data over time.",
        style={'color': '#666', 'marginBottom': '10px'}
    ),
    LineChart(
        id='zoom-linechart',
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
        # Show the zoom slider below the chart
        showSlider=True,
        # Initial zoom state (start zoomed in to first half)
        initialZoom=[{'axisId': 'x-axis', 'start': 0, 'end': 50}],
    ),
    html.H3("Zoom State:"),
    html.Pre(
        id='zoom-output',
        style={
            'background': '#f5f5f5',
            'padding': '15px',
            'borderRadius': '5px',
            'whiteSpace': 'pre-wrap',
        }
    ),

    html.Hr(),

    # Basic LineChart with multiple series
    html.H2("Basic Line Chart with Grid"),
    LineChart(
        id='basic-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=400,
        series=[
            {
                'data': [2, 5.5, 2, 8.5, 1.5, 5],
                'label': 'Series A',
                'showMark': True,
            },
            {
                'data': [4, 3.5, 6, 2.5, 4.5, 3],
                'label': 'Series B',
            },
        ],
        xAxis=[{
            'data': [1, 2, 3, 4, 5, 6],
            'scaleType': 'point',
        }],
        grid={'horizontal': True, 'vertical': True},
    ),

    html.Hr(),

    # Area chart example
    html.H2("Area Chart"),
    LineChart(
        id='area-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=300,
        series=[
            {
                'data': [2, 5.5, 2, 8.5, 1.5, 5],
                'label': 'Revenue',
                'area': True,
                'color': '#1976d2',
            },
        ],
        xAxis=[{
            'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'scaleType': 'band',
        }],
    ),

    html.Hr(),

    # Stacked Area Chart
    html.H2("Stacked Area Chart"),
    LineChart(
        id='stacked-area-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=300,
        series=[
            {
                'data': [4, 3, 5, 4, 6, 3, 5],
                'label': 'Product A',
                'area': True,
                'stack': 'total',
            },
            {
                'data': [3, 4, 3, 5, 4, 6, 4],
                'label': 'Product B',
                'area': True,
                'stack': 'total',
            },
            {
                'data': [2, 2, 3, 2, 3, 2, 3],
                'label': 'Product C',
                'area': True,
                'stack': 'total',
            },
        ],
        xAxis=[{
            'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'scaleType': 'point',
        }],
        colors=['#4e79a7', '#f28e2c', '#e15759'],
    ),

    html.Hr(),

    # Chart with custom colors and curves
    html.H2("Custom Colors and Curves"),
    LineChart(
        id='custom-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=300,
        series=[
            {
                'data': [1, 4, 2, 5, 7, 2, 4],
                'label': 'Linear',
                'curve': 'linear',
            },
            {
                'data': [2, 3, 5, 4, 6, 3, 5],
                'label': 'Monotone',
                'curve': 'monotoneX',
            },
            {
                'data': [3, 2, 4, 6, 5, 4, 3],
                'label': 'Step',
                'curve': 'step',
            },
        ],
        xAxis=[{
            'data': [0, 1, 2, 3, 4, 5, 6],
        }],
        colors=['#ff6384', '#36a2eb', '#ffce56'],
    ),

    html.Hr(),

    # Interactive chart with click callback
    html.H2("Interactive Chart with Click Events"),
    LineChart(
        id='interactive-linechart',
        licenseKey=MUI_LICENSE_KEY,
        height=350,
        series=[
            {
                'data': [2400, 1398, 9800, 3908, 4800, 3800, 4300],
                'label': 'Sales',
                'showMark': True,
            },
            {
                'data': [4000, 3000, 2000, 2780, 1890, 2390, 3490],
                'label': 'Expenses',
                'showMark': True,
            },
        ],
        xAxis=[{
            'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'scaleType': 'point',
            'label': 'Day of Week',
        }],
        yAxis=[{
            'label': 'Amount ($)',
        }],
        grid={'horizontal': True},
    ),

    html.H3("Click Data:"),
    html.Pre(
        id='click-output',
        style={
            'background': '#f5f5f5',
            'padding': '15px',
            'borderRadius': '5px',
            'whiteSpace': 'pre-wrap',
        }
    ),

], style={'maxWidth': '900px', 'margin': '0 auto', 'padding': '20px'})


@callback(
    Output('click-output', 'children'),
    Input('interactive-linechart', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    """Display click event data."""
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on the chart to see event data"


@callback(
    Output('zoom-output', 'children'),
    Input('zoom-linechart', 'zoomData'),
    prevent_initial_call=True
)
def display_zoom(zoom_data):
    """Display zoom state data."""
    if zoom_data:
        return json.dumps(zoom_data, indent=2)
    return "Zoom the chart to see state changes"


if __name__ == '__main__':
    app.run(debug=True, port=7666)
