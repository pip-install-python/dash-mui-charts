---
name: Pie Chart Props
description: Interactive playground for nested two-ring PieCharts on Titanic survival data with live controls for dimensions, radii, ring gap, labels and highlighting.
endpoint: /pie-props
package: dash_mui_charts
nav: Props Explorer
category: PieChart
order: 2
icon: mdi:tune-variant
---

.. llms_copy::Pie Chart Props

.. toc::

### Overview

An interactive control panel for nested/multi-series pie charts —
hierarchical data as inner and outer rings, based on the MUI X Charts
Titanic survival statistics example. Switch between three data views
(by class, by survival, simple budget demo), tune every ring prop, and
copy the generated `PieChart(...)` call from the code panel.

Controls cover:

- **Chart dimensions** — width and height
- **Inner / outer ring** — each ring's inner/outer radius, corner radius and padding angle
- **Ring gap & labels** — spacing between rings, arc label source and minimum angle
- **Interactions** — hover highlight, fade-others scope, tooltip, legend, animation
- **Margins**

The Hover Info and Click Data panels stream `highlightedItem` and
`clickData` from the live chart.

---

### Playground

.. exec::docs.pie-props.playground
    :code: false

.. source::docs/pie-props/playground.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [PieChart examples](/pie) — basic pie, donut, arc labels, gauge and interactivity
