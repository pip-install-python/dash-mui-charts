---
name: Bar Chart - Stacking
description: "BarChart stacking options: standard, normalized (expand) and diverging stack offsets, multiple stack groups, and horizontal stacked bars."
endpoint: /barchart-stacking
package: dash_mui_charts
category: BarChart
order: 3
icon: mdi:chart-bar-stacked
---

.. llms_copy::Bar Chart - Stacking

.. toc::

### Overview

Series sharing a `stack` id render stacked. `stackOffset` controls the
arithmetic: `'none'` (default, accumulate from zero), `'expand'`
(normalized to 100%), or `'diverging'` (positives above zero, negatives
below). Different `stack` ids render as side-by-side stack groups.

```python
series=[
    {'data': [40, 35], 'stack': 'g', 'stackOffset': 'expand'},
    {'data': [30, 25], 'stack': 'g', 'stackOffset': 'expand'},
]
```

---

### Standard stack (offset: none)

Default stacking — bars accumulate from zero.

.. exec::docs.barchart_stacking.normal_example
    :code: false

.. source::docs/barchart_stacking/normal_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Normalized stack (offset: expand)

All bars fill to 100% — shows proportions rather than absolute values.

.. exec::docs.barchart_stacking.expand_example
    :code: false

.. source::docs/barchart_stacking/expand_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Diverging stack

Positive values above zero, negative below — useful for sentiment or net
scores.

.. exec::docs.barchart_stacking.diverging_example
    :code: false

.. source::docs/barchart_stacking/diverging_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Multiple stack groups

Different stack IDs create separate stacked groups side by side.

.. exec::docs.barchart_stacking.groups_example
    :code: false

.. source::docs/barchart_stacking/groups_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Horizontal stacked

Stacked bars in horizontal layout with rounded corners.

.. exec::docs.barchart_stacking.horizontal_example
    :code: false

.. source::docs/barchart_stacking/horizontal_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Basic](/barchart-basic) · [Dataset Mode](/barchart-dataset) · [Interaction](/barchart-interaction) · [Reference Lines](/barchart-reference) · [Pro Features](/barchart-pro)
