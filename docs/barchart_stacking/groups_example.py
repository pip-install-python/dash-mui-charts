from dash_mui_charts import BarChart

categories = ['Q1', 'Q2', 'Q3', 'Q4']

component = BarChart(
    id='bar-stack-groups',
    series=[
        {'data': [40, 35, 50, 45], 'label': '2024 Online',
         'stack': 'year2024', 'color': '#1565c0'},
        {'data': [20, 15, 25, 30], 'label': '2024 Retail',
         'stack': 'year2024', 'color': '#42a5f5'},
        {'data': [35, 40, 45, 55], 'label': '2025 Online',
         'stack': 'year2025', 'color': '#2e7d32'},
        {'data': [25, 20, 30, 35], 'label': '2025 Retail',
         'stack': 'year2025', 'color': '#66bb6a'},
    ],
    xAxis=[{'data': categories, 'scaleType': 'band'}],
    yAxis=[{'label': 'Sales ($k)'}],
    grid={'horizontal': True},
    height=350,
)
