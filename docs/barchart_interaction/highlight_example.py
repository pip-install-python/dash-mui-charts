import json

from dash import Input, Output, callback, html

from dash_mui_charts import BarChart
from docs.barchart_interaction._data import PRE_STYLE

component = html.Div(
    [
        BarChart(
            id='bar-int-highlight',
            series=[
                {'data': [4, 3, 5, 7, 6], 'label': 'Alpha',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'},
                 'color': '#5c6bc0'},
                {'data': [2, 5, 6, 3, 4], 'label': 'Beta',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'},
                 'color': '#26a69a'},
                {'data': [3, 4, 2, 5, 3], 'label': 'Gamma',
                 'highlightScope': {'highlight': 'series', 'fade': 'global'},
                 'color': '#ef5350'},
            ],
            xAxis=[{'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                    'scaleType': 'band'}],
            grid={'horizontal': True},
            height=300,
        ),
        html.P("highlightedItem:", style={'fontSize': '12px',
                                          'color': 'var(--mantine-color-dimmed)',
                                          'marginTop': '12px',
                                          'marginBottom': '4px'}),
        html.Pre(id='bar-int-highlight-out', children='Hover over a bar...',
                 style=PRE_STYLE),
    ]
)


@callback(
    Output('bar-int-highlight-out', 'children'),
    Input('bar-int-highlight', 'highlightedItem'),
    prevent_initial_call=True,
)
def show_highlight(data):
    if not data:
        return 'Hover over a bar...'
    return json.dumps(data, indent=2)
