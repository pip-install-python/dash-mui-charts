from dash_mui_charts import BarChart

categories = ['Q1', 'Q2', 'Q3', 'Q4']

component = BarChart(
    id='bar-stack-normal',
    series=[
        {'data': [40, 35, 50, 45], 'label': 'Product A', 'stack': 'revenue',
         'color': '#1976d2'},
        {'data': [30, 25, 35, 40], 'label': 'Product B', 'stack': 'revenue',
         'color': '#42a5f5'},
        {'data': [20, 30, 25, 20], 'label': 'Product C', 'stack': 'revenue',
         'color': '#90caf9'},
    ],
    xAxis=[{'data': categories, 'scaleType': 'band'}],
    yAxis=[{'label': 'Revenue ($k)'}],
    grid={'horizontal': True},
    height=320,
)
