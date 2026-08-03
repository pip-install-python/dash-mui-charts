from dash import html

from dash_mui_charts import PieChart

task_data = [
    {'id': 0, 'value': 72, 'label': 'Completed'},
    {'id': 1, 'value': 28, 'label': 'Remaining'},
]

component = html.Div(
    PieChart(
        id='gauge-pie',
        data=task_data,
        startAngle=-90,    # Start at 12 o'clock
        endAngle=90,       # End at 6 o'clock (half circle)
        innerRadius=50,    # Donut style
        colors=['#4caf50', '#e0e0e0'],
        height=200,
    ),
    style={'display': 'flex', 'justifyContent': 'center'},
)
