"""
LineChart Ticks & Hover - Tooltips, reference lines, ticks, and grid at various date ranges
"""

import os
import json
import math
import random
from datetime import datetime, timedelta

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/linechart-tick-hover', name='LineChart Ticks & Hover')

from dash_mui_charts import LineChart

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Common styles
section_style = {'marginBottom': '50px'}
description_style = {'color': '#666', 'marginBottom': '15px'}
code_style = {
    'backgroundColor': '#f5f5f5',
    'padding': '15px',
    'borderRadius': '5px',
    'whiteSpace': 'pre-wrap',
    'fontSize': '12px',
    'overflow': 'auto',
}
note_style = {
    'backgroundColor': '#fff3e0',
    'border': '1px solid #ffcc80',
    'borderRadius': '5px',
    'padding': '12px 16px',
    'marginBottom': '15px',
    'fontSize': '14px',
    'color': '#e65100',
}
tip_style = {
    'backgroundColor': '#e8f5e9',
    'border': '1px solid #a5d6a7',
    'borderRadius': '5px',
    'padding': '12px 16px',
    'marginBottom': '15px',
    'fontSize': '14px',
    'color': '#1b5e20',
}

# ---------------------------------------------------------------------------
# Data Generation (fixed seed for reproducibility)
# ---------------------------------------------------------------------------
random.seed(42)

def generate_sensor_data(start_date, num_days, base=72, noise=5, trend=0.01):
    """Generate fake equipment sensor readings with slight upward trend."""
    dates = []
    values = []
    for i in range(num_days):
        d = start_date + timedelta(days=i)
        dates.append(d.strftime('%Y-%m-%d'))
        val = base + trend * i + noise * math.sin(i * 0.3) + random.gauss(0, noise * 0.3)
        values.append(round(val, 1))
    return dates, values

# 1-week data
week_start = datetime(2025, 3, 1)
week_dates, week_temps = generate_sensor_data(week_start, 7, base=68, noise=4, trend=0.3)

# 3-month data
quarter_start = datetime(2025, 1, 1)
quarter_dates, quarter_temps = generate_sensor_data(quarter_start, 90, base=65, noise=6, trend=0.05)

# 1-year data
year_start = datetime(2025, 1, 1)
year_dates, year_temps = generate_sensor_data(year_start, 365, base=70, noise=8, trend=0.02)

# Epoch-ms timestamps for time-scale charts (sections 5a-5c)
quarter_timestamps = [
    int(datetime(2025, 1, 1).timestamp() + i * 86400) * 1000
    for i in range(90)
]
year_timestamps = [
    int(datetime(2025, 1, 1).timestamp() + i * 86400) * 1000
    for i in range(365)
]

