import json

from dash import Input, Output, callback, html

from dash_mui_charts import SparklineChart

stock_prices = [142.5, 145.2, 143.8, 148.9, 151.2, 149.5, 155.8, 158.2,
                154.3, 160.1]

component = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Span("Stock Price: ",
                                  style={"fontWeight": "bold"}),
                        html.Span(id="stock-price-display",
                                  children=f"${stock_prices[-1]:.2f}"),
                    ],
                    style={"marginBottom": "10px"},
                ),
                SparklineChart(
                    id="interactive-stock-sparkline",
                    data=stock_prices,
                    width=300,
                    height=60,
                    color="#1976d2",
                    area=True,
                    showTooltip=True,
                    showHighlight=True,
                    xAxis={"id": "stock-axis",
                           "data": ["Day 1", "Day 2", "Day 3", "Day 4",
                                    "Day 5", "Day 6", "Day 7", "Day 8",
                                    "Day 9", "Day 10"]},
                    axisHighlight={"x": "line"},
                ),
            ]
        ),
        html.Div(
            [
                html.Strong("Hover Data:"),
                html.Pre(
                    id="stock-hover-output",
                    children="Hover over the chart to see details",
                    style={
                        "backgroundColor": "#f5f5f5",
                        "padding": "15px",
                        "borderRadius": "5px",
                        "whiteSpace": "pre-wrap",
                        "fontSize": "12px",
                        "overflow": "auto",
                        "marginTop": "10px",
                        "minHeight": "60px",
                    },
                ),
            ],
            style={"marginTop": "15px"},
        ),
    ]
)


@callback(
    Output("stock-price-display", "children"),
    Output("stock-hover-output", "children"),
    Input("interactive-stock-sparkline", "hoverIndex"),
    Input("interactive-stock-sparkline", "hoverValue"),
    prevent_initial_call=True,
)
def update_stock_display(index, value):
    """Update stock price display based on hover."""
    if index is not None and value is not None:
        return f"${value:.2f}", json.dumps({
            "index": index,
            "value": value,
            "day": f"Day {index + 1}",
        }, indent=2)
    return f"${stock_prices[-1]:.2f}", "Hover over the chart to see details"
