"""
BarChart Demo - Basic
Vertical, horizontal, stacked bar charts, border radius, and bar labels.
"""

import json
import random

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/barchart-basic', name='Bar Chart - Basic')

from dash_mui_charts import BarChart

random.seed(42)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [random.randint(30, 90) for _ in months]
expenses = [random.randint(20, 65) for _ in months]
profit = [r - e for r, e in zip(revenue, expenses)]

CARD = 'page-card'

layout = html.Div([
    html.H2("Bar Chart — Basic Examples"),
    html.P("Vertical, horizontal, stacked bars, border radius, and bar labels.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Multi-Series Vertical ---
    html.Div([
        html.H4("Multi-Series Vertical"),
        html.P("Revenue, expenses, and profit by month.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-multi',
            series=[
                {'data': revenue, 'label': 'Revenue ($k)', 'color': '#1976d2'},
                {'data': expenses, 'label': 'Expenses ($k)', 'color': '#f57c00'},
                {'data': profit, 'label': 'Profit ($k)', 'color': '#388e3c'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band', 'label': 'Month'}],
            yAxis=[{'label': 'Amount ($k)'}],
            grid={'horizontal': True},
            height=350,
        ),
    ], className=CARD),

    # --- 2. Stacked ---
    html.Div([
        html.H4("Stacked Bar Chart"),
        html.P("Traffic sources stacked per month.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-stacked',
            series=[
                {'data': [random.randint(10, 30) for _ in months], 'label': 'Organic', 'color': '#66bb6a', 'stack': 'traffic'},
                {'data': [random.randint(8, 25) for _ in months], 'label': 'Paid', 'color': '#42a5f5', 'stack': 'traffic'},
                {'data': [random.randint(5, 15) for _ in months], 'label': 'Referral', 'color': '#ab47bc', 'stack': 'traffic'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            yAxis=[{'label': 'Visitors (k)'}],
            grid={'horizontal': True},
            height=300,
        ),
    ], className=CARD),

    # --- 3. Horizontal with Border Radius ---
    html.Div([
        html.H4("Horizontal Bar Chart"),
        html.P("Revenue displayed horizontally with rounded corners.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-horizontal',
            series=[{'data': revenue, 'label': 'Revenue ($k)', 'color': '#1976d2'}],
            yAxis=[{'data': months, 'scaleType': 'band'}],
            xAxis=[{'label': 'Amount ($k)'}],
            layout='horizontal',
            borderRadius=6,
            grid={'vertical': True},
            height=300,
        ),
    ], className=CARD),

    # --- 4. Bar Labels ---
    html.Div([
        html.H4("Bar Labels"),
        html.P("Display values on bars with center and outside placement.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-labels',
            series=[
                {'data': [4, 3, 5], 'barLabel': 'value', 'barLabelPlacement': 'outside', 'label': 'Outside'},
                {'data': [2, 5, 6], 'barLabel': 'value', 'barLabelPlacement': 'center', 'label': 'Center'},
                {'data': [3, 4, 2], 'label': 'No label'},
            ],
            xAxis=[{'data': ['Group A', 'Group B', 'Group C'], 'scaleType': 'band'}],
            height=300,
            grid={'horizontal': True},
        ),
    ], className=CARD),

    # --- 5. Border Radius + Colors ---
    html.Div([
        html.H4("Rounded Bars with Custom Colors"),
        html.P("Border radius and custom color palette.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-rounded',
            series=[
                {'data': [25, 50, 35, 70, 45], 'label': 'Sales'},
            ],
            xAxis=[{'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'scaleType': 'band'}],
            borderRadius=10,
            colors=['#7c4dff'],
            grid={'horizontal': True},
            height=280,
        ),
    ], className=CARD),

    # --- 6. Negative Values ---
    html.Div([
        html.H4("Negative Values"),
        html.P("Bars with negative values extend below the zero baseline.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-basic-negative',
            series=[
                {'data': [35, -20, 45, -15, 55, -30], 'label': 'Net Change', 'color': '#00897b'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})
