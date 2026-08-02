from dash import html

from dash_mui_charts import SparklineChart

sales_trend = [10, 15, 8, 22, 18, 25, 30, 28, 35, 40, 38, 45]


def _row(label, curve, color):
    return html.Div(
        [
            html.Span(label, style={"width": "100px",
                                    "display": "inline-block"}),
            SparklineChart(data=sales_trend, width=120, height=30,
                           color=color, curve=curve),
        ],
        style={"marginBottom": "10px"},
    )


component = html.Div(
    [
        _row("Linear: ", "linear", "#1976d2"),
        _row("Natural: ", "natural", "#4caf50"),
        _row("Step: ", "step", "#ff9800"),
        _row("MonotoneX: ", "monotoneX", "#9c27b0"),
    ]
)
