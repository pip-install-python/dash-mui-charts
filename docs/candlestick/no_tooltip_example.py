from dash_mui_charts import CandlestickChart
from docs.candlestick._data import dates, ohlc_tuples

component = CandlestickChart(
    id='candle-no-tooltip',
    series=[{
        'data': ohlc_tuples[:10],
        'upColor': '#7b1fa2',
        'downColor': '#e65100',
    }],
    xAxis=[{'data': dates[:10]}],
    tooltip={'trigger': 'none'},
    grid={'horizontal': True},
    height=300,
)
