"""
Crosshair Explorer
Demonstrates crosshair tracking, right-click alert placement with inline
HoverCard management anchored to reference lines on the chart edge.
"""

import os
import math
import random
from datetime import datetime, timedelta

import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, ctx, no_update, ALL
from dash_iconify import DashIconify

dash.register_page(__name__, path='/crosshair', name='Crosshair Explorer')

from dash_mui_charts import CompositeChart

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
random.seed(99)
N = 2016
BASE = datetime(2025, 6, 1)
TIMESTAMPS = [int((BASE + timedelta(minutes=5 * i)).timestamp()) * 1000 for i in range(N)]


def _random_walk(start, mean, noise, daily_amp, n):
    val, out = start, []
    for i in range(n):
        daily = math.sin(2 * math.pi * i / 288)
        val += 0.02 * (mean - val) + random.gauss(0, noise) + daily_amp * daily
        out.append(round(val, 2))
    return out


TEMP_DATA = _random_walk(22, 22, 0.15, 0.8, N)
PRESSURE_DATA = _random_walk(1013, 1013, 0.1, 0.3, N)
HUMIDITY_DATA = _random_walk(55, 55, 0.2, 0.6, N)

CHART_META = {
    'temp':     {'label': 'Temperature', 'unit': 'C',   'color': '#1976d2', 'data': TEMP_DATA},
    'pressure': {'label': 'Pressure',    'unit': 'hPa', 'color': '#7b1fa2', 'data': PRESSURE_DATA},
    'humidity': {'label': 'Humidity',     'unit': '%',   'color': '#00838f', 'data': HUMIDITY_DATA},
}

ALERT_COLORS = ['#e53935', '#ff9800', '#4caf50', '#2196f3', '#9c27b0', '#00bcd4']

# Chart layout constants for pixel mapping
CHART_HEIGHTS = {'temp': 200, 'pressure': 200, 'humidity': 230}
MARGIN = {'top': 10, 'bottom': 5, 'right': 15}
MARGIN_BOT_VISIBLE = 55  # bottom chart has x-axis

# Styles
section_style = {'marginBottom': '40px'}
description_style = {'color': 'var(--mantine-color-dimmed)', 'marginBottom': '12px', 'fontSize': '14px'}
code_style = {
    'backgroundColor': 'var(--mantine-color-default)', 'padding': '12px', 'borderRadius': '5px',
    'whiteSpace': 'pre-wrap', 'fontSize': '11px', 'overflow': 'auto',
}
coord_bar = {
    'fontFamily': 'monospace', 'fontSize': '14px', 'padding': '10px 16px',
    'backgroundColor': '#1a1a1a', 'color': '#a0e8d8', 'borderRadius': '10px',
    'marginBottom': '10px', 'minHeight': '40px', 'display': 'flex',
    'alignItems': 'center', 'gap': '24px', 'flexWrap': 'wrap',
    'backdropFilter': 'blur(10px)',
}

X_AXIS_BASE = {
    'id': 'x', 'data': TIMESTAMPS, 'scaleType': 'time',
    'tickNumber': 7, 'tickMinStep': 86400 * 1000,
    'dateFormat': 'dd/MM/YYYY HH:mm', 'dateTickFormat': 'dd/MM HH:mm',
    'tickLabelStyle': {'fontSize': 11}, 'labelStyle': {'fontSize': 12},
}
X_HIDDEN = [{**X_AXIS_BASE, 'position': 'none'}]
X_VISIBLE = [{**X_AXIS_BASE, 'label': 'Date', 'height': 40}]


def _fmt_ts(ms):
    try:
        return datetime.fromtimestamp(ms / 1000).strftime('%d/%m/%Y %H:%M')
    except Exception:
        return str(ms)


def _y_to_pixel(y_val, data, chart_height, bottom_margin):
    """Map a y data value to a pixel offset from the top of the chart div."""
    vals = [v for v in data if v is not None]
    if not vals:
        return 0
    y_min, y_max = min(vals), max(vals)
    # Add 5% padding to match domainLimit='nice'
    pad = (y_max - y_min) * 0.08
    y_min -= pad
    y_max += pad
    if y_max == y_min:
        return MARGIN['top']
    draw_h = chart_height - MARGIN['top'] - bottom_margin
    frac = (y_val - y_min) / (y_max - y_min)
    # SVG y increases downward, data increases upward
    return MARGIN['top'] + draw_h * (1 - frac)


