"""
LiveTradingChart Demo — Candlestick Trading Simulation
Real-time OHLCV candlestick chart with volume bars, forecast, and alert labels.
"""

import os
import json

import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output, State, ctx

dash.register_page(__name__, path='/live-trading', name='Live Trading Chart')

from dash_mui_charts import LiveTradingChart

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Styles
stat_card = {
    'backgroundColor': '#f5f5f5',
    'padding': '12px 20px',
    'borderRadius': '8px',
    'textAlign': 'center',
    'minWidth': '130px',
}
code_style = {
    'backgroundColor': '#f5f5f5',
    'padding': '15px',
    'borderRadius': '5px',
    'whiteSpace': 'pre-wrap',
    'fontSize': '12px',
    'overflow': 'auto',
    'maxHeight': '300px',
}

layout = dmc.MantineProvider(html.Div([
    html.H1("Live Trading Chart"),
    html.P(
        "Real-time candlestick trading simulation with OHLCV data, volume bars, "
        "forecast line with uncertainty bands, and alert labels on significant moves. "
        "All simulation parameters are controllable via the sliders below.",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '20px'}
    ),

    # ── Controls Row 1: Buttons + Toggles ─────────────────────────────────
    html.Div([
        html.Div([
            dmc.Button("Start", id='lt-start-btn', color='green', size='md',
                       style={'marginRight': '10px'}),
            dmc.Button("Stop", id='lt-stop-btn', color='yellow', size='md', variant='outline',
                       style={'marginRight': '10px'}),
            dmc.Button("Reset", id='lt-reset-btn', color='red', size='md', variant='outline'),
        ], style={'display': 'flex', 'alignItems': 'center'}),
        html.Div([
            dmc.Switch(id='lt-volume-toggle', label='Volume Bars', checked=True, size='md'),
            dmc.Switch(id='lt-labels-toggle', label='Price Labels', checked=False, size='md'),
            dmc.Switch(id='lt-slider-toggle', label='Zoom Preview', checked=True, size='md'),
        ], style={'display': 'flex', 'gap': '25px', 'alignItems': 'center'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '15px'}),

    # ── Controls Row 2: Sliders ───────────────────────────────────────────
    html.Div([
        html.Div([
            html.Label("Speed (ms/tick)", style={'fontWeight': 500, 'marginBottom': '5px', 'display': 'block'}),
            dmc.Slider(
                id='lt-speed', value=200, min=50, max=1000, step=50,
                marks=[{'value': 50, 'label': '50'}, {'value': 200, 'label': '200'},
                       {'value': 500, 'label': '500'}, {'value': 1000, 'label': '1s'}],
                style={'maxWidth': '280px'},
            ),
        ], style={'flex': '1'}),
        html.Div([
            html.Label("Volatility", style={'fontWeight': 500, 'marginBottom': '5px', 'display': 'block'}),
            dmc.Slider(
                id='lt-volatility', value=2.0, min=0.5, max=8.0, step=0.5,
                marks=[{'value': 0.5, 'label': '0.5'}, {'value': 2.0, 'label': '2.0'},
                       {'value': 5.0, 'label': '5.0'}, {'value': 8.0, 'label': '8.0'}],
                style={'maxWidth': '280px'},
            ),
        ], style={'flex': '1'}),
        html.Div([
            html.Label("Drift", style={'fontWeight': 500, 'marginBottom': '5px', 'display': 'block'}),
            dmc.Slider(
                id='lt-drift', value=0.1, min=-0.5, max=0.5, step=0.05,
                marks=[{'value': -0.5, 'label': '-0.5'}, {'value': 0, 'label': '0'},
                       {'value': 0.5, 'label': '+0.5'}],
                style={'maxWidth': '280px'},
            ),
        ], style={'flex': '1'}),
        html.Div([
            html.Label("Window", style={'fontWeight': 500, 'marginBottom': '5px', 'display': 'block'}),
            dmc.Slider(
                id='lt-window', value=80, min=30, max=200, step=10,
                marks=[{'value': 30, 'label': '30'}, {'value': 80, 'label': '80'},
                       {'value': 200, 'label': '200'}],
                style={'maxWidth': '280px'},
            ),
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'gap': '30px', 'marginBottom': '20px'}),

    # ── Stats Row ─────────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.Div("Price", style={'fontSize': '11px', 'color': '#999'}),
            html.Div(id='lt-price-display', children="$100.00",
                     style={'fontSize': '22px', 'fontWeight': 'bold'}),
        ], style=stat_card),
        html.Div([
            html.Div("Ticks", style={'fontSize': '11px', 'color': '#999'}),
            html.Div(id='lt-tick-display', children="0",
                     style={'fontSize': '22px', 'fontWeight': 'bold'}),
        ], style=stat_card),
        html.Div([
            html.Div("Alerts", style={'fontSize': '11px', 'color': '#999'}),
            html.Div(id='lt-alert-count', children="0",
                     style={'fontSize': '22px', 'fontWeight': 'bold'}),
        ], style=stat_card),
        html.Div([
            html.Div("Status", style={'fontSize': '11px', 'color': '#999'}),
            html.Div(id='lt-status', children="Stopped",
                     style={'fontSize': '22px', 'fontWeight': 'bold', 'color': '#999'}),
        ], style=stat_card),
    ], style={'display': 'flex', 'gap': '12px', 'marginBottom': '15px'}),

    # ── Chart ─────────────────────────────────────────────────────────────
    LiveTradingChart(
        id='lt-chart',
        licenseKey=MUI_LICENSE_KEY,
        height=520,
        running=False,
        intervalMs=200,
        seed=42,
        windowSize=80,
        forecastSize=20,
        initialPrice=100,
        volatility=0.02,
        drift=0.001,
        forecastVolatility=1.5,
        # Swing-point alert detection (labels at extreme highs/lows only)
        alertLookback=5,          # Candles on each side to confirm swing point
        alertMinDistance=10,       # Min ticks between alerts
        maxVisibleAlerts=6,        # Cap visible labels in window
        # Functions-as-props: custom label formatting via JS registry
        alertFormatter={
            'function': 'priceAlertFormatter',
            'options': {'decimals': 2},
        },
        # Uncomment to use custom alert detection logic:
        # alertFilter={
        #     'function': 'swingAlertFilter',
        #     'options': {'lookback': 7},
        # },
        showVolume=True,
        showLabels=False,
        showSlider=True,
        volumeHeightPct=20,
        margin={'left': 75, 'right': 30, 'top': 20, 'bottom': 50},
    ),

    # ── Alert History ─────────────────────────────────────────────────────
    html.H4("Recent Alerts", style={'marginTop': '15px'}),
    html.Pre(id='lt-alert-log', children="Alerts will appear here...", style=code_style),

    # ── Code Example ──────────────────────────────────────────────────────
    html.Details([
        html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '15px'}),
        html.Pre("""LiveTradingChart(
    id='lt-chart',
    height=520,
    running=True,            # Start/stop simulation
    intervalMs=200,          # Tick speed
    windowSize=80,           # Visible candles
    forecastSize=20,         # Forecast horizon
    initialPrice=100,
    volatility=0.02,         # Candle volatility
    drift=0.001,             # Price trend
    showVolume=True,         # Volume bars
    showLabels=False,        # Price labels on candles

    # Swing-point alert detection
    alertLookback=5,         # Candles on each side to confirm extreme
    alertMinDistance=10,      # Min ticks between alerts
    maxVisibleAlerts=6,       # Cap visible labels

    # Functions-as-props: custom formatting via JS registry
    alertFormatter={
        'function': 'priceAlertFormatter',
        'options': {'decimals': 2},
    },

    # Outputs for callbacks:
    # currentPrice, tickCount, alertHistory
)""", style=code_style),
    ]),
], style={'padding': '20px'}))


