---
name: Heatmap Props
description: "Interactive Heatmap props playground (MUI X Pro): live controls for color scale, dimensions, cell style, interactions and margins on a 5x5 grid."
endpoint: /heatmap-props
package: dash_mui_charts
category: Heatmap
icon: mdi:tune-vertical
---

.. llms_copy::Heatmap Props

.. toc::

### Overview

An interactive control panel for exploring and customizing `Heatmap`
props on a 5×5 grid — changes reflect in real time, and the generated
code panel writes the exact `Heatmap(...)` call for the current settings.

.. admonition::Pro component
    :icon: mdi:diamond-outline
    :color: orange

    Heatmap is a **MUI X Pro** component. These demos read the license key
    from the `MUI_PRO_API_KEY` environment variable; without it the chart
    renders with the unlicensed watermark and the playground shows a
    warning banner.

---

### Playground

.. exec::docs.heatmap-props.playground
    :code: false

.. source::docs/heatmap-props/playground.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Heatmap examples](/heatmap) — activity grids, correlation matrix, color scales, click interaction
