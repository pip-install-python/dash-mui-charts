from dash_mui_charts import BarChart

from docs.barchart_basic._data import months, revenue

component = BarChart(
    id='bar-basic-horizontal',
    series=[{'data': revenue, 'label': 'Revenue ($k)', 'color': '#1976d2'}],
    yAxis=[{'data': months, 'scaleType': 'band'}],
    xAxis=[{'label': 'Amount ($k)'}],
    layout='horizontal',
    borderRadius=6,
    grid={'vertical': True},
    height=300,
)
