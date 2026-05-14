# MUI X Bar Charts + Candlestick — Complete API Reference

## BarChart Props (Community + Pro)

Source: `@mui/x-charts/BarChart` / `@mui/x-charts-pro/BarChartPro`

| Prop | Type | Default | Description |
|---|---|---|---|
| `series`* | object[] | — | Array of BarSeries objects |
| `axisHighlight` | `{x?: 'band'|'line'|'none', y?: 'band'|'line'|'none'}` | band in bar direction | Axis highlight config |
| `borderRadius` | number | — | Border radius on bars |
| `brushConfig` | `{enabled?, preventHighlight?, preventTooltip?}` | — | Brush selection (Pro) |
| `colors` | string[] \| func | `rainbowSurgePalette` | Color palette |
| `dataset` | object[] | — | Array of row objects for `dataKey` referencing |
| `disableAxisListener` | bool | `false` | Disable mouse tracking (perf) |
| `grid` | `{horizontal?: bool, vertical?: bool}` | — | Background grid |
| `height` | number | — | Chart height px |
| `hiddenItems` | object[] | — | Controlled hidden series/items |
| `hideLegend` | bool | — | Hide legend |
| `highlightedAxis` | object[] | — | Controlled axis highlight |
| `highlightedItem` | `{dataIndex?, seriesId}` | — | Controlled item highlight |
| `id` | string | — | Accessibility id |
| `initialHiddenItems` | object[] | — | Default hidden items |
| `layout` | `'horizontal'` \| `'vertical'` | `'vertical'` | Bar direction |
| `loading` | bool | `false` | Loading overlay |
| `localeText` | object | — | Localization |
| `margin` | number \| `{top?, bottom?, left?, right?}` | — | Chart margins |
| `onAxisClick` | func | — | `(event, data) => void` |
| `onHiddenItemsChange` | func | — | Hidden items callback |
| `onHighlightChange` | func | — | Highlight callback |
| `onHighlightedAxisChange` | func | — | Axis highlight callback |
| `onItemClick` | func | — | `(event, barItemIdentifier) => void` |
| `onTooltipItemChange` | func | — | Tooltip callback |
| `renderer` | `'svg-single'` \| `'svg-batch'` | `'svg-single'` | Render strategy |
| `showToolbar` | bool | `false` | Show toolbar |
| `skipAnimation` | bool | — | Disable animations |
| `slotProps` | object | `{}` | Slot props |
| `slots` | object | `{}` | Overridable slots |
| `tooltipItem` | object | — | Controlled tooltip |
| `width` | number | — | Chart width px |
| `xAxis` | object[] | — | X-axis config array |
| `yAxis` | object[] | — | Y-axis config array |

### BarSeries Interface

| Field | Type | Description |
|---|---|---|
| `data` | number[] | Bar values |
| `dataKey` | string | Column key when using `dataset` |
| `label` | string | Series label |
| `color` | string | Series color |
| `stack` | string | Stack group ID |
| `stackOffset` | `'none'|'expand'|'diverging'|'silhouette'|'wiggle'` | Stack offset strategy |
| `stackOrder` | `'none'|'appearance'|'ascending'|'descending'|'insideOut'|'reverse'` | Stack ordering |
| `barLabel` | `'value'` \| `'formattedValue'` \| func | Bar label content |
| `barLabelPlacement` | `'center'` \| `'outside'` | Label position |
| `highlightScope` | `{highlight?, fade?}` | Highlight behavior |
| `yAxisId` | string | Y-axis binding (biaxial) |
| `valueFormatter` | func | Tooltip value format |

### Band Axis Props (xAxis with `scaleType: 'band'`)

| Field | Type | Description |
|---|---|---|
| `data` | array | Category labels |
| `dataKey` | string | Column key from dataset |
| `scaleType` | `'band'` | Required for bar charts |
| `label` | string | Axis label |
| `categoryGapRatio` | number | Gap between categories (0-1) |
| `barGapRatio` | number | Gap between bars in same category (-1 to ∞) |
| `tickPlacement` | `'start'|'end'|'middle'|'extremities'` | Tick position |
| `tickLabelPlacement` | `'tick'|'middle'` | Label position |
| `colorMap` | object | Piecewise/continuous/ordinal color mapping |
| `zoom` | object | Zoom config (Pro): `{minSpan, maxSpan, panning, filterMode, slider}` |

