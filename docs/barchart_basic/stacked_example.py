from dash_mui_charts import BarChart

from docs.barchart_basic._data import months, organic, paid, referral

component = BarChart(
    id='bar-basic-stacked',
    series=[
        {'data': organic, 'label': 'Organic', 'color': '#66bb6a',
         'stack': 'traffic'},
        {'data': paid, 'label': 'Paid', 'color': '#42a5f5',
         'stack': 'traffic'},
        {'data': referral, 'label': 'Referral', 'color': '#ab47bc',
         'stack': 'traffic'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    yAxis=[{'label': 'Visitors (k)'}],
    grid={'horizontal': True},
    height=300,
)
