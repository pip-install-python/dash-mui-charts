from dash_mui_charts import CandlestickChart
from docs.candlestick._data import ohlc_dataset

component = CandlestickChart(
    id='candle-volume',
    dataset=ohlc_dataset,
    series=[{
        'datasetKeys': {'open': 'open', 'high': 'high', 'low': 'low',
                        'close': 'close'},
        'volumeKey': 'volume',
        'upColor': '#4caf50',
        'downColor': '#f44336',
    }],
    xAxis=[{'dataKey': 'date'}],
    yAxis=[{'label': 'Price ($)'}],
    showVolume=True,
    volumeHeightRatio=0.3,
    grid={'horizontal': True},
    height=450,
)
