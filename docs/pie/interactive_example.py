import json

from dash import Input, Output, callback, html

from dash_mui_charts import PieChart

budget_data = [
    {'id': 0, 'value': 35, 'label': 'Marketing'},
    {'id': 1, 'value': 25, 'label': 'Engineering'},
    {'id': 2, 'value': 20, 'label': 'Sales'},
    {'id': 3, 'value': 15, 'label': 'Support'},
    {'id': 4, 'value': 5, 'label': 'Other'},
]

component = html.Div(
    [
        html.Div(
            PieChart(
                id='interactive-pie',
                data=budget_data,
                innerRadius=40,
                paddingAngle=2,
                cornerRadius=4,
                highlightScope={'highlight': 'item', 'fade': 'global'},
                height=300,
            ),
            style={'flex': '1'},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Click Data",
                                style={'marginTop': 0, 'marginBottom': '10px'}),
                        html.Pre(
                            id='pie-click-data',
                            children='Click on a slice',
                            style={
                                'backgroundColor': '#e3f2fd',
                                'padding': '15px',
                                'borderRadius': '8px',
                                'minHeight': '80px',
                                'fontSize': '13px',
                                'margin': 0,
                            },
                        ),
                    ],
                    style={'marginBottom': '20px'},
                ),
                html.Div(
                    [
                        html.H4("Highlighted Item",
                                style={'marginTop': 0, 'marginBottom': '10px'}),
                        html.Pre(
                            id='pie-highlight-data',
                            children='Hover over a slice',
                            style={
                                'backgroundColor': '#e8f5e9',
                                'padding': '15px',
                                'borderRadius': '8px',
                                'minHeight': '80px',
                                'fontSize': '13px',
                                'margin': 0,
                            },
                        ),
                    ]
                ),
            ],
            style={'flex': '1', 'paddingLeft': '30px'},
        ),
    ],
    style={'display': 'flex', 'alignItems': 'flex-start'},
)


@callback(
    Output('pie-click-data', 'children'),
    Input('interactive-pie', 'clickData'),
    prevent_initial_call=True
)
def display_click_data(click_data):
    if click_data:
        return json.dumps(click_data, indent=2)
    return 'Click on a slice'


@callback(
    Output('pie-highlight-data', 'children'),
    Input('interactive-pie', 'highlightedItem'),
    prevent_initial_call=True
)
def display_highlight_data(highlighted_item):
    if highlighted_item:
        return json.dumps(highlighted_item, indent=2)
    return 'Hover over a slice'
