"""
BarChart Demo - Dataset Mode
Using the dataset prop with dataKey references for clean data management.
"""

import dash
from dash import html

dash.register_page(__name__, path='/barchart-dataset', name='Bar Chart - Dataset')

from dash_mui_charts import BarChart

CARD = 'page-card'

# City temperature data
temp_dataset = [
    {'month': 'Jan', 'london': 5, 'paris': 4, 'nyc': 0, 'tokyo': 6},
    {'month': 'Feb', 'london': 6, 'paris': 5, 'nyc': 1, 'tokyo': 7},
    {'month': 'Mar', 'london': 9, 'paris': 10, 'nyc': 7, 'tokyo': 11},
    {'month': 'Apr', 'london': 13, 'paris': 14, 'nyc': 13, 'tokyo': 17},
    {'month': 'May', 'london': 16, 'paris': 18, 'nyc': 18, 'tokyo': 21},
    {'month': 'Jun', 'london': 20, 'paris': 22, 'nyc': 24, 'tokyo': 25},
    {'month': 'Jul', 'london': 22, 'paris': 25, 'nyc': 28, 'tokyo': 29},
    {'month': 'Aug', 'london': 21, 'paris': 24, 'nyc': 27, 'tokyo': 30},
    {'month': 'Sep', 'london': 18, 'paris': 20, 'nyc': 22, 'tokyo': 26},
    {'month': 'Oct', 'london': 14, 'paris': 15, 'nyc': 16, 'tokyo': 20},
    {'month': 'Nov', 'london': 9, 'paris': 9, 'nyc': 9, 'tokyo': 14},
    {'month': 'Dec', 'london': 6, 'paris': 5, 'nyc': 2, 'tokyo': 8},
]

# Product sales data
product_dataset = [
    {'product': 'Widget A', 'q1': 120, 'q2': 150, 'q3': 180, 'q4': 200},
    {'product': 'Widget B', 'q1': 90, 'q2': 110, 'q3': 95, 'q4': 130},
    {'product': 'Widget C', 'q1': 200, 'q2': 180, 'q3': 220, 'q4': 250},
    {'product': 'Widget D', 'q1': 60, 'q2': 85, 'q3': 100, 'q4': 90},
]

layout = html.Div([
    html.H2("Bar Chart — Dataset Mode"),
    html.P("Using dataset prop with dataKey references — no data duplication across series.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Basic Dataset ---
    html.Div([
        html.H4("City Temperatures (Dataset Mode)"),
        html.P("Data is passed once via dataset, series reference columns by dataKey.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ds-temps',
            dataset=temp_dataset,
            xAxis=[{'dataKey': 'month', 'scaleType': 'band'}],
            series=[
                {'dataKey': 'london', 'label': 'London', 'color': '#1976d2'},
                {'dataKey': 'paris', 'label': 'Paris', 'color': '#f57c00'},
                {'dataKey': 'nyc', 'label': 'New York', 'color': '#388e3c'},
                {'dataKey': 'tokyo', 'label': 'Tokyo', 'color': '#d32f2f'},
            ],
            yAxis=[{'label': '°C'}],
            height=380,
            grid={'horizontal': True},
        ),
    ], className=CARD),

    # --- 2. Stacked Dataset ---
    html.Div([
        html.H4("Stacked Quarterly Sales"),
        html.P("Stacked bars from dataset with horizontal layout.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ds-stacked',
            dataset=product_dataset,
            yAxis=[{'dataKey': 'product', 'scaleType': 'band'}],
            series=[
                {'dataKey': 'q1', 'label': 'Q1', 'stack': 'annual', 'color': '#5c6bc0'},
                {'dataKey': 'q2', 'label': 'Q2', 'stack': 'annual', 'color': '#42a5f5'},
                {'dataKey': 'q3', 'label': 'Q3', 'stack': 'annual', 'color': '#26c6da'},
                {'dataKey': 'q4', 'label': 'Q4', 'stack': 'annual', 'color': '#66bb6a'},
            ],
            layout='horizontal',
            borderRadius=4,
            grid={'vertical': True},
            height=300,
        ),
    ], className=CARD),

    # --- 3. Two cities, side-by-side with bar gap control ---
    html.Div([
        html.H4("Bar Gap & Category Gap"),
        html.P("Control spacing with categoryGapRatio and barGapRatio on the band axis.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ds-gaps',
            dataset=temp_dataset,
            xAxis=[{
                'dataKey': 'month',
                'scaleType': 'band',
                'categoryGapRatio': 0.4,
                'barGapRatio': 0.1,
            }],
            series=[
                {'dataKey': 'london', 'label': 'London', 'color': '#1565c0'},
                {'dataKey': 'tokyo', 'label': 'Tokyo', 'color': '#c62828'},
            ],
            yAxis=[{'label': '°C'}],
            height=320,
            grid={'horizontal': True},
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})
