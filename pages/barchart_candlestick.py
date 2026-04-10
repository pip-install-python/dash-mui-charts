"""
CandlestickChart Demo - OHLC Charts
Static candlestick charts with array and dataset modes, volume overlay, click events.
"""

import json
import random

import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/candlestick', name='Candlestick Chart')

from dash_mui_charts import CandlestickChart

random.seed(42)

CARD = 'page-card'

PRE_STYLE = {
    'fontSize': '12px',
    'margin': 0,
    'padding': '10px 14px',
    'borderRadius': '6px',
    'background': 'var(--mantine-color-body)',
    'border': '1px solid var(--mantine-color-default-border)',
    'maxHeight': '120px',
    'overflow': 'auto',
    'color': 'var(--mantine-color-text)',
}

# --- Generate realistic-looking OHLC data ---
def generate_ohlc(start_price=100, n=30, seed=42):
    random.seed(seed)
    data = []
    price = start_price
    for _ in range(n):
        change = random.gauss(0, 2)
        open_p = round(price + random.uniform(-0.5, 0.5), 2)
        close_p = round(open_p + change, 2)
        high_p = round(max(open_p, close_p) + random.uniform(0.5, 3), 2)
        low_p = round(min(open_p, close_p) - random.uniform(0.5, 3), 2)
        vol = random.randint(500, 5000)
        data.append({'open': open_p, 'high': high_p, 'low': low_p, 'close': close_p, 'volume': vol})
        price = close_p
    return data

ohlc_data = generate_ohlc(100, 25)

# Date labels
dates = [f'Apr {i+1}' for i in range(25)]

# Array format (tuples)
ohlc_tuples = [[d['open'], d['high'], d['low'], d['close']] for d in ohlc_data]

# Dataset format
ohlc_dataset = [{**d, 'date': dates[i]} for i, d in enumerate(ohlc_data)]

# Larger dataset for zoom demo
big_ohlc = generate_ohlc(150, 60, seed=99)
big_dates = [f'Day {i+1}' for i in range(60)]

