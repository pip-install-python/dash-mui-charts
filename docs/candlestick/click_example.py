import json

from dash import Input, Output, callback, html

from dash_mui_charts import CandlestickChart
from docs.candlestick._data import PRE_STYLE, dates, ohlc_tuples

component = html.Div(
    [
        CandlestickChart(
            id='candle-click',
            series=[{
                'data': ohlc_tuples[:15],
                'upColor': '#1976d2',
                'downColor': '#c62828',
            }],
            xAxis=[{'data': dates[:15]}],
            yAxis=[{'label': 'Price ($)'}],
            grid={'horizontal': True},
            height=380,
        ),
        html.P("clickData:", style={'fontSize': '12px',
                                    'color': 'var(--mantine-color-dimmed)',
                                    'marginTop': '12px',
                                    'marginBottom': '4px'}),
        html.Pre(id='candle-click-out', children='Click a candle...',
                 style=PRE_STYLE),
    ]
)


@callback(
    Output('candle-click-out', 'children'),
    Input('candle-click', 'clickData'),
    prevent_initial_call=True,
)
def show_candle_click(data):
    if not data:
        return 'Click a candle...'
    return json.dumps(data, indent=2)
