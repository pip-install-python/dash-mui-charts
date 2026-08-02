from dash_mui_charts import BarChart

from docs.barchart_reference._data import months, sales

component = BarChart(
    id='bar-ref-multi',
    series=[
        {'data': sales, 'label': 'Sales', 'color': '#5c6bc0'},
    ],
    xAxis=[{'data': months, 'scaleType': 'band'}],
    referenceLines=[
        {
            'y': min(sales),
            'label': f'Min ({min(sales)})',
            'labelAlign': 'start',
            'lineStyle': {'stroke': '#f44336', 'strokeWidth': 1.5,
                          'strokeDasharray': '4 4'},
            'labelStyle': {'fill': '#f44336', 'fontSize': 11},
        },
        {
            'y': sum(sales) / len(sales),
            'label': f'Avg ({sum(sales) / len(sales):.0f})',
            'labelAlign': 'middle',
            'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2},
            'labelStyle': {'fill': '#ff9800', 'fontSize': 11},
        },
        {
            'y': max(sales),
            'label': f'Max ({max(sales)})',
            'labelAlign': 'end',
            'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 1.5,
                          'strokeDasharray': '4 4'},
            'labelStyle': {'fill': '#4caf50', 'fontSize': 11},
        },
    ],
    grid={'horizontal': True},
    height=350,
)
