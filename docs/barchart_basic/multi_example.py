from dash_mui_charts import BarChart

from docs.barchart_basic._data import expenses, months, profit, revenue

component = BarChart(
    id='bar-basic-multi',
    series=[
        {'data': revenue, 'label': 'Revenue ($k)', 'color': '#1976d2'},
        {'data': expenses, 'label': 'Expenses ($k)', 'color': '#f57c00'},
        {'data': profit, 'label': 'Profit ($k)', 'color': '#388e3c'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band', 'label': 'Month'}],
    yAxis=[{'label': 'Amount ($k)'}],
    grid={'horizontal': True},
    height=350,
)
