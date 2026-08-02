import json

from dash import Input, Output, callback, html

from dash_mui_charts import BarChart
from docs.barchart_interaction._data import PRE_STYLE, expenses, months, revenue

component = html.Div(
    [
        BarChart(
            id='bar-int-click',
            series=[
                {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                {'data': expenses, 'label': 'Expenses', 'color': '#f57c00'},
            ],
            xAxis=[{'data': months, 'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
        html.P("clickData:", style={'fontSize': '12px',
                                    'color': 'var(--mantine-color-dimmed)',
                                    'marginTop': '12px',
                                    'marginBottom': '4px'}),
        html.Pre(id='bar-int-click-out', children='Click a bar...',
                 style=PRE_STYLE),
    ]
)


@callback(
    Output('bar-int-click-out', 'children'),
    Input('bar-int-click', 'clickData'),
    prevent_initial_call=True,
)
def show_click(data):
    if not data:
        return 'Click a bar...'
    return json.dumps(data, indent=2)
