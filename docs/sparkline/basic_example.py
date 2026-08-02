from dash import html

from dash_mui_charts import SparklineChart

sales_trend = [10, 15, 8, 22, 18, 25, 30, 28, 35, 40, 38, 45]
stock_prices = [142.5, 145.2, 143.8, 148.9, 151.2, 149.5, 155.8, 158.2,
                154.3, 160.1]

component = html.Div(
    [
        html.Div(
            [
                html.Span("Sales Trend: ",
                          style={"marginRight": "10px", "fontWeight": "bold"}),
                SparklineChart(
                    data=sales_trend,
                    width=150,
                    height=30,
                    color="#1976d2",
                ),
            ],
            style={"display": "flex", "alignItems": "center",
                   "marginBottom": "15px"},
        ),
        html.Div(
            [
                html.Span("Stock Price: ",
                          style={"marginRight": "10px", "fontWeight": "bold"}),
                SparklineChart(
                    data=stock_prices,
                    width=150,
                    height=30,
                    color="#4caf50",
                ),
            ],
            style={"display": "flex", "alignItems": "center"},
        ),
    ]
)
