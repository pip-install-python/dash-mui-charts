from dash_mui_charts import BarChart

categories = ['Q1', 'Q2', 'Q3', 'Q4']

component = BarChart(
    id='bar-stack-expand',
    series=[
        {'data': [40, 35, 50, 45], 'label': 'Product A', 'stack': 'revenue',
         'stackOffset': 'expand', 'color': '#e65100'},
        {'data': [30, 25, 35, 40], 'label': 'Product B', 'stack': 'revenue',
         'stackOffset': 'expand', 'color': '#ff9800'},
        {'data': [20, 30, 25, 20], 'label': 'Product C', 'stack': 'revenue',
         'stackOffset': 'expand', 'color': '#ffcc80'},
    ],
    xAxis=[{'data': categories, 'scaleType': 'band'}],
    grid={'horizontal': True},
    height=320,
)
