---
name: Heatmap
description: "Heatmap (MUI X Pro) demos: activity grids, a correlation matrix, continuous and piecewise color scales, custom cell styling and click interaction."
endpoint: /heatmap
package: dash_mui_charts
category: Heatmap
order: 1
icon: mdi:grid
---

.. llms_copy::Heatmap

.. toc::

### Overview

`Heatmap` renders matrix/grid visualizations with color-coded cells,
wrapping the MUI X Charts Pro heatmap for Plotly Dash.

Cells are addressed by x/y index against categorical axis labels, and each
cell's color is derived from its value through a color scale (continuous
or piecewise). Cell clicks flow back to Dash as `clickData` with x, y, and
value.

.. admonition::Pro component
    :icon: mdi:diamond-outline
    :color: orange

    Heatmap is a **MUI X Pro** component — a Pro license key is required,
    passed via the `licenseKey` prop. These demos read it from the
    `MUI_PRO_API_KEY` environment variable; without it the charts render
    with the unlicensed watermark.

```python
# Data format: [x_index, y_index, value] triples
from dash_mui_charts import Heatmap

Heatmap(
    id='my-heatmap',
    licenseKey=MUI_LICENSE_KEY,
    data=[[0, 0, 10], [0, 1, 20], [1, 0, 40], [1, 1, 50]],
    xAxis={'data': ['Mon', 'Tue'], 'label': 'Day'},
    yAxis={'data': ['Week 1', 'Week 2'], 'label': 'Week'},
    height=300,
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 100,
        'colors': ['#e3f2fd', '#1976d2'],
    },
)
```

---

### Basic heatmap

A simple heatmap showing weekly activity levels. Data is provided as
`[x_index, y_index, value]` tuples.

.. exec::docs.heatmap.basic_example
    :code: false

.. source::docs/heatmap/basic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Correlation matrix

Heatmaps are ideal for displaying correlation matrices. Use a diverging
color scale to show positive and negative correlations.

.. exec::docs.heatmap.correlation_example
    :code: false

.. source::docs/heatmap/correlation_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Temperature heatmap

A practical example showing hourly temperatures across the week, with a
warm color scale from cool (blue) to hot (red).

.. exec::docs.heatmap.temperature_example
    :code: false

.. source::docs/heatmap/temperature_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom rounded cells

Use `cellStyle='rounded'` for cells with gaps, rounded corners, and value
labels.

.. exec::docs.heatmap.rounded_example
    :code: false

.. source::docs/heatmap/rounded_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom cell configuration

Fine-tune cell appearance with custom gap, border radius, font size, and
colors.

.. exec::docs.heatmap.custom_cells_example
    :code: false

.. source::docs/heatmap/custom_cells_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Piecewise color scale

Use a piecewise color scale for discrete color bands — useful for
categorizing values into ranges (Low, Medium, High).

.. exec::docs.heatmap.piecewise_example
    :code: false

.. source::docs/heatmap/piecewise_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Interactive heatmap

Click on cells to see their data — the heatmap reports click events with
x, y coordinates and value.

.. exec::docs.heatmap.interactive_example
    :code: false

.. source::docs/heatmap/interactive_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Color scale reference

| Type | Configuration | Use case |
|------|---------------|----------|
| Continuous | `{'type': 'continuous', 'min': 0, 'max': 100, 'colors': ['#low', '#high']}` | Smooth gradient for numerical data |
| Diverging | `{'type': 'continuous', 'min': -1, 'max': 1, 'colors': ['#neg', '#mid', '#pos']}` | Correlations, deviations from center |
| Piecewise | `{'type': 'piecewise', 'thresholds': [a, b, c], 'colors': ['#1', '#2', '#3', '#4']}` | Categorical ranges (Low/Med/High) |

Piecewise thresholds `[3, 5, 7]` create four bands (0–2, 3–4, 5–6, 7+) and
need `len(thresholds) + 1` colors.

---

### Related pages

- [Props Explorer](/heatmap-props) — interactive props playground with live controls