# ── Callbacks ─────────────────────────────────────────────────────────────

@callback(
    Output('lt-chart', 'running'),
    Input('lt-start-btn', 'n_clicks'),
    Input('lt-stop-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def toggle_running(start_clicks, stop_clicks):
    return ctx.triggered_id == 'lt-start-btn'


@callback(
    Output('lt-chart', 'resetTrigger'),
    Input('lt-reset-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def reset_chart(n_clicks):
    return n_clicks or 0


@callback(Output('lt-chart', 'intervalMs'), Input('lt-speed', 'value'))
def update_speed(val):
    return val or 200


@callback(Output('lt-chart', 'volatility'), Input('lt-volatility', 'value'))
def update_volatility(val):
    return (val or 2.0) / 100


@callback(Output('lt-chart', 'drift'), Input('lt-drift', 'value'))
def update_drift(val):
    return (val or 0) / 100


@callback(Output('lt-chart', 'windowSize'), Input('lt-window', 'value'))
def update_window(val):
    return val or 80


@callback(Output('lt-chart', 'showVolume'), Input('lt-volume-toggle', 'checked'))
def toggle_volume(checked):
    return checked if checked is not None else True


@callback(Output('lt-chart', 'showLabels'), Input('lt-labels-toggle', 'checked'))
def toggle_labels(checked):
    return checked if checked is not None else False


@callback(Output('lt-chart', 'showSlider'), Input('lt-slider-toggle', 'checked'))
def toggle_slider(checked):
    return checked if checked is not None else True


@callback(
    Output('lt-price-display', 'children'),
    Output('lt-price-display', 'style'),
    Output('lt-tick-display', 'children'),
    Output('lt-status', 'children'),
    Output('lt-status', 'style'),
    Input('lt-chart', 'currentPrice'),
    Input('lt-chart', 'tickCount'),
    State('lt-chart', 'running'),
)
def update_stats(price, ticks, is_running):
    price_val = price if price is not None else 100
    color = '#4caf50' if price_val >= 100 else '#f44336'
    return (
        f"${price_val:,.2f}",
        {'fontSize': '22px', 'fontWeight': 'bold', 'color': color},
        str(ticks or 0),
        "Running" if is_running else "Stopped",
        {'fontSize': '22px', 'fontWeight': 'bold', 'color': '#4caf50' if is_running else '#999'},
    )


@callback(
    Output('lt-alert-count', 'children'),
    Output('lt-alert-log', 'children'),
    Input('lt-chart', 'alertHistory'),
)
def update_alerts(alerts):
    if not alerts:
        return "0", "Alerts will appear here..."
    recent = list(reversed(alerts[-15:]))
    lines = []
    for a in recent:
        d = "UP" if a.get('type') == 'up' else "DN"
        lines.append(f"[Tick {a.get('tick', '?'):>5}]  {d}  ${a.get('price', 0):>8.2f}  ({a.get('message', '')})")
    return str(len(alerts)), "\n".join(lines)