from dash_mui_charts import BarChart

from docs.barchart_reference._data import months, sales

component = BarChart(
    id='bar-ref-vertical',
    series=[
        {'data': sales, 'label': 'Sales', 'color': '#00897b'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    referenceLines=[
        {
            'x': 'May',
            'label': 'New Policy',
            'labelAlign': 'start',
            'lineStyle': {'stroke': '#9c27b0', 'strokeWidth': 2},
            'labelStyle': {'fill': '#9c27b0', 'fontWeight': 'bold',
                           'fontSize': 12},
        },
    ],
    grid={'horizontal': True},
    height=350,
)
