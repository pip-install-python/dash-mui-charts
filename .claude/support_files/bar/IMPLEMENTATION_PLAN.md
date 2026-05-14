# MUI X Bar Charts + Candlestick — Dash Integration Plan

## Overview

Extend `dash-mui-charts` with three new components following the same patterns as the existing `LineChart`:

| Component | MUI Source | License | Key Features |
|---|---|---|---|
| `BarChart` | `@mui/x-charts/BarChart` + `BarChartPro` | Free + Pro | Vertical/horizontal bars, stacking, labels, dataset mode, border radius, color maps, bar gap/category gap, min bar size, batch renderer |
| `RangeBarChart` | `@mui/x-charts-premium/BarChartPremium` | Premium | Range bars (`{start, end}`), temperature ranges, Gantt-style timelines |
| `CandlestickChart` | `@mui/x-charts-premium` (Preview) | Premium | OHLC candlestick, `upColor`/`downColor`, dataset mode with `datasetKeys`, WebGL rendering, composition with volume bars + moving averages |

> **Note:** The existing `LiveTradingChart` in dash-mui-charts is a custom client-side simulation. The new `CandlestickChart` wraps MUI's native candlestick which is data-driven (no simulation) and supports all MUI chart features (zoom, tooltip, axis formatting, composition).

---

## Phase 1: `BarChart` (Free + Pro)

### Dash Component: `BarChart`

**File:** `src/lib/components/BarChart.react.js`

This follows the exact same architectural pattern as the existing `LineChart` — pass-through props to MUI's `<BarChart>`, with Pro features gated behind `licenseKey`.

#### Props

**Data Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `id` | string | — | Standard Dash id |
| `series` | list[dict] | `series` | Array of bar series: `{data, label, color, stack, barLabel, barLabelPlacement, highlightScope, dataKey}` |
| `dataset` | list[dict] | `dataset` | Alternative: array of row objects, series use `dataKey` |
| `xAxis` | list[dict] | `xAxis` | Axis config: `{data, scaleType, label, dataKey, categoryGapRatio, barGapRatio, tickPlacement, tickLabelPlacement, colorMap, zoom}` |
| `yAxis` | list[dict] | `yAxis` | Same structure as xAxis |

**Layout & Appearance:**

| Dash Prop | Type | Default | MUI Prop | Notes |
|---|---|---|---|---|
| `layout` | string | `"vertical"` | `layout` | `"vertical"` or `"horizontal"` |
| `borderRadius` | number | `None` | `borderRadius` | Rounded bar corners |
| `height` | number | `300` | `height` | Chart height px |
| `width` | number | `None` | `width` | Chart width px (default: parent) |
| `margin` | dict | `None` | `margin` | `{top, bottom, left, right}` |
| `grid` | dict | `None` | `grid` | `{horizontal: bool, vertical: bool}` |
| `colors` | list[string] | `None` | `colors` | Color palette |
| `skipAnimation` | bool | `None` | `skipAnimation` | Disable animations |
| `loading` | bool | `False` | `loading` | Show loading overlay |
| `hideLegend` | bool | `None` | `hideLegend` | Hide legend |
| `renderer` | string | `None` | `renderer` | `"svg-single"` (default) or `"svg-batch"` for performance |

**Interaction Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `axisHighlight` | dict | `axisHighlight` | `{x: 'band'/'line'/'none', y: 'band'/'line'/'none'}` |
| `tooltip` | dict | — | Tooltip trigger config (via slotProps) |
| `highlightedItem` | dict | `highlightedItem` | Controlled highlight `{seriesId, dataIndex}` |

**Pro Features (require `licenseKey`):**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `licenseKey` | string | — | MUI Pro license key |
| `initialZoom` | list[dict] | `initialZoom` | Initial zoom state |
| `showSlider` | bool | — | Zoom range slider (Pro) |
| `showToolbar` | bool | `showToolbar` | Zoom/export toolbar |
| `brushConfig` | dict | `brushConfig` | Brush selection (Pro) |

**Output Props (Dash callbacks):**

| Dash Prop | Type | Fires On | Notes |
|---|---|---|---|
| `clickData` | dict | `onItemClick` | `{seriesId, dataIndex, value, event_timestamp}` |
| `axisClickData` | dict | `onAxisClick` | `{axisValue, seriesValues, event_timestamp}` |
| `highlightedItem` | dict | `onHighlightChange` | Controlled + output |

