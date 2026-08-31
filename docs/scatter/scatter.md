---
name: Scatter Chart
description: "ScatterChart demos: two-series scatter, custom marker sizes, z-axis color mapping, log-scale axes, click events, dataset-driven series and axis styling."
endpoint: /scatter
package: dash_mui_charts
nav: Examples
category: ScatterChart
order: 1
icon: mdi:chart-scatter-plot
---

.. llms_copy::Scatter Chart

.. toc::

### Overview

`ScatterChart` renders scatter/point charts with optional z-axis color
mapping, voronoi-based proximity interaction, and dataset-driven data,
wrapping the MUI X Charts scatter chart for Plotly Dash. It is a
**Community (free)** component — no MUI X Pro license required.

```python
from dash_mui_charts import ScatterChart

ScatterChart(
    series=[
        {
            'id': 'group-a',
            'label': 'Group A',
            'data': [{'x': 1, 'y': 5, 'id': 0}, {'x': 2, 'y': 8, 'id': 1}],
            'color': '#1976d2',
            'markerSize': 6,
        },
    ],
    voronoiMaxRadius=30,   # proximity-based hover/click
    height=400,
)
```

Axes support `scaleType` including log and sqrt scales;
`renderer='svg-batch'` speeds up large datasets.

.. admonition::seriesId, not seriesIndex
    :icon: mdi:information-outline
    :color: blue

    MUI X Charts uses `seriesId` (a string), not `seriesIndex`, in event
    payloads like `clickData`.

---

### Basic scatter — two series

Two data clusters plotted as separate series with grid lines.

.. exec::docs.scatter.basic_example
    :code: false

.. source::docs/scatter/basic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom marker sizes

Use `markerSize` (the radius in pixels) to differentiate series — smaller
markers for dense data, larger for emphasis.

.. exec::docs.scatter.sizes_example
    :code: false

.. source::docs/scatter/sizes_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Z-axis color mapping

Use `zAxis` with a `colorMap` to color scatter points by a third variable
(continuous, piecewise, or ordinal). Color priority: z-axis > y-axis >
x-axis > series color.

.. exec::docs.scatter.colormap_example
    :code: false

.. source::docs/scatter/colormap_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Log scale axis

Scatter charts support logarithmic axis scales for data spanning multiple
orders of magnitude.

.. exec::docs.scatter.log_example
    :code: false

.. source::docs/scatter/log_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Click events

Click on scatter points to capture event data in Dash callbacks —
`clickData` reports `{'type': 'scatter', 'seriesId': ..., 'dataIndex': ...,
'x': ..., 'y': ...}`. `voronoiMaxRadius` controls the interaction distance.

.. exec::docs.scatter.click_example
    :code: false

.. source::docs/scatter/click_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Dataset-driven scatter

Use the `dataset` prop with `datasetKeys` to map columns to x/y axes —
useful when data comes from a shared table format.

.. exec::docs.scatter.dataset_example
    :code: false

.. source::docs/scatter/dataset_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Axis styling

The full axis API: `tickLabelStyle`, `labelStyle`, `tickSize`,
`tickNumber`, `domainLimit`, `disableLine` and more.

.. exec::docs.scatter.axis_styling_example
    :code: false

.. source::docs/scatter/axis_styling_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [CompositeChart](/composite) — layer scatter and line series on one surface
