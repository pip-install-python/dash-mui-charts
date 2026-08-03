from dash_mui_charts import BarChart

from docs.barchart_dataset._data import temp_dataset

component = BarChart(
    id='bar-ds-gaps',
    dataset=temp_dataset,
    xAxis=[{
        'dataKey': 'month',
        'scaleType': 'band',
        'categoryGapRatio': 0.4,
        'barGapRatio': 0.1,
    }],
    series=[
        {'dataKey': 'london', 'label': 'London', 'color': '#1565c0'},
        {'dataKey': 'tokyo', 'label': 'Tokyo', 'color': '#c62828'},
    ],
    yAxis=[{'label': '°C'}],
    height=320,
    grid={'horizontal': True},
)
