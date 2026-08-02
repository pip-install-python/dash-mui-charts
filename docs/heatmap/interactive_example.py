import json
import os

from dash import Input, Output, callback, html

from dash_mui_charts import Heatmap
from docs.heatmap._data import activity_data, days, weeks

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

component = html.Div(
    [
        Heatmap(
            id='interactive-heatmap',
            licenseKey=MUI_LICENSE_KEY,
            data=activity_data,
            xAxis={'data': days, 'label': 'Day'},
            yAxis={'data': weeks, 'label': 'Week'},
            height=300,
            colorScale={
                'type': 'continuous',
                'min': 0,
                'max': 10,
                'colors': ['#fff3e0', '#ff9800'],
            },
        ),
        html.H4("Click Data:", style={'marginTop': '20px'}),
        html.Pre(
            id='heatmap-click-output',
            children="Click on a cell to see its data",
            style={
                'backgroundColor': '#f5f5f5',
                'padding': '15px',
                'borderRadius': '5px',
                'whiteSpace': 'pre-wrap',
                'fontSize': '12px',
                'overflow': 'auto',
            },
        ),
    ]
)


@callback(
    Output('heatmap-click-output', 'children'),
    Input('interactive-heatmap', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    """Display clicked cell data from heatmap."""
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a cell to see its data"
