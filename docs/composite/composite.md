---
name: Composite Chart (0.0.8)
description: "CompositeChart demos layering scatter and line series on one surface: trend overlays, reference lines, multi-axis charts and Pro zoom with slider preview."
endpoint: /composite
package: dash_mui_charts
nav: Examples
category: CompositeChart
order: 1
icon: mdi:layers-outline
---

.. llms_copy::Composite Chart (0.0.8)

.. toc::

### Overview

CompositeChart demos layering scatter and line series on one surface: trend overlays, reference lines, multi-axis charts and Pro zoom with slider preview.


`CompositeChart` layers multiple chart types — `type: 'scatter'` and
`type: 'line'` series — on a single surface using the MUI X Charts composition
API (`ChartDataProviderPro` + `ChartsSurface` + individual plot components).
Basic layering is **Community (free)**; zoom/pan, slider preview, and the
toolbar are **Pro** features that require a `licenseKey`.

It ships a custom axis tooltip that shows both line and scatter data at the
hovered x-position (scatter matches by proximity, auto-computed from axis data
spacing), and epoch-ms values are converted to Date objects automatically on
`scaleType: 'time'` axes.

### Basic scatter + line overlay

```python
from dash_mui_charts import CompositeChart

CompositeChart(
    series=[
        {'type': 'scatter', 'id': 'readings', 'label': 'Sensor Readings',
         'data': [{'x': 0, 'y': 18.5, 'id': 0}], 'markerSize': 4},
        {'type': 'line', 'id': 'trend', 'label': 'Trend Line',
         'data': [20.0, 22.1],  # positional values
         'curve': 'natural', 'showMark': False},
    ],
    xAxis=[{'data': x_values, 'scaleType': 'linear'}],
)
```

### Zoom with slider preview (Pro)

```python
CompositeChart(
    licenseKey=MUI_PRO_LICENSE,
    series=[
        {'type': 'line', 'id': 'baseline', 'data': values, 'area': True},
        {'type': 'scatter', 'id': 'anomalies', 'data': scatter_points,
         'markerSize': 6,
         'preview': {'markerSize': 2},  # marker size in the slider preview
         'highlightScope': {'highlight': 'item'}},
    ],
    xAxis=[{
        'data': timestamps,
        'scaleType': 'time',  # epoch ms auto-converted to Date objects
        'zoom': {'slider': {'enabled': True, 'preview': True}},
    }],
    initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 30}],
)
```

### Multi-axis

```python
CompositeChart(
    series=[
        {'type': 'scatter', 'yAxisId': 'left-axis'},
        {'type': 'line', 'yAxisId': 'right-axis'},
    ],
    yAxis=[
        {'id': 'left-axis', 'position': 'left'},
        {'id': 'right-axis', 'position': 'right'},
    ],
)
```

### Reference lines

```python
CompositeChart(
    referenceLines=[
        {'y': 28, 'label': 'Upper Limit', 'lineStyle': {'stroke': 'red'}},
        {'y': 16, 'label': 'Lower Limit', 'lineStyle': {'stroke': 'red'}},
    ],
)
```

### Related pages

- `/composite` — this demo (overlays, reference lines, multi-axis, Pro zoom)
- `/composite-v120` — v1.2.0 axis tooltip fix, highlightedAxis, cross-chart sync
- `/composite-render-bp` — rendering best practices for large time ranges
- `/scatter` — standalone ScatterChart

.. admonition::Pro component demos
    :icon: mdi:diamond-outline
    :color: orange

    The examples on this page read a **MUI X Pro license key** from the
    `MUI_PRO_API_KEY` environment variable and pass it as `licenseKey`.
    Without it the charts render with the unlicensed watermark.

---

### Live examples

.. exec::docs.composite.demo
    :code: false

.. source::docs/composite/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
