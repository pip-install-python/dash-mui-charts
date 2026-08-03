import os

from dash_mui_charts import BarChart
from docs.barchart_pro._data import categories, online, retail, wholesale

MUI_KEY = os.getenv('MUI_PRO_API_KEY', '')

component = BarChart(
    id='bar-pro-stacked-zoom',
    licenseKey=MUI_KEY,
    series=[
        {'data': online, 'label': 'Online', 'stack': 'channel',
         'color': '#1976d2'},
        {'data': retail, 'label': 'Retail', 'stack': 'channel',
         'color': '#42a5f5'},
        {'data': wholesale, 'label': 'Wholesale', 'stack': 'channel',
         'color': '#90caf9'},
    ],
    xAxis=[{
        'data': categories,
        'scaleType': 'band',
        'zoom': {'minSpan': 6},
    }],
    showSlider=True,
    grid={'horizontal': True},
    height=380,
)
