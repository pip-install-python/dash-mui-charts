from dash_mui_charts import BarChart

component = BarChart(
    id='bar-basic-rounded',
    series=[
        {'data': [25, 50, 35, 70, 45], 'label': 'Sales'},
    ],
    xAxis=[{'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'scaleType': 'band'}],
    borderRadius=10,
    colors=['#7c4dff'],
    grid={'horizontal': True},
    height=280,
)
