---
name: Bar Chart - Reference Lines
description: "BarChart reference lines and styling: target and threshold markers, vertical reference lines, skip animation, hidden legend and custom color palettes."
endpoint: /barchart-reference
package: dash_mui_charts
nav: Reference Lines
category: BarChart
order: 5
icon: mdi:chart-bar
---

.. llms_copy::Bar Chart - Reference Lines

.. toc::

### Overview

`referenceLines` draws horizontal (`y`) and vertical (`x`) markers over
the bars — targets, thresholds, dates — each with its own `label`,
`labelAlign`, `lineStyle` and `labelStyle`. The rest of this page covers
the styling switches: `skipAnimation`, `hideLegend` and the `colors`
palette.

---

### Target line

Horizontal reference line showing a sales target.

.. exec::docs.barchart_reference.target_example
    :code: false

.. source::docs/barchart_reference/target_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Multiple reference lines

Min, average, and max thresholds on one chart.

.. exec::docs.barchart_reference.multi_example
    :code: false

.. source::docs/barchart_reference/multi_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Vertical reference line

Mark a specific category (e.g., a policy change date).

.. exec::docs.barchart_reference.vertical_example
    :code: false

.. source::docs/barchart_reference/vertical_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Skip animation

Bars render instantly when `skipAnimation=True`.

.. exec::docs.barchart_reference.noanim_example
    :code: false

.. source::docs/barchart_reference/noanim_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Hidden legend

Use `hideLegend=True` when the legend is redundant.

.. exec::docs.barchart_reference.nolegend_example
    :code: false

.. source::docs/barchart_reference/nolegend_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Custom color palette

Override the default palette with the `colors` prop.

.. exec::docs.barchart_reference.colors_example
    :code: false

.. source::docs/barchart_reference/colors_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Basic](/barchart-basic) · [Dataset Mode](/barchart-dataset) · [Stacking](/barchart-stacking) · [Interaction](/barchart-interaction) · [Pro Features](/barchart-pro)
