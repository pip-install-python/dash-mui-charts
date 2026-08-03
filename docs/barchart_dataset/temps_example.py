from dash_mui_charts import BarChart

from docs.barchart_dataset._data import temp_dataset

component = BarChart(
    id='bar-ds-temps',
    dataset=temp_dataset,
    xAxis=[{'dataKey': 'month', 'scaleType': 'band'}],
    series=[
        {'dataKey': 'london', 'label': 'London', 'color': '#1976d2'},
        {'dataKey': 'paris', 'label': 'Paris', 'color': '#f57c00'},
        {'dataKey': 'nyc', 'label': 'New York', 'color': '#388e3c'},
        {'dataKey': 'tokyo', 'label': 'Tokyo', 'color': '#d32f2f'},
    ],
    yAxis=[{'label': '°C'}],
    height=380,
    grid={'horizontal': True},
)
