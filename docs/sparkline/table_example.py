from dash import html

from dash_mui_charts import SparklineChart

_th = {"textAlign": "left", "padding": "12px",
       "borderBottom": "2px solid #ddd"}
_td = {"padding": "12px"}
_num = {"textAlign": "right", "padding": "12px", "fontWeight": "bold"}
_mid = {"textAlign": "center", "padding": "12px"}


def _spark_row(metric, current, spark, change, change_color):
    return html.Tr(
        [
            html.Td(metric, style=_td),
            html.Td(current, style=_num),
            html.Td(spark, style=_mid),
            html.Td(change, style={"textAlign": "right", "padding": "12px",
                                   "color": change_color}),
        ]
    )


component = html.Table(
    [
        html.Thead(
            html.Tr(
                [
                    html.Th("Metric", style=_th),
                    html.Th("Current", style={**_th, "textAlign": "right"}),
                    html.Th("Trend (7 days)",
                            style={**_th, "textAlign": "center"}),
                    html.Th("Change", style={**_th, "textAlign": "right"}),
                ]
            )
        ),
        html.Tbody(
            [
                _spark_row(
                    "Revenue", "$45,230",
                    SparklineChart(data=[38, 42, 40, 44, 43, 45, 45],
                                   width=100, height=25, color="#4caf50",
                                   area=True),
                    "+12%", "#4caf50",
                ),
                _spark_row(
                    "Users", "2,847",
                    SparklineChart(data=[2200, 2350, 2400, 2500, 2650, 2750,
                                         2847],
                                   width=100, height=25, color="#2196f3",
                                   area=True),
                    "+29%", "#4caf50",
                ),
                _spark_row(
                    "Errors", "23",
                    SparklineChart(data=[45, 38, 42, 35, 30, 28, 23],
                                   width=100, height=25, color="#f44336"),
                    "-49%", "#4caf50",
                ),
                _spark_row(
                    "Response Time", "245ms",
                    SparklineChart(data=[220, 235, 242, 238, 250, 248, 245],
                                   width=100, height=25, color="#ff9800"),
                    "+11%", "#f44336",
                ),
            ]
        ),
    ],
    style={"width": "100%", "borderCollapse": "collapse", "marginTop": "10px"},
)
