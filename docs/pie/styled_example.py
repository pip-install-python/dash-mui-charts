from dash import html

from dash_mui_charts import PieChart

budget_data = [
    {'id': 0, 'value': 35, 'label': 'Marketing'},
    {'id': 1, 'value': 25, 'label': 'Engineering'},
    {'id': 2, 'value': 20, 'label': 'Sales'},
    {'id': 3, 'value': 15, 'label': 'Support'},
    {'id': 4, 'value': 5, 'label': 'Other'},
]

component = html.Div(
    PieChart(
        id='styled-pie',
        data=budget_data,
        paddingAngle=3,     # Gap between slices in degrees
        cornerRadius=8,     # Rounded corners on slices
        colors=['#1976d2', '#dc004e', '#ff9800', '#4caf50', '#9c27b0'],
        height=300,
    ),
    style={'display': 'flex', 'justifyContent': 'center'},
)
