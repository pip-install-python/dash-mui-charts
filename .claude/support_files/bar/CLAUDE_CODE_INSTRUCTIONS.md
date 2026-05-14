# Claude Code — Bar Chart + Candlestick Implementation Instructions

## Context

You are adding BarChart, RangeBarChart, and CandlestickChart to the existing `dash-mui-charts` Dash component library. Follow the EXACT patterns used by the existing `LineChart` component.

## Files Provided

- `IMPLEMENTATION_PLAN.md` — Architecture, phases, prop mappings, Python usage examples
- `API_REFERENCE.md` — Exhaustive MUI prop/slot surface for all three components
- `stubs/BarChart.react.js` — React stub (~70% complete)
- `stubs/RangeBarChart.react.js` — React stub (~70% complete)
- `stubs/CandlestickChart.react.js` — React stub (~70% complete)

## Critical: Study the Existing LineChart First

Before writing any code, study the existing `LineChart.react.js`:

```bash
cat src/lib/components/LineChart.react.js
```

The BarChart should mirror this component's structure exactly:
- Same license key activation pattern
- Same Pro feature gating logic
- Same `setProps` output prop pattern for click events
- Same `initialZoom`, `showSlider`, `showToolbar` prop handling
- Same `referenceLines` pass-through pattern

## Execution Steps

### 1. Check existing project
```bash
cat package.json | grep -E "mui|charts"
cat src/lib/index.js
ls src/lib/components/
cat src/lib/components/LineChart.react.js | head -80
```

### 2. Install dependencies
```bash
# Check what's already installed
npm ls @mui/x-charts @mui/x-charts-pro 2>/dev/null

# Install what's missing
npm install @mui/x-charts-premium
# @mui/x-charts and @mui/x-charts-pro should already be installed
```

### 3. Copy and complete stubs

**BarChart.react.js** — Key completions:
- Replace placeholder with actual MUI import: `import { BarChart as MuiBarChart } from '@mui/x-charts/BarChart'` and `import { BarChartPro } from '@mui/x-charts-pro/BarChartPro'`
- Copy the license key activation from `LineChart.react.js` verbatim
- Wire Pro/Free component selection (same pattern as LineChart)
- Pass through `referenceLines` (if the existing chart wrapper supports them)
- Wire `showSlider` — look at how LineChart handles it (may need zoom slider component)

**RangeBarChart.react.js** — Key completions:
- Import `BarChartPremium` from `@mui/x-charts-premium`
- Auto-inject `type: 'rangeBar'` into all series
- Premium license activation

**CandlestickChart.react.js** — Key completions:
- Import `CandlestickChart` from `@mui/x-charts-premium`
- Handle both data formats: `[[o,h,l,c], ...]` and `datasetKeys`
- Note: CandlestickPlot uses WebGL canvas — the chart handles this internally
- `upColor` and `downColor` can be strings or functions. For Dash, only support strings (functions can't be serialized).

### 4. Register components in `src/lib/index.js`
```js
export {default as BarChart} from './components/BarChart.react';
export {default as RangeBarChart} from './components/RangeBarChart.react';
export {default as CandlestickChart} from './components/CandlestickChart.react';
```

### 5. Build and verify
```bash
npm run build
cat dash_mui_charts/BarChart.py | head -30
cat dash_mui_charts/RangeBarChart.py | head -30
cat dash_mui_charts/CandlestickChart.py | head -30
```

### 6. Update `__init__.py`

### 7. Test
```python
# Quick test
import dash
from dash import html
from dash_mui_charts import BarChart

app = dash.Dash(__name__)
app.layout = html.Div([
    BarChart(
        id="test",
        series=[{"data": [4, 3, 5]}, {"data": [1, 6, 3]}],
        xAxis=[{"data": ["A", "B", "C"], "scaleType": "band"}],
        height=300,
    )
])
app.run(debug=True)
```

## Key Gotchas

1. **`scaleType: 'band'` is required on the category axis for bar charts.** Without it, MUI throws. Make sure docs and examples always include it.

2. **`barLabel` functions can't be serialized by Dash.** Only support string values: `"value"` and `"formattedValue"`. If a user wants custom formatting, they'd need a JS clientside callback or a future `barLabelFormat` string prop.

3. **`upColor`/`downColor` functions can't be serialized.** Only support string color values in Dash. Document this limitation.

4. **`@mui/x-charts-premium` is a separate package** with its own license tier. The existing `@mui/x-charts-pro` package is NOT sufficient for RangeBarChart or CandlestickChart.

5. **CandlestickChart is in Preview.** MUI warns the API may change. Document this clearly. The component name and import path may change in future MUI versions.

6. **The existing `LiveTradingChart` is a DIFFERENT component.** It's a custom client-side real-time simulation. The new `CandlestickChart` wraps MUI's native static OHLC chart. Both should coexist — they serve different use cases.

7. **`dataset` mode with `dataKey`:** When users provide `dataset=[{month: "Jan", revenue: 30}, ...]`, series use `dataKey: "revenue"` instead of `data: [30, ...]`. This is a pass-through — MUI handles the mapping internally.

8. **Batch renderer (`renderer: 'svg-batch'`):** Only works for regular BarChart, NOT for RangeBarChart. Has trade-offs (no CSS styling per bar, no transparency in highlights). Only recommend for datasets > 200 bars.