**Series Object Structure:**

```python
{
    "data": [4, 3, 5],           # or use dataKey with dataset
    "dataKey": "revenue",         # alternative to data, used with dataset prop
    "label": "Revenue",
    "color": "#1976d2",
    "stack": "group1",            # stack ID (series with same value are stacked)
    "stackOffset": "none",        # "none", "expand", "diverging", "silhouette", "wiggle"
    "stackOrder": "none",         # "none", "appearance", "ascending", "descending", "insideOut", "reverse"
    "barLabel": "value",          # "value", "formattedValue", or omit
    "barLabelPlacement": "center",# "center" or "outside"
    "highlightScope": {"highlight": "series", "fade": "global"},
    "yAxisId": "left",            # for biaxial
}
```

---

## Phase 2: `RangeBarChart` (Premium)

### Dash Component: `RangeBarChart`

**File:** `src/lib/components/RangeBarChart.react.js`

Uses `BarChartPremium` from `@mui/x-charts-premium`.

#### Key Differences from BarChart

- Series type is `"rangeBar"` instead of `"bar"`
- Each data point is `{start: number, end: number}` instead of a single number
- Uses `BarChartPremium` / `RangeBarPlot` under the hood
- No batch renderer support
- `colorMap` does NOT work on the numerical axis

**Data Props:**

| Dash Prop | Type | Notes |
|---|---|---|
| `series` | list[dict] | Series with `type: "rangeBar"`, `data: [{start, end}, ...]` |
| `dataset` | list[dict] | Row objects; series use `dataKey` |
| `xAxis` | list[dict] | Same as BarChart |
| `yAxis` | list[dict] | Same as BarChart |
| `licenseKey` | string | **Required** — Premium license |

All appearance, layout, and Pro props from BarChart apply here too.

**Series Object Structure:**

```python
{
    "type": "rangeBar",  # REQUIRED — distinguishes from regular bar
    "data": [
        {"start": 5, "end": 15},
        {"start": 3, "end": 12},
    ],
    "label": "Temperature Range",
    "color": "#1976d2",
}
```

**Output Props:** Same as BarChart (`clickData`, `axisClickData`).

---

## Phase 3: `CandlestickChart` (Premium — Preview)

### Dash Component: `CandlestickChart`

**File:** `src/lib/components/CandlestickChart.react.js`

Uses `CandlestickChart` from `@mui/x-charts-premium`.

> **Important:** This is MUI's PREVIEW candlestick — not the existing custom `LiveTradingChart`. It's a static data-driven chart, not a real-time simulation. The two components serve different purposes and should coexist.

**Data Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `series` | list[dict] | `series` | OHLC series: `{data: [[o,h,l,c], ...], upColor, downColor, datasetKeys}` |
| `dataset` | list[dict] | `dataset` | Row objects with open/high/low/close columns |
| `xAxis` | list[dict] | `xAxis` | Band axis with dates/labels. Supports `zoom` (Pro) |
| `yAxis` | list[dict] | `yAxis` | Value axis with `valueFormatter` |
| `licenseKey` | string | — | **Required** — Premium license |

**Candlestick-Specific Props:**

| Dash Prop | Type | Notes |
|---|---|---|
| `height` | number | Chart height |
| `width` | number | Chart width |
| `margin` | dict | `{top, bottom, left, right}` |
| `grid` | dict | `{horizontal, vertical}` |
| `skipAnimation` | bool | Disable animations |
| `showToolbar` | bool | Toolbar |

**Series Object Structure:**

```python
# Array format
{
    "data": [
        [100, 110, 95, 105],   # [open, high, low, close]
        [105, 115, 100, 112],
    ],
    "upColor": "#4caf50",       # Close >= Open color
    "downColor": "#f44336",     # Close < Open color
}

# Dataset format
{
    "datasetKeys": {"open": "open", "high": "high", "low": "low", "close": "close"},
    "upColor": "#4caf50",
    "downColor": "#f44336",
}
```

**Output Props:**

| Dash Prop | Type | Fires On |
|---|---|---|
| `clickData` | dict | Item click — `{dataIndex, ohlc: {open, high, low, close}, event_timestamp}` |

---

## File Structure