# Target / threshold values
warning_threshold = 78
critical_threshold = 85

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div([
    html.H1("LineChart Ticks & Hover"),
    html.P(
        "This page demonstrates best practices for configuring tooltips, reference lines, "
        "ticks, and grid on LineCharts across different date ranges. It addresses common "
        "alignment issues that appear when rendering large date ranges (year+).",
        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '30px'}
    ),

    # ======================================================================
    # 1. Short Date Range (1 Week) - Baseline
    # ======================================================================
    html.Div([
        html.H2("1. Short Date Range (1 Week) - Baseline"),
        html.P(
            "With a small number of data points, tooltips, reference lines, and ticks "
            "align perfectly. This is the baseline for comparison.",
            style=description_style
        ),
        LineChart(
            id='tick-hover-week',
            licenseKey=MUI_LICENSE_KEY,
            height=350,
            series=[{
                'data': week_temps,
                'label': 'Temp (F)',
                'color': '#1976d2',
                'showMark': True,
            }],
            xAxis=[{
                'data': week_dates,
                'scaleType': 'point',
                'label': 'Date',
            }],
            yAxis=[{
                'label': 'Temperature (F)',
                'min': 60,
                'max': 80,
            }],
            grid={'horizontal': True, 'vertical': True},
            axisHighlight={'x': 'line', 'y': 'line'},
            tooltip={'trigger': 'axis'},
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
                {
                    'x': week_dates[3],
                    'label': 'Inspection',
                    'lineStyle': {'stroke': '#9c27b0', 'strokeWidth': 2, 'strokeDasharray': '4 4'},
                    'labelStyle': {'fill': '#9c27b0'},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=350,
    series=[{'data': temps, 'label': 'Temp (F)', 'showMark': True}],
    xAxis=[{'data': dates, 'scaleType': 'point', 'label': 'Date'}],
    yAxis=[{'label': 'Temperature (F)', 'min': 60, 'max': 80}],
    grid={'horizontal': True, 'vertical': True},
    axisHighlight={'x': 'line', 'y': 'line'},
    tooltip={'trigger': 'axis'},
    referenceLines=[
        {
            'y': 78,
            'label': 'Warning (78F)',
            'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
            'labelStyle': {'fill': '#ff9800', 'fontWeight': 'bold'},
            'labelAlign': 'end',
        },
        {
            'x': '2025-03-04',  # Must match an x-axis data value exactly
            'label': 'Inspection',
            'lineStyle': {'stroke': '#9c27b0', 'strokeDasharray': '4 4'},
            'labelAlign': 'start',
        },
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 2. Medium Date Range (3 Months)
    # ======================================================================
    html.Div([
        html.H2("2. Medium Date Range (3 Months) - Daily Data"),
        html.P(
            "With ~90 data points, tick labels start to crowd. Use 'tickNumber' on a "
            "'point' scale to thin out labels. Reference lines at month boundaries "
            "still align well at this range.",
            style=description_style
        ),
        html.Div(
            "Tip: For point/band scale axes, 'tickNumber' controls how many ticks "
            "are shown. D3 will round to a readable number near your target.",
            style=tip_style
        ),
        LineChart(
            id='tick-hover-quarter',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[{
                'data': quarter_temps,
                'label': 'Equipment Temp (F)',
                'color': '#0288d1',
                'showMark': False,
            }],
            xAxis=[{
                'data': quarter_dates,
                'scaleType': 'point',
                'label': 'Date',
                'tickNumber': 12,
            }],
            yAxis=[{
                'label': 'Temperature (F)',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'line'},
            tooltip={'trigger': 'axis'},
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
                {
                    'x': '2025-02-01',
                    'label': 'Feb',
                    'lineStyle': {'stroke': '#78909c', 'strokeWidth': 1, 'strokeDasharray': '3 3'},
                    'labelStyle': {'fill': '#78909c', 'fontSize': 11},
                    'labelAlign': 'start',
                },
                {
                    'x': '2025-03-01',
                    'label': 'Mar',
                    'lineStyle': {'stroke': '#78909c', 'strokeWidth': 1, 'strokeDasharray': '3 3'},
                    'labelStyle': {'fill': '#78909c', 'fontSize': 11},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    height=400,
    series=[{'data': temps, 'label': 'Equipment Temp (F)', 'showMark': False}],
    xAxis=[{
        'data': dates,          # 90 daily date strings
        'scaleType': 'point',
        'label': 'Date',
        'tickNumber': 12,       # Show ~12 ticks across the axis
    }],
    grid={'horizontal': True},
    axisHighlight={'x': 'line'},
    tooltip={'trigger': 'axis'},
    referenceLines=[
        {'y': 78, 'label': 'Warning', ...},
        {'x': '2025-02-01', 'label': 'Feb', ...},  # Must match exact data value
        {'x': '2025-03-01', 'label': 'Mar', ...},
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 3. Large Date Range (1 Year) - scaleType 'point'
    # ======================================================================
    html.Div([
        html.H2("3. Large Date Range (1 Year) - 'point' Scale"),
        html.P(
            "With 365 data points on a 'point' scale, vertical reference lines placed by "
            "date string must match an exact data value. Horizontal reference lines remain "
            "accurate since they use the Y-axis numeric scale. The axis highlight and "
            "tooltip still track correctly on hover.",
            style=description_style
        ),
        html.Div(
            "Note: On a 'point' scale, each data value gets equal spacing regardless of "
            "actual time gaps. If your data has irregular intervals (missing days, weekends "
            "excluded), the visual spacing won't reflect real time - which can make "
            "reference lines appear offset from where you'd expect them calendrically.",
            style=note_style
        ),
        LineChart(
            id='tick-hover-year-point',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[{
                'data': year_temps,
                'label': 'Equipment Temp (F)',
                'color': '#2e7d32',
                'showMark': False,
            }],
            xAxis=[{
                'data': year_dates,
                'scaleType': 'point',
                'label': 'Date (365 points, point scale)',
                'tickNumber': 12,
            }],
            yAxis=[{
                'label': 'Temperature (F)',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'line'},
            tooltip={'trigger': 'axis'},
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
                {
                    'y': critical_threshold,
                    'label': 'Critical (85F)',
                    'lineStyle': {'stroke': '#d32f2f', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#d32f2f', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
                {
                    'x': '2025-07-01',
                    'label': 'Mid-Year',
                    'lineStyle': {'stroke': '#5c6bc0', 'strokeWidth': 2, 'strokeDasharray': '6 3'},
                    'labelStyle': {'fill': '#5c6bc0'},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# 365 daily points on a 'point' scale
LineChart(
    height=400,
    series=[{'data': year_temps, 'label': 'Equipment Temp (F)', 'showMark': False}],
    xAxis=[{
        'data': year_dates,         # ['2025-01-01', '2025-01-02', ...]
        'scaleType': 'point',       # Equal spacing per point
        'label': 'Date',
        'tickNumber': 12,           # ~12 tick labels
    }],
    axisHighlight={'x': 'line'},
    tooltip={'trigger': 'axis'},
    referenceLines=[
        {'y': 78, 'label': 'Warning (78F)', ...},
        {'y': 85, 'label': 'Critical (85F)', ...},
        {
            'x': '2025-07-01',     # Must match exact value in data array
            'label': 'Mid-Year',
            ...
        },
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 4. Large Date Range (1 Year) - Best Practice with Linear Index
    # ======================================================================
    html.Div([
        html.H2("4. Large Date Range (1 Year) - Linear Index (Best Practice)"),
        html.P(
            "For large date ranges, using integer indices with 'linear' scale type gives "
            "uniform spacing and precise reference line placement. Vertical reference "
            "lines are placed by index number, ensuring exact pixel alignment.",
            style=description_style
        ),
        html.Div(
            "Best Practice: Use 'scaleType': 'linear' with integer indices for large "
            "datasets. Place vertical reference lines by index position. This avoids "
            "the string-matching and equal-spacing issues of 'point' scale.",
            style=tip_style
        ),
        LineChart(
            id='tick-hover-year-linear',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[{
                'data': year_temps,
                'label': 'Equipment Temp (F)',
                'color': '#1565c0',
                'showMark': False,
            }],
            xAxis=[{
                'data': list(range(len(year_dates))),
                'scaleType': 'linear',
                'label': 'Day Index (0 = Jan 1, 2025)',
                'tickNumber': 12,
            }],
            yAxis=[{
                'label': 'Temperature (F)',
            }],
            grid={'horizontal': True, 'vertical': True},
            axisHighlight={'x': 'line'},
            tooltip={'trigger': 'axis'},
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
                {
                    'y': critical_threshold,
                    'label': 'Critical (85F)',
                    'lineStyle': {'stroke': '#d32f2f', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#d32f2f', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
                {
                    'x': 181,  # July 1 = day index 181
                    'label': 'Mid-Year (Day 181)',
                    'lineStyle': {'stroke': '#5c6bc0', 'strokeWidth': 2, 'strokeDasharray': '6 3'},
                    'labelStyle': {'fill': '#5c6bc0'},
                    'labelAlign': 'start',
                },
                {
                    'x': 90,  # ~April 1
                    'label': 'Q1 End (Day 90)',
                    'lineStyle': {'stroke': '#78909c', 'strokeWidth': 1, 'strokeDasharray': '3 3'},
                    'labelStyle': {'fill': '#78909c', 'fontSize': 11},
                    'labelAlign': 'start',
                },
                {
                    'x': 273,  # ~Oct 1
                    'label': 'Q3 End (Day 273)',
                    'lineStyle': {'stroke': '#78909c', 'strokeWidth': 1, 'strokeDasharray': '3 3'},
                    'labelStyle': {'fill': '#78909c', 'fontSize': 11},
                    'labelAlign': 'start',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Use integer indices with linear scale for large datasets
year_indices = list(range(365))

LineChart(
    height=400,
    series=[{'data': year_temps, 'label': 'Equipment Temp (F)', 'showMark': False}],
    xAxis=[{
        'data': year_indices,
        'scaleType': 'linear',      # Uniform numeric spacing
        'label': 'Day Index (0 = Jan 1)',
        'tickNumber': 12,
    }],
    grid={'horizontal': True, 'vertical': True},
    axisHighlight={'x': 'line'},
    tooltip={'trigger': 'axis'},
    referenceLines=[
        {'y': 78, 'label': 'Warning', ...},
        {'y': 85, 'label': 'Critical', ...},
        {
            'x': 181,               # Place by index, not string
            'label': 'Mid-Year (Day 181)',
            ...
        },
        {'x': 90, 'label': 'Q1 End', ...},
        {'x': 273, 'label': 'Q3 End', ...},
    ],
)""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 5. Tick Configuration Best Practices
    # ======================================================================
    html.Div([
        html.H2("5. Tick Configuration Best Practices"),
        html.P(
            "Fine-tune tick appearance with tickNumber, tickSize, and tickLabelStyle. "
            "For dense data, angled labels and controlled tick counts improve readability.",
            style=description_style
        ),

        # --- 5a. Angled tick labels ---
        html.H3("5a. Angled Labels & Controlled Tick Count", style={'marginTop': '25px'}),
        html.Div(
            "Tip: Use 'scaleType': 'time' with epoch-ms timestamps and a valueFormatter "
            "to control date label format. Define JS functions in assets/*.js using the "
            "dashMuiChartsFunctions pattern (like Dash Mantine Components).",
            style=tip_style
        ),
        LineChart(
            id='tick-hover-config',
            licenseKey=MUI_LICENSE_KEY,
            height=420,
            series=[
                {
                    'data': quarter_temps,
                    'label': 'Sensor A',
                    'color': '#1976d2',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'data': quarter_timestamps,
                'scaleType': 'time',
                'label': 'Date',
                'height': 80,
                'tickNumber': 6,
                'tickMinStep': 86400 * 1000 * 15,
                'dateFormat': 'M/d HH:mm',
                'dateTickFormat': 'M/d',
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 12,
                    'textAnchor': 'start',
                },
                'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
            }],
            yAxis=[{
                'label': 'Temperature (F)',
            }],
            grid={'horizontal': True, 'vertical': True},
            axisHighlight={'x': 'line'},
            tooltip={'trigger': 'axis'},
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 100},
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Convert dates to epoch-ms timestamps for time scale
timestamps = [int(datetime(2025, 1, 1).timestamp() + i * 86400) * 1000 for i in range(90)]

LineChart(
    height=420,
    series=[{'data': temps, 'label': 'Sensor A', 'showMark': False}],
    xAxis=[{
        'data': timestamps,
        'scaleType': 'time',
        'label': 'Date',
        'height': 80,                        # Extra vertical space for angled labels
        'tickNumber': 6,                     # ~6 ticks for 90-day range
        'tickMinStep': 86400 * 1000 * 15,    # Min 15 days between ticks
        'dateFormat': 'M/d HH:mm',           # Full format for tooltips
        'dateTickFormat': 'M/d',              # Short format for tick labels
        'tickLabelStyle': {
            'angle': 35,
            'fontSize': 11,
            'textAnchor': 'start',
        },
        'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
    }],
    yAxis=[{'label': 'Temperature (F)'}],
    grid={'horizontal': True, 'vertical': True},
    axisHighlight={'x': 'line'},
    tooltip={'trigger': 'axis'},
    margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 80},
)
""", style=code_style),
        ]),

        # --- 5b. Zoom with Slider (Pro) ---
        html.H3("5b. Zoom with Slider - Tick Behavior on Zoom", style={'marginTop': '40px'}),
        html.P(
            "When zoomed in, tick density increases to match the visible range. "
            "The slider provides a minimap of the full dataset. Notice how tick labels "
            "automatically adjust as you zoom - this is why 'tickNumber' is approximate.",
            style=description_style
        ),
        html.Div(
            "Pro Feature: showSlider=True enables the zoom slider. Drag the slider "
            "handles or use mouse wheel to zoom. The chart auto-adjusts tick density.",
            style=note_style
        ),
        LineChart(
            id='tick-hover-zoom-slider',
            licenseKey=MUI_LICENSE_KEY,
            height=450,
            series=[{
                'data': year_temps,
                'label': 'Equipment Temp (F)',
                'color': '#0288d1',
                'showMark': False,
                'curve': 'natural',
            }],
            xAxis=[{
                'id': 'tick-zoom-x',
                'data': year_timestamps,
                'scaleType': 'time',
                'label': 'Date',
                'height': 80,
                'tickNumber': 6,
                'tickMinStep': 86400 * 1000 * 30,
                'dateFormat': 'M/d HH:mm',
                'dateTickFormat': 'M/d',
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 12,
                    'textAnchor': 'start',
                },
                'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
                'zoom': {
                    'minSpan': 5,
                    'panning': True,
                    'slider': {
                        'enabled': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Temperature (F)',
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'line'},
            tooltip={'trigger': 'axis'},
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 100},
            initialZoom=[{'axisId': 'tick-zoom-x', 'start': 0, 'end': 30}],
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
            ],
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Epoch-ms timestamps for time scale
year_timestamps = [int(datetime(2025, 1, 1).timestamp() + i * 86400) * 1000 for i in range(365)]

LineChart(
    height=450,
    series=[{
        'data': year_temps, 'label': 'Equipment Temp (F)',
        'showMark': False, 'curve': 'natural',
    }],
    xAxis=[{
        'id': 'tick-zoom-x',
        'data': year_timestamps,
        'scaleType': 'time',
        'label': 'Date',
        'height': 80,
        'tickNumber': 6,
        'tickMinStep': 86400 * 1000 * 30,    # Min 30 days between ticks
        'dateFormat': 'M/d HH:mm',           # Full format for tooltips
        'dateTickFormat': 'M/d',              # Short format for tick labels
        'tickLabelStyle': {'angle': 35, 'fontSize': 12, 'textAnchor': 'start'},
        'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
        'zoom': {
            'minSpan': 5,
            'panning': True,
            'slider': {'enabled': True},
        },
    }],
    yAxis=[{'label': 'Temperature (F)', 'domainLimit': 'nice'}],
    margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 80},
    initialZoom=[{'axisId': 'tick-zoom-x', 'start': 0, 'end': 30}],
    referenceLines=[{'y': 78, 'label': 'Warning (78F)', ...}],
)""", style=code_style),
        ]),

        # --- 5c. Pro Zoom with Brush & Preview ---
        html.H3("5c. Pro Zoom - Brush Select & Slider Preview", style={'marginTop': '40px'}),
        html.P(
            "Advanced zoom with brush selection (click-drag to zoom), slider preview "
            "showing the data shape, and fine-grained zoomInteractionConfig. "
            "Double-click to reset zoom. Ticks adapt dynamically as the visible range changes.",
            style=description_style
        ),
        html.Div(
            "Pro Feature: zoomInteractionConfig controls how zoom/pan interactions work. "
            "Use 'brush' for click-drag area selection, 'scroll' for mousewheel zoom. "
            "The slider 'preview: True' renders a miniature line in the slider track.",
            style=note_style
        ),
        LineChart(
            id='tick-hover-zoom-pro',
            licenseKey=MUI_LICENSE_KEY,
            height=480,
            series=[
                {
                    'data': year_temps,
                    'label': 'Equipment Temp (F)',
                    'color': '#1565c0',
                    'showMark': False,
                    'curve': 'natural',
                },
                {
                    'data': [t + random.gauss(5, 2) for t in year_temps],
                    'label': 'Ambient Temp (F)',
                    'color': '#e65100',
                    'showMark': False,
                    'curve': 'natural',
                },
            ],
            xAxis=[{
                'id': 'tick-zoom-pro-x',
                'data': year_timestamps,
                'scaleType': 'time',
                'label': 'Date',
                'height': 80,
                'tickNumber': 6,
                'tickMinStep': 86400 * 1000 * 30,
                'dateFormat': 'M/d HH:mm',
                'dateTickFormat': 'M/d',
                'tickLabelStyle': {
                    'angle': 35,
                    'fontSize': 12,
                    'textAnchor': 'start',
                },
                'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
                'zoom': {
                    'minSpan': 2,
                    'panning': True,
                    'filterMode': 'discard',
                    'slider': {
                        'enabled': True,
                        'preview': True,
                    },
                },
            }],
            yAxis=[{
                'label': 'Temperature (F)',
                'domainLimit': 'nice',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'line', 'y': 'line'},
            tooltip={'trigger': 'axis'},
            margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 100},
            initialZoom=[{'axisId': 'tick-zoom-pro-x', 'start': 20, 'end': 50}],
            zoomInteractionConfig={
                'enabled': True,
                'panOnScrollEnabled': True,
            },
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
                {
                    'y': critical_threshold,
                    'label': 'Critical (85F)',
                    'lineStyle': {'stroke': '#d32f2f', 'strokeWidth': 2},
                    'labelStyle': {'fill': '#d32f2f', 'fontWeight': 'bold'},
                    'labelAlign': 'end',
                },
            ],
            showToolbar=True,
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""# Epoch-ms timestamps for time scale
year_timestamps = [int(datetime(2025, 1, 1).timestamp() + i * 86400) * 1000 for i in range(365)]

LineChart(
    height=480,
    series=[
        {'data': equipment_temps, 'label': 'Equipment Temp (F)',
         'color': '#1565c0', 'showMark': False, 'curve': 'natural'},
        {'data': ambient_temps, 'label': 'Ambient Temp (F)',
         'color': '#e65100', 'showMark': False, 'curve': 'natural'},
    ],
    xAxis=[{
        'id': 'tick-zoom-pro-x',
        'data': year_timestamps,
        'scaleType': 'time',
        'label': 'Date',
        'height': 80,
        'tickNumber': 6,
        'tickMinStep': 86400 * 1000 * 30,
        'dateFormat': 'M/d HH:mm',
        'dateTickFormat': 'M/d',
        'tickLabelStyle': {'angle': 35, 'fontSize': 12, 'textAnchor': 'start'},
        'labelStyle': {'fontSize': 13, 'fontWeight': 'bold'},
        'zoom': {
            'minSpan': 2,
            'panning': True,
            'filterMode': 'discard',
            'slider': {'enabled': True, 'preview': True},
        },
    }],
    yAxis=[{'label': 'Temperature (F)', 'domainLimit': 'nice'}],
    margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 80},
    initialZoom=[{'axisId': 'tick-zoom-pro-x', 'start': 20, 'end': 50}],
    zoomInteractionConfig={'enabled': True, 'panOnScrollEnabled': True},
    referenceLines=[
        {'y': 78, 'label': 'Warning', ...},
        {'y': 85, 'label': 'Critical', ...},
    ],
    showToolbar=True,
)

# In assets/muiChartsFunctions.js, define the formatDate function:
# window.dashMuiChartsFunctions.formatDate = function(value, context, options) { ... };
""", style=code_style),
        ]),

        # --- Key Tick Props Table ---
        html.Div([
            html.H4("Key Tick & Zoom Props:", style={'marginTop': '30px'}),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Prop", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                        html.Th("Type", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                        html.Th("Description", style={'textAlign': 'left', 'padding': '8px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([html.Td("tickNumber", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Approximate number of ticks. D3 rounds for readability.", style={'padding': '8px'})]),
                    html.Tr([html.Td("tickSize", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Length of tick marks in pixels (default: 6).", style={'padding': '8px'})]),
                    html.Tr([html.Td("tickMinStep", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Min step between ticks. For time scale, value in ms (e.g. 86400000 = 1 day).", style={'padding': '8px'})]),
                    html.Tr([html.Td("tickMaxStep", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Max step between ticks.", style={'padding': '8px'})]),
                    html.Tr([html.Td("tickLabelStyle", style={'padding': '8px'}), html.Td("object", style={'padding': '8px'}), html.Td("CSS style for labels: angle, fontSize, textAnchor, dominantBaseline.", style={'padding': '8px'})]),
                    html.Tr([html.Td("tickLabelMinGap", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Minimum gap in px between tick labels (default: 4).", style={'padding': '8px'})]),
                    html.Tr([html.Td("height", style={'padding': '8px'}), html.Td("number", style={'padding': '8px'}), html.Td("Axis height in px. Increase for angled labels (e.g. 50).", style={'padding': '8px'})]),
                    html.Tr([html.Td("disableTicks", style={'padding': '8px'}), html.Td("boolean", style={'padding': '8px'}), html.Td("Hide tick marks entirely.", style={'padding': '8px'})]),
                    html.Tr([html.Td("disableLine", style={'padding': '8px'}), html.Td("boolean", style={'padding': '8px'}), html.Td("Hide the axis line.", style={'padding': '8px'})]),
                    html.Tr([
                        html.Td("valueFormatter", style={'padding': '8px', 'fontWeight': 'bold', 'color': '#2e7d32'}),
                        html.Td("object", style={'padding': '8px'}),
                        html.Td("Functions-as-props: {'function': 'name', 'options': {...}}. Resolves from window.dashMuiChartsFunctions.", style={'padding': '8px'}),
                    ]),
                    html.Tr([
                        html.Td("zoom (Pro)", style={'padding': '8px', 'fontWeight': 'bold', 'color': '#1565c0'}),
                        html.Td("object", style={'padding': '8px'}),
                        html.Td("Enable zoom on axis: minSpan, panning, filterMode, slider.enabled, slider.preview.", style={'padding': '8px'}),
                    ]),
                    html.Tr([
                        html.Td("initialZoom", style={'padding': '8px', 'fontWeight': 'bold', 'color': '#1565c0'}),
                        html.Td("array", style={'padding': '8px'}),
                        html.Td("Initial zoom state: [{axisId, start, end}]. Values are percentages (0-100).", style={'padding': '8px'}),
                    ]),
                    html.Tr([
                        html.Td("showToolbar (Pro)", style={'padding': '8px', 'fontWeight': 'bold', 'color': '#1565c0'}),
                        html.Td("boolean", style={'padding': '8px'}),
                        html.Td("Show Pro toolbar with zoom/export controls above the chart.", style={'padding': '8px'}),
                    ]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse'}),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 6. Hover Events & Axis Highlight
    # ======================================================================
    html.Div([
        html.H2("6. Interactive Hover Events & Axis Highlight"),
        html.P(
            "Combine axis highlight, tooltips, and reference lines on a medium-range chart. "
            "Click on the chart to capture event data via Dash callbacks.",
            style=description_style
        ),
        LineChart(
            id='tick-hover-interactive',
            licenseKey=MUI_LICENSE_KEY,
            height=400,
            series=[
                {
                    'data': quarter_temps,
                    'label': 'Sensor A',
                    'color': '#1565c0',
                    'showMark': True,
                },
                {
                    'data': [t + random.gauss(3, 1.5) for t in quarter_temps],
                    'label': 'Sensor B',
                    'color': '#e65100',
                    'showMark': False,
                },
            ],
            xAxis=[{
                'data': quarter_dates,
                'scaleType': 'point',
                'label': 'Date',
                'tickNumber': 10,
            }],
            yAxis=[{
                'label': 'Temperature (F)',
            }],
            grid={'horizontal': True},
            axisHighlight={'x': 'line', 'y': 'line'},
            tooltip={'trigger': 'axis'},
            referenceLines=[
                {
                    'y': warning_threshold,
                    'label': 'Warning (78F)',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 2, 'strokeDasharray': '5 5'},
                    'labelStyle': {'fill': '#ff9800'},
                    'labelAlign': 'end',
                },
            ],
        ),
        html.H4("Click Data:", style={'marginTop': '15px'}),
        html.Pre(
            id='tick-hover-click-output',
            children="Click on the chart to see event data",
            style=code_style
        ),
        html.Details([
            html.Summary("View Code", style={'cursor': 'pointer', 'marginTop': '10px'}),
            html.Pre("""LineChart(
    id='tick-hover-interactive',
    height=400,
    series=[
        {'data': sensor_a, 'label': 'Sensor A', 'showMark': True},
        {'data': sensor_b, 'label': 'Sensor B', 'showMark': False},
    ],
    xAxis=[{'data': dates, 'scaleType': 'point', 'tickNumber': 10}],
    grid={'horizontal': True},
    axisHighlight={'x': 'line', 'y': 'line'},  # Crosshair on hover
    tooltip={'trigger': 'axis'},                # Show all series at position
    referenceLines=[
        {'y': 78, 'label': 'Warning', ...},
    ],
)

@callback(
    Output('tick-hover-click-output', 'children'),
    Input('tick-hover-interactive', 'clickData'),
    prevent_initial_call=True
)
def display_click(click_data):
    return json.dumps(click_data, indent=2) if click_data else "Click on the chart"
""", style=code_style),
        ]),
    ], style=section_style),

    html.Hr(),

    # ======================================================================
    # 7. Best Practices Summary
    # ======================================================================
    html.Div([
        html.H2("7. Best Practices Summary"),
        html.P(
            "Key recommendations for configuring LineCharts with large date ranges.",
            style=description_style
        ),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Topic", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5', 'width': '180px'}),
                    html.Th("Recommendation", style={'textAlign': 'left', 'padding': '10px', 'borderBottom': '2px solid #ddd', 'backgroundColor': '#f5f5f5'}),
                ]),
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("Scale Type", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Use 'linear' with integer indices for 100+ data points. "
                        "'point' scale gives equal spacing regardless of time gaps, "
                        "which can misalign reference lines on irregular data.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Vertical Ref Lines", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "On 'point' scale: x value must exactly match a data array value. "
                        "On 'linear' scale: use the numeric index. "
                        "Mismatched values silently fail to render.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Tick Labels", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Set 'tickNumber' to control label density (~12 for a year). "
                        "Use 'tickLabelStyle': {'angle': 35} with extra bottom margin "
                        "for rotated labels. Set 'tickSize' for longer tick marks.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Tooltips", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Use tooltip={'trigger': 'axis'} to show all series values "
                        "at the hovered position. Combine with axisHighlight={'x': 'line'} "
                        "for a vertical crosshair.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Grid", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Enable grid={'horizontal': True} for readability. "
                        "Add 'vertical': True sparingly - it can be noisy on dense data.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Axis Highlight", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Options: 'none', 'line', 'band'. Use {'x': 'line'} for a "
                        "vertical crosshair, {'x': 'band'} for a highlighted column. "
                        "Add {'y': 'line'} for a horizontal crosshair.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Show Marks", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Set 'showMark': False for datasets with 50+ points to avoid "
                        "visual clutter and improve rendering performance.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
                html.Tr([
                    html.Td("Margins", style={'padding': '10px', 'borderBottom': '1px solid #eee', 'fontWeight': 'bold'}),
                    html.Td(
                        "Increase margin={'bottom': 60} when using angled tick labels. "
                        "Increase margin={'left': 70, 'right': 80} for dual Y-axes.",
                        style={'padding': '10px', 'borderBottom': '1px solid #eee'}
                    ),
                ]),
            ]),
        ], style={'width': '100%', 'borderCollapse': 'collapse'}),
    ], style=section_style),
])


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
@callback(
    Output('tick-hover-click-output', 'children'),
    Input('tick-hover-interactive', 'clickData'),
    prevent_initial_call=True
)
def display_tick_hover_click(click_data):
    """Display click event data from the interactive chart."""
    if click_data:
        return json.dumps(click_data, indent=2)
    return "Click on the chart to see event data"
