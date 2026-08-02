import json

from dash import Input, Output, callback, html

from dash_mui_charts import ScatterChart

component = html.Div(
    [
        ScatterChart(
            id='scatter-click',
            height=300,
            series=[
                {
                    'id': 'series-a',
                    'label': 'A',
                    'data': [
                        {'x': 1, 'y': 5, 'id': 0},
                        {'x': 2, 'y': 3, 'id': 1},
                        {'x': 3, 'y': 8, 'id': 2},
                        {'x': 4, 'y': 2, 'id': 3},
                        {'x': 5, 'y': 7, 'id': 4},
                        {'x': 6, 'y': 4, 'id': 5},
                        {'x': 7, 'y': 9, 'id': 6},
                        {'x': 8, 'y': 1, 'id': 7},
                    ],
                    'color': '#7e57c2',
                    'markerSize': 8,
                    'highlightScope': {'highlight': 'item'},
                },
                {
                    'id': 'series-b',
                    'label': 'B',
                    'data': [
                        {'x': 1.5, 'y': 6, 'id': 0},
                        {'x': 2.5, 'y': 4, 'id': 1},
                        {'x': 3.5, 'y': 7, 'id': 2},
                        {'x': 4.5, 'y': 3, 'id': 3},
                        {'x': 5.5, 'y': 8, 'id': 4},
                        {'x': 6.5, 'y': 5, 'id': 5},
                        {'x': 7.5, 'y': 6, 'id': 6},
                    ],
                    'color': '#26a69a',
                    'markerSize': 8,
                    'highlightScope': {'highlight': 'item'},
                },
            ],
            grid={'horizontal': True},
            voronoiMaxRadius=50,
        ),
        html.H4("Click Data:", style={'marginTop': '15px'}),
        html.Pre(
            id='scatter-click-output',
            children="Click on a scatter point to see event data",
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
    Output('scatter-click-output', 'children'),
    Input('scatter-click', 'clickData'),
    prevent_initial_call=True
)
def display_scatter_click(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on a scatter point to see event data"
