from dash_mui_charts import BarChart

from docs.barchart_reference._data import months, sales

component = BarChart(
    id='bar-ref-target',
    series=[
        {'data': sales, 'label': 'Monthly Sales', 'color': '#1976d2'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    yAxis=[{'label': 'Units Sold'}],
    referenceLines=[
        {
            'y': 60,
            'label': 'Target (60)',
            'labelAlign': 'end',
            'lineStyle': {'stroke': '#f44336', 'strokeWidth': 2,
                          'strokeDasharray': '6 4'},
            'labelStyle': {'fill': '#f44336', 'fontWeight': 'bold',
                           'fontSize': 12},
        },
    ],
    grid={'horizontal': True},
    height=350,
)
