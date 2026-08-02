from dash import html

from dash_mui_charts import SparklineChart

error_rates = [2, 5, 3, 8, 4, 2, 1, 3, 2, 4]

component = html.Div(
    [
        html.Div(
            [
                html.Span("Daily Errors: ",
                          style={"marginRight": "10px", "fontWeight": "bold"}),
                SparklineChart(
                    data=error_rates,
                    width=150,
                    height=40,
                    plotType="bar",
                    color="#f44336",
                ),
            ],
            style={"display": "flex", "alignItems": "center",
                   "marginBottom": "15px"},
        ),
        html.Div(
            [
                html.Span("Weekly Sales: ",
                          style={"marginRight": "10px", "fontWeight": "bold"}),
                SparklineChart(
                    data=[120, 145, 132, 168, 155, 142, 178],
                    width=150,
                    height=40,
                    plotType="bar",
                    color="#2196f3",
                ),
            ],
            style={"display": "flex", "alignItems": "center"},
        ),
    ]
)
