from dash_mui_charts import ScatterChart

from docs.scatter._data import log_data_a, log_data_b

component = ScatterChart(
    id='scatter-log',
    height=350,
    series=[
        {
            'id': 'manufacturer-a',
            'label': 'Manufacturer A',
            'data': log_data_a,
            'markerSize': 4,
            'color': '#1565c0',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
        {
            'id': 'manufacturer-b',
            'label': 'Manufacturer B',
            'data': log_data_b,
            'markerSize': 4,
            'color': '#e65100',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
    ],
    xAxis=[{
        'label': 'Year',
        'tickLabelStyle': {'fontSize': 11},
    }],
    yAxis=[{
        'scaleType': 'log',
        'label': 'Density (units/mm²)',
        'width': 65,
        'tickLabelStyle': {'fontSize': 11},
    }],
    grid={'horizontal': True},
    voronoiMaxRadius=25,
)
