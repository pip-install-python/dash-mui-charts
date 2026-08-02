from dash_mui_charts import BarChart

component = BarChart(
    id='bar-stack-horizontal',
    series=[
        {'data': [60, 45, 70, 55], 'label': 'Completed', 'stack': 'tasks',
         'color': '#4caf50'},
        {'data': [20, 25, 15, 30], 'label': 'In Progress', 'stack': 'tasks',
         'color': '#ff9800'},
        {'data': [10, 15, 5, 10], 'label': 'Blocked', 'stack': 'tasks',
         'color': '#f44336'},
    ],
    yAxis=[{'data': ['Team A', 'Team B', 'Team C', 'Team D'],
            'scaleType': 'band'}],
    layout='horizontal',
    borderRadius=4,
    grid={'vertical': True},
    height=280,
)
