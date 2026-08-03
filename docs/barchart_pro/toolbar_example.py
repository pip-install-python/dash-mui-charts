import os

from dash_mui_charts import BarChart
from docs.barchart_pro._data import categories, weekly_returns, weekly_sales

MUI_KEY = os.getenv('MUI_PRO_API_KEY', '')

component = BarChart(
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
)