```
src/lib/components/
├── BarChart.react.js           # MUI BarChart + BarChartPro wrapper
├── RangeBarChart.react.js      # MUI BarChartPremium (rangeBar series)
├── CandlestickChart.react.js   # MUI CandlestickChart wrapper (static OHLC)
├── ... (existing components)
```

```
dash_mui_charts/
├── BarChart.py                 # Auto-generated
├── RangeBarChart.py            # Auto-generated
├── CandlestickChart.py         # Auto-generated
```

```
docs/dash_mui_charts/
├── bar_basic.py                # Basic bars, stacking, horizontal
├── bar_pro.py                  # Zoom, brush, labels, border radius
├── range_bar.py                # Range bar demos
├── candlestick_basic.py        # Static OHLC candlestick
```

---

## npm Dependencies

Add/verify in `package.json`:

```json
{
  "dependencies": {
    "@mui/x-charts": "^7.x || ^8.x || ^9.x",
    "@mui/x-charts-pro": "^7.x || ^8.x || ^9.x",
    "@mui/x-charts-premium": "^9.x"
  }
}
```

> **Note:** `@mui/x-charts` is likely already installed for the existing chart components. `@mui/x-charts-pro` may already be installed for zoom/brush. `@mui/x-charts-premium` is new — needed for RangeBarChart and CandlestickChart.

---

## Implementation Order

### Step 1 — `BarChart` (Free)
1. Create `BarChart.react.js` with full prop surface
2. Wire `series`, `dataset`, `xAxis`, `yAxis` pass-through
3. Wire `layout`, `borderRadius`, `grid`, `colors`, `margin`
4. Wire `onItemClick` → `clickData`, `onAxisClick` → `axisClickData`
5. Wire `highlightedItem` controlled + output
6. Wire `barLabel` / `barLabelPlacement` in series
7. Wire `categoryGapRatio` / `barGapRatio` on xAxis
8. Build, test with basic vertical + horizontal + stacked demos

### Step 2 — `BarChart` Pro Features
1. Add `licenseKey` gating (same as existing LineChart Pro)
2. Wire `initialZoom`, `showSlider`, `showToolbar`, `brushConfig`
3. Wire `renderer` prop for batch rendering performance mode
4. Write `bar_pro.py` docs

### Step 3 — `RangeBarChart` (Premium)
1. Create `RangeBarChart.react.js` using `BarChartPremium`
2. Handle `rangeBar` series type with `{start, end}` data format
3. Wire same appearance/interaction props as BarChart
4. Write `range_bar.py` docs

### Step 4 — `CandlestickChart` (Premium — Preview)
1. Create `CandlestickChart.react.js`
2. Wire OHLC `data: [[o,h,l,c], ...]` format
3. Wire `dataset` mode with `datasetKeys: {open, high, low, close}`
4. Wire `upColor` / `downColor` on series
5. Wire zoom support on xAxis
6. Write `candlestick_basic.py` docs

### Step 5 — Polish
1. Update `llms.txt` with all three components
2. Update `__init__.py` exports
3. Bump version

---

## Callback Patterns (Python Usage Examples)

### Basic BarChart

```python
from dash_mui_charts import BarChart

BarChart(
    id="bar-basic",
    series=[
        {"data": [4, 3, 5], "label": "Group A", "color": "#1976d2"},
        {"data": [1, 6, 3], "label": "Group B", "color": "#388e3c"},
        {"data": [2, 5, 6], "label": "Group C", "color": "#f57c00"},
    ],
    xAxis=[{"data": ["Q1", "Q2", "Q3"], "scaleType": "band"}],
    height=350,
    grid={"horizontal": True},
)
```

### Stacked Horizontal with Labels

```python
BarChart(
    id="bar-stacked",
    series=[
        {"data": [30, 25, 40], "label": "Revenue", "stack": "total", "barLabel": "value"},
        {"data": [20, 15, 25], "label": "Expenses", "stack": "total", "barLabel": "value"},
    ],
    xAxis=[{"data": ["2022", "2023", "2024"], "scaleType": "band"}],
    layout="horizontal",
    borderRadius=6,
    height=300,
)
```

### Dataset Mode

```python
BarChart(
    id="bar-dataset",
    dataset=[
        {"month": "Jan", "london": 18, "paris": 15, "nyc": 12},
        {"month": "Feb", "london": 22, "paris": 18, "nyc": 15},
        {"month": "Mar", "london": 30, "paris": 25, "nyc": 22},
    ],
    xAxis=[{"dataKey": "month"}],
    series=[
        {"dataKey": "london", "label": "London"},
        {"dataKey": "paris", "label": "Paris"},
        {"dataKey": "nyc", "label": "New York"},
    ],
    height=350,
)
```

