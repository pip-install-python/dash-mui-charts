from dash_mui_charts import BarChart

from docs.barchart_dataset._data import product_dataset

component = BarChart(
    id='bar-ds-stacked',
    dataset=product_dataset,
    yAxis=[{'dataKey': 'product', 'scaleType': 'band'}],
    series=[
        {'dataKey': 'q1', 'label': 'Q1', 'stack': 'annual',
         'color': '#5c6bc0'},
        {'dataKey': 'q2', 'label': 'Q2', 'stack': 'annual',
         'color': '#42a5f5'},
        {'dataKey': 'q3', 'label': 'Q3', 'stack': 'annual',
         'color': '#26c6da'},
        {'dataKey': 'q4', 'label': 'Q4', 'stack': 'annual',
         'color': '#66bb6a'},
    ],
    layout='horizontal',
    borderRadius=4,
    grid={'vertical': True},
    height=300,
)
