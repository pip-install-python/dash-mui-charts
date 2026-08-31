---
name: Bar Chart - Pro
description: "BarChart Pro features with a MUI X license key: zoom with slider, zoom plus toolbar, and stacked bars with zoom on 52 weeks of data."
endpoint: /barchart-pro
package: dash_mui_charts
nav: Pro Features
category: BarChart
order: 6
icon: mdi:diamond-outline
---

.. llms_copy::Bar Chart - Pro

.. toc::

### Overview

Pro features — zoom, the range slider and the toolbar — flip the component
onto `BarChartPro` from `@mui/x-charts-pro` automatically when used.

.. admonition::Pro features
    :icon: mdi:diamond-outline
    :color: orange

    These demos require a **MUI X Pro license key**, read from the
    `MUI_PRO_API_KEY` environment variable and passed as `licenseKey`.
    Without it the charts render with the unlicensed watermark.

```python
BarChart(
    licenseKey=MUI_KEY,
    series=[{'data': weekly_sales, 'label': 'Sales'}],
    xAxis=[{'data': categories, 'scaleType': 'band',
            'zoom': {'minSpan': 8}}],
    showSlider=True,
    initialZoom=[{'axisId': 'auto-generated-id-0', 'start': 0, 'end': 40}],
)
```

---

### Zoom with slider

52 weeks of data with a zoom slider — drag the slider or use the mouse
wheel to zoom.

.. exec::docs.barchart_pro.slider_example
    :code: false

.. source::docs/barchart_pro/slider_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Zoom + toolbar

Toolbar with zoom in/out buttons and export options.

.. exec::docs.barchart_pro.toolbar_example
    :code: false

.. source::docs/barchart_pro/toolbar_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Stacked with zoom

Stacked bars with zoom and slider.

.. exec::docs.barchart_pro.stacked_zoom_example
    :code: false

.. source::docs/barchart_pro/stacked_zoom_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Related pages

- [Basic](/barchart-basic) · [Dataset Mode](/barchart-dataset) · [Stacking](/barchart-stacking) · [Interaction](/barchart-interaction) · [Reference Lines](/barchart-reference)
