from dash_mui_charts import ScatterChart

from docs.scatter._data import correlated

component = ScatterChart(
    id='scatter-colormap',
    height=400,
    series=[
        {
            'id': 'correlated',
            'label': 'Data Points',
            'data': correlated,
            'markerSize': 5,
        },
    ],
    xAxis=[{
        'label': 'X Value',
        'min': -5,
        'max': 105,
    }],
    yAxis=[{
        'label': 'Y Value (2x + 20 + noise)',
        'width': 60,
        'domainLimit': 'nice',
    }],
    zAxis=[{
        'colorMap': {
            'type': 'continuous',
            'min': 30,
            'max': 300,
            'color': ['#4fc3f7', '#e53935'],
        },
    }],
    grid={'horizontal': True, 'vertical': True},
    voronoiMaxRadius=40,
)
