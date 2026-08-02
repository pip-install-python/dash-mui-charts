from dash import Input, Output, callback, html

from dash_mui_charts import SparklineChart

revenue_data = [42, 45, 48, 52, 49, 55, 58, 62, 60, 65]
users_data = [1200, 1350, 1420, 1580, 1520, 1680, 1750, 1890, 1820, 1950]
sessions_data = [3500, 3800, 4100, 4500, 4200, 4800, 5100, 5400, 5200, 5600]
metric_labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5',
                 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10']

kpi_card_style = {
    "backgroundColor": "white",
    "borderRadius": "8px",
    "padding": "20px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    "width": "280px",
}


def _kpi_card(title, value_id, label_id, value, spark):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "12px", "color": "#666",
                                   "marginBottom": "5px"}),
            html.Div(
                [
                    html.Span(id=value_id, children=value,
                              style={"fontSize": "24px",
                                     "fontWeight": "bold"}),
                    html.Span(id=label_id, children="",
                              style={"fontSize": "11px", "color": "#999",
                                     "marginLeft": "8px"}),
                ]
            ),
            spark,
        ],
    )


component = html.Div(
    [
        html.Div(
            _kpi_card(
                "Revenue", "sync-revenue-value", "sync-revenue-label",
                f"${revenue_data[-1]}K",
                SparklineChart(
                    id="sync-revenue-spark",
                    data=revenue_data,
                    width=200,
                    height=35,
                    color="#4caf50",
                    area=True,
                    showHighlight=True,
                    xAxis={"id": "rev-axis", "data": metric_labels},
                ),
            ),
            style={**kpi_card_style, "borderTop": "3px solid #4caf50"},
        ),
        html.Div(
            _kpi_card(
                "Active Users", "sync-users-value", "sync-users-label",
                f"{users_data[-1]:,}",
                SparklineChart(
                    id="sync-users-spark",
                    data=users_data,
                    width=200,
                    height=35,
                    color="#2196f3",
                    area=True,
                    showHighlight=True,
                    xAxis={"id": "users-axis", "data": metric_labels},
                ),
            ),
            style={**kpi_card_style, "borderTop": "3px solid #2196f3"},
        ),
        html.Div(
            _kpi_card(
                "Sessions", "sync-sessions-value", "sync-sessions-label",
                f"{sessions_data[-1]:,}",
                SparklineChart(
                    id="sync-sessions-spark",
                    data=sessions_data,
                    width=200,
                    height=35,
                    color="#ff9800",
                    area=True,
                    showHighlight=True,
                    xAxis={"id": "sessions-axis", "data": metric_labels},
                ),
            ),
            style={**kpi_card_style, "borderTop": "3px solid #ff9800"},
        ),
    ],
    style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
)


@callback(
    Output("sync-revenue-value", "children"),
    Output("sync-revenue-label", "children"),
    Output("sync-users-value", "children"),
    Output("sync-users-label", "children"),
    Output("sync-sessions-value", "children"),
    Output("sync-sessions-label", "children"),
    Input("sync-revenue-spark", "hoverIndex"),
    Input("sync-users-spark", "hoverIndex"),
    Input("sync-sessions-spark", "hoverIndex"),
    prevent_initial_call=True,
)
def sync_hover(rev_idx, users_idx, sessions_idx):
    """Sync hover state across multiple sparklines."""
    idx = None
    for i in [rev_idx, users_idx, sessions_idx]:
        if i is not None:
            idx = i
            break

    if idx is not None:
        label = metric_labels[idx]
        return (
            f"${revenue_data[idx]}K", label,
            f"{users_data[idx]:,}", label,
            f"{sessions_data[idx]:,}", label,
        )
    return (
        f"${revenue_data[-1]}K", "",
        f"{users_data[-1]:,}", "",
        f"{sessions_data[-1]:,}", "",
    )
