# dash-mui-charts Skills Guide

This document provides LLMs and developers with detailed knowledge about the dash-mui-charts component library, enabling effective assistance with development, debugging, and feature implementation.

---

## Project Overview

**dash-mui-charts** is a Dash component library that wraps [MUI X Charts](https://mui.com/x/react-charts/) for Python developers. It bridges the gap between MUI's powerful React charting library and Plotly Dash's Python ecosystem.

### Architecture

```
React Components (src/lib/components/)
        ↓ [npm run build]
Webpack Bundle (dash_mui_charts/*.min.js)
        ↓ [dash-generate-components]
Python Wrappers (dash_mui_charts/*.py)
        ↓
Dash Application
```

---

## Project Structure

```
dash-mui-charts/
├── src/lib/components/              # React component source files
│   ├── LineChart.react.js          # Line/Area chart with Pro features
│   ├── BarChart.react.js           # Vertical/horizontal bar charts
│   ├── CandlestickChart.react.js   # OHLC candlestick charts
│   ├── PieChart.react.js           # Pie/Donut/Nested pie charts
│   ├── ScatterChart.react.js       # Scatter/point charts
│   ├── CompositeChart.react.js     # Layered scatter + line charts
│   ├── LiveTradingChart.react.js   # Real-time streaming charts
│   ├── Heatmap.react.js            # Heatmap with Pro features
│   ├── SparklineChart.react.js     # Compact inline sparklines
│   ├── SimpleTreeView.react.js     # JSX-driven tree
│   ├── TreeView.react.js           # Data-driven RichTreeView
│   ├── TreeViewPro.react.js        # Pro tree (reorder, lazy, per-item controls)
│   └── TimeClock.react.js          # Inline clock-face time picker
├── dash_mui_charts/                 # Python package (auto-generated)
│   ├── __init__.py                 # Package initialization
│   ├── LineChart.py                # Python wrapper for LineChart
│   ├── BarChart.py                 # Python wrapper for BarChart
│   ├── CandlestickChart.py         # Python wrapper for CandlestickChart
│   ├── PieChart.py                 # Python wrapper for PieChart
│   ├── ScatterChart.py             # Python wrapper for ScatterChart
│   ├── CompositeChart.py           # Python wrapper for CompositeChart
│   ├── LiveTradingChart.py         # Python wrapper for LiveTradingChart
│   ├── Heatmap.py                  # Python wrapper for Heatmap
│   ├── SparklineChart.py           # Python wrapper for SparklineChart
│   ├── SimpleTreeView.py           # Python wrapper for SimpleTreeView
│   ├── TreeView.py                 # Python wrapper for TreeView
│   ├── TreeViewPro.py              # Python wrapper for TreeViewPro
│   ├── TimeClock.py                # Python wrapper for TimeClock
│   ├── _imports_.py                # Auto-generated imports
│   └── dash_mui_charts.min.js      # Bundled JavaScript
├── assets/                          # Dash assets (auto-loaded)
│   ├── muiChartsFunctions.js       # Functions-as-props registry
│   └── liquid_glass_clock.css      # Glassmorphic TimeClock theme (light/dark)
├── pages/                           # Demo pages
│   ├── home.py                     # Landing page
│   ├── linechart_basic.py          # Basic line chart examples
│   ├── linechart_pro.py            # Pro features (zoom, pan)
│   ├── linechart_brush.py          # Brush selection (Pro)
│   ├── linechart_referencelines.py # Reference lines
│   ├── linechart_tick_hover.py      # Tick config, axis formatting, zoom best practices
│   ├── live_trading.py             # LiveTradingChart demo
│   ├── barchart_basic.py           # Bar chart: multi-series, horizontal, labels, negative
│   ├── barchart_dataset.py         # Bar chart: dataset mode, bar gap control
│   ├── barchart_stacking.py        # Bar chart: stack offsets, diverging, groups
│   ├── barchart_interaction.py     # Bar chart: click events, highlighting, tooltips
│   ├── barchart_reference.py       # Bar chart: reference lines, colors, animation
│   ├── barchart_pro.py             # Bar chart: zoom, slider, toolbar (Pro)
│   ├── barchart_candlestick.py     # Candlestick: OHLC, volume, styling, click events
│   ├── pie.py                      # Pie chart examples
│   ├── pie_props.py                # Nested pie property explorer
│   ├── scatter.py                  # Scatter chart examples
│   ├── composite.py                # Composite chart examples
│   ├── heatmap.py                  # Heatmap examples
│   ├── heatmap_props.py            # Heatmap property explorer
│   ├── sparkline.py                # Sparkline examples
│   ├── sparkline_style.py          # Sparkline styling
│   ├── tree_basic.py … tree_pro.py # TreeView / TreeViewPro demos
│   ├── time_clock.py               # TimeClock basics
│   └── time_clock_lab.py           # TimeClock × dash-mantine-components
├── .claude/                         # Claude Code configuration
│   ├── CLAUDE.md                   # Quick project reference
│   ├── SKILLS.md                   # This file
│   ├── settings.json               # Project settings
│   └── agents/                     # Reference documentation
├── app.py                          # Main Dash application
├── usage.py                        # Standalone examples
├── package.json                    # NPM dependencies
├── setup.py                        # Python package setup
├── webpack.config.js               # Build configuration
├── README.md                       # Project documentation
└── CHANGELOG.md                    # Version history
```

---

## Components (13 Total)

### 1. LineChart

**File:** `src/lib/components/LineChart.react.js`
**License:** Community (basic) / Pro (zoom/pan)

**Purpose:** Full-featured line and area charts with optional Pro features.

**Key Implementation:**

```javascript
// Series structure
series: [
  {
    data: [1, 2, 3, 4],           // Y values (required)
    label: 'Series Name',         // Legend label
    color: '#1976d2',             // Line color
    area: true,                   // Fill area under line
    curve: 'monotoneX',           // Curve interpolation
    stack: 'group1',              // Stack group ID
    yAxisId: 'right',             // For biaxial charts
  }
]

// Axis structure
xAxis: [
  {
    data: ['Jan', 'Feb', 'Mar'],  // Tick values
    scaleType: 'band',            // 'band' | 'linear' | 'time' | 'log'
    label: 'Month',
  }
]
```

**Pro Features (require license):**
- `zoom` / `initialZoom` - Controlled/uncontrolled zoom state
- `showSlider` - Zoom range slider
- Zoom callbacks via `zoomData` output prop
- `brushConfig` - Range selection with brush interaction

**Reference Lines:**
```python
LineChart(
    referenceLines=[
        # Horizontal line (target/threshold)
        {
            'y': 100,
            'label': 'Target',
            'labelAlign': 'end',  # 'start' | 'middle' | 'end'
            'lineStyle': {'stroke': '#4caf50', 'strokeWidth': 2},
            'labelStyle': {'fill': '#4caf50', 'fontWeight': 'bold'},
        },
        # Vertical line (date/event marker)
        {
            'x': 'Q2',
            'label': 'Launch',
            'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '5 5'},
        },
        # With multi-axis support
        {
            'y': 50,
            'axisId': 'right-axis',  # Reference specific axis
            'label': 'Threshold',
        },
    ],
)
```

**Brush Selection (Pro):**
```python
LineChart(
    series=[{'id': 'my-series', 'data': [1, 2, 3, 4, 5]}],
    brushConfig={'enabled': True},
    brushOverlay='values',  # 'none' | 'default' | 'values'
    brushSeriesId='my-series',  # For 'values' overlay calculations
)
```

**Axis Highlight:**
```python
LineChart(
    axisHighlight={
        'x': 'band',  # 'none' | 'line' | 'band'
        'y': 'line',  # 'none' | 'line'
    },
)
```

**Controlled Item Highlight:**
```python
LineChart(
    id='my-chart',
    series=[
        {
            'id': 'sales',
            'data': [1, 2, 3, 4, 5],
            'showMark': True,  # Required for item hover
            'highlightScope': {'highlight': 'item', 'fade': 'global'},
        },
    ],
    tooltip={'trigger': 'item'},
    highlightedItem={'seriesId': 'sales', 'dataIndex': 2},  # Highlight 3rd point
)

# Callback to handle highlight changes
@callback(
    Output('display', 'children'),
    Input('my-chart', 'highlightedItem'),
)
def show_highlight(item):
    return json.dumps(item) if item else "No highlight"

# Callback to set highlight programmatically
@callback(
    Output('my-chart', 'highlightedItem'),
    Input('highlight-btn', 'n_clicks'),
    prevent_initial_call=True
)
def set_highlight(n):
    return {'seriesId': 'sales', 'dataIndex': 0}
```

**Controlled Axis Highlight:**
```python
LineChart(
    id='my-chart',
    xAxis=[{'id': 'x-axis', 'data': ['A', 'B', 'C']}],
    highlightedAxis=[{'axisId': 'x-axis', 'dataIndex': 1}],  # Highlight 'B'
)

@callback(
    Output('my-chart', 'highlightedAxis'),
    Input('my-chart', 'highlightedAxis'),  # Updates on hover
)
def sync_axis_highlight(axis_highlight):
    # Use for cross-chart synchronization
    return axis_highlight
```

**Per-Series Highlight Scope:**
```python
LineChart(
    series=[
        {
            'id': 'series-a',
            'data': [1, 2, 3],
            'highlightScope': {
                'highlight': 'series',  # Highlight entire series on hover
                'fade': 'global',        # Fade all other series
            },
        },
        {
            'id': 'series-b',
            'data': [3, 2, 1],
            'highlightScope': {
                'highlight': 'item',     # Highlight single point
                'fade': 'series',        # Fade other points in same series
            },
        },
    ],
)
```

**Toolbar (Pro):**
```python
LineChart(
    licenseKey=MUI_PRO_LICENSE,
    showToolbar=True,  # Displays zoom/export controls
    ...
)
```

**Synchronized Tooltips with Custom Overlays:**

MUI X Charts has a known limitation: native tooltips only appear on the hovered chart, not on synchronized charts (see GitHub issues #14455, #17555). The solution is to use custom HTML tooltip overlays.

```python
# 1. Disable MUI's built-in tooltip
LineChart(
    id='chart-a',
    series=[{
        'id': 'series-a',
        'data': data_a,
        'showMark': True,
        'highlightScope': {'highlight': 'item', 'fade': 'global'},
    }],
    tooltip={'trigger': 'none'},  # Disable MUI tooltip
)

# 2. Add custom tooltip div positioned over each chart
html.Div([
    LineChart(id='chart-a', tooltip={'trigger': 'none'}, ...),
    html.Div(id='custom-tooltip-a', style={
        'position': 'absolute',
        'display': 'none',
        'backgroundColor': 'white',
        'border': '1px solid #e0e0e0',
        'borderRadius': '4px',
        'padding': '8px 12px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
        'pointerEvents': 'none',
        'zIndex': 1000,
        'transform': 'translateX(-50%)',
    }),
], style={'position': 'relative'})

# 3. Sync highlights AND control custom tooltips
@callback(
    Output('chart-a', 'highlightedItem'),
    Output('chart-b', 'highlightedItem'),
    Output('custom-tooltip-a', 'style'),
    Output('custom-tooltip-a', 'children'),
    Output('custom-tooltip-b', 'style'),
    Output('custom-tooltip-b', 'children'),
    Input('chart-a', 'highlightedItem'),
    Input('chart-b', 'highlightedItem'),
)
def sync_charts_with_tooltips(highlight_a, highlight_b):
    # Chart layout constants
    LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN = 80, 20, 20
    NUM_POINTS = 6

    # Get data index from triggered chart
    triggered = ctx.triggered_id
    data_index = None
    if triggered == 'chart-a' and highlight_a:
        data_index = highlight_a.get('dataIndex')
    elif triggered == 'chart-b' and highlight_b:
        data_index = highlight_b.get('dataIndex')

    if data_index is None:
        # Hide tooltips
        hidden = {'display': 'none', ...}
        return None, None, hidden, "", hidden, ""

    # Calculate tooltip position using CSS calc()
    position_fraction = data_index / (NUM_POINTS - 1)
    tooltip_style = {
        'display': 'block',
        'left': f'calc({LEFT_MARGIN}px + {position_fraction} * (100% - {LEFT_MARGIN + RIGHT_MARGIN}px))',
        'top': f'{TOP_MARGIN + 15}px',
        ...
    }

    # Return synced highlights + visible tooltips for BOTH charts
    return (
        {'seriesId': 'series-a', 'dataIndex': data_index},
        {'seriesId': 'series-b', 'dataIndex': data_index},
        tooltip_style, tooltip_content_a,
        tooltip_style, tooltip_content_b,
    )
```

See `pages/highlighting_sync.py` for the complete implementation.

**Click Event Data:**
```python
clickData = {
    'type': 'mark',  # 'axis' | 'mark' | 'line' | 'area'
    'seriesIndex': 0,
    'dataIndex': 2,
    'value': 5.5,
    'timestamp': '2025-01-10T...'
}
```

**Built-in Date Formatting (v1.1.0):**

For time-scale axes, use `dateFormat` / `dateTickFormat` to control label format without writing JavaScript:

```python
LineChart(
    xAxis=[{
        'data': epoch_ms_timestamps,
        'scaleType': 'time',
        'dateFormat': 'M/d HH:mm',     # Full format (tooltips)
        'dateTickFormat': 'M/d',        # Short format (tick labels)
        'height': 80,                   # Extra space for angled labels
        'tickMinStep': 86400 * 1000 * 14,  # Min 2 weeks between ticks
        'tickLabelStyle': {'angle': 35, 'fontSize': 12, 'textAnchor': 'start'},
    }],
    margin={'left': 65, 'right': 20, 'top': 20, 'bottom': 100},
)
```

Supported format tokens: `YYYY` (year), `MMM` (Jan), `MM` (01), `M` (1), `dd` (01), `d` (1), `HH` (00-23), `mm` (00-59).

The component internally creates a `valueFormatter` function using `context.location === 'tick'` to choose between the tick and tooltip format. The `dateFormat`/`dateTickFormat` props are stripped before passing the axis config to MUI.

**Functions-as-Props Pattern (v1.1.0):**

For advanced formatting beyond dates, use the DMC-style functions-as-props pattern:

```python
# Python: pass a function reference
LineChart(
    xAxis=[{
        'scaleType': 'time',
        'valueFormatter': {
            'function': 'formatDate',          # Function name in registry
            'options': {'format': 'M/d HH:mm'},  # Passed as last arg
        },
    }],
)
```

```javascript
// assets/muiChartsFunctions.js: define the function
var dmcf = window.dashMuiChartsFunctions = window.dashMuiChartsFunctions || {};

dmcf.formatDate = function(value, context, options) {
    var d = value instanceof Date ? value : new Date(value);
    var fmt = (options && options.format) || 'M/d';
    // ... format date using tokens
};
```

The `resolveFunctionProp` utility in LineChart/CompositeChart resolves `{function, options}` objects from `window.dashMuiChartsFunctions` at render time. The wrapper passes `options` as the last argument to the resolved function.

**Axis Formatting Best Practices:**
- Use `scaleType: 'time'` (not `'point'`) for date axes when you need angled labels or zoom
- `'point'` scale with `tickLabelStyle.angle` hides labels due to MUI collision detection
- Increase `tickMinStep` to reduce tick count — more space per label prevents truncation
- Set `height: 80` on x-axis + `margin.bottom: 100` for rotated labels
- Use `tickNumber: 6` to cap total ticks for predictable spacing
- `axisHighlight: 'band'` does NOT work on `'time'` scale — use `'line'` instead

---

### 2. BarChart

**File:** `src/lib/components/BarChart.react.js`
**License:** Community (basic) / Pro (zoom/brush/toolbar)

**Purpose:** Vertical and horizontal bar charts with stacking, labels, dataset mode, and Pro features.

**Architecture:** Uses direct `BarChart` from `@mui/x-charts/BarChart` for community features, automatically switches to `BarChartPro` from `@mui/x-charts-pro/BarChartPro` when Pro features (zoom, brush, toolbar) are requested with a license key.

**Key Implementation:**

```javascript
// Series structure
series: [
  {
    data: [4, 3, 5],                // Bar values
    dataKey: 'sales',               // OR use with dataset prop
    label: 'Sales',
    color: '#1976d2',
    stack: 'group1',                // Stack group ID
    stackOffset: 'none',            // 'none', 'expand', 'diverging'
    stackOrder: 'none',             // 'none', 'appearance', 'ascending', 'descending'
    barLabel: 'value',              // Show value on bars
    barLabelPlacement: 'center',    // 'center' or 'outside'
    highlightScope: { highlight: 'series', fade: 'global' },
    yAxisId: 'left',                // For biaxial
  }
]

// Band axis for categories
xAxis: [
  {
    data: ['Q1', 'Q2', 'Q3'],
    scaleType: 'band',              // Required for bar charts
    categoryGapRatio: 0.3,          // Gap between categories (0-1)
    barGapRatio: 0.1,               // Gap between bars in category (-1 to Inf)
  }
]
```

**Dataset Mode:**
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

**Stacking Patterns:**
```python
# Normalized to 100%
series=[
    {'data': [40, 35], 'stack': 'g', 'stackOffset': 'expand'},
    {'data': [30, 25], 'stack': 'g', 'stackOffset': 'expand'},
]

# Diverging (positive above, negative below zero)
series=[
    {'data': [20, -10], 'stack': 'net', 'stackOffset': 'diverging'},
    {'data': [-15, 25], 'stack': 'net', 'stackOffset': 'diverging'},
]

# Multiple stack groups (side by side)
series=[
    {'data': [40], 'stack': '2024'},
    {'data': [20], 'stack': '2024'},
    {'data': [35], 'stack': '2025'},
    {'data': [25], 'stack': '2025'},
]
```

**Horizontal Layout:**
```python
BarChart(
    series=[{'data': revenue, 'label': 'Revenue'}],
    yAxis=[{'data': months, 'scaleType': 'band'}],  # Categories on Y
    xAxis=[{'label': 'Amount'}],                      # Values on X
    layout='horizontal',
    borderRadius=6,
)
```

**Reference Lines:**
```python
BarChart(
    referenceLines=[
        {'y': 60, 'label': 'Target', 'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '6 4'}},
        {'x': 'May', 'label': 'New Policy', 'lineStyle': {'stroke': '#9c27b0'}},
    ],
)
```

**Click Events:**
```python
# clickData output: {seriesId, dataIndex, timestamp}
# axisClickData output: {axisValue, dataIndex, seriesValues, timestamp}
@callback(
    Output('display', 'children'),
    Input('my-bar', 'clickData'),
)
def show_click(data):
    return json.dumps(data) if data else 'Click a bar...'
```

**Pro Features (require licenseKey):**
```python
BarChart(
    licenseKey=os.getenv('MUI_PRO_API_KEY'),
    series=[{'data': big_data, 'label': 'Sales'}],
    xAxis=[{'data': categories, 'scaleType': 'band', 'zoom': {'minSpan': 5}}],
    showSlider=True,
    showToolbar=True,
    initialZoom=[{'axisId': 'auto-generated-id-0', 'start': 0, 'end': 40}],
)
```

---

### 3. CandlestickChart

**File:** `src/lib/components/CandlestickChart.react.js`
**License:** Community (basic) / Pro (zoom/toolbar)

**Purpose:** Static OHLC candlestick charts for financial data. NOT the same as LiveTradingChart (which is a real-time client-side simulation).

**Architecture:** Uses MUI X Charts Pro composition API (`ChartDataProviderPro` + `ChartsSurface`) with custom SVG rendering for candle bodies and wicks. Does NOT require `@mui/x-charts-premium` — works with existing v8.24.0 stack. Internal components:
- `CandlePlot` — Renders candle bodies (rect) and wicks (line) using `useXScale`/`useYScale` hooks
- `VolumePlot` — Renders semi-transparent volume bars (optional)
- `CandleTooltip` — Custom OHLC hover tooltip with crosshair line
- Hidden bar series drives band scale + y-axis domain computation

**Data Formats:**

```python
# Array format — OHLC tuples
CandlestickChart(
    series=[{
        'data': [
            [100, 110, 95, 105],   # [open, high, low, close]
            [105, 115, 100, 112],
        ],
        'upColor': '#4caf50',       # Close >= Open
        'downColor': '#f44336',     # Close < Open
    }],
    xAxis=[{'data': ['Mon', 'Tue']}],
)

# Dataset format — row objects
CandlestickChart(
    dataset=[
        {'date': '2025-01-02', 'open': 100, 'high': 110, 'low': 95, 'close': 105, 'volume': 1200},
    ],
    series=[{
        'datasetKeys': {'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'},
        'volumeKey': 'volume',
        'upColor': '#4caf50',
        'downColor': '#f44336',
    }],
    xAxis=[{'dataKey': 'date'}],
)
```

**Volume Overlay:**
```python
CandlestickChart(
    showVolume=True,
    volumeHeightRatio=0.3,  # 30% of chart height
    series=[{..., 'volumeKey': 'volume'}],  # dataset mode
    # OR
    series=[{..., 'volume': [100, 200, 300]}],  # array mode
)
```

**Candle Styling:**
```python
CandlestickChart(
    bodyWidthRatio=0.8,  # Wider candles (default 0.6)
    wickWidth=3,          # Thicker wicks (default 2)
)
```

**Reference Lines (Support/Resistance):**
```python
CandlestickChart(
    referenceLines=[
        {'y': 110, 'label': 'Resistance', 'lineStyle': {'stroke': '#f44336', 'strokeDasharray': '6 4'}},
        {'y': 95, 'label': 'Support', 'lineStyle': {'stroke': '#4caf50', 'strokeDasharray': '6 4'}},
    ],
)
```

**Click Events:**
```python
# clickData output: {dataIndex, label, open, high, low, close, timestamp}
@callback(
    Output('display', 'children'),
    Input('my-candles', 'clickData'),
)
def show_click(data):
    return json.dumps(data) if data else 'Click a candle...'
```

---

### 4. PieChart

**File:** `src/lib/components/PieChart.react.js`
**License:** Community (Free)

**Purpose:** Pie, donut, and nested/concentric pie charts.

**Single Series (Simple Pie/Donut):**
```python
PieChart(
    data=[
        {'id': 'a', 'value': 35, 'label': 'Marketing', 'color': '#1976d2'},
        {'id': 'b', 'value': 25, 'label': 'Engineering'},
    ],
    innerRadius=50,   # >0 creates donut
    outerRadius=100,
    cornerRadius=5,
    paddingAngle=2,
)
```

**Multi-Series (Nested Pies):**
```python
PieChart(
    series=[
        {
            'data': inner_data,
            'innerRadius': 0,
            'outerRadius': 80,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
        {
            'data': outer_data,
            'innerRadius': 90,
            'outerRadius': 120,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
    ],
)
```

**Important:** MUI X Charts uses `seriesId` (string like "series-0") not `seriesIndex` in event callbacks. The React component converts this for Python.

**Half-Pie / Gauge:**
```python
PieChart(
    data=data,
    startAngle=-90,   # 12 o'clock position
    endAngle=90,      # Half circle
    innerRadius=50,
)
```

**Controlled Highlighting (for synchronization):**
```python
PieChart(
    id='my-pie',
    data=[
        {'id': 0, 'value': 35, 'label': 'A'},
        {'id': 1, 'value': 25, 'label': 'B'},
    ],
    highlightScope={'highlight': 'item', 'fade': 'global'},
    highlightedItem={'seriesId': 'auto-generated-id-0', 'dataIndex': 0},
)

# Sync with another chart
@callback(
    Output('my-pie', 'highlightedItem'),
    Input('line-chart', 'highlightedItem'),
)
def sync_pie_highlight(line_item):
    if line_item:
        # Map line series to pie index
        return {'seriesId': 'auto-generated-id-0', 'dataIndex': mapped_index}
    return None
```

---

### 5. ScatterChart

**File:** `src/lib/components/ScatterChart.react.js`
**License:** Community (Free)

**Purpose:** Scatter/point charts with optional z-axis color mapping, voronoi interaction, and dataset-driven data.

**Multi-Series Scatter:**
```python
ScatterChart(
    series=[
        {
            'id': 'group-a',
            'label': 'Group A',
            'data': [{'x': 1, 'y': 5, 'id': 0}, {'x': 2, 'y': 8, 'id': 1}],
            'color': '#1976d2',
            'markerSize': 6,
        },
        {
            'id': 'group-b',
            'label': 'Group B',
            'data': [{'x': 1.5, 'y': 3, 'id': 0}, {'x': 3, 'y': 7, 'id': 1}],
            'color': '#e53935',
        },
    ],
    voronoiMaxRadius=30,
    height=400,
)
```

**Z-Axis Color Mapping:**
```python
ScatterChart(
    series=[{
        'id': 'points',
        'data': [{'x': 1, 'y': 5, 'z': 100, 'id': 0}, ...],
    }],
    zAxis=[{
        'data': z_values,
        'colorMap': {
            'type': 'continuous',
            'min': 0, 'max': 100,
            'color': ['#e3f2fd', '#1565c0'],
        },
    }],
)
```

**Dataset-Driven:**
```python
ScatterChart(
    dataset=[{'temp': 20, 'humidity': 65}, ...],
    series=[{
        'id': 'weather',
        'datasetKeys': {'x': 'temp', 'y': 'humidity'},
    }],
)
```

**Click Events:**
```python
clickData = {
    'type': 'scatter',
    'seriesId': 'group-a',
    'dataIndex': 2,
    'x': 3.5,
    'y': 7.2,
    'timestamp': '2025-01-10T...'
}
```

---

### 6. CompositeChart

**File:** `src/lib/components/CompositeChart.react.js`
**License:** Community (basic) / Pro (zoom/pan)

**Purpose:** Layer multiple chart types (scatter + line) on a single surface using MUI X Charts composition API.

**Key Implementation Details:**
- Uses `ChartDataProviderPro` + `ChartsSurface` + individual plot components
- Custom tooltip system (`CompositeAxisTooltipContent`) that shows both line and scatter data
- Automatic epoch ms → Date conversion for `scaleType: 'time'` axes
- Proximity-based scatter tooltip matching (auto-computed from axis data spacing)

**Basic Scatter + Line Overlay:**
```python
CompositeChart(
    series=[
        {
            'type': 'scatter',
            'id': 'readings',
            'label': 'Sensor Readings',
            'data': [{'x': 0, 'y': 18.5, 'id': 0}, ...],
            'markerSize': 4,
        },
        {
            'type': 'line',
            'id': 'trend',
            'label': 'Trend Line',
            'data': [20.0, 22.1, ...],  # positional values
            'curve': 'natural',
            'showMark': False,
        },
    ],
    xAxis=[{'data': x_values, 'scaleType': 'linear'}],
)
```

**Zoom with Slider Preview (Pro):**
```python
CompositeChart(
    licenseKey=MUI_PRO_LICENSE,
    series=[
        {'type': 'line', 'id': 'baseline', 'data': values, 'area': True},
        {
            'type': 'scatter',
            'id': 'anomalies',
            'data': scatter_points,
            'markerSize': 6,
            'preview': {'markerSize': 2},  # Marker size in zoom slider preview
            'highlightScope': {'highlight': 'item'},
        },
    ],
    xAxis=[{
        'data': timestamps,
        'scaleType': 'time',  # Epoch ms auto-converted to Date objects
        'zoom': {
            'slider': {'enabled': True, 'preview': True},
        },
    }],
    initialZoom=[{'axisId': 'time-axis', 'start': 0, 'end': 30}],
)
```

**Multi-Axis:**
```python
CompositeChart(
    series=[
        {'type': 'scatter', 'yAxisId': 'left-axis', ...},
        {'type': 'line', 'yAxisId': 'right-axis', ...},
    ],
    yAxis=[
        {'id': 'left-axis', 'position': 'left'},
        {'id': 'right-axis', 'position': 'right'},
    ],
)
```

**Reference Lines:**
```python
CompositeChart(
    referenceLines=[
        {'y': 28, 'label': 'Upper Limit', 'lineStyle': {'stroke': 'red'}},
        {'y': 16, 'label': 'Lower Limit', 'lineStyle': {'stroke': 'red'}},
    ],
)
```

---

### 7. Heatmap

**File:** `src/lib/components/Heatmap.react.js`
**License:** Pro (Required)

**Purpose:** Matrix/grid visualization with color-coded cells.

**Data Format:**
```python
# Array of [x_index, y_index, value] tuples
data = [
    [0, 0, 10], [0, 1, 20], [0, 2, 30],
    [1, 0, 40], [1, 1, 50], [1, 2, 60],
]
```

**Color Scales:**
```python
# Continuous
colorScale = {
    'type': 'continuous',
    'min': 0,
    'max': 100,
    'colors': ['#e3f2fd', '#1976d2'],
}

# Piecewise
colorScale = {
    'type': 'piecewise',
    'thresholds': [25, 50, 75],
    'colors': ['#green', '#yellow', '#orange', '#red'],
}
```

---

### 8. SparklineChart

**File:** `src/lib/components/SparklineChart.react.js`
**License:** Community (Free)

**Purpose:** Compact inline charts (default 36px height) for dashboards and tables.

```python
SparklineChart(
    data=[1, 4, 2, 5, 7, 2, 4, 6],
    plotType='line',  # or 'bar'
    color='#1976d2',
    area=True,
    height=40,
    width=150,
)
```

**Controlled Highlight:**
```python
SparklineChart(
    data=data,
    highlightedIndex=selected_index,  # Sync with external component
)
```

---

### 9. LiveTradingChart

**File:** `src/lib/components/LiveTradingChart.react.js`
**License:** Community (basic) / Pro (zoom/slider)

**Purpose:** Real-time streaming chart for live data visualization (trading, sensor feeds, etc.).

---

### 10. SimpleTreeView

**File:** `src/lib/components/SimpleTreeView.react.js`
**License:** Community

**Purpose:** JSX-driven tree (no MUI store). Useful for navigation sidebars and small static trees. Items support an `icon` field resolved through `iconResolver.js`.

---

### 11. TreeView

**File:** `src/lib/components/TreeView.react.js`
**License:** Community

**Purpose:** Data-driven `RichTreeView` wrapper. Accepts a nested `items` array with `getItemId` / `getItemLabel` / `getItemChildren` string accessors. Supports controlled selection, expansion, in-place label editing, and per-item disabling.

---

### 12. TreeViewPro

**File:** `src/lib/components/TreeViewPro.react.js`
**License:** Pro (drag-and-drop reordering, lazy loading)

**Purpose:** Extends `TreeView` with MUI X Pro features and per-item UI controls. Designed for the "tree paired with a map / canvas" pattern where each leaf is a layer with a 0–100 value and a row-level actions menu.

**Pro features:**

```python
TreeViewPro(
    id="layers",
    items=LAYER_ITEMS,
    licenseKey=os.environ["MUI_PRO_API_KEY"],
    itemsReordering=True,            # drag-and-drop reorder
    reorderableItems=["task-1"],     # optional subset
    lazyLoading=True,                # fire `lazyLoadRequest` on expand
    lazyLoadedChildren={...},        # parentId -> [child items]
)
```

**Outputs from reorder / lazy:**
- `itemPositionChanged` — `{itemId, oldPosition, newPosition, event_timestamp}` per move.
- `orderedItems` — the full live tree after each reorder (computed via internal `applyReorder` walk). Lets Python render the current nested order without re-applying deltas. Falls back to `items` until the first reorder.
- `lazyLoadRequest` — `{itemId, event_timestamp}` when an unloaded node is expanded.

**Per-item Slider + Kebab controls** (`showItemControls=True`):

```python
TreeViewPro(
    showItemControls=True,
    controlsItems=LEAF_IDS,                  # optional subset (leaves only)
    sliderValues={"layer-a": 80, ...},       # bidirectional dict
    sliderMin=0, sliderMax=100, sliderStep=1,
    sliderColor="teal",                       # see resolver below
    kebabMenuItems=[
        {"label": "Duplicate", "value": "duplicate", "icon": "ContentCopy"},
        {"label": "Delete",    "value": "delete",    "icon": "Delete"},
    ],
)
```

**Slider color resolver:**
- Mantine palette names — `"teal"` → `var(--mantine-color-teal-6)`, `"blue.5"` → `var(--mantine-color-blue-5)` (bare names use shade 6).
- CSS literals — `"#ff6b6b"`, `"rgb(255,100,50)"`, `"oklch(...)"`.
- CSS expressions — `"var(--mantine-color-...)"`, `"light-dark(white, black)"`.
- Applied via `sx` to the slider track, thumb, hover ring, value label and rail.

**Per-item outputs:**
- `sliderChange` — `{itemId, value, event_timestamp}` on slider commit (mouse-up / touch-end). For live mid-drag readouts, observe `sliderValues` directly — it updates on every change.
- `kebabAction` — `{itemId, action, event_timestamp}` when a menu item is selected; `action` is the `value` field of the chosen menu entry.

**Implementation notes:**
- `useMantineColorScheme` watches `<html data-mantine-color-scheme>` via a `MutationObserver` and re-skins MUI components through an `MUI ThemeProvider` (Checkbox, Slider, IconButton, Menu paper, MenuItems) when the Mantine theme toggles.
- `ItemLabelWithControls` holds a **local React state** for each slider during drag so the thumb tracks instantly even when Dash callback round-trips are slow. `useEffect` re-syncs from props when no drag is in flight.
- `dragstart` is `preventDefault`-cancelled on the slider + kebab area to keep `itemsReordering`'s HTML5 native drag from swallowing desktop mouse drags. Passive pointer/touch events use `stopPropagation` only.
- Demo page: `/tree-pro` (see `pages/tree_pro.py`). `slugify_label` + `assign_ids` derive stable IDs from labels at startup; duplicates get `-1`, `-2`, … suffixes.

**Known upstream warnings (benign):**
- `Each child in a list should have a unique "key" prop` from `ButtonBase`/`SwitchBase`/`Checkbox` (triggered by `checkboxSelection=True`) and from `FocusTrap` inside an open `Menu`. Both originate in MUI v6 internals — not our code. They clear on upgrade to MUI v7.

---

### 13. TimeClock

**File:** `src/lib/components/TimeClock.react.js`
**License:** Community (Free)
**Package:** `@mui/x-date-pickers` (8.24.0) + `dayjs` adapter — the first **Date & Time Pickers** component, NOT a chart.

**Purpose:** Inline clock-face time selector (no input / popper / modal). The user drags the hand or clicks the numbers to pick hours, minutes, and optionally seconds.

**String ↔ dayjs boundary:** dayjs objects can't cross the Dash boundary, so values are exchanged as strings — full wall-time ISO (`"2022-04-17T15:30:00"`) or time-only (`"15:30"` / `"15:30:45"`). `parseToDayjs()` maps strings → dayjs on the way in; `newVal.format('YYYY-MM-DDTHH:mm:ss')` maps dayjs → string on the way out (local wall-time, NOT `toISOString()`, to avoid a UTC shift).

```python
from dash_mui_charts import TimeClock

TimeClock(
    id="clock",
    value="15:30:00",                       # controlled, in/out (wall-time ISO out)
    defaultValue="15:30:00",                # uncontrolled initial (use instead of value)
    views=["hours", "minutes", "seconds"],  # default ["hours", "minutes"]
    view="hours",                           # controlled view, in/out
    ampm=False,                             # force 12h/24h (omit = locale default)
    minutesStep=5,
    minTime="09:00", maxTime="18:00",
    disabled=False, readOnly=False,
    showViewSwitcher=True,
)

# Outputs: value (wall-time ISO), view, and timeData:
#   {"hours", "minutes", "seconds", "formatted" ("HH:mm:ss"), "event_timestamp"}
@callback(Output("out", "children"), Input("clock", "timeData"))
def show(td):
    return td["formatted"] if td else "—"
```

**Function-only MUI props omitted** (not serializable): `shouldDisableTime`, `referenceDate`, `slots`/`slotProps`. `skipDisabled` is intentionally NOT exposed — it belongs to the *digital* clock variants, not the analog `TimeClock`, and leaks onto the DOM if forwarded.

**Recolouring via `sx`** — internal MUI class names (verified from source): face `.MuiClock-clock`, hand `.MuiClockPointer-root` + `.MuiClockPointer-thumb` (set `backgroundColor` + `borderColor`) + centre `.MuiClock-pin`, digits `.MuiClockNumber-root` / `-selected`, meridiem `.MuiClock-amButton` / `-pmButton`. See `assets/liquid_glass_clock.css` and `/time-clock-lab` for a glassmorphic theme with a magnifying-lens thumb.

**Demo pages:** `/time-clock` (basic) and `/time-clock-lab` (dynamic colours, liquid glass, stopwatch, and two-way pairings with `dmc.TimeInput` / `TimePicker` / `TimeGrid` / `DateTimePicker`).

---

## Development Workflow

### Building Components

```bash
# Full build (JS + Python generation)
npm run build

# Build only JS
npm run build:js

# Generate Python wrappers only
npm run build:backends

# Watch mode during development
npm run start
```

### Running the App

```bash
# Set MUI Pro license key (optional, for Pro features)
export MUI_PRO_API_KEY="your-license-key"

# Run development server
python app.py
```

### Pages

| Path | Description |
|------|-------------|
| `/` | Home page with overview |
| `/linechart-basic` | Basic LineChart features |
| `/linechart-pro` | Pro features (zoom, pan, slider) |
| `/linechart-brush` | Brush selection with value overlays (Pro) |
| `/linechart-referencelines` | Reference lines (horizontal/vertical) |
| `/linechart-highlighting` | Controlled item/axis highlights, per-series highlightScope |
| `/linechart-tick-hover` | Tick config, date formatting, zoom best practices |
| `/linechart-zoom-preview` | Biaxial chart with zoom slider preview |
| `/highlighting-sync` | Synchronized highlights across charts |
| `/live-trading` | LiveTradingChart streaming demo |
| `/pie` | Pie chart examples |
| `/pie-props` | Nested pie property explorer |
| `/scatter` | ScatterChart examples (multi-series, z-axis, voronoi, dataset) |
| `/composite` | CompositeChart examples (scatter+line, zoom, reference lines) |
| `/heatmap` | Heatmap examples |
| `/heatmap-props` | Heatmap property explorer |
| `/sparkline` | Sparkline examples |
| `/sparkline-style` | Sparkline styling playground |
| `/tree-basic` … `/tree-pro` | TreeView / TreeViewPro examples (selection, editing, drag-reorder, per-item controls) |
| `/time-clock` | TimeClock basics (views, controlled, 12h/24h, form props) |
| `/time-clock-lab` | TimeClock × DMC: dynamic colours, liquid glass, stopwatch, two-way pairings |

---

## Common Patterns

### Adding a New Component

1. Create React component: `src/lib/components/NewChart.react.js`
2. Export in `src/lib/index.js`
3. Define PropTypes with JSDoc comments
4. Run `npm run build`
5. Python wrapper auto-generated in `dash_mui_charts/`

### Event Handling Pattern

```javascript
// React component
const handleClick = (event, params) => {
    if (setProps) {
        setProps({
            clickData: {
                ...params,
                timestamp: new Date().toISOString(),
            },
            n_clicks: (n_clicks || 0) + 1,
        });
    }
};
```

```python
# Python callback
@callback(
    Output('output', 'children'),
    Input('chart', 'clickData'),
)
def handle_click(click_data):
    if click_data:
        return f"Clicked: {click_data['value']}"
    return "Click on chart"
```

### Functions-as-Props (Bridging Python ↔ JavaScript Functions)

Dash serializes props as JSON, so JavaScript functions can't be passed from Python. Two approaches are supported:

**Approach 1: Built-in `dateFormat` (recommended for dates)**
```python
# No JavaScript needed — the React component creates the formatter internally
xAxis=[{
    'scaleType': 'time',
    'dateFormat': 'MMM d, YYYY',     # Tooltip format
    'dateTickFormat': 'M/d',          # Tick label format
}]
```

**Approach 2: DMC-style function reference (advanced)**
```python
# Python: reference a function by name
xAxis=[{
    'valueFormatter': {'function': 'myFormatter', 'options': {'unit': 'F'}},
}]
```
```javascript
// assets/myFunctions.js: define the function
var dmcf = window.dashMuiChartsFunctions = window.dashMuiChartsFunctions || {};
dmcf.myFormatter = function(value, context, options) {
    return value + ' °' + options.unit;
};
```

**Architecture:** In `processedXAxis` (useMemo), the component:
1. Checks for `dateFormat` → creates a `valueFormatter` via `createDateFormatter()`
2. Else checks for `valueFormatter` object → resolves via `resolveFunctionProp()`
3. Strips non-MUI props (`dateFormat`, `dateTickFormat`) before passing to `ChartDataProviderPro`

### Controlled vs Uncontrolled Props

```python
# Uncontrolled (internal state)
LineChart(initialZoom=[{'axisId': 'x', 'start': 0, 'end': 50}])

# Controlled (external state via callback)
LineChart(zoom=current_zoom_state)

@callback(
    Output('chart', 'zoom'),
    Input('chart', 'zoomData'),
)
def sync_zoom(zoom_data):
    return zoom_data
```

---

## Callback Patterns

### Reading Chart State

```python
@callback(
    Output('output', 'children'),
    Input('chart', 'zoomData'),    # Fires on zoom change
    Input('chart', 'clickData'),   # Fires on click
    Input('chart', 'n_clicks'),    # Click counter
)
def handle_chart_events(zoom, click, n):
    ...
```

### Controlling Chart State

```python
@callback(
    Output('chart', 'zoom'),       # Set zoom programmatically
    Input('reset-btn', 'n_clicks'),
)
def reset_zoom(n):
    return [{'axisId': 'x-axis', 'start': 0, 'end': 100}]
```

### Synchronized Highlighting Across Charts

```python
# Sync highlights between LineChart and PieChart
@callback(
    Output('line-chart', 'highlightedItem'),
    Output('pie-chart', 'highlightedItem'),
    Input('line-chart', 'highlightedItem'),
    Input('pie-chart', 'highlightedItem'),
    prevent_initial_call=True
)
def sync_highlights(line_item, pie_item):
    triggered = ctx.triggered_id

    if triggered == 'line-chart' and line_item:
        # Map line series to pie index
        pie_index = SERIES_TO_INDEX.get(line_item['seriesId'])
        if pie_index is not None:
            # Use no_update for source to avoid echo
            return dash.no_update, {'seriesId': 'auto-generated-id-0', 'dataIndex': pie_index}

    elif triggered == 'pie-chart' and pie_item:
        # Map pie index to line series
        series_id = INDEX_TO_SERIES.get(pie_item['dataIndex'])
        if series_id:
            return {'seriesId': series_id}, dash.no_update

    return dash.no_update, dash.no_update
```

**Key Pattern:** Use `dash.no_update` for the source chart to prevent callback loops.

---

## Debugging Tips

### Component Not Rendering

1. Check browser console for React errors
2. Verify `npm run build` completed successfully
3. Check `dash_mui_charts/*.min.js` exists and is recent
4. Clear browser cache / hard refresh

### Click Events Not Firing

1. Verify component has `id` prop set
2. Check callback input matches component ID
3. Look for `setProps` calls in React component
4. **Important:** MUI X Charts uses `seriesId` not `seriesIndex`

### Pro Features Not Working

1. Verify license key is valid
2. Pass `licenseKey` prop to component
3. Check console for MUI license warnings
4. Heatmap requires Pro license for all features

### X-Axis Labels Not Showing or Truncated

1. **Labels completely invisible on time scale with angle**: `tickLabelStyle.angle` on `scaleType: 'point'` triggers MUI collision detection — use `scaleType: 'time'` instead
2. **Labels truncated (shows "J..." or "1...")**: Too many ticks — increase `tickMinStep` and add `tickNumber: 6`
3. **MUI clips labels by available horizontal space per tick**: ~100px+ per tick needed for "1/15" at 12px font
4. **`axisHighlight: 'band'` breaks time scale**: Use `'line'` instead — band is for categorical axes only
5. **`dateFormat` not applied**: Verify `processedXAxis` runs (check that the early `if (!showSlider) return xAxis` shortcut was removed in v1.1.0)
6. **Angled labels need extra space**: Set `height: 80` on xAxis + `margin.bottom: 100`

### Python Import Errors

1. Run `npm run build` to regenerate Python wrappers
2. Check `dash_mui_charts/_imports_.py` includes component
3. Verify `__init__.py` has correct imports

### Duplicate Callback Outputs

When using multi-page apps, ensure component IDs are unique across pages. Prefix IDs with page name:
```python
# In pie_props.py
dmc.Slider(id='pie-ctrl-width', ...)

# In heatmap_props.py
dmc.Slider(id='heatmap-ctrl-width', ...)
```

---

## Dependencies

### NPM (package.json)

| Package | Version | Purpose |
|---------|---------|---------|
| @mui/x-charts | 8.24.0 | Community charts |
| @mui/x-charts-pro | 8.24.0 | Pro charts |
| @mui/x-tree-view(-pro) | 8.27.2 | TreeView / TreeViewPro |
| @mui/x-date-pickers | 8.24.0 (pinned) | TimeClock (Date & Time Pickers) |
| dayjs | 1.11.13 | Date adapter for the pickers |
| @mui/x-license | 7.24.0 | License management |
| @mui/material | 6.5.0 | Material UI base |
| react | 18.2.0 | React library |
| webpack | 5.x | Build bundler |

### Python (setup.py)

| Package | Version | Purpose |
|---------|---------|---------|
| dash | >= 3.0.0 | Dash framework |
| python-dotenv | >= 1.0.0 | Environment variables |

---

## Environment Variables

```bash
# MUI X Pro license key (optional)
MUI_PRO_API_KEY=your-key-here
```

---

## Build Outputs

After `npm run build`:

| File | Description |
|------|-------------|
| `dash_mui_charts/dash_mui_charts.min.js` | Bundled component JS (~603KB) |
| `dash_mui_charts/dash_mui_charts.min.js.map` | Source map |
| `dash_mui_charts/*.py` | Generated Python wrappers |
| `dash_mui_charts/metadata.json` | Component metadata |

---

## License Requirements Summary

| Component | Community (Free) | Pro Required |
|-----------|------------------|--------------|
| LineChart | Basic features, Reference Lines, dateFormat | Zoom, Pan, Brush |
| BarChart | Bars, stacking, labels, dataset mode, reference lines | Zoom, Brush, Toolbar |
| CandlestickChart | OHLC candles, volume, reference lines, tooltips | Zoom, Toolbar |
| PieChart | All features | - |
| ScatterChart | All features | - |
| CompositeChart | Basic layering, Reference Lines, dateFormat | Zoom, Pan, Toolbar |
| LiveTradingChart | Basic streaming | Zoom, Slider |
| Heatmap | - | All features |
| SparklineChart | All features | - |
| TimeClock | All features | - |

---

## Testing

```bash
# Validate Python syntax
python -m py_compile dash_mui_charts/*.py

# Run demo app
python app.py

# Run standalone example
python usage.py
```

---

## Future Enhancements

Potential components from MUI X Charts:
- GaugeChart (Pro)
- TreemapChart (Pro)
- RadarChart
- RangeBarChart (Premium — requires `@mui/x-charts-premium` and `@mui/material` v7+)
- Native CandlestickChart (Premium — available in `@mui/x-charts-premium` v9+, requires `@mui/material` v7+)

Potential features:
- Extend `resolveFunctionProp` to support more axis props (e.g. `tickInterval`, `tickLabelInterval` as function references)
- Support `valueFormatter` on series (not just axes) for custom tooltip value formatting
- Support `valueFormatter` on yAxis (currently `processedXAxis` handles it, need matching `processedYAxis`)
- BarChart: `barLabelFormat` string prop (like `dateFormat` on LineChart) for custom label formatting without JS
- CandlestickChart: moving average line overlay, Bollinger bands, RSI sub-chart

Follow existing component patterns for implementation.