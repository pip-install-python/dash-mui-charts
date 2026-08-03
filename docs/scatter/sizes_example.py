from dash_mui_charts import ScatterChart

from docs.scatter._data import size_data_large, size_data_small

component = ScatterChart(
    id='scatter-sizes',
    height=300,
    series=[
        {
            'id': 'small-markers',
            'label': 'Background (r=3)',
            'data': size_data_large,
            'color': '#90caf9',
            'markerSize': 3,
        },
        {
            'id': 'large-markers',
            'label': 'Focus Points (r=10)',
            'data': size_data_small,
            'color': '#e53935',
            'markerSize': 10,
            'highlightScope': {'highlight': 'item', 'fade': 'global'},
        },
    ],
    xAxis=[{'label': 'X', 'min': 0, 'max': 100}],
    yAxis=[{'label': 'Y', 'min': 0, 'max': 100, 'width': 40}],
)
