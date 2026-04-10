"""
BarChart Demo - Pro Features
Zoom, toolbar, slider, and brush (requires MUI Pro license key).
"""

import os
import random

import dash
from dash import html

dash.register_page(__name__, path='/barchart-pro', name='Bar Chart - Pro')

from dash_mui_charts import BarChart

random.seed(42)

CARD = 'page-card'

MUI_KEY = os.getenv('MUI_PRO_API_KEY', '')

# Large dataset for zoom demos
categories = [f'W{i+1}' for i in range(52)]
weekly_sales = [random.randint(20, 100) for _ in categories]
weekly_returns = [random.randint(2, 20) for _ in categories]

layout = html.Div([
    html.H2("Bar Chart — Pro Features"),
    html.P("Zoom, slider, toolbar, and brush selection. Requires MUI_PRO_API_KEY env variable.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    html.Div(
        html.P(
            "⚠️ Set MUI_PRO_API_KEY environment variable to enable Pro features." if not MUI_KEY
            else "✓ Pro license key detected.",
            style={'color': 'var(--mantine-color-orange-6)' if not MUI_KEY else 'var(--mantine-color-green-7)', 'fontWeight': 600},
        ),
        className=CARD,
        style={'background': 'var(--mantine-color-body)' if not MUI_KEY else 'var(--mantine-color-body)'},
    ),

    # --- 1. Zoom with Slider ---
    html.Div([
        html.H4("Zoom with Slider"),
        html.P("52 weeks of data with a zoom slider. Drag the slider or use mouse wheel to zoom.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-pro-slider',
            licenseKey=MUI_KEY,
            series=[
                {'data': weekly_sales, 'label': 'Sales', 'color': '#1976d2'},
            ],
            xAxis=[{
                'data': categories,
                'scaleType': 'band',
                'zoom': {'minSpan': 8},
                'label': 'Week',
            }],
            yAxis=[{'label': 'Units'}],
            showSlider=True,
            initialZoom=[{'axisId': 'auto-generated-id-0', 'start': 0, 'end': 40}],
            grid={'horizontal': True},
            height=400,
        ),
    ], className=CARD),

    # --- 2. Multi-Series Zoom + Toolbar ---
    html.Div([
        html.H4("Zoom + Toolbar"),
        html.P("Toolbar with zoom in/out buttons and export options.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-pro-toolbar',
            licenseKey=MUI_KEY,
            series=[
                {'data': weekly_sales, 'label': 'Sales', 'color': '#1565c0'},
                {'data': weekly_returns, 'label': 'Returns', 'color': '#c62828'},
            ],
            xAxis=[{
                'data': categories,
                'scaleType': 'band',
                'zoom': {'minSpan': 5},
            }],
            showSlider=True,
            showToolbar=True,
            grid={'horizontal': True},
            height=420,
        ),
    ], className=CARD),

    # --- 3. Stacked Zoom ---
    html.Div([
        html.H4("Stacked with Zoom"),
        html.P("Stacked bars with zoom and slider.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        BarChart(
            id='bar-pro-stacked-zoom',
            licenseKey=MUI_KEY,
            series=[
                {'data': [random.randint(10, 40) for _ in categories], 'label': 'Online', 'stack': 'channel', 'color': '#1976d2'},
                {'data': [random.randint(5, 30) for _ in categories], 'label': 'Retail', 'stack': 'channel', 'color': '#42a5f5'},
                {'data': [random.randint(3, 15) for _ in categories], 'label': 'Wholesale', 'stack': 'channel', 'color': '#90caf9'},
            ],
            xAxis=[{
                'data': categories,
                'scaleType': 'band',
                'zoom': {'minSpan': 6},
            }],
            showSlider=True,
            grid={'horizontal': True},
            height=380,
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})