### Pro: Zoom + Brush

```python
BarChart(
    id="bar-zoom",
    licenseKey=os.getenv("MUI_PRO_API_KEY", ""),
    series=[{"data": big_dataset, "label": "Sales"}],
    xAxis=[{
        "data": categories,
        "scaleType": "band",
        "zoom": {"minSpan": 5, "panning": True},
    }],
    showSlider=True,
    showToolbar=True,
    height=400,
)
```

### RangeBarChart (Temperature Ranges)

```python
from dash_mui_charts import RangeBarChart

RangeBarChart(
    id="range-temp",
    licenseKey=os.getenv("MUI_PREMIUM_API_KEY", ""),
    series=[{
        "type": "rangeBar",
        "data": [
            {"start": 5, "end": 14},
            {"start": 6, "end": 16},
            {"start": 9, "end": 20},
        ],
        "label": "Temperature Range",
        "color": "#ef5350",
    }],
    xAxis=[{"data": ["Jan", "Feb", "Mar"], "scaleType": "band"}],
    yAxis=[{"label": "°C"}],
    borderRadius=4,
    height=350,
)
```

### CandlestickChart (Static OHLC)

```python
from dash_mui_charts import CandlestickChart

CandlestickChart(
    id="candle-basic",
    licenseKey=os.getenv("MUI_PREMIUM_API_KEY", ""),
    series=[{
        "data": [
            [100, 110, 95, 105],
            [105, 115, 100, 112],
            [112, 120, 108, 118],
        ],
        "upColor": "#4caf50",
        "downColor": "#f44336",
    }],
    xAxis=[{
        "data": ["Mon", "Tue", "Wed"],
        "scaleType": "band",
        "zoom": {"minSpan": 1, "filterMode": "discard"},
    }],
    yAxis=[{"label": "Price ($)"}],
    height=400,
)
```

### CandlestickChart with Dataset

```python
CandlestickChart(
    id="candle-dataset",
    licenseKey=os.getenv("MUI_PREMIUM_API_KEY", ""),
    dataset=[
        {"date": "2025-01-02", "open": 100, "high": 110, "low": 95, "close": 105},
        {"date": "2025-01-03", "open": 105, "high": 115, "low": 100, "close": 112},
    ],
    series=[{
        "datasetKeys": {"open": "open", "high": "high", "low": "low", "close": "close"},
        "upColor": "#4caf50",
        "downColor": "#f44336",
    }],
    xAxis=[{"dataKey": "date", "zoom": {"minSpan": 1, "filterMode": "discard"}}],
    height=400,
)
```

---

## Key Architecture Decisions

1. **BarChart mirrors LineChart pattern exactly.** Same prop structure for `series`, `xAxis`, `yAxis`, `grid`, `height`, `licenseKey`, `initialZoom`, `showSlider`, `showToolbar`, `brushConfig`. This is intentional — users learn one pattern.

2. **`dataset` mode is a direct pass-through.** MUI's dataset helper avoids data duplication. Dash users pass `dataset=[{...}, ...]` and reference columns via `dataKey` in series and axes.

3. **RangeBarChart is a separate component** (not a mode of BarChart) because it requires `@mui/x-charts-premium` and uses `BarChartPremium` internally. This keeps the free `BarChart` tree-shakeable.

4. **CandlestickChart coexists with LiveTradingChart.** They serve different purposes: `CandlestickChart` = static MUI native OHLC chart with zoom/tooltip/composition support. `LiveTradingChart` = real-time client-side simulation with alerts/forecast. Document both clearly.

5. **`barLabel` as string, not function.** MUI accepts functions for `barLabel` but Dash can't serialize JS functions. We support `"value"` and `"formattedValue"` strings. For custom formatting, a future enhancement could use a `barLabelFormat` string (like `dateFormat` on LineChart).

6. **License tiers:** `BarChart` = Free + Pro gated by `licenseKey`. `RangeBarChart` + `CandlestickChart` = Premium gated by `licenseKey`. Use the same `LicenseInfo.setLicenseKey()` pattern as existing Heatmap.
