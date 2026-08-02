from dash_mui_charts import BarChart

from docs.barchart_reference._data import months, sales

component = BarChart(
    id='bar-ref-nolegend',
    series=[
        {'data': sales, 'label': 'Sales', 'color': '#7b1fa2'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    hideLegend=True,
    borderRadius=8,
    grid={'horizontal': True},
    height=280,
)
