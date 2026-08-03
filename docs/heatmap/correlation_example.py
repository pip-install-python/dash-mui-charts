import os

from dash_mui_charts import Heatmap
from docs.heatmap._data import correlation_data, variables

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Correlation values range from -1 to 1 — a diverging red-white-blue scale.
component = Heatmap(
    id='correlation-heatmap',
    licenseKey=MUI_LICENSE_KEY,
    data=correlation_data,
    xAxis={'data': variables},
    yAxis={'data': variables},
    height=400,
    colorScale={
        'type': 'continuous',
        'min': -1,
        'max': 1,
        'colors': ['#d32f2f', '#fff', '#1976d2'],  # Red to White to Blue
    },
    margin={'left': 100, 'right': 20, 'top': 20, 'bottom': 80},
)