### BarChart Slots

| Slot | Default | Description |
|---|---|---|
| `axisLabel` | `ChartsText` | Axis label component |
| `axisLine` | `'line'` | Axis line element |
| `axisTick` | `'line'` | Tick element |
| `axisTickLabel` | `ChartsText` | Tick label |
| `bar` | `BarElementPath` | Individual bar element |
| `barLabel` | `BarLabel` | Bar label component |
| `legend` | `ChartsLegend` | Legend component |
| `loadingOverlay` | `ChartsLoadingOverlay` | Loading state |
| `noDataOverlay` | `ChartsNoDataOverlay` | Empty state |
| `toolbar` | `ChartsToolbar` | Toolbar component |
| `tooltip` | `ChartsTooltipRoot` | Tooltip container |

---

## RangeBarChart Props (Premium)

Source: `@mui/x-charts-premium/BarChartPremium`

Inherits all BarChart props. Key differences:

- Uses `BarChartPremium` component internally
- Series must have `type: 'rangeBar'`
- Data format: `{start: number, end: number}` per point
- `colorMap` on numerical axis NOT supported
- Batch renderer NOT available
- Requires Premium license

### RangeBar Series Interface

| Field | Type | Description |
|---|---|---|
| `type` | `'rangeBar'` | **Required** — identifies range bar series |
| `data` | `{start: number, end: number}[]` | Range values |
| `dataKey` | string | Column key from dataset |
| `label` | string | Series label |
| `color` | string | Series color |
| `highlightScope` | object | Highlight behavior |

---

## CandlestickChart Props (Premium — Preview)

Source: `@mui/x-charts-premium/CandlestickChart`

| Prop | Type | Default | Description |
|---|---|---|---|
| `series`* | object[] | — | OHLC series |
| `dataset` | object[] | — | Row objects for `datasetKeys` mode |
| `xAxis` | object[] | — | Band axis (dates/labels) |
| `yAxis` | object[] | — | Value axis |
| `height` | number | — | Chart height |
| `width` | number | — | Chart width |
| `margin` | object | — | `{top, bottom, left, right}` |
| `grid` | object | — | `{horizontal, vertical}` |
| `skipAnimation` | bool | — | Disable animations |
| `showToolbar` | bool | `false` | Show toolbar |

### Candlestick Series Interface

| Field | Type | Description |
|---|---|---|
| `data` | `[open, high, low, close][]` | Array of OHLC tuples |
| `datasetKeys` | `{open, high, low, close}` | Map dataset columns to OHLC fields |
| `upColor` | string \| func | Color when close >= open. Func: `(mode: 'light'|'dark') => string` |
| `downColor` | string \| func | Color when close < open |
| `valueFormatter` | func | `(value, {dataIndex, field}) => string` where field is `'open'|'high'|'low'|'close'` |

### Candlestick Composition

For composed charts (candlestick + volume bars + moving average lines):
- xAxis must have `scaleType: 'band'`
- CandlestickPlot renders inside `ChartsWebGLLayer`
- Volume can use regular `BarPlot` on a secondary yAxis
- Moving averages use `LinePlot`

---

## Feature / License Matrix

| Feature | Free (BarChart) | Pro (BarChartPro) | Premium |
|---|---|---|---|
| Vertical/horizontal bars | ✅ | ✅ | ✅ |
| Stacking | ✅ | ✅ | ✅ |
| Bar labels | ✅ | ✅ | ✅ |
| Border radius | ✅ | ✅ | ✅ |
| Dataset mode | ✅ | ✅ | ✅ |
| Color maps | ✅ | ✅ | ✅ |
| Grid/tooltip/legend | ✅ | ✅ | ✅ |
| Click events | ✅ | ✅ | ✅ |
| Highlighting | ✅ | ✅ | ✅ |
| Batch renderer (perf) | ✅ | ✅ | ✅ |
| Zoom & pan | ❌ | ✅ | ✅ |
| Toolbar | ❌ | ✅ | ✅ |
| Brush selection | ❌ | ✅ | ✅ |
| Slider preview | ❌ | ✅ | ✅ |
| Range bars | ❌ | ❌ | ✅ |
| Candlestick (OHLC) | ❌ | ❌ | ✅ (Preview) |
