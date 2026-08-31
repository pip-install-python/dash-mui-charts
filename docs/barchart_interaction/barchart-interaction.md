---
name: Bar Chart - Interaction
description: "BarChart interaction in Dash: bar and axis click callbacks, series highlighting, axis highlight modes, and axis vs item tooltip triggers."
endpoint: /barchart-interaction
package: dash_mui_charts
nav: Interaction
category: BarChart
order: 4
icon: mdi:cursor-default-click-outline
---

.. llms_copy::Bar Chart - Interaction

.. toc::

### Overview

Interaction flows back to Dash through two callback outputs: `clickData`
(the clicked bar's `seriesId` and `dataIndex`) and `axisClickData` (the
axis value plus every series' value at the clicked position).
`highlightedItem` reports hover state, and `highlightScope` per series
controls what highlights and what fades.

---

### Click events

Click any bar to capture `seriesId` and `dataIndex`.

.. exec::docs.barchart_interaction.click_example
    :code: false

.. source::docs/barchart_interaction/click_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Axis click

Click on the chart area to capture the axis value and all series values
at that point.

.. exec::docs.barchart_interaction.axis_click_example
    :code: false

.. source::docs/barchart_interaction/axis_click_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Series highlighting

Hover over a bar to highlight the entire series and fade others.

.. exec::docs.barchart_interaction.highlight_example
    :code: false

.. source::docs/barchart_interaction/highlight_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Axis highlight: band vs line vs none

Control the hover band/line on each axis with `axisHighlight`.

.. exec::docs.barchart_interaction.axis_highlight_example
    :code: false

.. source::docs/barchart_interaction/axis_highlight_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Tooltip triggers

`'axis'` shows all series at the hover position; `'item'` shows only the
hovered bar.

.. exec::docs.barchart_interaction.tooltip_example
    :code: false

.. source::docs/barchart_interaction/tooltip_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Basic](/barchart-basic) · [Dataset Mode](/barchart-dataset) · [Stacking](/barchart-stacking) · [Reference Lines](/barchart-reference) · [Pro Features](/barchart-pro)
