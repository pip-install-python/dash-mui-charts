---
name: Candlestick Chart
description: "CandlestickChart OHLC demos: array and dataset formats, volume overlay, candle styling, support/resistance reference lines and click events."
endpoint: /candlestick
package: dash_mui_charts
category: CandlestickChart
order: 1
icon: mdi:chart-waterfall
---

.. llms_copy::Candlestick Chart

.. toc::

### Overview

Static OHLC candlestick charts for financial data in Plotly Dash. Built on
the MUI X Charts Pro composition API (`ChartDataProviderPro` plus a custom
SVG `CandlePlot` for candle bodies and wicks), so it does not need
`@mui/x-charts-premium`. Basic charts work without a license; zoom, slider
and toolbar are Pro features that require a MUI X Pro `licenseKey`.

Not the same as [LiveTradingChart](/live-trading), which is a real-time
streaming chart.

```python
from dash_mui_charts import CandlestickChart

CandlestickChart(
    id='my-candles',
    series=[{
        'data': [
            [100, 110, 95, 105],   # [open, high, low, close]
            [105, 115, 100, 112],
        ],
        'upColor': '#4caf50',      # close >= open
        'downColor': '#f44336',    # close < open
    }],
    xAxis=[{'data': ['Mon', 'Tue']}],
)
```

Key props: `showVolume` + `volumeHeightRatio` (volume bars from
`volumeKey` or a `volume` array), `bodyWidthRatio` (0–1, default 0.6),
`wickWidth` (px), `referenceLines`, and a built-in OHLC hover tooltip with
vertical crosshair. The y-axis domain is computed automatically.

---

### Basic candlestick (array format)

OHLC data as `[open, high, low, close]` tuples.

.. exec::docs.candlestick.basic_example
    :code: false

.. source::docs/candlestick/basic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Dataset mode

Data as row objects with a `datasetKeys` mapping.

.. exec::docs.candlestick.dataset_example
    :code: false

.. source::docs/candlestick/dataset_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Candlestick + volume

Volume bars overlaid below the candles (30% of chart height).

.. exec::docs.candlestick.volume_example
    :code: false

.. source::docs/candlestick/volume_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom styling

Wider candle bodies and thicker wicks with custom colors.

.. exec::docs.candlestick.styled_example
    :code: false

.. source::docs/candlestick/styled_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Support & resistance lines

Reference lines marking key price levels.

.. exec::docs.candlestick.refs_example
    :code: false

.. source::docs/candlestick/refs_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Click events

Click a candle to see its OHLC data — `clickData` carries `dataIndex`,
`label`, `open`, `high`, `low`, `close`.

.. exec::docs.candlestick.click_example
    :code: false

.. source::docs/candlestick/click_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Tooltip disabled

Set the tooltip trigger to `'none'` to hide the OHLC tooltip.

.. exec::docs.candlestick.no_tooltip_example
    :code: false

.. source::docs/candlestick/no_tooltip_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [LiveTradingChart](/live-trading) — real-time streaming charts
- [BarChart](/barchart-basic) — the BarChart component family
