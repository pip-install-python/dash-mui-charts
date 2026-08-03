from dash import html

from dash_mui_charts import BarChart
from docs.barchart_interaction._data import expenses, months, revenue


def _variant(chart_id, title, trigger):
    return html.Div(
        [
            html.P(title, style={'fontWeight': 600, 'fontSize': '13px'}),
            BarChart(
                id=chart_id,
                series=[
                    {'data': revenue, 'label': 'Revenue', 'color': '#1976d2'},
                    {'data': expenses, 'label': 'Expenses',
                     'color': '#f57c00'},
                ],
                xAxis=[{'data': months, 'scaleType': 'band'}],
                tooltip={'trigger': trigger},
                height=250,
            ),
        ],
        style={'flex': 1},
    )


component = html.Div(
    [
        _variant('bar-int-tt-axis', "trigger: 'axis' (default)", 'axis'),
        _variant('bar-int-tt-item', "trigger: 'item'", 'item'),
    ],
    style={'display': 'flex', 'gap': '16px'},
)
