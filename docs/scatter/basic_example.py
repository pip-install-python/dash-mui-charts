from dash_mui_charts import ScatterChart

from docs.scatter._data import cluster_a, cluster_b

component = ScatterChart(
    id='scatter-basic',
    height=350,
    series=[
        {
            'id': 'cluster-a',
            'label': 'Cluster A',
            'data': cluster_a,
            'color': '#1976d2',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
        {
            'id': 'cluster-b',
            'label': 'Cluster B',
            'data': cluster_b,
            'color': '#ff7043',
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
    ],
    grid={'horizontal': True, 'vertical': True},
    xAxis=[{'label': 'X Value'}],
    yAxis=[{'label': 'Y Value', 'width': 50}],
    voronoiMaxRadius=30,
)
