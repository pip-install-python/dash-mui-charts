import os

from dash_mui_charts import Heatmap
from docs.heatmap._data import activity_data, days, weeks

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = Heatmap(
    id='rounded-heatmap',
    licenseKey=MUI_LICENSE_KEY,
    data=activity_data,
    xAxis={'data': days, 'label': 'Day of Week'},
    yAxis={'data': weeks, 'label': 'Week'},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 10,
        'colors': ['#e8f5e9', '#2e7d32'],
    },
    cellStyle='rounded',  # Enable rounded corners with gap
    highlightScope={'highlight': 'item'},  # Highlight on hover
)