# ---------------------------------------------------------------------------
# Alert tag component — anchored to chart right edge
# ---------------------------------------------------------------------------
def _build_inline_tag(alert, idx, prefix, chart_key, chart_height, bottom_margin):
    """Build a HoverCard tag positioned at the alert's y-pixel on the chart."""
    color = ALERT_COLORS[idx % len(ALERT_COLORS)]
    meta = CHART_META.get(chart_key, {})
    unit = meta.get('unit', '')
    data = meta.get('data', [])
    condition = alert.get('condition', 'none')
    cond_sym = {'above': '\u25B2', 'below': '\u25BC'}.get(condition, '')

    pixel_y = _y_to_pixel(alert['y'], data, chart_height, bottom_margin)

    tag_label = f"{alert['y']:.1f} {cond_sym}"

    return html.Div(
        dmc.HoverCard(
            withArrow=True, width=200, shadow='lg', position='left',
            openDelay=100, closeDelay=200,
            children=[
                dmc.HoverCardTarget(
                    html.Div(tag_label, style={
                        'fontSize': '10px', 'fontWeight': 600, 'color': color,
                        'backgroundColor': 'var(--mantine-color-body)', 'border': f'1.5px solid {color}',
                        'borderRadius': '6px', 'padding': '1px 7px',
                        'cursor': 'pointer', 'lineHeight': '16px',
                        'boxShadow': '0 1px 4px rgba(0,0,0,0.08)',
                        'whiteSpace': 'nowrap', 'userSelect': 'none',
                    }),
                ),
                dmc.HoverCardDropdown(
                    html.Div([
                        # Header
                        html.Div([
                            html.Div(f"{meta.get('label', '')} Alert", style={
                                'fontWeight': 600, 'fontSize': '13px', 'color': 'var(--mantine-color-text)',
                            }),
                            html.Div(f"{alert['y']:.2f} {unit}", style={
                                'fontSize': '20px', 'fontWeight': 700, 'color': color,
                                'letterSpacing': '-0.5px', 'marginTop': '2px',
                            }),
                            html.Div(alert.get('x_label', ''), style={
                                'fontSize': '11px', 'color': 'var(--mantine-color-dimmed)', 'marginTop': '2px',
                            }),
                        ], style={'marginBottom': '12px'}),
                        # Condition selector
                        html.Div("Trigger", style={
                            'fontSize': '10px', 'fontWeight': 600, 'color': 'var(--mantine-color-dimmed)',
                            'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                            'marginBottom': '6px',
                        }),
                        dmc.SegmentedControl(
                            id={'type': f'{prefix}-cond', 'index': idx},
                            data=[
                                {'value': 'above', 'label': 'Above'},
                                {'value': 'none', 'label': 'Off'},
                                {'value': 'below', 'label': 'Below'},
                            ],
                            value=condition,
                            size='xs', fullWidth=True,
                            style={'marginBottom': '12px'},
                        ),
                        # Delete
                        dmc.Button(
                            "Remove",
                            id={'type': f'{prefix}-delete', 'index': idx},
                            size='xs', color='red', variant='subtle', fullWidth=True,
                            leftSection=DashIconify(icon='mdi:trash-can-outline', width=14),
                            styles={'root': {'fontWeight': 500}},
                        ),
                    ], style={'padding': '2px'}),
                    style={
                        'borderRadius': '12px', 'border': '1px solid var(--mantine-color-default-border)',
                        'boxShadow': '0 8px 30px rgba(0,0,0,0.12)',
                    },
                ),
            ],
        ),
        style={
            'position': 'absolute',
            'right': '0px',
            'top': f'{pixel_y - 9}px',
            'zIndex': 10,
        },
    )


