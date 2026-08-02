import os

from dash import html

from dash_mui_charts import BarChart
from docs.barchart_pro._data import categories, weekly_sales

MUI_KEY = os.getenv('MUI_PRO_API_KEY', '')

component = html.Div(
    [
        # License posture, stated in-page either way: the keyless banner is
        # what tests/test_pages_smoke.py BANNER_ROUTES asserts.
        html.P(
            "⚠️ Set MUI_PRO_API_KEY environment variable to enable Pro "
            "features." if not MUI_KEY else "✓ Pro license key detected.",
            style={'color': 'var(--mantine-color-orange-6)' if not MUI_KEY
                   else 'var(--mantine-color-green-7)',
                   'fontWeight': 600},
        ),
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
            initialZoom=[{'axisId': 'auto-generated-id-0',
                          'start': 0, 'end': 40}],
            grid={'horizontal': True},
            height=400,
        ),
    ]
)
