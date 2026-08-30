---
name: Bar Chart - Basic
description: "BarChart basics for Dash: multi-series vertical, stacked and horizontal bars, bar labels, rounded corners, custom colors and negative values."
endpoint: /barchart-basic
package: dash_mui_charts
category: BarChart
order: 1
icon: mdi:chart-bar
---

.. llms_copy::Bar Chart - Basic

.. toc::

### Overview

Vertical and horizontal bar charts for Plotly Dash, wrapping MUI X Charts'
`BarChart`. Community features — bars, stacking, bar labels, dataset mode,
reference lines, click events — need no license. Pro features (zoom,
slider, toolbar) require a MUI X Pro `licenseKey`; the component
automatically switches to `BarChartPro` when Pro features are used.

```python
from dash_mui_charts import BarChart

BarChart(
    id='my-bar',
    series=[{'data': [4, 3, 5], 'label': 'Sales', 'color': '#1976d2'}],
    xAxis=[{'data': ['Q1', 'Q2', 'Q3'], 'scaleType': 'band'}],
    height=350,
)
```

`scaleType: 'band'` is required on the category axis. For horizontal bars,
put the band axis on `yAxis` and set `layout='horizontal'`.

---

### Multi-series vertical

Revenue, expenses, and profit by month.

.. exec::docs.barchart_basic.multi_example
    :code: false

.. source::docs/barchart_basic/multi_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Stacked bar chart

Traffic sources stacked per month via a shared `stack` id.

.. exec::docs.barchart_basic.stacked_example
    :code: false

.. source::docs/barchart_basic/stacked_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Horizontal bar chart

Revenue displayed horizontally with rounded corners — the band axis moves
to `yAxis` and `layout='horizontal'`.

.. exec::docs.barchart_basic.horizontal_example
    :code: false

.. source::docs/barchart_basic/horizontal_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Bar labels

Display values on bars with `barLabel='value'` and center or outside
placement.

.. exec::docs.barchart_basic.labels_example
    :code: false

.. source::docs/barchart_basic/labels_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Rounded bars with custom colors

`borderRadius` and a custom `colors` palette.

.. exec::docs.barchart_basic.rounded_example
    :code: false

.. source::docs/barchart_basic/rounded_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Negative values

Bars with negative values extend below the zero baseline.

.. exec::docs.barchart_basic.negative_example
    :code: false

.. source::docs/barchart_basic/negative_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Dataset Mode](/barchart-dataset) · [Stacking](/barchart-stacking) · [Interaction](/barchart-interaction) · [Reference Lines](/barchart-reference) · [Pro Features](/barchart-pro)
