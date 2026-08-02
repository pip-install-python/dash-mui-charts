from dash_mui_charts import BarChart

categories = ['Q1', 'Q2', 'Q3', 'Q4']

component = BarChart(
    id='bar-stack-diverging',
    series=[
        {'data': [20, -10, 30, -5], 'label': 'Gains', 'stack': 'net',
         'stackOffset': 'diverging', 'color': '#4caf50'},
        {'data': [-15, 25, -20, 35], 'label': 'Losses', 'stack': 'net',
         'stackOffset': 'diverging', 'color': '#f44336'},
    ],
    xAxis=[{'data': categories, 'scaleType': 'band'}],
    grid={'horizontal': True},
    height=320,
)
