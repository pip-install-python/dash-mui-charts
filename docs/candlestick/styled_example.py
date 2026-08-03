from dash_mui_charts import CandlestickChart
from docs.candlestick._data import dates, ohlc_tuples

component = CandlestickChart(
    id='candle-styled',
    series=[{
        'data': ohlc_tuples[:15],
        'upColor': '#00bcd4',
        'downColor': '#ff5722',
    }],
    xAxis=[{'data': dates[:15]}],
    yAxis=[{'label': 'Price'}],
    bodyWidthRatio=0.8,
    wickWidth=3,
    grid={'horizontal': True, 'vertical': True},
    height=380,
)
