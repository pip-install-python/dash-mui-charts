from dash_mui_charts import CandlestickChart
from docs.candlestick._data import dates, ohlc_tuples

component = CandlestickChart(
    id='candle-basic',
    series=[{
        'data': ohlc_tuples,
        'upColor': '#4caf50',
        'downColor': '#f44336',
    }],
    xAxis=[{'data': dates, 'label': 'Date'}],
    yAxis=[{'label': 'Price ($)'}],
    grid={'horizontal': True},
    height=400,
)
