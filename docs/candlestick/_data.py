"""Shared OHLC demo data for the CandlestickChart examples.

`generate_ohlc` seeds its own RNG, so the series is reproducible wherever
it is called from. (The pre-migration page also generated a 60-candle
`big_ohlc` it never rendered — dropped here as dead code.)
"""
import random


def generate_ohlc(start_price=100, n=30, seed=42):
    """Realistic-looking OHLCV rows as a random walk."""
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
        data.append({'open': open_p, 'high': high_p, 'low': low_p,
                     'close': close_p, 'volume': vol})
        price = close_p
    return data


ohlc_data = generate_ohlc(100, 25)

dates = [f'Apr {i+1}' for i in range(25)]

# Array format — [open, high, low, close] tuples
ohlc_tuples = [[d['open'], d['high'], d['low'], d['close']]
               for d in ohlc_data]

# Dataset format — row objects
ohlc_dataset = [{**d, 'date': dates[i]} for i, d in enumerate(ohlc_data)]

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
