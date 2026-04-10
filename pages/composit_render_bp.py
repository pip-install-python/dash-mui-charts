"""
Composite Render Best Practices
Optimal rendering of stacked Discharge Time / Temperature / Pressure dashboards
across different date ranges: 7d (LIVE), 30d, 3mo, 6mo, 1yr, 1yr+.

Each range uses tuned tick spacing, date formatting, marker visibility, and
chart heights to produce the best visual density for that data volume.
Equipment pings every ~5 minutes; data scales from ~2k to ~150k+ points.
"""

import os
import math
import random
from datetime import datetime, timedelta

import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, ctx, no_update

dash.register_page(__name__, path='/composite-render-bp', name='Composite Render BP')

from dash_mui_charts import CompositeChart

MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FIVE_MIN_MS = 5 * 60 * 1000
DAY_MS = 86400 * 1000

# Live 7d config
LIVE_INITIAL_POINTS = 1440  # 5 days of history to start (5*288)
LIVE_WINDOW_DEFAULT = 288   # 1 day visible window by default
LIVE_MAX_POINTS = 2016      # 7 days max


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------
def generate_initial_live_data():
    """Build the initial 5 days of history with realistic random walk data."""
    random.seed(42)
    base_ts = int(datetime(2025, 4, 1).timestamp()) * 1000

    timestamps, discharge, temp, init_p, min_p = [], [], [], [], []

    # Random-walk state with mean reversion
    d_val = 4.0    # discharge (sec), mean ~4
    t_val = 45.0   # temp (C), mean ~45
    ip_val = 110.0  # init pressure (PSI), mean ~110
    mp_val = 90.0   # min pressure (PSI), mean ~90

    for i in range(LIVE_INITIAL_POINTS):
        ts = base_ts + i * FIVE_MIN_MS
        # Daily cycle component
        daily = math.sin(2 * math.pi * i / 288)

        # Discharge: mean-reverting random walk + daily cycle
        d_val += 0.02 * (4.0 - d_val) + random.gauss(0, 0.08) + 0.15 * daily
        d_val = max(1.5, min(7.0, d_val))

        # Temperature: slower drift + daily cycle
        t_val += 0.01 * (45.0 - t_val) + random.gauss(0, 0.4) + 1.0 * daily
        t_val = max(25, min(65, t_val))

        # Init pressure: gradual decline + daily cycle
        ip_val += 0.005 * (110.0 - ip_val) - 0.002 + random.gauss(0, 0.3) + 0.8 * daily
        ip_val = max(85, min(130, ip_val))

        # Min pressure: tracks below init with its own noise
        mp_val += 0.01 * (ip_val - 20 - mp_val) + random.gauss(0, 0.25)
        mp_val = max(60, min(ip_val - 5, mp_val))

        timestamps.append(ts)
        discharge.append(round(d_val, 2))
        temp.append(round(t_val, 1))
        init_p.append(round(ip_val, 1))
        min_p.append(round(mp_val, 1))

    # Scatter events at fixed indices
    event_indices = sorted(random.sample(range(LIVE_INITIAL_POINTS), 5))
    events_d = [{'x': timestamps[i], 'y': round(discharge[i] + random.choice([-1, 1]) * 2, 2), 'id': j}
                for j, i in enumerate(event_indices)]
    events_t = [{'x': timestamps[i], 'y': round(temp[i] + random.choice([-1, 1]) * 10, 1), 'id': j}
                for j, i in enumerate(event_indices)]
    events_p = [{'x': timestamps[i], 'y': round(min_p[i] - 8, 1), 'id': j}
                for j, i in enumerate(event_indices)]

    return {
        'timestamps': timestamps,
        'discharge': discharge,
        'temp': temp,
        'init_pressure': init_p,
        'min_pressure': min_p,
        'events_discharge': events_d,
        'events_temp': events_t,
        'events_pressure': events_p,
        'tick_index': LIVE_INITIAL_POINTS,
        'base_ts': base_ts,
        'event_counter': len(event_indices),
        # Carry forward last values for random walk continuation
        'last_d': round(d_val, 2),
        'last_t': round(t_val, 1),
        'last_ip': round(ip_val, 1),
        'last_mp': round(mp_val, 1),
    }


