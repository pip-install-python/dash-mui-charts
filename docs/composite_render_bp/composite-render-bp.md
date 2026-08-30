---
name: Composite Render BP
description: "Best-practice CompositeChart rendering for stacked discharge/temperature/pressure dashboards across 7d-live to 1yr+ date ranges (~2k to 150k+ points)."
endpoint: /composite-render-bp
package: dash_mui_charts
category: CompositeChart
order: 3
icon: mdi:speedometer
---

.. llms_copy::Composite Render BP

.. toc::

### Overview

Best-practice CompositeChart rendering for stacked discharge/temperature/pressure dashboards across 7d-live to 1yr+ date ranges (~2k to 150k+ points).

.. admonition::Pro component demos
    :icon: mdi:diamond-outline
    :color: orange

    The examples on this page read a **MUI X Pro license key** from the
    `MUI_PRO_API_KEY` environment variable and pass it as `licenseKey`.
    Without it the charts render with the unlicensed watermark.

---

### Live examples

.. exec::docs.composite_render_bp.demo
    :code: false

.. source::docs/composite_render_bp/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
