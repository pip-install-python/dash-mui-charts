---
name: Sparkline Advanced
description: "Advanced SparklineChart demo: a liquid glass (glassmorphism) stock card with reveal animation, hover opacity effects and real-time value display."
endpoint: /sparkline-style-advanced
package: dash_mui_charts
category: SparklineChart
order: 3
icon: mdi:blur
---

.. llms_copy::Sparkline Advanced

.. toc::

### Overview

An Apple-inspired glassmorphism stock card built around a single
`SparklineChart`, showing how far the component styles with plain CSS:

- liquid glass (glassmorphism) card design — `assets/liquid_glass.css`
- left-to-right reveal animation on page load
- hover effect: left side 100% opacity, right side 40% opacity, driven by a
  CSS custom property the callback sets from `hoverIndex`
- x-axis highlight line follows the cursor
- real-time value display fed by `hoverIndex` / `hoverValue`

.. admonition::CSS dependency
    :icon: mdi:language-css3
    :color: blue

    The card's entire look lives in `assets/liquid_glass.css`
    (`liquid-glass-background`, `liquid-glass-card`, `sparkline-container`,
    `value-display-panel`, …). The component itself only carries data and
    hover props — delete the stylesheet and the page silently degrades to
    unstyled divs.

---

### Live example

.. exec::docs.sparkline-style-advanced.glass_example
    :code: false

.. source::docs/sparkline-style-advanced/glass_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [SparklineChart examples](/sparkline) — the component's full demo tour
- [Styling playground](/sparkline-style) — interactive controls with generated code
