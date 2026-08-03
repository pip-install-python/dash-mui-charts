from dash import html

from dash_mui_charts import BarChart
from docs.barchart_interaction._data import months, revenue


def _variant(chart_id, title, color, mode):
    return html.Div(
        [
            html.P(title, style={'fontWeight': 600, 'fontSize': '13px'}),
            BarChart(
                id=chart_id,
                series=[{'data': revenue, 'label': 'Revenue',
                         'color': color}],
                xAxis=[{'data': months, 'scaleType': 'band'}],
                axisHighlight={'x': mode, 'y': 'none'},
                height=200,
            ),
        ],
        style={'flex': 1},
    )


component = html.Div(
    [
        _variant('bar-int-ax-band', "x: 'band' (default)", '#1976d2', 'band'),
        _variant('bar-int-ax-line', "x: 'line'", '#f57c00', 'line'),
        _variant('bar-int-ax-none', "x: 'none'", '#388e3c', 'none'),
    ],
    style={'display': 'flex', 'gap': '16px'},
)
