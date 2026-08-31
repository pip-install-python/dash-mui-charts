---
name: API Reference
description: Every prop of all 13 dash-mui-charts components — generated from the components' own metadata, so it always matches the installed version.
endpoint: /api
package: dash_mui_charts
category: Reference
# The prop tables are generated from the installed package, so this page's
# content moves when the PACKAGE does — not when the docs are rebuilt.
# So this is dash_mui_charts 1.4.0's release date, NOT the day the tables
# were last regenerated (muischeduler's correction, carried to this fork by
# the template seat 2026-08-31: it was briefly 2026-08-31, the day of the
# port, which would have had the sitemap assert a content date that was not
# one). tests/test_seo_icons.py holds it to the CHANGELOG entry for the
# INSTALLED version, so bumping the package moves this in the same change.
lastmod: 2026-08-03
order: 1
icon: mdi:api
---

.. llms_copy::API Reference

.. toc::

### Overview

The tables below are generated from each component's own metadata (the
docstrings `dash-generate-components` builds from the React prop types),
so they always match the installed version. Interaction props
(`clickData`, `highlightedItem`, `hoverIndex`, `zoomData`, …) are Dash
callback outputs; controlled props (`highlightedItem`, `expandedItems`,
`value`, …) also work as inputs.

Pro-tier features (zoom, sliders, toolbars, Heatmap, TreeViewPro extras)
require a MUI X Pro license key passed via each component's `licenseKey`
prop.

---

### LineChart

Line/area charts with biaxial axes, reference lines, and Pro zoom/pan,
slider, brush and toolbar. [Demos →](/linechart-basic)

.. kwargs::dash_mui_charts.LineChart

---

### BarChart

Vertical/horizontal bars with stacking, bar labels, dataset mode, and Pro
zoom. [Demos →](/barchart-basic)

.. kwargs::dash_mui_charts.BarChart

---

### CandlestickChart

Static OHLC candlesticks with volume overlay and reference lines.
[Demos →](/candlestick)

.. kwargs::dash_mui_charts.CandlestickChart

---

### PieChart

Pie, donut, and nested pies with controlled highlighting.
[Demos →](/pie)

.. kwargs::dash_mui_charts.PieChart

---

### ScatterChart

Scatter charts with z-axis color mapping and voronoi interaction.
[Demos →](/scatter)

.. kwargs::dash_mui_charts.ScatterChart

---

### CompositeChart

Scatter + line series layered on one surface, multi-axis, Pro zoom.
[Demos →](/composite)

.. kwargs::dash_mui_charts.CompositeChart

---

### Heatmap

Matrix visualization with continuous/piecewise color scales (Pro).
[Demos →](/heatmap)

.. kwargs::dash_mui_charts.Heatmap

---

### SparklineChart

Compact inline charts for dashboards, KPI cards and tables.
[Demos →](/sparkline)

.. kwargs::dash_mui_charts.SparklineChart

---

### LiveTradingChart

Real-time streaming OHLCV simulation with forecast and alerts.
[Demos →](/live-trading)

.. kwargs::dash_mui_charts.LiveTradingChart

---

### TreeView

Data-driven RichTreeView: selection, expansion, inline editing.
[Demos →](/tree-basic)

.. kwargs::dash_mui_charts.TreeView

---

### SimpleTreeView

JSX-driven tree for navigation sidebars and static hierarchies.
[Demos →](/tree-simple)

.. kwargs::dash_mui_charts.SimpleTreeView

---

### TreeViewPro

Drag-reorder, lazy loading, per-item slider and kebab controls (Pro).
[Demos →](/tree-pro)

.. kwargs::dash_mui_charts.TreeViewPro

---

### TimeClock

Inline clock-face time picker (MUI X Date & Time Pickers).
[Demos →](/time-clock)

.. kwargs::dash_mui_charts.TimeClock
