import os

from dash_mui_charts import Heatmap
from docs.heatmap._data import activity_data, days, weeks

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = Heatmap(
    id='custom-cell-heatmap',
    licenseKey=MUI_LICENSE_KEY,
    data=activity_data,
    xAxis={'data': days},
    yAxis={'data': weeks},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 10,
        'colors': ['#fce4ec', '#c2185b'],  # Pink gradient
    },
    cellStyle={
        'gap': 6,               # Space between cells
        'borderRadius': 8,      # Rounded corners
        'showValue': True,      # Display value in cell
        'fontSize': 14,         # Text size
        'fontWeight': 600,      # Text weight
        'textColor': '#ffffff',  # Text color
    },
    highlightScope={'highlight': 'item'},
)
