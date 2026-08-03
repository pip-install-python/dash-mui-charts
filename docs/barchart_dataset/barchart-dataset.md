---
name: Bar Chart - Dataset
description: "BarChart dataset mode: pass table-format data once and reference columns by dataKey, with stacked series and bar/category gap control."
endpoint: /barchart-dataset
package: dash_mui_charts
category: BarChart
icon: mdi:table
---

.. llms_copy::Bar Chart - Dataset

.. toc::

### Overview

Dataset mode passes table-format data ONCE via the `dataset` prop; each
series and the band axis reference columns by `dataKey` — no data
duplication across series.

```python
BarChart(
    dataset=[
        {'month': 'Jan', 'london': 18, 'paris': 15},
        {'month': 'Feb', 'london': 22, 'paris': 18},
    ],
    xAxis=[{'dataKey': 'month', 'scaleType': 'band'}],
    series=[
        {'dataKey': 'london', 'label': 'London'},
        {'dataKey': 'paris', 'label': 'Paris'},
    ],
)
```

---

### City temperatures (dataset mode)

Data is passed once via `dataset`; series reference columns by `dataKey`.

.. exec::docs.barchart_dataset.temps_example
    :code: false

.. source::docs/barchart_dataset/temps_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Stacked quarterly sales

Stacked bars from a dataset, in horizontal layout.

.. exec::docs.barchart_dataset.stacked_example
    :code: false

.. source::docs/barchart_dataset/stacked_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Bar gap & category gap

Control spacing with `categoryGapRatio` and `barGapRatio` on the band
axis.

.. exec::docs.barchart_dataset.gaps_example
    :code: false

.. source::docs/barchart_dataset/gaps_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Basic](/barchart-basic) · [Stacking](/barchart-stacking) · [Interaction](/barchart-interaction) · [Reference Lines](/barchart-reference) · [Pro Features](/barchart-pro)
