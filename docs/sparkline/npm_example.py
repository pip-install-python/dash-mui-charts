from dash import Input, Output, callback, html

from dash_mui_charts import SparklineChart

weekly_downloads = [
    125430, 142350, 138200, 156780, 162340, 158900, 171200,
    168500, 175600, 182300, 178900, 195400,
]
weeks = [
    'Dec 1-7', 'Dec 8-14', 'Dec 15-21', 'Dec 22-28',
    'Dec 29-Jan 4', 'Jan 5-11', 'Jan 12-18',
    'Jan 19-25', 'Jan 26-Feb 1', 'Feb 2-8', 'Feb 9-15', 'Feb 16-22',
]

component = html.Div(
    html.Div(
        [
            html.Div(
                [
                    html.Span("📦 ", style={"marginRight": "5px"}),
                    html.Span(
                        id="npm-week-label",
                        children="Weekly Downloads",
                        style={"color": "#666", "fontSize": "14px"},
                    ),
                ],
                style={"marginBottom": "8px"},
            ),
            html.Div(
                [
                    html.Span(
                        id="npm-download-count",
                        children=f"{weekly_downloads[-1]:,}",
                        style={"fontSize": "28px", "fontWeight": "bold",
                               "color": "#333"},
                    ),
                    html.Div(
                        SparklineChart(
                            id="npm-sparkline",
                            data=weekly_downloads,
                            width=200,
                            height=45,
                            color="rgb(137, 86, 255)",
                            area=True,
                            showHighlight=True,
                            baseline="min",
                            margin={"top": 5, "right": 0, "bottom": 0,
                                    "left": 4},
                            xAxis={"id": "week-axis", "data": weeks},
                            axisHighlight={"x": "line"},
                            slotProps={"lineHighlight": {"r": 4}},
                            clipAreaOffset={"top": 2, "bottom": 2},
                        ),
                        style={"marginLeft": "auto"},
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "flex-end",
                    "justifyContent": "space-between",
                    "borderBottom": "2px solid rgba(137, 86, 255, 0.2)",
                    "paddingBottom": "5px",
                },
            ),
        ],
        style={
            "width": "350px",
            "backgroundColor": "white",
            "padding": "15px 20px",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
        },
    )
)


@callback(
    Output("npm-download-count", "children"),
    Output("npm-week-label", "children"),
    Input("npm-sparkline", "hoverIndex"),
    Input("npm-sparkline", "hoverValue"),
    prevent_initial_call=True,
)
def update_npm_display(hover_index, hover_value):
    """Update npm-style display based on hover."""
    if hover_index is not None and hover_value is not None:
        return f"{int(hover_value):,}", weeks[hover_index]
    return f"{weekly_downloads[-1]:,}", "Weekly Downloads"
