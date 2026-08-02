from dash_mui_charts import CandlestickChart
from docs.candlestick._data import ohlc_dataset

component = CandlestickChart(
    id='candle-dataset',
    dataset=ohlc_dataset,
    series=[{
        'datasetKeys': {'open': 'open', 'high': 'high', 'low': 'low',
                        'close': 'close'},
        'upColor': '#26a69a',
        'downColor': '#ef5350',
    }],
    xAxis=[{'dataKey': 'date', 'label': 'Date'}],
    yAxis=[{'label': 'Price ($)'}],
    grid={'horizontal': True},
    height=400,
)
