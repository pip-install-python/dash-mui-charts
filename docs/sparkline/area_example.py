from dash import html

from dash_mui_charts import SparklineChart

temperature_week = [72, 75, 78, 82, 79, 74, 71]


def _row(label, spark):
    return html.Div(
        [
            html.Span(label, style={"width": "120px",
                                    "display": "inline-block"}),
            spark,
        ],
        style={"marginBottom": "10px"},
    )


component = html.Div(
    [
        # baseline='min' — fills from the minimum value (default)
        _row("baseline='min': ",
             SparklineChart(data=temperature_week, width=150, height=40,
                            color="#ff9800", area=True, baseline="min")),
        # baseline='max' — fills from the maximum (inverted)
        _row("baseline='max': ",
             SparklineChart(data=temperature_week, width=150, height=40,
                            color="#2196f3", area=True, baseline="max")),
        # baseline=75 — fills from a specific value
        _row("baseline=75: ",
             SparklineChart(data=temperature_week, width=150, height=40,
                            color="#9c27b0", area=True, baseline=75)),
    ]
)
