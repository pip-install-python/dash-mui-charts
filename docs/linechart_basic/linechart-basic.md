---
name: LineChart Basics
description: "Fundamentals of the LineChart Dash component: grid, area and stacked-area charts, curve interpolation, dual y-axes, and click-event callbacks."
endpoint: /linechart-basic
package: dash_mui_charts
category: LineChart
icon: mdi:chart-line
---

.. llms_copy::LineChart Basics

.. toc::

### Overview

Fundamentals of the LineChart Dash component: grid, area and stacked-area charts, curve interpolation, dual y-axes, and click-event callbacks.


`LineChart` is the line and area chart component of dash-mui-charts, a Plotly
Dash wrapper around MUI X Charts. It draws one or more line series with
optional area fill, stacking, curve interpolation, dual y-axes, grid lines,
reference lines, hover highlighting and click-event callbacks — all configured
from Python dicts.

Core charting is Community tier (no license needed). Pro features require an
MUI X Pro license key passed as `licenseKey`: zoom/pan (`zoom`, `initialZoom`,
`zoomData` output), the zoom range slider (`showSlider`), brush range
selection (`brushConfig`) and the toolbar (`showToolbar`).

### Basic usage

```python
from dash_mui_charts import LineChart
LineChart(
    height=350,
    series=[
        {'data': [2, 5.5, 2, 8.5, 1.5, 5], 'label': 'Series A', 'showMark': True},
        {'data': [4, 3.5, 6, 2.5, 4.5, 3], 'label': 'Series B'},
    ],
    xAxis=[{'data': [1, 2, 3, 4, 5, 6], 'scaleType': 'point'}],
    grid={'horizontal': True, 'vertical': True},
)
```

### Series options

Each series dict supports `data` (y values, required), `label`, `color`,
`area` (fill under the line), `curve` ('linear', 'monotoneX', 'monotoneY',
'natural', 'step', 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'),
`stack` (group id for stacked areas), `showMark`, and `yAxisId` for biaxial
charts (give each `yAxis` entry an `id` and a `position` of 'left' or
'right', then reference it from the series via `yAxisId`).

### Reference lines

Horizontal (`y`) or vertical (`x`) markers; on multi-axis charts, `axisId`
picks which axis the value refers to.

```python
referenceLines=[
    {'y': 100, 'label': 'Target', 'labelAlign': 'end',
     'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2}},
    {'x': 'Q2', 'label': 'Launch',
     'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '5 5'}},
]
```

### Highlighting

`highlightedItem` and `highlightedAxis` are controlled props (input and
output) for cross-chart sync. Per-series `highlightScope` sets hover behavior:
`highlight` 'none' | 'item' | 'series'; `fade` 'none' | 'series' | 'global'.

```python
series=[{'id': 'sales', 'data': [1, 2, 3], 'showMark': True,
         'highlightScope': {'highlight': 'item', 'fade': 'global'}}],
tooltip={'trigger': 'item'},
highlightedItem={'seriesId': 'sales', 'dataIndex': 2},
```

### Pro: zoom and brush

```python
LineChart(
    licenseKey=MUI_PRO_LICENSE,
    xAxis=[{'id': 'x', 'data': years, 'scaleType': 'point',
            'zoom': {'minSpan': 5, 'maxSpan': 100, 'panning': True}}],
    showSlider=True,
    initialZoom=[{'axisId': 'x', 'start': 0, 'end': 50}],
    brushConfig={'enabled': True},
    brushOverlay='values',   # 'none' | 'default' | 'values'
    brushSeriesId='my-series',
)
# Current zoom state is reported via the zoomData output prop.
```

### Date formatting and functions-as-props

For time-scale axes, `dateFormat` / `dateTickFormat` set tooltip and tick
label formats without JavaScript (tokens: YYYY, MMM, MM, M, dd, d, HH, mm).
For anything else, `valueFormatter` accepts `{'function': name, 'options':
{...}}` resolved from the `window.dashMuiChartsFunctions` registry defined in
`assets/*.js`.

```python
xAxis=[{'data': epoch_ms_timestamps, 'scaleType': 'time',
        'dateFormat': 'M/d HH:mm',   # tooltip labels
        'dateTickFormat': 'M/d'}]    # tick labels
```

### Click events

The `clickData` output prop reports `{'type': 'axis' | 'mark' | 'line' |
'area', 'seriesIndex', 'dataIndex', 'value', 'timestamp'}`; read it with a
Dash callback (`n_clicks` also increments per click).

### Related pages

- /linechart-pro — zoom, pan, slider and controlled zoom state (Pro)
- /linechart-brush — brush range selection and overlay types (Pro)
- /linechart-referencelines — reference line styling, spacing, multi-axis
- /linechart-highlighting — controlled highlights and highlightScope
- /linechart-tick-hover — ticks, tooltips and grid across date ranges
- /linechart-zoom-preview — zoom slider preview, zoomInteractionConfig
- /crosshair — crosshair tracking dashboard (CompositeChart)
- /highlighting-sync — synchronized highlights across multiple charts

.. admonition::Pro component demos
    :icon: mdi:diamond-outline
    :color: orange

    The examples on this page read a **MUI X Pro license key** from the
    `MUI_PRO_API_KEY` environment variable and pass it as `licenseKey`.
    Without it the charts render with the unlicensed watermark.

---

### Live examples

.. exec::docs.linechart_basic.demo
    :code: false

.. source::docs/linechart_basic/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