def _build_ref_lines(alerts):
    """Reference lines — no label (the inline tag handles it)."""
    lines = []
    for i, a in enumerate(alerts):
        color = ALERT_COLORS[i % len(ALERT_COLORS)]
        condition = a.get('condition', 'none')
        lines.append({
            'y': a['y'],
            'lineStyle': {
                'stroke': color, 'strokeWidth': 2,
                'strokeDasharray': '8 4' if condition == 'none' else '0',
            },
        })
    return lines


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div([
    html.H1("Crosshair Explorer"),
    html.P(
        "Crosshair tracking reports pointer position in data coordinates. "
        "Right-click to place alerts as reference lines — hover the tag on the "
        "chart edge to manage trigger conditions or remove the alert.",
        style={'fontSize': '15px', 'color': 'var(--mantine-color-dimmed)', 'marginBottom': '25px'},
    ),

    # ==================================================================
    # 1. Position tracking
    # ==================================================================
    html.Div([
        html.H2("1. Crosshair Position Tracking"),
        html.P(
            "Move your mouse over the chart. The bar shows exact data coordinates.",
            style=description_style),
        html.Div(id='cross-coord-display', children=[
            html.Span("X: —"), html.Span("Y: —"),
        ], style=coord_bar),
        CompositeChart(
            id='cross-basic',
            licenseKey=MUI_LICENSE_KEY, height=350,
            series=[{'type': 'line', 'id': 'temp', 'label': 'Temperature (C)',
                     'data': TEMP_DATA, 'color': '#1976d2', 'showMark': False}],
            xAxis=X_VISIBLE,
            yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
            tooltip={'trigger': 'none'},
            axisHighlight={'x': 'line', 'y': 'line'},
            enableCrosshair=True,
            grid={'horizontal': True, 'vertical': True},
            margin={'left': 65, 'right': 20, 'top': 15, 'bottom': 55},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '8px'}),
            html.Pre("""CompositeChart(
    axisHighlight={'x': 'line', 'y': 'line'},
    enableCrosshair=True,
    tooltip={'trigger': 'none'},
)
# Output: crosshairPosition = {x: epoch_ms, y: value}
# Output: crosshairClick = {x, y, button: 'right', timestamp}""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ==================================================================
    # 2. Single-chart alert placement
    # ==================================================================
    html.Div([
        html.H2("2. Right-Click Alert Placement"),
        html.P(
            "Right-click the chart to place an alert. The tag appears on the right "
            "edge of the chart — hover it to set Above/Below triggers or remove it.",
            style=description_style),
        html.Div([
            dmc.Button("Clear All", id='sec2-clear', color='red', size='xs', variant='subtle',
                       leftSection=DashIconify(icon='mdi:trash-can-outline', width=14)),
            html.Span(id='sec2-count', children="0 alerts",
                      style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginLeft': '8px'}),
        ], style={'marginBottom': '8px'}),
        html.Div(id='sec2-alert-status', children=[
            html.Span("Right-click to set an alert"),
        ], style=coord_bar),
        # Chart wrapper with positioned alert tags
        html.Div([
            CompositeChart(
                id='sec2-chart',
                licenseKey=MUI_LICENSE_KEY, height=380,
                series=[{'type': 'line', 'id': 'temp', 'label': 'Temperature (C)',
                         'data': TEMP_DATA, 'color': '#1976d2', 'showMark': False}],
                xAxis=X_VISIBLE,
                yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
                tooltip={'trigger': 'axis'},
                axisHighlight={'x': 'line', 'y': 'line'},
                enableCrosshair=True, grid={'horizontal': True},
                margin={'left': 65, 'right': 50, 'top': 10, 'bottom': 55},
            ),
            html.Div(id='sec2-tags'),
        ], style={'position': 'relative'}),
    ], style=section_style),

    html.Hr(),

    # ==================================================================
    # 3. Synced 3-chart dashboard with per-chart alerts
    # ==================================================================
    html.Div([
        html.H2("3. Synced Crosshair Dashboard with Alerts"),
        html.P(
            "Three synced charts. Right-click any chart to place an alert on it. "
            "Hover the tag on the right edge to manage it.",
            style=description_style),
        html.Div([
            dmc.Button("Clear All", id='sec3-clear', color='red', size='xs', variant='subtle',
                       leftSection=DashIconify(icon='mdi:trash-can-outline', width=14)),
            html.Span(id='sec3-count', children="0 alerts",
                      style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginLeft': '8px'}),
        ], style={'marginBottom': '8px'}),
        html.Div(id='sec3-coord', children=[
            html.Span("Temp: —"), html.Span("Pressure: —"), html.Span("Humidity: —"),
        ], style=coord_bar),
        html.Div([
            # Temperature
            html.Div([
                html.Div("Temperature (C)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                html.Div([
                    CompositeChart(
                        id='sec3-temp', licenseKey=MUI_LICENSE_KEY, height=200,
                        series=[{'type': 'line', 'id': 'temp', 'label': 'Temperature',
                                 'data': TEMP_DATA, 'color': '#1976d2', 'showMark': False}],
                        xAxis=X_HIDDEN, yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
                        tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line', 'y': 'line'},
                        enableCrosshair=True, hideLegend=True, grid={'horizontal': True},
                        margin={'left': 65, 'right': 50, 'top': 10, 'bottom': 5}),
                    html.Div(id='sec3-tags-temp'),
                ], style={'position': 'relative'}),
            ]),
            # Pressure
            html.Div([
                html.Div("Pressure (hPa)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                html.Div([
                    CompositeChart(
                        id='sec3-pressure', licenseKey=MUI_LICENSE_KEY, height=200,
                        series=[{'type': 'line', 'id': 'pressure', 'label': 'Pressure',
                                 'data': PRESSURE_DATA, 'color': '#7b1fa2', 'showMark': False}],
                        xAxis=X_HIDDEN, yAxis=[{'label': 'hPa', 'width': 60, 'domainLimit': 'nice'}],
                        tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line', 'y': 'line'},
                        enableCrosshair=True, hideLegend=True, grid={'horizontal': True},
                        margin={'left': 65, 'right': 50, 'top': 10, 'bottom': 5}),
                    html.Div(id='sec3-tags-pressure'),
                ], style={'position': 'relative'}),
            ]),
            # Humidity
            html.Div([
                html.Div("Humidity (%)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                html.Div([
                    CompositeChart(
                        id='sec3-humidity', licenseKey=MUI_LICENSE_KEY, height=230,
                        series=[{'type': 'line', 'id': 'humidity', 'label': 'Humidity',
                                 'data': HUMIDITY_DATA, 'color': '#00838f', 'showMark': False}],
                        xAxis=X_VISIBLE, yAxis=[{'label': '%', 'width': 60, 'domainLimit': 'nice'}],
                        tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line', 'y': 'line'},
                        enableCrosshair=True, hideLegend=True, grid={'horizontal': True},
                        margin={'left': 65, 'right': 50, 'top': 10, 'bottom': 55}),
                    html.Div(id='sec3-tags-humidity'),
                ], style={'position': 'relative'}),
            ]),
        ]),
    ], style=section_style),

    # Stores
    dcc.Store(id='sec2-store', data=[]),
    dcc.Store(id='sec3-store', data=[]),

], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


# ===========================================================================
# Section 1
# ===========================================================================
@callback(Output('cross-coord-display', 'children'), Input('cross-basic', 'crosshairPosition'))
def s1_coords(pos):
    if not pos or pos.get('x') is None:
        return [html.Span("X: —"), html.Span("Y: —")]
    return [html.Span(f"X: {_fmt_ts(pos['x'])}"), html.Span(f"Y: {pos['y']:.2f} C")]


# ===========================================================================
# Section 2
# ===========================================================================
@callback(
    Output('sec2-store', 'data'),
    Input('sec2-chart', 'crosshairClick'),
    Input('sec2-clear', 'n_clicks'),
    Input({'type': 'sec2-delete', 'index': ALL}, 'n_clicks'),
    Input({'type': 'sec2-cond', 'index': ALL}, 'value'),
    State('sec2-store', 'data'),
    prevent_initial_call=True,
)
def s2_manage(click, clear, del_clicks, cond_vals, alerts):
    alerts = list(alerts or [])
    triggered = ctx.triggered_id

    if triggered == 'sec2-clear':
        return []
    if isinstance(triggered, dict):
        idx = triggered['index']
        if triggered['type'] == 'sec2-delete' and 0 <= idx < len(alerts):
            alerts.pop(idx)
            return alerts
        if triggered['type'] == 'sec2-cond' and 0 <= idx < len(alerts):
            # Find the value from the matching segmented control
            for prop in ctx.triggered:
                if 'value' in prop['prop_id']:
                    alerts[idx] = {**alerts[idx], 'condition': prop['value']}
                    return alerts
    if triggered == 'sec2-chart' and click and click.get('x') is not None:
        alerts.append({
            'y': round(click['y'], 2), 'x': click['x'], 'chart': 'temp',
            'x_label': _fmt_ts(click['x']), 'condition': 'none',
        })
        return alerts
    return no_update


@callback(
    Output('sec2-chart', 'referenceLines'),
    Output('sec2-tags', 'children'),
    Output('sec2-count', 'children'),
    Output('sec2-alert-status', 'children'),
    Input('sec2-store', 'data'),
)
def s2_render(alerts):
    if not alerts:
        return [], None, "0 alerts", [html.Span("Right-click to set an alert")]
    lines = _build_ref_lines(alerts)
    tags = [_build_inline_tag(a, i, 'sec2', 'temp', 380, 55) for i, a in enumerate(alerts)]
    n = len(alerts)
    a = alerts[-1]
    status = [html.Span(f"{n} alert{'s' if n != 1 else ''}"),
              html.Span(f"Latest: {a['y']:.2f} C")]
    return lines, tags, f"{n} alert{'s' if n != 1 else ''}", status


# ===========================================================================
# Section 3
# ===========================================================================
SEC3_IDS = ['sec3-temp', 'sec3-pressure', 'sec3-humidity']
SEC3_KEYS = ['temp', 'pressure', 'humidity']

# Crosshair sync
@callback(
    *[Output(cid, 'highlightedAxis') for cid in SEC3_IDS],
    *[Output(cid, 'syncedTooltipIndex') for cid in SEC3_IDS],
    Output('sec3-coord', 'children'),
    *[Input(cid, 'highlightedAxis') for cid in SEC3_IDS],
    prevent_initial_call=True,
)
def s3_sync(ax_t, ax_p, ax_h):
    source = ctx.triggered_id
    axes_map = dict(zip(SEC3_IDS, [ax_t, ax_p, ax_h]))
    axis = axes_map.get(source, ax_t)
    idx = axis[0]['dataIndex'] if axis and len(axis) > 0 else -1
    tips = [idx if cid != source else -1 for cid in SEC3_IDS]
    display = []
    for key in SEC3_KEYS:
        m = CHART_META[key]
        if 0 <= idx < len(m['data']):
            display.append(html.Span(f"{m['label']}: {m['data'][idx]:.2f} {m['unit']}"))
        else:
            display.append(html.Span(f"{m['label']}: —"))
    return axis, axis, axis, tips[0], tips[1], tips[2], display


# Alert management
@callback(
    Output('sec3-store', 'data'),
    *[Input(cid, 'crosshairClick') for cid in SEC3_IDS],
    Input('sec3-clear', 'n_clicks'),
    Input({'type': 'sec3-delete', 'index': ALL}, 'n_clicks'),
    Input({'type': 'sec3-cond', 'index': ALL}, 'value'),
    State('sec3-store', 'data'),
    prevent_initial_call=True,
)
def s3_manage(click_t, click_p, click_h, clear, del_clicks, cond_vals, alerts):
    alerts = list(alerts or [])
    triggered = ctx.triggered_id

    if triggered == 'sec3-clear':
        return []
    if isinstance(triggered, dict):
        idx = triggered['index']
        if triggered['type'] == 'sec3-delete' and 0 <= idx < len(alerts):
            alerts.pop(idx)
            return alerts
        if triggered['type'] == 'sec3-cond' and 0 <= idx < len(alerts):
            for prop in ctx.triggered:
                if 'value' in prop['prop_id']:
                    alerts[idx] = {**alerts[idx], 'condition': prop['value']}
                    return alerts

    click_map = dict(zip(SEC3_IDS, [click_t, click_p, click_h]))
    key_map = dict(zip(SEC3_IDS, SEC3_KEYS))
    if triggered in SEC3_IDS:
        click = click_map[triggered]
        if click and click.get('x') is not None:
            chart_key = key_map[triggered]
            alerts.append({
                'y': round(click['y'], 2), 'x': click['x'], 'chart': chart_key,
                'x_label': _fmt_ts(click['x']), 'condition': 'none',
            })
            return alerts
    return no_update


# Render alerts per chart
@callback(
    Output('sec3-temp', 'referenceLines'),
    Output('sec3-pressure', 'referenceLines'),
    Output('sec3-humidity', 'referenceLines'),
    Output('sec3-tags-temp', 'children'),
    Output('sec3-tags-pressure', 'children'),
    Output('sec3-tags-humidity', 'children'),
    Output('sec3-count', 'children'),
    Input('sec3-store', 'data'),
)
def s3_render(alerts):
    if not alerts:
        return [], [], [], None, None, None, "0 alerts"

    per_chart = {'temp': [], 'pressure': [], 'humidity': []}
    per_chart_idx = {'temp': [], 'pressure': [], 'humidity': []}
    for i, a in enumerate(alerts):
        k = a.get('chart', 'temp')
        per_chart.setdefault(k, []).append(a)
        per_chart_idx.setdefault(k, []).append(i)

    ref_lines = []
    tag_lists = []
    for key in SEC3_KEYS:
        chart_alerts = per_chart.get(key, [])
        global_indices = per_chart_idx.get(key, [])
        ref_lines.append(_build_ref_lines(chart_alerts))
        bot = MARGIN_BOT_VISIBLE if key == 'humidity' else MARGIN['bottom']
        tags = [_build_inline_tag(a, global_indices[j], 'sec3', key,
                                  CHART_HEIGHTS[key], bot)
                for j, a in enumerate(chart_alerts)]
        tag_lists.append(tags if tags else None)

    n = len(alerts)
    # Output order: ref_temp, ref_pressure, ref_humidity, tags_temp, tags_pressure, tags_humidity, count
    return (*ref_lines, *tag_lists, f"{n} alert{'s' if n != 1 else ''}")
