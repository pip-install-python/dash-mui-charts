from dash_mui_charts import BarChart

from docs.barchart_basic._data import months

component = BarChart(
    id='bar-basic-negative',
    series=[
        {'data': [35, -20, 45, -15, 55, -30], 'label': 'Net Change',
         'color': '#00897b'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    grid={'horizontal': True},
    height=300,
)
