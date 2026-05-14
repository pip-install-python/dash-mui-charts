# File: docs/dash_mui_charts/bar_basic.py
"""Bar Charts — Basic examples: vertical, horizontal, stacked, dataset mode, labels, border radius."""

import os
import random
import json
import dash_mantine_components as dmc
from dash import html, callback, Input, Output
from dash_mui_charts import BarChart

MUI_KEY = os.getenv('MUI_PRO_API_KEY', '')
random.seed(42)

GLASS = {
    "background": "light-dark(rgba(255,255,255,0.55), rgba(30,30,30,0.55))",
    "backdropFilter": "blur(16px) saturate(1.8)",
    "WebkitBackdropFilter": "blur(16px) saturate(1.8)",
    "border": "1px solid light-dark(rgba(255,255,255,0.5), rgba(255,255,255,0.08))",
}

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [random.randint(30, 90) for _ in months]
expenses = [random.randint(20, 65) for _ in months]
profit = [r - e for r, e in zip(revenue, expenses)]

component = dmc.Stack([
    dmc.Text("Bar Charts", fw=700, size="xl"),
    dmc.Text("Compare discrete categories with vertical, horizontal, and stacked bar charts.", size="sm", c="dimmed"),

    # --- Basic Vertical ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Multi-Series Bar Chart", fw=600),
            dmc.Text("Revenue, expenses, and profit by month.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-basic",
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
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Stacked ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Stacked Bar Chart", fw=600),
            dmc.Text("Traffic sources stacked per month.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-stacked",
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
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Horizontal ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Horizontal Bar Chart", fw=600),
            dmc.Text("Rainfall data displayed horizontally with border radius.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-horizontal",
                series=[{'data': revenue, 'label': 'Revenue ($k)', 'color': '#1976d2'}],
                yAxis=[{'data': months, 'scaleType': 'band'}],
                xAxis=[{'label': 'Amount ($k)'}],
                layout='horizontal',
                borderRadius=6,
                grid={'vertical': True},
                height=300,
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Dataset Mode ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Dataset Mode", fw=600),
            dmc.Text("Using dataset prop with dataKey references — no data duplication.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-dataset",
                dataset=[
                    {'month': 'Jan', 'london': 18, 'paris': 15, 'nyc': 12},
                    {'month': 'Feb', 'london': 22, 'paris': 18, 'nyc': 15},
                    {'month': 'Mar', 'london': 30, 'paris': 25, 'nyc': 22},
                    {'month': 'Apr', 'london': 45, 'paris': 38, 'nyc': 35},
                    {'month': 'May', 'london': 55, 'paris': 48, 'nyc': 45},
                    {'month': 'Jun', 'london': 60, 'paris': 55, 'nyc': 52},
                ],
                xAxis=[{'dataKey': 'month', 'scaleType': 'band'}],
                series=[
                    {'dataKey': 'london', 'label': 'London'},
                    {'dataKey': 'paris', 'label': 'Paris'},
                    {'dataKey': 'nyc', 'label': 'New York'},
                ],
                height=350,
                grid={'horizontal': True},
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Bar Labels ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Bar Labels", fw=600),
            dmc.Text("Display values directly on bars with center and outside placement.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-labels",
                series=[
                    {'data': [4, 3, 5], 'barLabel': 'value', 'barLabelPlacement': 'outside', 'label': 'Outside'},
                    {'data': [2, 5, 6], 'barLabel': 'value', 'barLabelPlacement': 'center', 'label': 'Center'},
                    {'data': [3, 4, 2], 'label': 'No label'},
                ],
                xAxis=[{'data': ['Group A', 'Group B', 'Group C'], 'scaleType': 'band'}],
                height=300,
                grid={'horizontal': True},
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Click Events ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Click Events", fw=600),
            dmc.Text("Click any bar to capture data via the clickData output prop.", size="sm", c="dimmed"),
            BarChart(
                id="mc-bar-click",
                series=[
                    {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                    {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
                ],
                xAxis=[{'data': months, 'scaleType': 'band'}],
                height=300,
                grid={'horizontal': True},
            ),
            dmc.Text("Click output:", size="xs", c="dimmed"),
            html.Pre(
                id="mc-bar-click-out",
                children="Click a bar...",
                style={
                    "fontSize": "11px", "margin": 0,
                    "padding": "8px 12px", "borderRadius": "6px",
                    "background": "light-dark(#f8f9fa, #1a1b1e)",
                    "border": "1px solid light-dark(#dee2e6, #373a40)",
                },
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),
], gap="lg")


@callback(
    Output("mc-bar-click-out", "children"),
    Input("mc-bar-click", "clickData"),
    prevent_initial_call=True,
)
def show_click(data):
    if not data:
        return "Click a bar..."
    return json.dumps(data, indent=2)
