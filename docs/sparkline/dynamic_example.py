from dash import Input, Output, callback, dcc, html

from dash_mui_charts import SparklineChart

revenue_data = [42, 45, 48, 52, 49, 55, 58, 62, 60, 65]
users_data = [1200, 1350, 1420, 1580, 1520, 1680, 1750, 1890, 1820, 1950]
sessions_data = [3500, 3800, 4100, 4500, 4200, 4800, 5100, 5400, 5200, 5600]
error_rates = [2, 5, 3, 8, 4, 2, 1, 3, 2, 4]

component = html.Div(
    [
        html.Div(
            [
                html.Label("Select Metric:",
                           style={"marginRight": "10px",
                                  "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="metric-selector",
                    options=[
                        {"label": "Revenue", "value": "revenue"},
                        {"label": "Users", "value": "users"},
                        {"label": "Sessions", "value": "sessions"},
                        {"label": "Errors", "value": "errors"},
                    ],
                    value="revenue",
                    style={"width": "200px"},
                    clearable=False,
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                html.Div(id="dynamic-metric-label", children="Revenue Trend",
                         style={"fontSize": "14px", "color": "#666",
                                "marginBottom": "5px"}),
                html.Div(id="dynamic-metric-value", children="$65K",
                         style={"fontSize": "32px", "fontWeight": "bold",
                                "marginBottom": "10px"}),
                html.Div(id="dynamic-sparkline-container"),
            ],
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "width": "300px",
            },
        ),
    ]
)


@callback(
    Output("dynamic-sparkline-container", "children"),
    Output("dynamic-metric-label", "children"),
    Output("dynamic-metric-value", "children"),
    Input("metric-selector", "value"),
)
def update_dynamic_sparkline(metric):
    """Update sparkline based on selected metric."""
    data_map = {
        "revenue": (revenue_data, "#4caf50", "Revenue Trend",
                    f"${revenue_data[-1]}K"),
        "users": (users_data, "#2196f3", "Active Users",
                  f"{users_data[-1]:,}"),
        "sessions": (sessions_data, "#ff9800", "Sessions",
                     f"{sessions_data[-1]:,}"),
        "errors": (error_rates, "#f44336", "Error Rate",
                   str(error_rates[-1])),
    }
    data, color, label, value = data_map[metric]

    return SparklineChart(
        data=data,
        width=260,
        height=50,
        color=color,
        area=True,
        showHighlight=True,
        showTooltip=True,
    ), label, value
