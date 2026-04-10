"""
BarChart Demo - Reference Lines & Styling
Reference lines for thresholds/targets, custom colors, animations, and legend control.
"""

import random

import dash
from dash import html

dash.register_page(__name__, path='/barchart-reference', name='Bar Chart - Reference Lines')

from dash_mui_charts import BarChart

random.seed(42)

CARD = 'page-card'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
sales = [45, 52, 48, 61, 55, 70, 65, 72]

layout = html.Div([
    html.H2("Bar Chart — Reference Lines & Styling"),
    html.P("Reference lines, animation control, custom rendering, and legend options.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Horizontal Reference Line (Target) ---
    html.Div([
        html.H4("Target Line"),
        html.P("Horizontal reference line showing a sales target.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-target',
            series=[
                {'data': sales, 'label': 'Monthly Sales', 'color': '#1976d2'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            yAxis=[{'label': 'Units Sold'}],
            referenceLines=[
                {
                    'y': 60,
                    'label': 'Target (60)',
                    'labelAlign': 'end',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2, 'strokeDasharray': '6 4'},
                    'labelStyle': {'fill': '#f44336', 'fontWeight': 'bold', 'fontSize': 12},
                },
            ],
            grid={'horizontal': True},
            height=350,
        ),
    ], className=CARD),

    # --- 2. Multiple Reference Lines ---
    html.Div([
        html.H4("Multiple Reference Lines"),
        html.P("Show min, avg, and max thresholds.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-multi',
            series=[
                {'data': sales, 'label': 'Sales', 'color': '#5c6bc0'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            referenceLines=[
                {
                    'y': min(sales),
                    'label': f'Min ({min(sales)})',
                    'labelAlign': 'start',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 1.5, 'strokeDasharray': '4 4'},
                    'labelStyle': {'fill': '#f44336', 'fontSize': 11},
                },
                {
                    'y': sum(sales) / len(sales),
                    'label': f'Avg ({sum(sales) / len(sales):.0f})',
                    'labelAlign': 'middle',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#ff9800', 'fontSize': 11},
                },
                {
                    'y': max(sales),
                    'label': f'Max ({max(sales)})',
                    'labelAlign': 'end',
                    'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 1.5, 'strokeDasharray': '4 4'},
                    'labelStyle': {'fill': '#4caf50', 'fontSize': 11},
                },
            ],
            grid={'horizontal': True},
            height=350,
        ),
    ], className=CARD),

    # --- 3. Vertical Reference Line ---
    html.Div([
        html.H4("Vertical Reference Line"),
        html.P("Mark a specific category (e.g., policy change date).",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-vertical',
            series=[
                {'data': sales, 'label': 'Sales', 'color': '#00897b'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            referenceLines=[
                {
                    'x': 'May',
                    'label': 'New Policy',
                    'labelAlign': 'start',
                    'lineStyle': {'stroke': '#9c27b0', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#9c27b0', 'fontWeight': 'bold', 'fontSize': 12},
                },
            ],
            grid={'horizontal': True},
            height=350,
        ),
    ], className=CARD),

    # --- 4. No Animation ---
    html.Div([
        html.H4("Skip Animation"),
        html.P("Bars render instantly when skipAnimation=True.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-noanim',
            series=[
                {'data': sales, 'label': 'Sales', 'color': '#ef6c00'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            skipAnimation=True,
            grid={'horizontal': True},
            height=280,
        ),
    ], className=CARD),

    # --- 5. Hidden Legend ---
    html.Div([
        html.H4("Hidden Legend"),
        html.P("Use hideLegend=True when the legend is redundant.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-nolegend',
            series=[
                {'data': sales, 'label': 'Sales', 'color': '#7b1fa2'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            hideLegend=True,
            borderRadius=8,
            grid={'horizontal': True},
            height=280,
        ),
    ], className=CARD),

    # --- 6. Custom Color Palette ---
    html.Div([
        html.H4("Custom Color Palette"),
        html.P("Override the default palette with the colors prop.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-ref-colors',
            series=[
                {'data': [30, 45, 35], 'label': 'East'},
                {'data': [25, 50, 40], 'label': 'West'},
                {'data': [40, 30, 55], 'label': 'Central'},
            ],
            xAxis=[{'data': ['2023', '2024', '2025'], 'scaleType': 'band'}],
            colors=['#ff6f00', '#00bfa5', '#6200ea'],
            grid={'horizontal': True},
            height=300,
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})
