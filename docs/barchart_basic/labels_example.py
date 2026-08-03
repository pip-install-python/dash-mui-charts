from dash_mui_charts import BarChart

component = BarChart(
    id='bar-basic-labels',
    series=[
        {'data': [4, 3, 5], 'barLabel': 'value',
         'barLabelPlacement': 'outside', 'label': 'Outside'},
        {'data': [2, 5, 6], 'barLabel': 'value',
         'barLabelPlacement': 'center', 'label': 'Center'},
        {'data': [3, 4, 2], 'label': 'No label'},
    ],
    xAxis=[{'data': ['Group A', 'Group B', 'Group C'], 'scaleType': 'band'}],
    height=300,
    grid={'horizontal': True},
)
