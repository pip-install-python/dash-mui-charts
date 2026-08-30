---
name: Sparkline Style
description: "Interactive SparklineChart styling playground: tweak color, plot type, curve, area, size and highlights with a live preview and generated code."
endpoint: /sparkline-style
package: dash_mui_charts
category: SparklineChart
order: 2
icon: mdi:palette-outline
---

.. llms_copy::Sparkline Style

.. toc::

### Overview

An interactive control board for customizing sparkline appearance. Adjust
the controls to see real-time changes in the live preview — the **Generated
Code** panel at the bottom writes the exact `SparklineChart(...)` call for
the current settings, ready to copy into your app.

Controls cover the full styling surface:

- **Colors** — chart color and preview background
- **Chart type** — line or bar, curve interpolation, stroke width, area fill and baseline
- **Dimensions** — width and height
- **Interactive features** — tooltip, highlight, x-axis highlight, highlight dot size
- **Margins** and **clip-area offsets** — fine positioning

---

### Playground

.. exec::docs.sparkline-style.playground
    :code: false

.. source::docs/sparkline-style/playground.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [SparklineChart examples](/sparkline) — the component's full demo tour
- [Advanced styling](/sparkline-style-advanced) — liquid glass (glassmorphism) sparkline card
