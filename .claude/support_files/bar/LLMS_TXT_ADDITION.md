# Bar Chart Components — llms.txt Addition

Append to existing `llms.txt`.

---

## Bar Charts

| Component | License | Key Features |
|:----------|:--------|:-------------|
| **BarChart** | Free + Pro | Vertical/horizontal bars, stacking, dataset mode, bar labels, border radius, color maps, batch renderer, zoom/pan (Pro), brush (Pro) |
| **RangeBarChart** | Premium | Range bars ({start, end}), temperature ranges, Gantt timelines, border radius, color maps |
| **CandlestickChart** | Premium (Preview) | Static OHLC candlestick, upColor/downColor, dataset mode with datasetKeys, zoom, WebGL rendering |

### BarChart Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `series` | list | Required | Array of `{data, dataKey, label, color, stack, barLabel, barLabelPlacement, highlightScope}` |
| `dataset` | list | `None` | Row objects for `dataKey`-based series |
| `xAxis` | list | `None` | X-axis config: `{data, scaleType, label, dataKey, categoryGapRatio, barGapRatio, tickPlacement, tickLabelPlacement, colorMap, zoom}` |
| `yAxis` | list | `None` | Y-axis config |
| `layout` | string | `"vertical"` | `"vertical"` or `"horizontal"` |
| `borderRadius` | int | `None` | Rounded bar corners |
| `height` | int | `300` | Chart height in pixels |
| `width` | int | `None` | Chart width (default: parent) |
| `margin` | dict | `None` | `{top, bottom, left, right}` |
| `grid` | dict | `None` | `{horizontal: bool, vertical: bool}` |
| `colors` | list | `None` | Color palette |
| `skipAnimation` | bool | `None` | Disable animations |
| `loading` | bool | `False` | Show loading overlay |
| `hideLegend` | bool | `None` | Hide legend |
| `renderer` | string | `None` | `"svg-single"` (default) or `"svg-batch"` for performance |
| `axisHighlight` | dict | `None` | `{x: 'band'/'line'/'none', y: ...}` |
| `highlightedItem` | dict | `None` | Controlled highlight `{seriesId, dataIndex}` |
| `licenseKey` | string | `""` | MUI Pro license key (for zoom, brush, toolbar) |
| `initialZoom` | list | `None` | Initial zoom state (Pro) |
| `showSlider` | bool | `False` | Zoom range slider (Pro) |
| `showToolbar` | bool | `False` | Zoom/export toolbar (Pro) |
| `brushConfig` | dict | `None` | Brush selection (Pro) |
| `clickData` | dict | Output | Bar click: `{seriesId, dataIndex, event_timestamp}` |
| `axisClickData` | dict | Output | Axis click: `{axisValue, event_timestamp}` |

### RangeBarChart Properties

Inherits all BarChart props. Key differences:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `series` | list | Required | `{data: [{start, end}, ...], label, color}` — type auto-set to `"rangeBar"` |
| `licenseKey` | string | Required | Premium license key |

### CandlestickChart Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `series` | list | Required | `{data: [[o,h,l,c], ...], upColor, downColor}` or `{datasetKeys: {open, high, low, close}}` |
| `dataset` | list | `None` | Row objects with OHLC columns |
| `xAxis` | list | `None` | Band axis config |
| `yAxis` | list | `None` | Value axis config |
| `height` | int | `400` | Chart height |
| `licenseKey` | string | Required | Premium license key |
| `clickData` | dict | Output | `{dataIndex, event_timestamp}` |

> **Note:** CandlestickChart is a static OHLC chart, distinct from LiveTradingChart which provides real-time simulation.
