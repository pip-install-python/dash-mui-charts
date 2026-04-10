"""
LineChart Highlighting - Controlled axis/item highlights and per-series highlightScope
"""

import os
import json
import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, ctx

dash.register_page(__name__, path='/linechart-highlighting', name='LineChart Highlighting')

from dash_mui_charts import LineChart

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales_2023 = [120, 135, 150, 145, 160, 175, 190, 185, 200, 210, 195, 220]
sales_2024 = [130, 145, 165, 160, 180, 195, 210, 205, 225, 235, 220, 250]

CARD = 'page-card'

PRE_STYLE = {
    'fontSize': '12px',
    'margin': 0,
    'padding': '10px 14px',
    'borderRadius': '6px',
    'background': 'var(--mantine-color-body)',
    'border': '1px solid var(--mantine-color-default-border)',
    'color': 'var(--mantine-color-text)',
    'maxHeight': '200px',
    'overflow': 'auto',
}

layout = html.Div([
    html.H2("LineChart Highlighting"),
    html.P(
        "Controlled highlighting features: axis highlights, item highlights, "
        "and per-series highlight scopes.",
        style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}
    ),

    # ==========================================================================
    # Controlled Item Highlight
    # ==========================================================================
    html.Div([
        html.H4("Controlled Item Highlight"),
        html.P(
            "Click a button to programmatically highlight a data point. "
            "The highlight persists until you clear it or set a new one. "
            "Hovering the chart also updates the highlight state.",
            style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}
        ),
        html.Div([
            html.Button("Highlight Jan 2023", id='highlight-jan-btn',
                        style={'marginRight': '8px', 'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-blue-6)', 'color': 'white', 'cursor': 'pointer'}),
            html.Button("Highlight Jun 2024", id='highlight-jun-btn',
                        style={'marginRight': '8px', 'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-green-7)', 'color': 'white', 'cursor': 'pointer'}),
            html.Button("Clear", id='clear-highlight-btn',
                        style={'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-gray-6)', 'color': 'white', 'cursor': 'pointer'}),
        ], style={'marginBottom': '12px'}),
        LineChart(
            id='item-highlight-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'sales-2023',
                    'data': sales_2023,
                    'label': 'Sales 2023',
                    'color': '#1976d2',
                    'showMark': True,
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
                {
                    'id': 'sales-2024',
                    'data': sales_2024,
                    'label': 'Sales 2024',
                    'color': '#4caf50',
                    'showMark': True,
                    'highlightScope': {'highlight': 'series', 'fade': 'global'},
                },
            ],
            xAxis=[{
                'id': 'x-axis',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            tooltip={'trigger': 'item'},
        ),
        html.P("highlightedItem:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)',
                                          'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='item-highlight-output', children='null (no highlight)', style=PRE_STYLE),

        dmc.CodeHighlight(
            language="python",
            code="""# Controlled item highlight — set via callback, reads on hover
LineChart(
    id='item-highlight-chart',
    series=[
        {
            'id': 'sales-2023',
            'data': sales_2023,
            'showMark': True,
            'highlightScope': {'highlight': 'series', 'fade': 'global'},
        },
    ],
    tooltip={'trigger': 'item'},
)

@callback(
    Output('item-highlight-chart', 'highlightedItem'),
    Input('highlight-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def set_highlight(n):
    return {'seriesId': 'sales-2023', 'dataIndex': 0}""",
            mt="md",
        ),
    ], className=CARD),

    # ==========================================================================
    # Controlled Axis Highlight
    # ==========================================================================
    html.Div([
        html.H4("Controlled Axis Highlight"),
        html.P(
            "Use highlightedAxis to control which axis position is highlighted. "
            "Useful for synchronizing highlights across multiple charts.",
            style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}
        ),
        html.Div([
            html.Button("Highlight March", id='highlight-mar-axis-btn',
                        style={'marginRight': '8px', 'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-blue-6)', 'color': 'white', 'cursor': 'pointer'}),
            html.Button("Highlight September", id='highlight-sep-axis-btn',
                        style={'marginRight': '8px', 'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-violet-6)', 'color': 'white', 'cursor': 'pointer'}),
            html.Button("Clear", id='clear-axis-btn',
                        style={'marginBottom': '8px', 'padding': '6px 14px',
                               'borderRadius': '4px', 'border': '1px solid var(--mantine-color-default-border)',
                               'background': 'var(--mantine-color-gray-6)', 'color': 'white', 'cursor': 'pointer'}),
        ], style={'marginBottom': '12px'}),
        LineChart(
            id='axis-highlight-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[
                {
                    'id': 'sales',
                    'data': sales_2024,
                    'label': 'Sales 2024',
                    'color': '#9c27b0',
                    'showMark': True,
                },
            ],
            xAxis=[{
                'id': 'month-axis',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'band', 'y': 'none'},
        ),
        html.P("highlightedAxis:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)',
                                          'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='axis-highlight-output', children='[] (no highlight)', style=PRE_STYLE),

        dmc.CodeHighlight(
            language="python",
            code="""LineChart(
    id='axis-highlight-chart',
    xAxis=[{'id': 'month-axis', 'data': months, 'scaleType': 'point'}],
    axisHighlight={'x': 'band', 'y': 'none'},
)

@callback(
    Output('axis-highlight-chart', 'highlightedAxis'),
    Input('highlight-mar-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def set_axis_highlight(n):
    return [{'axisId': 'month-axis', 'dataIndex': 2}]  # March""",
            mt="md",
        ),
    ], className=CARD),

    # ==========================================================================
    # Per-Series Highlight Scope
    # ==========================================================================
    html.Div([
        html.H4("Per-Series Highlight Scope"),
        html.P(
            "Each series can define its own highlight behavior. Below, all three series "
            "use different scopes. Hover over marks (circles) to see the difference:",
            style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}
        ),
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 3},
            spacing="xs",
            mb="sm",
            children=[
                dmc.Paper(
                    [dmc.Text("Series A", fw=600, c="orange", size="sm"),
                     dmc.Text("highlight: 'series' / fade: 'global'", size="xs", c="dimmed"),
                     dmc.Text("Hovering highlights the entire series and fades everything else.", size="xs")],
                    p="sm", radius="sm", withBorder=True,
                ),
                dmc.Paper(
                    [dmc.Text("Series B", fw=600, c="cyan", size="sm"),
                     dmc.Text("highlight: 'item' / fade: 'global'", size="xs", c="dimmed"),
                     dmc.Text("Hovering highlights only the hovered point and fades everything else.", size="xs")],
                    p="sm", radius="sm", withBorder=True,
                ),
                dmc.Paper(
                    [dmc.Text("Series C", fw=600, c="grape", size="sm"),
                     dmc.Text("highlight: 'item' / fade: 'none'", size="xs", c="dimmed"),
                     dmc.Text("Hovering highlights the point but nothing else fades.", size="xs")],
                    p="sm", radius="sm", withBorder=True,
                ),
            ],
        ),
        LineChart(
            id='highlight-scope-chart',
            licenseKey=MUI_LICENSE_KEY,
            height=380,
            series=[
                {
                    'id': 'series-a',
                    'data': sales_2023,
                    'label': 'Series A (series + fade:global)',
                    'color': '#ff5722',
                    'showMark': True,
                    'highlightScope': {
                        'highlight': 'series',
                        'fade': 'global',
                    },
                },
                {
                    'id': 'series-b',
                    'data': sales_2024,
                    'label': 'Series B (item + fade:global)',
                    'color': '#00bcd4',
                    'showMark': True,
                    'highlightScope': {
                        'highlight': 'item',
                        'fade': 'global',
                    },
                },
                {
                    'id': 'series-c',
                    'data': [100, 115, 130, 125, 140, 155, 170, 165, 180, 190, 175, 200],
                    'label': 'Series C (item + fade:none)',
                    'color': '#9c27b0',
                    'showMark': True,
                    'highlightScope': {
                        'highlight': 'item',
                        'fade': 'none',
                    },
                },
            ],
            xAxis=[{
                'id': 'x-axis-scope',
                'data': months,
                'scaleType': 'point',
            }],
            grid={'horizontal': True},
            tooltip={'trigger': 'item'},
        ),
        html.P(
            "Hover over the data point marks (circles) on each series to see the different behaviors. "
            "With trigger='item', you must hover directly on a mark.",
            style={'color': 'var(--mantine-color-dimmed)', 'fontStyle': 'italic', 'fontSize': '13px', 'marginTop': '10px'}
        ),

        dmc.CodeHighlight(
            language="python",
            code="""LineChart(
    series=[
        {
            'id': 'series-a',
            'data': data_a,
            'showMark': True,
            'highlightScope': {
                'highlight': 'series',  # Entire series lights up
                'fade': 'global',       # Everything else fades
            },
        },
        {
            'id': 'series-b',
            'data': data_b,
            'showMark': True,
            'highlightScope': {
                'highlight': 'item',    # Only hovered point
                'fade': 'global',       # Everything else fades
            },
        },
        {
            'id': 'series-c',
            'data': data_c,
            'showMark': True,
            'highlightScope': {
                'highlight': 'item',    # Only hovered point
                'fade': 'none',         # Nothing fades
            },
        },
    ],
    tooltip={'trigger': 'item'},  # Must hover on marks
)""",
            mt="md",
        ),
    ], className=CARD),

    # ==========================================================================
    # Highlight Scope Reference
    # ==========================================================================
    html.Div([
        html.H4("Highlight Scope Reference"),
        html.P(
            "The highlightScope configuration controls how items are highlighted and how other items fade.",
            style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}
        ),
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2},
            spacing="md",
            children=[
                dmc.Paper([
                    dmc.Text("highlight options", fw=600, size="sm", mb="xs"),
                    dmc.Text("'none' — No highlighting", size="sm", c="dimmed"),
                    dmc.Text("'item' — Highlight single data point on hover", size="sm", c="dimmed"),
                    dmc.Text("'series' — Highlight entire series on hover", size="sm", c="dimmed"),
                ], p="md", radius="sm", withBorder=True),
                dmc.Paper([
                    dmc.Text("fade options", fw=600, size="sm", mb="xs"),
                    dmc.Text("'none' — No fading", size="sm", c="dimmed"),
                    dmc.Text("'series' — Fade other items in the same series", size="sm", c="dimmed"),
                    dmc.Text("'global' — Fade all items in all series", size="sm", c="dimmed"),
                ], p="md", radius="sm", withBorder=True),
            ],
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})


