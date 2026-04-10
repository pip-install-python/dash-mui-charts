"""
BarChart Demo - Stacking
Stack offsets, stack ordering, and diverging stacked bars.
"""

import random

import dash
from dash import html

dash.register_page(__name__, path='/barchart-stacking', name='Bar Chart - Stacking')

from dash_mui_charts import BarChart

random.seed(99)

CARD = 'page-card'

categories = ['Q1', 'Q2', 'Q3', 'Q4']

layout = html.Div([
    html.H2("Bar Chart — Stacking Options"),
    html.P("Stack offsets, ordering, and diverging stacked bars.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Standard Stack ---
    html.Div([
        html.H4("Standard Stack (offset: none)"),
        html.P("Default stacking — bars accumulate from zero.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-stack-normal',
            series=[
                {'data': [40, 35, 50, 45], 'label': 'Product A', 'stack': 'revenue', 'color': '#1976d2'},
                {'data': [30, 25, 35, 40], 'label': 'Product B', 'stack': 'revenue', 'color': '#42a5f5'},
                {'data': [20, 30, 25, 20], 'label': 'Product C', 'stack': 'revenue', 'color': '#90caf9'},
            ],
            xAxis=[{'data': categories, 'scaleType': 'band'}],
            yAxis=[{'label': 'Revenue ($k)'}],
            grid={'horizontal': True},
            height=320,
        ),
    ], className=CARD),

    # --- 2. Expand (Normalized to 100%) ---
    html.Div([
        html.H4("Normalized Stack (offset: expand)"),
        html.P("All bars fill to 100% — shows proportions rather than absolute values.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-stack-expand',
            series=[
                {'data': [40, 35, 50, 45], 'label': 'Product A', 'stack': 'revenue', 'stackOffset': 'expand', 'color': '#e65100'},
                {'data': [30, 25, 35, 40], 'label': 'Product B', 'stack': 'revenue', 'stackOffset': 'expand', 'color': '#ff9800'},
                {'data': [20, 30, 25, 20], 'label': 'Product C', 'stack': 'revenue', 'stackOffset': 'expand', 'color': '#ffcc80'},
            ],
            xAxis=[{'data': categories, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=320,
        ),
    ], className=CARD),

    # --- 3. Diverging Stack ---
    html.Div([
        html.H4("Diverging Stack"),
        html.P("Positive values above zero, negative below — useful for sentiment or net scores.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-stack-diverging',
            series=[
                {'data': [20, -10, 30, -5], 'label': 'Gains', 'stack': 'net', 'stackOffset': 'diverging', 'color': '#4caf50'},
                {'data': [-15, 25, -20, 35], 'label': 'Losses', 'stack': 'net', 'stackOffset': 'diverging', 'color': '#f44336'},
            ],
            xAxis=[{'data': categories, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=320,
        ),
    ], className=CARD),

    # --- 4. Multiple Stack Groups ---
    html.Div([
        html.H4("Multiple Stack Groups"),
        html.P("Different stack IDs create separate stacked groups side by side.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-stack-groups',
            series=[
                {'data': [40, 35, 50, 45], 'label': '2024 Online', 'stack': 'year2024', 'color': '#1565c0'},
                {'data': [20, 15, 25, 30], 'label': '2024 Retail', 'stack': 'year2024', 'color': '#42a5f5'},
                {'data': [35, 40, 45, 55], 'label': '2025 Online', 'stack': 'year2025', 'color': '#2e7d32'},
                {'data': [25, 20, 30, 35], 'label': '2025 Retail', 'stack': 'year2025', 'color': '#66bb6a'},
            ],
            xAxis=[{'data': categories, 'scaleType': 'band'}],
            yAxis=[{'label': 'Sales ($k)'}],
            grid={'horizontal': True},
            height=350,
        ),
    ], className=CARD),

    # --- 5. Horizontal Stacked ---
    html.Div([
        html.H4("Horizontal Stacked"),
        html.P("Stacked bars in horizontal layout with rounded corners.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-stack-horizontal',
            series=[
                {'data': [60, 45, 70, 55], 'label': 'Completed', 'stack': 'tasks', 'color': '#4caf50'},
                {'data': [20, 25, 15, 30], 'label': 'In Progress', 'stack': 'tasks', 'color': '#ff9800'},
                {'data': [10, 15, 5, 10], 'label': 'Blocked', 'stack': 'tasks', 'color': '#f44336'},
            ],
            yAxis=[{'data': ['Team A', 'Team B', 'Team C', 'Team D'], 'scaleType': 'band'}],
            layout='horizontal',
            borderRadius=4,
            grid={'vertical': True},
            height=280,
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})
