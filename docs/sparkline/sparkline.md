---
name: SparklineChart
description: "SparklineChart demos: line, area and bar sparklines for KPI cards and tables, synced multi-metric hover, custom curves and callback-driven data."
endpoint: /sparkline
package: dash_mui_charts
category: SparklineChart
icon: mdi:chart-line-variant
---

.. llms_copy::SparklineChart

.. toc::

### Overview

Sparklines are compact, inline charts (default 36px height) that show a data
trend without axes or labels — ideal for dashboards, KPI cards and table
cells. This is a **Community component**: no MUI X license key required.

```python
from dash_mui_charts import SparklineChart

SparklineChart(
    data=[1, 4, 2, 5, 7, 2, 4, 6],
    plotType='line',  # or 'bar'
    color='#1976d2',
    area=True,
    height=40,
    width=150,
)
```

Key props:

- `data` — list of numbers to plot
- `plotType` — `'line'` (default) or `'bar'`
- `area` — fill the region under the line
- `color`, `height`, `width` — appearance and sizing
- `curve` — line interpolation: `'linear'`, `'natural'`, `'monotoneX'`, `'step'`, and more
- `showTooltip` / `showHighlight` — hover value display and point marker
- `baseline` and `margin` — area baseline and plot margins
- `highlightedIndex` — controlled highlight, to sync the marked point with a table row, slider or another chart

---

### Basic line sparkline

The simplest sparkline — just pass an array of numbers. Great for showing
trends at a glance.

.. exec::docs.sparkline.basic_example
    :code: false

.. source::docs/sparkline/basic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### NPM-style downloads sparkline

A rich interactive sparkline like npm's package download chart. Hover over
the chart to see weekly download counts update in real time — the
`hoverIndex` / `hoverValue` props feed a Dash callback.

.. exec::docs.sparkline.npm_example
    :code: false

.. source::docs/sparkline/npm_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Synchronized multi-metric dashboard

Multiple sparklines that sync their hover state. Hover over any chart to see
all metrics for that time period.

.. exec::docs.sparkline.synced_example
    :code: false

.. source::docs/sparkline/synced_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Area sparkline

Add `area=True` to fill the area under the line. Use `baseline` to control
where the fill starts: `'min'` (default), `'max'`, or a specific value.

.. exec::docs.sparkline.area_example
    :code: false

.. source::docs/sparkline/area_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Bar sparkline

Use `plotType='bar'` for a bar chart sparkline. Good for discrete values or
comparing magnitudes.

.. exec::docs.sparkline.bar_example
    :code: false

.. source::docs/sparkline/bar_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Sparklines in a table

Sparklines are perfect for embedding in data tables to show trends alongside
other metrics.

.. exec::docs.sparkline.table_example
    :code: false

.. source::docs/sparkline/table_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Callback-triggered data changes

Change the sparkline data dynamically from a Dash callback. Select a metric
to see different trend data.

.. exec::docs.sparkline.dynamic_example
    :code: false

.. source::docs/sparkline/dynamic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom curves

Use different curve interpolation methods for different visual effects.
Available curves: `'linear'`, `'natural'`, `'step'`, `'stepBefore'`,
`'stepAfter'`, `'monotoneX'`, `'monotoneY'`, `'catmullRom'`, `'bumpX'`,
`'bumpY'`.

.. exec::docs.sparkline.curves_example
    :code: false

.. source::docs/sparkline/curves_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Interactive sparkline with hover details

Enable tooltips and highlighting to make sparklines interactive. The
`hoverIndex` and `hoverValue` props update as you move across the chart.

.. exec::docs.sparkline.interactive_example
    :code: false

.. source::docs/sparkline/interactive_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Styling playground](/sparkline-style) — interactive styling controls with live preview and generated code
- [Advanced styling](/sparkline-style-advanced) — liquid glass (glassmorphism) sparkline card