layout = html.Div([
    html.H2("Candlestick Chart — OHLC"),
    html.P("Static candlestick charts for financial data visualization.",
           style={'color': 'var(--mantine-color-dimmed)', 'marginBottom': '24px'}),

    # --- 1. Basic Array Format ---
    html.Div([
        html.H4("Basic Candlestick (Array Format)"),
        html.P("OHLC data as [open, high, low, close] tuples.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-basic',
            series=[{
                'data': ohlc_tuples,
                'upColor': '#4caf50',
                'downColor': '#f44336',
            }],
            xAxis=[{'data': dates, 'label': 'Date'}],
            yAxis=[{'label': 'Price ($)'}],
            grid={'horizontal': True},
            height=400,
        ),
    ], className=CARD),

    # --- 2. Dataset Mode ---
    html.Div([
        html.H4("Dataset Mode"),
        html.P("Data as row objects with datasetKeys mapping.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-dataset',
            dataset=ohlc_dataset,
            series=[{
                'datasetKeys': {'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'},
                'upColor': '#26a69a',
                'downColor': '#ef5350',
            }],
            xAxis=[{'dataKey': 'date', 'label': 'Date'}],
            yAxis=[{'label': 'Price ($)'}],
            grid={'horizontal': True},
            height=400,
        ),
    ], className=CARD),

    # --- 3. With Volume ---
    html.Div([
        html.H4("Candlestick + Volume"),
        html.P("Volume bars overlaid below candles (30% of chart height).",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-volume',
            dataset=ohlc_dataset,
            series=[{
                'datasetKeys': {'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'},
                'volumeKey': 'volume',
                'upColor': '#4caf50',
                'downColor': '#f44336',
            }],
            xAxis=[{'dataKey': 'date'}],
            yAxis=[{'label': 'Price ($)'}],
            showVolume=True,
            volumeHeightRatio=0.3,
            grid={'horizontal': True},
            height=450,
        ),
    ], className=CARD),

    # --- 4. Custom Candle Styling ---
    html.Div([
        html.H4("Custom Styling"),
        html.P("Wider candle bodies and thicker wicks with custom colors.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-styled',
            series=[{
                'data': ohlc_tuples[:15],
                'upColor': '#00bcd4',
                'downColor': '#ff5722',
            }],
            xAxis=[{'data': dates[:15]}],
            yAxis=[{'label': 'Price'}],
            bodyWidthRatio=0.8,
            wickWidth=3,
            grid={'horizontal': True, 'vertical': True},
            height=380,
        ),
    ], className=CARD),

    # --- 5. Reference Lines ---
    html.Div([
        html.H4("Support & Resistance Lines"),
        html.P("Reference lines marking key price levels.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-refs',
            series=[{
                'data': ohlc_tuples,
                'upColor': '#4caf50',
                'downColor': '#f44336',
            }],
            xAxis=[{'data': dates}],
            yAxis=[{'label': 'Price ($)'}],
            referenceLines=[
                {
                    'y': max(d[1] for d in ohlc_tuples),
                    'label': 'Resistance',
                    'labelAlign': 'end',
                    'lineStyle': {'stroke': '#f44336', 'strokeWidth': 1.5, 'strokeDasharray': '6 4'},
                    'labelStyle': {'fill': '#f44336', 'fontSize': 11},
                },
                {
                    'y': min(d[2] for d in ohlc_tuples),
                    'label': 'Support',
                    'labelAlign': 'end',
                    'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 1.5, 'strokeDasharray': '6 4'},
                    'labelStyle': {'fill': '#4caf50', 'fontSize': 11},
                },
                {
                    'y': sum(d[3] for d in ohlc_tuples) / len(ohlc_tuples),
                    'label': 'Avg Close',
                    'labelAlign': 'start',
                    'lineStyle': {'stroke': '#ff9800', 'strokeWidth': 1},
                    'labelStyle': {'fill': '#ff9800', 'fontSize': 11},
                },
            ],
            grid={'horizontal': True},
            height=420,
        ),
    ], className=CARD),

    # --- 6. Click Events ---
    html.Div([
        html.H4("Click Events"),
        html.P("Click a candle to see its OHLC data.", style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-click',
            series=[{
                'data': ohlc_tuples[:15],
                'upColor': '#1976d2',
                'downColor': '#c62828',
            }],
            xAxis=[{'data': dates[:15]}],
            yAxis=[{'label': 'Price ($)'}],
            grid={'horizontal': True},
            height=380,
        ),
        html.P("clickData:", style={'fontSize': '12px', 'color': 'var(--mantine-color-dimmed)', 'marginTop': '12px', 'marginBottom': '4px'}),
        html.Pre(id='candle-click-out', children='Click a candle...', style=PRE_STYLE),
    ], className=CARD),

    # --- 7. Tooltip disabled ---
    html.Div([
        html.H4("Tooltip Disabled"),
        html.P("Set tooltip trigger to 'none' to hide the OHLC tooltip.",
               style={'color': 'var(--mantine-color-dimmed)', 'fontSize': '14px'}),
        CandlestickChart(
            id='candle-no-tooltip',
            series=[{
                'data': ohlc_tuples[:10],
                'upColor': '#7b1fa2',
                'downColor': '#e65100',
            }],
            xAxis=[{'data': dates[:10]}],
            tooltip={'trigger': 'none'},
            grid={'horizontal': True},
            height=300,
        ),
    ], className=CARD),

], style={'maxWidth': '900px', 'margin': '0 auto'})


@callback(
    Output('candle-click-out', 'children'),
    Input('candle-click', 'clickData'),
    prevent_initial_call=True,
)
def show_candle_click(data):
    if not data:
        return 'Click a candle...'
    return json.dumps(data, indent=2)
