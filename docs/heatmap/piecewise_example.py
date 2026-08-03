import os

from dash import html

from dash_mui_charts import Heatmap
from docs.heatmap._data import activity_data, days, weeks

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = html.Div(
    [
        Heatmap(
            id='piecewise-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days},
            yAxis={'data': weeks},
            height=300,
            colorScale={
                'type': 'piecewise',
                'thresholds': [3, 5, 7],  # Creates 4 color bands
                'colors': ['#e8f5e9', '#81c784', '#43a047', '#1b5e20'],
            },
        ),
        html.Div(
            [
                html.Span("Legend: ", style={'fontWeight': 'bold',
                                             'marginRight': '10px'}),
                html.Span("0-2 (Low) ",
                          style={'backgroundColor': '#e8f5e9',
                                 'padding': '2px 8px', 'marginRight': '5px'}),
                html.Span("3-4 ",
                          style={'backgroundColor': '#81c784',
                                 'padding': '2px 8px', 'marginRight': '5px'}),
                html.Span("5-6 ",
                          style={'backgroundColor': '#43a047',
                                 'padding': '2px 8px', 'marginRight': '5px',
                                 'color': 'white'}),
                html.Span("7+ (High)",
                          style={'backgroundColor': '#1b5e20',
                                 'padding': '2px 8px', 'color': 'white'}),
            ],
            style={'marginTop': '15px'},
        ),
    ]
)
