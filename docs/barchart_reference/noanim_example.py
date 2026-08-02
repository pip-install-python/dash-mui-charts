from dash_mui_charts import BarChart

from docs.barchart_reference._data import months, sales

component = BarChart(
    id='bar-ref-noanim',
    series=[
        {'data': sales, 'label': 'Sales', 'color': '#ef6c00'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    skipAnimation=True,
    grid={'horizontal': True},
    height=280,
)
