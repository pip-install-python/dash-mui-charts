from dash import html

from dash_mui_charts import PieChart

browser_data = [
    {'id': 0, 'value': 63.5, 'label': 'Chrome'},
    {'id': 1, 'value': 19.2, 'label': 'Safari'},
    {'id': 2, 'value': 4.3, 'label': 'Firefox'},
    {'id': 3, 'value': 3.9, 'label': 'Edge'},
    {'id': 4, 'value': 9.1, 'label': 'Other'},
]

component = html.Div(
    PieChart(
        id='donut-pie',
        data=browser_data,
        innerRadius=60,  # Creates the donut hole
        height=300,
    ),
    style={'display': 'flex', 'justifyContent': 'center'},
)
