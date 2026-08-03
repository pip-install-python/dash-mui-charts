---
name: Pie Chart
description: "PieChart demos: basic pie, donut, arc labels, styled slices, half-pie gauge, and an interactive example with clickData and highlightedItem callbacks."
endpoint: /pie
package: dash_mui_charts
category: PieChart
icon: mdi:chart-pie
---

.. llms_copy::Pie Chart

.. toc::

### Overview

`PieChart` renders pie, donut, and nested/concentric pie charts, wrapping
the MUI X Charts pie chart for Plotly Dash. It is a **Community (free)**
component — no MUI X Pro license required.

Slices come from a flat `data` list (single series) or a `series` list
(nested pies). Interaction flows back to Dash through `clickData` and
`highlightedItem`; `highlightedItem` also works as an input for
synchronized highlighting across charts.

```python
from dash_mui_charts import PieChart

PieChart(
    data=[
        {'id': 'a', 'value': 35, 'label': 'Marketing', 'color': '#1976d2'},
        {'id': 'b', 'value': 25, 'label': 'Engineering'},
    ],
    innerRadius=50,   # >0 creates donut
    outerRadius=100,
    cornerRadius=5,
    paddingAngle=2,
)
```

.. admonition::seriesId, not seriesIndex
    :icon: mdi:information-outline
    :color: blue

    MUI X Charts uses `seriesId` (a string such as
    `"auto-generated-id-0"`), not `seriesIndex`, in event payloads like
    `clickData` and `highlightedItem`.

---

### Basic pie chart

A simple pie chart showing budget allocation by department. Hover over
slices to see values, click to interact.

.. exec::docs.pie.basic_example
    :code: false

.. source::docs/pie/basic_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Donut chart

Set `innerRadius` to create a donut chart. The hollow center can be used
for additional information or just aesthetic appeal.

.. exec::docs.pie.donut_example
    :code: false

.. source::docs/pie/donut_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Arc labels

Display values directly on the arcs with `arcLabel` (`'value'`, `'label'`
or `'formattedValue'`). Use `arcLabelMinAngle` to hide labels on small
slices that would be too crowded.

.. exec::docs.pie.labels_example
    :code: false

.. source::docs/pie/labels_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Styled pie

Customize the appearance with padding between slices, rounded corners, and
custom color palettes.

.. exec::docs.pie.styled_example
    :code: false

.. source::docs/pie/styled_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Half pie / gauge

Create gauge-style visualizations by adjusting `startAngle` and
`endAngle`. Perfect for progress indicators or completion metrics.

.. exec::docs.pie.gauge_example
    :code: false

.. source::docs/pie/gauge_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Interactive example

Click on slices to see detailed click data. Hover to highlight slices and
see the highlight state update in real time — `clickData` and
`highlightedItem` both arrive as callback inputs.

.. exec::docs.pie.interactive_example
    :code: false

.. source::docs/pie/interactive_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Props Explorer](/pie-props) — interactive props playground with nested two-ring pies