# ==========================================================================
# Callbacks
# ==========================================================================

@callback(
    Output('item-highlight-chart', 'highlightedItem'),
    Input('highlight-jan-btn', 'n_clicks'),
    Input('highlight-jun-btn', 'n_clicks'),
    Input('clear-highlight-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def set_item_highlight(jan_clicks, jun_clicks, clear_clicks):
    triggered = ctx.triggered_id
    if triggered == 'highlight-jan-btn':
        return {'seriesId': 'sales-2023', 'dataIndex': 0}
    elif triggered == 'highlight-jun-btn':
        return {'seriesId': 'sales-2024', 'dataIndex': 5}
    elif triggered == 'clear-highlight-btn':
        return None
    return dash.no_update


@callback(
    Output('item-highlight-output', 'children'),
    Input('item-highlight-chart', 'highlightedItem'),
)
def display_item_highlight(current_highlight):
    if current_highlight:
        return json.dumps(current_highlight, indent=2)
    return "null (no highlight)"


@callback(
    Output('axis-highlight-chart', 'highlightedAxis'),
    Input('highlight-mar-axis-btn', 'n_clicks'),
    Input('highlight-sep-axis-btn', 'n_clicks'),
    Input('clear-axis-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def set_axis_highlight(mar_clicks, sep_clicks, clear_clicks):
    triggered = ctx.triggered_id
    if triggered == 'highlight-mar-axis-btn':
        return [{'axisId': 'month-axis', 'dataIndex': 2}]
    elif triggered == 'highlight-sep-axis-btn':
        return [{'axisId': 'month-axis', 'dataIndex': 8}]
    elif triggered == 'clear-axis-btn':
        return []
    return dash.no_update


@callback(
    Output('axis-highlight-output', 'children'),
    Input('axis-highlight-chart', 'highlightedAxis'),
)
def display_axis_highlight(current_highlight):
    if current_highlight:
        return json.dumps(current_highlight, indent=2)
    return "[] (no highlight)"
