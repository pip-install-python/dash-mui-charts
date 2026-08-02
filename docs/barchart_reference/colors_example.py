from dash_mui_charts import BarChart

component = BarChart(
    id='bar-ref-colors',
    series=[
        {'data': [30, 45, 35], 'label': 'East'},
        {'data': [25, 50, 40], 'label': 'West'},
        {'data': [40, 30, 55], 'label': 'Central'},
    ],
    xAxis=[{'data': ['2023', '2024', '2025'], 'scaleType': 'band'}],
    colors=['#ff6f00', '#00bfa5', '#6200ea'],
    grid={'horizontal': True},
    height=300,
)
