from dash_mui_charts import ScatterChart

from docs.scatter._data import correlated

component = ScatterChart(
    id='scatter-axis-styling',
    height=400,
    series=[
        {
            'id': 'styled',
            'label': 'Measurements',
            'data': correlated[:40],
            'markerSize': 6,
            'color': '#00897b',
            'highlightScope': {'highlight': 'item', 'fade': 'global'},
        },
    ],
    xAxis=[{
        'label': 'Independent Variable',
        'min': -5,
        'max': 105,
        'tickSize': 8,
        'tickNumber': 10,
        'tickLabelStyle': {
            'fontSize': 11,
            'fontWeight': 'bold',
        },
        'labelStyle': {
            'fontSize': 14,
            'fontWeight': 'bold',
            'fill': '#00897b',
        },
        'domainLimit': 'nice',
    }],
    yAxis=[{
        'label': 'Dependent Variable',
        'width': 65,
        'tickSize': 8,
        'tickLabelStyle': {
            'fontSize': 11,
            'fontWeight': 'bold',
        },
        'labelStyle': {
            'fontSize': 14,
            'fontWeight': 'bold',
            'fill': '#00897b',
        },
        'domainLimit': 'nice',
    }],
    grid={'horizontal': True, 'vertical': True},
    margin={'left': 75, 'bottom': 50, 'right': 20, 'top': 20},
    voronoiMaxRadius=40,
)
