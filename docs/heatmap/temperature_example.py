import os

from dash_mui_charts import Heatmap
from docs.heatmap._data import hours, temp_days, temperature_data

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = Heatmap(
    id='temperature-heatmap',
    licenseKey=MUI_LICENSE_KEY,
    data=temperature_data,
    xAxis={'data': temp_days, 'label': 'Day'},
    yAxis={'data': hours, 'label': 'Time'},
    height=350,
    colorScale={
        'type': 'continuous',
        'min': 50,
        'max': 90,
        'colors': ['#42a5f5', '#ffeb3b', '#f44336'],  # Blue-Yellow-Red
    },
)
