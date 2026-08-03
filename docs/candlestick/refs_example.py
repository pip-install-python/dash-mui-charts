from dash_mui_charts import CandlestickChart
from docs.candlestick._data import dates, ohlc_tuples

component = CandlestickChart(
    id='candle-refs',
    series=[{
        'data': ohlc_tuples,
        'upColor': '#4caf50',
        'downColor': '#f44336',
    }],
    xAxis=[{'data': dates}],
    yAxis=[{'label': 'Price ($)'}],
    referenceLines=[
        {
            'y': max(d[1] for d in ohlc_tuples),
            'label': 'Resistance',
            'labelAlign': 'end',
            'lineStyle': {'stroke': '#f44336', 'strokeWidth': 1.5,
                          'strokeDasharray': '6 4'},
            'labelStyle': {'fill': '#f44336', 'fontSize': 11},
        },
        {
            'y': min(d[2] for d in ohlc_tuples),
            'label': 'Support',
            'labelAlign': 'end',
            'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 1.5,
                          'strokeDasharray': '6 4'},
            'labelStyle': {'fill': '#4caf50', 'fontSize': 11},
        },
        {
            'y': sum(d[3] for d in ohlc_tuples) / len(ohlc_tuples),
            'label': 'Avg Close',
            'labelAlign': 'start',
            'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 1},
            'labelStyle': {'fill': '#ff9800', 'fontSize': 11},
        },
    ],
    grid={'horizontal': True},
    height=420,
)
