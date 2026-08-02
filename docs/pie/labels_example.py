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
        id='labeled-pie',
        data=budget_data,
        arcLabel='value',      # Options: 'value', 'label', 'formattedValue'
        arcLabelMinAngle=30,   # Hide labels on slices < 30 degrees
        height=300,
    ),
    style={'display': 'flex', 'justifyContent': 'center'},
)