def generate_dataset(n_days, seed=42):
    """Generate realistic equipment data for n_days at 5-min intervals."""
    random.seed(seed)
    n_points = n_days * 288
    base = datetime(2025, 4, 1)
    timestamps = [int((base + timedelta(minutes=5 * i)).timestamp()) * 1000 for i in range(n_points)]
    discharge = [round(4 + 1.5 * math.sin(2 * math.pi * i / 288) + random.gauss(0, 0.3), 2) for i in range(n_points)]
    temp = [round(45 + 10 * math.sin(2 * math.pi * i / (288 * 90)) + 5 * math.sin(2 * math.pi * i / 288) + random.gauss(0, 1.5), 1) for i in range(n_points)]
    init_pressure = [round(110 - 0.03 * (i / 288) + 5 * math.sin(2 * math.pi * i / 288) + random.gauss(0, 1.5), 1) for i in range(n_points)]
    min_pressure = [round(init_pressure[i] - 20 + 3 * math.sin(2 * math.pi * i / (288 * 7)) + random.gauss(0, 1), 1) for i in range(n_points)]
    n_events = max(3, n_days // 5)
    event_indices = sorted(random.sample(range(n_points), min(n_events, n_points)))
    events_discharge = [{'x': timestamps[i], 'y': round(discharge[i] + random.choice([-1, 1]) * random.uniform(1.5, 3), 2), 'id': j} for j, i in enumerate(event_indices)]
    events_temp = [{'x': timestamps[i], 'y': round(temp[i] + random.choice([-1, 1]) * random.uniform(8, 15), 1), 'id': j} for j, i in enumerate(event_indices)]
    events_pressure = [{'x': timestamps[i], 'y': round(min_pressure[i] - random.uniform(5, 12), 1), 'id': j} for j, i in enumerate(event_indices)]
    return {
        'timestamps': timestamps, 'discharge': discharge, 'temp': temp,
        'init_pressure': init_pressure, 'min_pressure': min_pressure,
        'events_discharge': events_discharge, 'events_temp': events_temp,
        'events_pressure': events_pressure, 'n_points': n_points,
    }


# ---------------------------------------------------------------------------
# Static range profiles (30d+)
# ---------------------------------------------------------------------------
RANGE_PROFILES = {
    '30d': {
        'label': '30 Days', 'n_days': 30,
        'description': '~8,640 points. Good balance of detail and overview. Ticks every ~5 days.',
        'tick_number': 6, 'tick_min_step': DAY_MS * 5,
        'date_format': 'dd/MM/YYYY HH:mm', 'date_tick_format': 'dd/MM',
        'tick_angle': 35, 'tick_font_size': 11, 'text_anchor': 'start',
        'x_height': 50, 'bottom_margin': 65,
        'chart_heights': (180, 180, 220), 'event_marker_size': 6,
    },
    '3mo': {
        'label': '3 Months', 'n_days': 90,
        'description': '~25,920 points. Medium density, ticks every ~2 weeks. Trends emerge.',
        'tick_number': 6, 'tick_min_step': DAY_MS * 14,
        'date_format': 'dd/MM/YYYY', 'date_tick_format': 'dd/MM/YY',
        'tick_angle': 35, 'tick_font_size': 11, 'text_anchor': 'start',
        'x_height': 55, 'bottom_margin': 70,
        'chart_heights': (180, 180, 220), 'event_marker_size': 5,
    },
    '6mo': {
        'label': '6 Months', 'n_days': 180,
        'description': '~51,840 points. Ticks monthly. Seasonal patterns visible.',
        'tick_number': 6, 'tick_min_step': DAY_MS * 30,
        'date_format': 'dd/MM/YYYY', 'date_tick_format': 'MMM YY',
        'tick_angle': 35, 'tick_font_size': 11, 'text_anchor': 'start',
        'x_height': 50, 'bottom_margin': 65,
        'chart_heights': (170, 170, 210), 'event_marker_size': 5,
    },
    '1yr': {
        'label': '1 Year', 'n_days': 365,
        'description': '~105,120 points. Ticks monthly. Full seasonal cycle.',
        'tick_number': 12, 'tick_min_step': DAY_MS * 30,
        'date_format': 'dd MMM YYYY', 'date_tick_format': 'MMM YY',
        'tick_angle': 35, 'tick_font_size': 10, 'text_anchor': 'start',
        'x_height': 50, 'bottom_margin': 65,
        'chart_heights': (170, 170, 210), 'event_marker_size': 4,
    },
    '1yr+': {
        'label': '18 Months', 'n_days': 548,
        'description': '~157,824 points. Ticks every 2 months. Long-term degradation visible.',
        'tick_number': 9, 'tick_min_step': DAY_MS * 60,
        'date_format': 'dd MMM YYYY', 'date_tick_format': 'MMM YY',
        'tick_angle': 35, 'tick_font_size': 10, 'text_anchor': 'start',
        'x_height': 50, 'bottom_margin': 65,
        'chart_heights': (170, 170, 210), 'event_marker_size': 4,
    },
}

DATASETS = {key: generate_dataset(p['n_days'], seed=hash(key) % 10000) for key, p in RANGE_PROFILES.items()}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
section_style = {'marginBottom': '50px'}
description_style = {'color': 'var(--mantine-color-dimmed)', 'marginBottom': '10px', 'fontSize': '14px'}
code_style = {
    'backgroundColor': 'var(--mantine-color-default)', 'padding': '12px', 'borderRadius': '5px',
    'whiteSpace': 'pre-wrap', 'fontSize': '11px', 'overflow': 'auto',
}
stat_card = {
    'backgroundColor': 'var(--mantine-color-default)', 'padding': '8px 16px', 'borderRadius': '8px',
    'textAlign': 'center', 'minWidth': '100px',
}
badge_style = {
    'backgroundColor': '#1565c0', 'color': 'white', 'padding': '2px 8px',
    'borderRadius': '4px', 'fontSize': '10px', 'fontWeight': 'bold',
    'marginLeft': '8px', 'verticalAlign': 'middle',
}
stat_style = {
    'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'fontFamily': 'monospace', 'marginBottom': '8px',
}


# ---------------------------------------------------------------------------
# Reference line generators
# ---------------------------------------------------------------------------
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

_REF_LINE_STYLE = {'stroke': '#bdbdbd', 'strokeDasharray': '4 4', 'strokeWidth': 1}
_REF_LABEL_STYLE = {'fill': '#757575', 'fontSize': 10}


def _month_reference_lines(n_days):
    """Vertical reference lines at the 1st of each month within the range."""
    base = datetime(2025, 4, 1)
    end = base + timedelta(days=n_days)
    lines = []
    # Start from the first month boundary after the base
    d = datetime(base.year, base.month, 1)
    if d <= base:
        if d.month == 12:
            d = datetime(d.year + 1, 1, 1)
        else:
            d = datetime(d.year, d.month + 1, 1)
    while d < end:
        ts = int(d.timestamp()) * 1000
        label = f"{MONTH_NAMES[d.month - 1]}"
        lines.append({
            'x': ts, 'label': label,
            'lineStyle': _REF_LINE_STYLE,
            'labelStyle': _REF_LABEL_STYLE,
            'labelAlign': 'start',
        })
        if d.month == 12:
            d = datetime(d.year + 1, 1, 1)
        else:
            d = datetime(d.year, d.month + 1, 1)
    return lines


def _quarter_reference_lines(n_days):
    """Vertical reference lines at Q1–Q4 boundaries within the range."""
    base = datetime(2025, 4, 1)
    end = base + timedelta(days=n_days)
    quarter_starts = [1, 4, 7, 10]  # Jan, Apr, Jul, Oct
    lines = []
    # Scan from base year through end year
    for year in range(base.year, end.year + 1):
        for qi, month in enumerate(quarter_starts, 1):
            d = datetime(year, month, 1)
            if d <= base or d >= end:
                continue
            ts = int(d.timestamp()) * 1000
            label = f"{str(year)[-2:]}Q{qi}"
            lines.append({
                'x': ts, 'label': label,
                'lineStyle': _REF_LINE_STYLE,
                'labelStyle': {**_REF_LABEL_STYLE, 'fontWeight': 'bold'},
                'labelAlign': 'start',
            })
    return lines


# ---------------------------------------------------------------------------
# Static section builder (30d+)
# ---------------------------------------------------------------------------
def build_range_section(range_key):
    """Build a full 3-chart stacked section for a given range profile."""
    p = RANGE_PROFILES[range_key]
    d = DATASETS[range_key]
    prefix = f'bp-{range_key}'
    h_top, h_mid, h_bot = p['chart_heights']
    tls = {'angle': p['tick_angle'], 'fontSize': p['tick_font_size'], 'textAnchor': p['text_anchor']}

    # Reference lines: months for 3mo/6mo, quarters for 1yr/1yr+
    if range_key in ('3mo', '6mo'):
        ref_lines = _month_reference_lines(p['n_days'])
    elif range_key in ('1yr', '1yr+'):
        ref_lines = _quarter_reference_lines(p['n_days'])
    else:
        ref_lines = None

    x_hidden = [{'id': 'x', 'data': d['timestamps'], 'scaleType': 'time',
                 'tickNumber': p['tick_number'], 'tickMinStep': p['tick_min_step'],
                 'dateFormat': p['date_format'], 'dateTickFormat': p['date_tick_format'],
                 'position': 'none', 'tickLabelStyle': tls}]
    x_visible = [{'id': 'x', 'data': d['timestamps'], 'scaleType': 'time',
                  'label': 'Date', 'height': p['x_height'],
                  'tickNumber': p['tick_number'], 'tickMinStep': p['tick_min_step'],
                  'dateFormat': p['date_format'], 'dateTickFormat': p['date_tick_format'],
                  'tickLabelStyle': tls, 'labelStyle': {'fontSize': 12}}]
    m_top = {'left': 65, 'right': 15, 'top': 10, 'bottom': 5}
    m_bot = {'left': 65, 'right': 15, 'top': 10, 'bottom': p['bottom_margin']}

    return html.Div([
        html.H3(f"{p['label']} Range", style={'marginBottom': '4px'}),
        html.P(p['description'], style=description_style),
        html.Div(
            f"{d['n_points']:,} data points  |  {len(d['events_discharge'])} events  |  "
            f"tickMinStep={p['tick_min_step'] // DAY_MS}d  |  tickNumber={p['tick_number']}  |  "
            f"format=\"{p['date_tick_format']}\"",
            style=stat_style),
        html.Div([dmc.Switch(id=f'{prefix}-sync', label='Sync tooltips', checked=True, size='sm')],
                 style={'marginBottom': '8px'}),
        html.Div([
            html.Div([
                html.Div("Discharge Time (sec)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id=f'{prefix}-discharge', licenseKey=MUI_LICENSE_KEY, height=h_top,
                    series=[
                        {'type': 'line', 'id': 'discharge', 'label': 'Discharge Time', 'data': d['discharge'], 'color': '#1976d2', 'showMark': False},
                        {'type': 'scatter', 'id': 'events', 'label': 'Events', 'data': d['events_discharge'], 'color': '#e53935', 'markerSize': p['event_marker_size']},
                    ],
                    xAxis=x_hidden, yAxis=[{'label': 'sec', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True, margin=m_top,
                    **({'referenceLines': ref_lines} if ref_lines else {})),
            ]),
            html.Div([
                html.Div("Temperature (C)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id=f'{prefix}-temp', licenseKey=MUI_LICENSE_KEY, height=h_mid,
                    series=[
                        {'type': 'line', 'id': 'temp', 'label': 'Temperature', 'data': d['temp'], 'color': '#e65100', 'showMark': False},
                        {'type': 'scatter', 'id': 'events', 'label': 'Events', 'data': d['events_temp'], 'color': '#e53935', 'markerSize': p['event_marker_size']},
                    ],
                    xAxis=x_hidden, yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True, margin=m_top,
                    **({'referenceLines': ref_lines} if ref_lines else {})),
            ]),
            html.Div([
                html.Div("Pressure (PSI)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id=f'{prefix}-pressure', licenseKey=MUI_LICENSE_KEY, height=h_bot,
                    series=[
                        {'type': 'line', 'id': 'init-pressure', 'label': 'Init Pressure', 'data': d['init_pressure'], 'color': '#7b1fa2', 'showMark': False},
                        {'type': 'line', 'id': 'min-pressure', 'label': 'Min Pressure', 'data': d['min_pressure'], 'color': '#00838f', 'showMark': False},
                        {'type': 'scatter', 'id': 'events', 'label': 'Events', 'data': d['events_pressure'], 'color': '#e53935', 'markerSize': p['event_marker_size']},
                    ],
                    xAxis=x_visible, yAxis=[{'label': 'PSI', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True, margin=m_bot,
                    **({'referenceLines': ref_lines} if ref_lines else {})),
            ]),
        ]),
    ], style=section_style)


# ---------------------------------------------------------------------------
# Live 7d section builder
# ---------------------------------------------------------------------------
def build_live_7d_section():
    """Build the live-streaming 7-day dashboard section."""
    return html.Div([
        html.H3("7 Days Range — Live", style={'marginBottom': '4px'}),
        html.P(
            "Live streaming equipment data at 5-min intervals. Starts with 5 days of history "
            "and streams new readings in real time. Adjust speed and visible window size.",
            style=description_style),

        # Controls row
        html.Div([
            html.Div([
                dmc.Button("Start", id='bp-live-start', color='green', size='sm', style={'marginRight': '8px'}),
                dmc.Button("Stop", id='bp-live-stop', color='yellow', size='sm', variant='outline', style={'marginRight': '8px'}),
                dmc.Button("Reset", id='bp-live-reset', color='red', size='sm', variant='outline'),
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                dmc.Switch(id='bp-live-sync', label='Sync tooltips', checked=True, size='sm'),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '10px'}),

        # Sliders row
        html.Div([
            html.Div([
                html.Label("Speed (ms/tick)", style={'fontWeight': 500, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
                dmc.Slider(
                    id='bp-live-speed', value=300, min=50, max=2000, step=50,
                    marks=[{'value': 50, 'label': '50ms'}, {'value': 300, 'label': '300ms'},
                           {'value': 1000, 'label': '1s'}, {'value': 2000, 'label': '2s'}],
                    style={'maxWidth': '260px'}),
            ], style={'flex': '1'}),
            html.Div([
                html.Label("Window (points)", style={'fontWeight': 500, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
                dmc.Slider(
                    id='bp-live-window', value=LIVE_WINDOW_DEFAULT, min=72, max=2016, step=72,
                    marks=[{'value': 72, 'label': '6h'}, {'value': 288, 'label': '1d'},
                           {'value': 1008, 'label': '3.5d'}, {'value': 2016, 'label': '7d'}],
                    style={'maxWidth': '260px'}),
            ], style={'flex': '1'}),
            html.Div([
                html.Label("Estimate (points ahead)", style={'fontWeight': 500, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
                dmc.Slider(
                    id='bp-live-estimate', value=36, min=0, max=144, step=12,
                    marks=[{'value': 0, 'label': '0'}, {'value': 36, 'label': '3h'},
                           {'value': 72, 'label': '6h'}, {'value': 144, 'label': '12h'}],
                    style={'maxWidth': '260px'}),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'gap': '25px', 'marginBottom': '12px'}),

        # Stats row
        html.Div([
            html.Div([
                html.Div("Points", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-stat-points', children=str(LIVE_INITIAL_POINTS),
                         style={'fontSize': '18px', 'fontWeight': 'bold'}),
            ], style=stat_card),
            html.Div([
                html.Div("Discharge", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-stat-discharge', children="—",
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#1976d2'}),
            ], style=stat_card),
            html.Div([
                html.Div("Temp", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-stat-temp', children="—",
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#e65100'}),
            ], style=stat_card),
            html.Div([
                html.Div("Init PSI", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-stat-initp', children="—",
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#7b1fa2'}),
            ], style=stat_card),
            html.Div([
                html.Div("Min PSI", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-stat-minp', children="—",
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#00838f'}),
            ], style=stat_card),
            html.Div([
                html.Div("Status", style={'fontSize': '10px', 'color': 'var(--mantine-color-dimmed)'}),
                html.Div(id='bp-live-status', children="Stopped",
                         style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'var(--mantine-color-dimmed)'}),
            ], style=stat_card),
        ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '10px', 'flexWrap': 'wrap'}),

        # Charts
        html.Div([
            html.Div([
                html.Div("Discharge Time (sec)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id='bp-live-discharge', licenseKey=MUI_LICENSE_KEY, height=180,
                    series=[], xAxis=[{'id': 'x', 'data': [], 'scaleType': 'time', 'position': 'none'}],
                    yAxis=[{'label': 'sec', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 5}),
            ]),
            html.Div([
                html.Div("Temperature (C)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id='bp-live-temp', licenseKey=MUI_LICENSE_KEY, height=180,
                    series=[], xAxis=[{'id': 'x', 'data': [], 'scaleType': 'time', 'position': 'none'}],
                    yAxis=[{'label': 'C', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 5}),
            ]),
            html.Div([
                html.Div("Pressure (PSI)", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '2px'}),
                CompositeChart(
                    id='bp-live-pressure', licenseKey=MUI_LICENSE_KEY, height=220,
                    series=[], xAxis=[{'id': 'x', 'data': [], 'scaleType': 'time'}],
                    yAxis=[{'label': 'PSI', 'width': 60, 'domainLimit': 'nice'}],
                    tooltip={'trigger': 'axis'}, axisHighlight={'x': 'line'}, hideLegend=True,
                    margin={'left': 65, 'right': 15, 'top': 10, 'bottom': 55}),
            ]),
        ]),

        # Hidden stores
        dcc.Store(id='bp-live-store', data=generate_initial_live_data()),
        dcc.Store(id='bp-live-running', data=False),
        dcc.Interval(id='bp-live-interval', interval=300, disabled=True),
    ], style=section_style)


# ---------------------------------------------------------------------------
# Layout — lightweight shell; heavy chart sections loaded via callback
# ---------------------------------------------------------------------------
layout = dmc.Box(
    pos="relative",
    children=[
        dmc.LoadingOverlay(
            id='bp-loading-overlay',
            visible=True,
            zIndex=10,
            overlayProps={"blur": 4},
            loaderProps={
                "variant": "custom",
                "children": dmc.Stack(
                    [
                        html.Img(
                            src='/assets/light_mode_2plot.png',
                            className='bp-loading-logo',
                            style={'width': '100px', 'height': '100px', 'objectFit': 'contain'},
                        ),
                        dmc.Text("Loading charts...", size="sm", c="dimmed", fw=500),
                    ],
                    align="center",
                    gap="sm",
                ),
            },
        ),

        html.Div([
            html.Div([
                html.H1("Composite Render Best Practices", style={'display': 'inline'}),
                html.Span("v1.2.0", style=badge_style),
            ]),
            html.P(
                "Optimal rendering of stacked equipment dashboards across date ranges. "
                "The 7-day range is a live streaming demo; the rest are static previews "
                "tuned per data volume. Equipment pings every ~5 minutes.",
                style={'fontSize': '15px', 'color': 'var(--mantine-color-dimmed)', 'marginBottom': '10px'}),
            html.Div([
                html.Div("Configuration tuned per range:", style={'fontWeight': 500, 'marginBottom': '4px'}),
                html.Ul([
                    html.Li("tickNumber / tickMinStep: controls label density to avoid overlap"),
                    html.Li("dateTickFormat: shorter at wider ranges (dd/MM -> MMM YY)"),
                    html.Li("dateFormat: full precision in tooltips"),
                    html.Li("event marker size: smaller at denser ranges for clarity"),
                ], style={'fontSize': '13px', 'color': 'var(--mantine-color-dimmed)', 'marginBottom': '20px'}),
            ]),

            html.Hr(),

            # Deferred content — populated by callback on page load
            html.Div(id='bp-deferred-content', style={'minHeight': '600px'}),

        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}),

        # Hidden trigger — fires once on page load
        dcc.Store(id='bp-page-loaded', data=True),
    ],
)


# ===========================================================================
# Deferred content — builds all chart sections on page load
# ===========================================================================
@callback(
    Output('bp-deferred-content', 'children'),
    Output('bp-loading-overlay', 'visible'),
    Input('bp-page-loaded', 'data'),
)
def load_chart_sections(_trigger):
    """Build all chart sections server-side. The overlay shows while this runs."""
    content = [
        # Live 7d section
        build_live_7d_section(),
        html.Hr(),
        # Static range sections
        *[build_range_section(key) for key in RANGE_PROFILES],
        # Config reference table
        html.Div([
            html.H3("Configuration Reference"),
            html.Pre(
                "Range      | Points   | tickNum | tickMinStep | tickFormat | markerSize\n"
                "-----------+----------+---------+-------------+------------+-----------\n"
                "7 Days     |    2,016 |       7 |       1d    |      dd/MM |      7  (live)\n"
                + "\n".join(
                    f"{p['label']:10s} | {DATASETS[k]['n_points']:>8,} | {p['tick_number']:>7} | "
                    f"{p['tick_min_step'] // DAY_MS:>8}d    | {p['date_tick_format']:>10s} | "
                    f"{p['event_marker_size']:>6}"
                    for k, p in RANGE_PROFILES.items()),
                style=code_style),
        ], style={'marginBottom': '40px'}),
    ]
    return content, False  # Hide overlay when done


# ===========================================================================
# Live 7d Callbacks
# ===========================================================================

@callback(
    Output('bp-live-interval', 'disabled'),
    Output('bp-live-running', 'data'),
    Output('bp-live-status', 'children'),
    Output('bp-live-status', 'style'),
    Input('bp-live-start', 'n_clicks'),
    Input('bp-live-stop', 'n_clicks'),
    prevent_initial_call=True,
)
def live_toggle(start, stop):
    running = ctx.triggered_id == 'bp-live-start'
    return (
        not running,
        running,
        "Streaming" if running else "Stopped",
        {'fontSize': '18px', 'fontWeight': 'bold', 'color': '#4caf50' if running else '#999'},
    )


@callback(
    Output('bp-live-store', 'data', allow_duplicate=True),
    Output('bp-live-interval', 'disabled', allow_duplicate=True),
    Output('bp-live-running', 'data', allow_duplicate=True),
    Output('bp-live-status', 'children', allow_duplicate=True),
    Output('bp-live-status', 'style', allow_duplicate=True),
    Input('bp-live-reset', 'n_clicks'),
    prevent_initial_call=True,
)
def live_reset(_):
    return (
        generate_initial_live_data(),
        True, False, "Stopped",
        {'fontSize': '18px', 'fontWeight': 'bold', 'color': 'var(--mantine-color-dimmed)'},
    )


@callback(Output('bp-live-interval', 'interval'), Input('bp-live-speed', 'value'))
def live_speed(val):
    return val or 300


@callback(
    Output('bp-live-store', 'data'),
    Input('bp-live-interval', 'n_intervals'),
    State('bp-live-store', 'data'),
    State('bp-live-running', 'data'),
    prevent_initial_call=True,
)
def live_tick(_, store, running):
    if not running or not store:
        return no_update

    i = store['tick_index']
    base_ts = store['base_ts']
    ts = base_ts + i * FIVE_MIN_MS
    daily = math.sin(2 * math.pi * i / 288)

    # Continue random walk from last stored values
    d_val = store.get('last_d', 4.0)
    t_val = store.get('last_t', 45.0)
    ip_val = store.get('last_ip', 110.0)
    mp_val = store.get('last_mp', 90.0)

    d_val += 0.02 * (4.0 - d_val) + random.gauss(0, 0.08) + 0.15 * daily
    d_val = max(1.5, min(7.0, d_val))

    t_val += 0.01 * (45.0 - t_val) + random.gauss(0, 0.4) + 1.0 * daily
    t_val = max(25, min(65, t_val))

    ip_val += 0.005 * (110.0 - ip_val) - 0.002 + random.gauss(0, 0.3) + 0.8 * daily
    ip_val = max(85, min(130, ip_val))

    mp_val += 0.01 * (ip_val - 20 - mp_val) + random.gauss(0, 0.25)
    mp_val = max(60, min(ip_val - 5, mp_val))

    d = round(d_val, 2)
    t = round(t_val, 1)
    ip = round(ip_val, 1)
    mp = round(mp_val, 1)

    store['timestamps'].append(ts)
    store['discharge'].append(d)
    store['temp'].append(t)
    store['init_pressure'].append(ip)
    store['min_pressure'].append(mp)
    store['tick_index'] = i + 1
    store['last_d'] = d
    store['last_t'] = t
    store['last_ip'] = ip
    store['last_mp'] = mp

    # Random event (~1% chance per tick)
    if random.random() < 0.01:
        eid = store['event_counter']
        store['events_discharge'].append({'x': ts, 'y': round(d + random.choice([-1, 1]) * 2, 2), 'id': eid})
        store['events_temp'].append({'x': ts, 'y': round(t + random.choice([-1, 1]) * 10, 1), 'id': eid})
        store['events_pressure'].append({'x': ts, 'y': round(mp - 8, 1), 'id': eid})
        store['event_counter'] = eid + 1

    # Cap total points
    n = len(store['timestamps'])
    if n > LIVE_MAX_POINTS * 2:
        trim = n - LIVE_MAX_POINTS
        store['timestamps'] = store['timestamps'][trim:]
        store['discharge'] = store['discharge'][trim:]
        store['temp'] = store['temp'][trim:]
        store['init_pressure'] = store['init_pressure'][trim:]
        store['min_pressure'] = store['min_pressure'][trim:]
        min_ts = store['timestamps'][0]
        store['events_discharge'] = [e for e in store['events_discharge'] if e['x'] >= min_ts]
        store['events_temp'] = [e for e in store['events_temp'] if e['x'] >= min_ts]
        store['events_pressure'] = [e for e in store['events_pressure'] if e['x'] >= min_ts]

    return store


def _build_forecast(timestamps, values, n_ahead, mean_target=None):
    """Build a smooth forecast with expanding uncertainty band.

    Uses exponential moving average over a long lookback to compute a stable
    trend, then projects forward with mean-reversion toward mean_target.
    Uncertainty band widens proportionally to sqrt(steps_ahead).
    """
    if not values or len(values) < 20 or n_ahead <= 0:
        return []

    last_ts = timestamps[-1]
    last_val = values[-1]

    # --- Smooth trend via EMA over last 72 points (~6 hours) ---
    lookback = min(72, len(values))
    recent = values[-lookback:]
    # EMA of per-step changes (alpha=0.05 for heavy smoothing)
    alpha = 0.05
    ema_delta = 0.0
    for k in range(1, len(recent)):
        delta = recent[k] - recent[k - 1]
        ema_delta = alpha * delta + (1 - alpha) * ema_delta

    # --- Volatility from standard deviation of recent diffs ---
    diffs = [recent[k] - recent[k - 1] for k in range(1, len(recent))]
    if diffs:
        mean_diff = sum(diffs) / len(diffs)
        variance = sum((d - mean_diff) ** 2 for d in diffs) / len(diffs)
        vol = math.sqrt(variance) if variance > 0 else abs(last_val) * 0.005
    else:
        vol = abs(last_val) * 0.005

    # --- Project forward with decaying trend + mean reversion ---
    forecast = []
    center = last_val
    trend = ema_delta

    for j in range(n_ahead + 1):
        ts = last_ts + j * FIVE_MIN_MS

        # Uncertainty grows with sqrt of distance
        spread = vol * 2.0 * math.sqrt(1 + j)

        forecast.append({
            'x': ts,
            'y': round(center, 2),
            'upper': round(center + spread, 2),
            'lower': round(center - spread, 2),
        })

        # Advance center: decaying trend + gentle mean reversion
        trend *= 0.98  # trend decays toward zero
        if mean_target is not None:
            # Pull gently toward the long-term mean
            reversion = 0.003 * (mean_target - center)
            center += trend + reversion
        else:
            center += trend

    return forecast


@callback(
    Output('bp-live-discharge', 'series'),
    Output('bp-live-discharge', 'xAxis'),
    Output('bp-live-discharge', 'forecast'),
    Output('bp-live-temp', 'series'),
    Output('bp-live-temp', 'xAxis'),
    Output('bp-live-temp', 'forecast'),
    Output('bp-live-pressure', 'series'),
    Output('bp-live-pressure', 'xAxis'),
    Output('bp-live-pressure', 'forecast'),
    Output('bp-live-stat-points', 'children'),
    Output('bp-live-stat-discharge', 'children'),
    Output('bp-live-stat-temp', 'children'),
    Output('bp-live-stat-initp', 'children'),
    Output('bp-live-stat-minp', 'children'),
    Input('bp-live-store', 'data'),
    State('bp-live-window', 'value'),
    State('bp-live-estimate', 'value'),
)
def live_render(store, window, estimate):
    if not store or not store['timestamps']:
        return no_update

    window = window or LIVE_WINDOW_DEFAULT
    estimate = estimate or 0
    n = len(store['timestamps'])
    start = max(0, n - window)

    # Windowed data (copies to avoid mutating store)
    ts_win = list(store['timestamps'][start:])
    dis_win = list(store['discharge'][start:])
    temp_win = list(store['temp'][start:])
    initp_win = list(store['init_pressure'][start:])
    minp_win = list(store['min_pressure'][start:])

    # Build forecast overlays with mean-reversion targets
    fc_discharge = _build_forecast(ts_win, dis_win, estimate, mean_target=4.0)
    fc_temp = _build_forecast(ts_win, temp_win, estimate, mean_target=45.0)
    fc_initp = _build_forecast(ts_win, initp_win, estimate, mean_target=110.0)
    fc_minp = _build_forecast(ts_win, minp_win, estimate, mean_target=90.0)

    # Extend x-axis to include forecast range so the band is visible
    if estimate > 0:
        last_ts = ts_win[-1]
        for j in range(1, estimate + 1):
            ts_win.append(last_ts + j * FIVE_MIN_MS)
            dis_win.append(None)
            temp_win.append(None)
            initp_win.append(None)
            minp_win.append(None)

    # Filter events to visible time range
    min_ts = ts_win[0]
    max_ts = ts_win[-1]
    ev_d = [e for e in store['events_discharge'] if min_ts <= e['x'] <= max_ts]
    ev_t = [e for e in store['events_temp'] if min_ts <= e['x'] <= max_ts]
    ev_p = [e for e in store['events_pressure'] if min_ts <= e['x'] <= max_ts]

    x_hidden = [{'id': 'x', 'data': ts_win, 'scaleType': 'time',
                 'tickNumber': 7, 'tickMinStep': DAY_MS,
                 'dateFormat': 'dd/MM/YYYY HH:mm', 'dateTickFormat': 'dd/MM HH:mm',
                 'position': 'none'}]
    x_visible = [{'id': 'x', 'data': ts_win, 'scaleType': 'time',
                  'label': 'Date', 'height': 40,
                  'tickNumber': 7, 'tickMinStep': DAY_MS,
                  'dateFormat': 'dd/MM/YYYY HH:mm', 'dateTickFormat': 'dd/MM HH:mm',
                  'tickLabelStyle': {'fontSize': 11},
                  'labelStyle': {'fontSize': 12}}]

    series_d = [
        {'type': 'line', 'id': 'discharge', 'label': 'Discharge Time',
         'data': dis_win, 'color': '#1976d2', 'showMark': False, 'connectNulls': False},
        {'type': 'scatter', 'id': 'events', 'label': 'Events',
         'data': ev_d, 'color': '#e53935', 'markerSize': 7},
    ]
    series_t = [
        {'type': 'line', 'id': 'temp', 'label': 'Temperature',
         'data': temp_win, 'color': '#e65100', 'showMark': False, 'connectNulls': False},
        {'type': 'scatter', 'id': 'events', 'label': 'Events',
         'data': ev_t, 'color': '#e53935', 'markerSize': 7},
    ]
    series_p = [
        {'type': 'line', 'id': 'init-pressure', 'label': 'Init Pressure',
         'data': initp_win, 'color': '#7b1fa2', 'showMark': False, 'connectNulls': False},
        {'type': 'line', 'id': 'min-pressure', 'label': 'Min Pressure',
         'data': minp_win, 'color': '#00838f', 'showMark': False, 'connectNulls': False},
        {'type': 'scatter', 'id': 'events', 'label': 'Events',
         'data': ev_p, 'color': '#e53935', 'markerSize': 7},
    ]

    # For pressure, merge init + min forecasts into a combined band
    # showing the wider envelope of both
    fc_pressure = []
    if fc_initp and fc_minp:
        for i in range(len(fc_initp)):
            ip, mp = fc_initp[i], fc_minp[i]
            fc_pressure.append({
                'x': ip['x'],
                'y': round((ip['y'] + mp['y']) / 2, 2),
                'upper': ip['upper'],
                'lower': mp['lower'],
            })

    # Latest values for stats
    last_d = store['discharge'][-1]
    last_t = store['temp'][-1]
    last_ip = store['init_pressure'][-1]
    last_mp = store['min_pressure'][-1]

    return (
        series_d, x_hidden, fc_discharge,
        series_t, x_hidden, fc_temp,
        series_p, x_visible, fc_pressure,
        f"{n:,}",
        f"{last_d:.2f}s",
        f"{last_t:.1f}C",
        f"{last_ip:.1f}",
        f"{last_mp:.1f}",
    )


# Live sync callback
@callback(
    Output('bp-live-discharge', 'highlightedAxis'),
    Output('bp-live-temp', 'highlightedAxis'),
    Output('bp-live-pressure', 'highlightedAxis'),
    Output('bp-live-discharge', 'syncedTooltipIndex'),
    Output('bp-live-temp', 'syncedTooltipIndex'),
    Output('bp-live-pressure', 'syncedTooltipIndex'),
    Input('bp-live-discharge', 'highlightedAxis'),
    Input('bp-live-temp', 'highlightedAxis'),
    Input('bp-live-pressure', 'highlightedAxis'),
    State('bp-live-sync', 'checked'),
    prevent_initial_call=True,
)
def live_sync(ax_d, ax_t, ax_p, synced):
    source = ctx.triggered_id
    ids = ['bp-live-discharge', 'bp-live-temp', 'bp-live-pressure']
    axes = dict(zip(ids, [ax_d, ax_t, ax_p]))
    axis = axes.get(source, ax_d)
    idx = axis[0]['dataIndex'] if axis and len(axis) > 0 else -1
    if not synced:
        return axis, axis, axis, -1, -1, -1
    tips = [idx if cid != source else -1 for cid in ids]
    return axis, axis, axis, tips[0], tips[1], tips[2]


# ===========================================================================
# Static range sync callbacks
# ===========================================================================
def make_sync_callback(range_key):
    prefix = f'bp-{range_key}'
    ids = [f'{prefix}-discharge', f'{prefix}-temp', f'{prefix}-pressure']

    @callback(
        *[Output(cid, 'highlightedAxis') for cid in ids],
        *[Output(cid, 'syncedTooltipIndex') for cid in ids],
        *[Input(cid, 'highlightedAxis') for cid in ids],
        State(f'{prefix}-sync', 'checked'),
        prevent_initial_call=True,
    )
    def sync_charts(*args):
        ax_d, ax_t, ax_p, synced = args[0], args[1], args[2], args[3]
        source = ctx.triggered_id
        axes_map = dict(zip(ids, [ax_d, ax_t, ax_p]))
        axis = axes_map.get(source, ax_d)
        idx = axis[0]['dataIndex'] if axis and len(axis) > 0 else -1
        if not synced:
            return axis, axis, axis, -1, -1, -1
        tips = [idx if cid != source else -1 for cid in ids]
        return axis, axis, axis, tips[0], tips[1], tips[2]

    sync_charts.__name__ = f'sync_{range_key}'
    return sync_charts


for _range_key in RANGE_PROFILES:
    make_sync_callback(_range_key)
