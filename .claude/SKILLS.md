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
│   ├── PieChart.react.js           # Pie/Donut/Nested pie charts
│   ├── Heatmap.react.js            # Heatmap with Pro features
│   └── SparklineChart.react.js     # Compact inline sparklines
├── dash_mui_charts/                 # Python package (auto-generated)
│   ├── __init__.py                 # Package initialization
│   ├── LineChart.py                # Python wrapper for LineChart
│   ├── PieChart.py                 # Python wrapper for PieChart
│   ├── Heatmap.py                  # Python wrapper for Heatmap
│   ├── SparklineChart.py           # Python wrapper for SparklineChart
│   ├── _imports_.py                # Auto-generated imports
│   └── dash_mui_charts.min.js      # Bundled JavaScript
├── pages/                           # Demo pages
│   ├── home.py                     # Landing page
│   ├── linechart_basic.py          # Basic line chart examples
│   ├── linechart_pro.py            # Pro features (zoom, pan)
│   ├── linechart_brush.py          # Brush selection (Pro)
│   ├── linechart_referencelines.py # Reference lines
│   ├── pie.py                      # Pie chart examples
│   ├── pie_props.py                # Nested pie property explorer
│   ├── heatmap.py                  # Heatmap examples
│   ├── heatmap_props.py            # Heatmap property explorer
│   ├── sparkline.py                # Sparkline examples
│   └── sparkline_style.py          # Sparkline styling
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

## Components (4 Total)

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

---

### 2. PieChart

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

---

### 3. Heatmap

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

### 4. SparklineChart

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
| `/pie` | Pie chart examples |
| `/pie-props` | Nested pie property explorer |
| `/heatmap` | Heatmap examples |
| `/heatmap-props` | Heatmap property explorer |
| `/sparkline` | Sparkline examples |
| `/sparkline-style` | Sparkline styling playground |

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
| `dash_mui_charts/dash_mui_charts.min.js` | Bundled component JS (~580KB) |
| `dash_mui_charts/dash_mui_charts.min.js.map` | Source map |
| `dash_mui_charts/*.py` | Generated Python wrappers |
| `dash_mui_charts/metadata.json` | Component metadata |

---

## License Requirements Summary

| Component | Community (Free) | Pro Required |
|-----------|------------------|--------------|
| LineChart | Basic features, Reference Lines | Zoom, Pan, Brush |
| PieChart | All features | - |
| Heatmap | - | All features |
| SparklineChart | All features | - |

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
- BarChart
- ScatterChart
- GaugeChart (Pro)
- TreemapChart (Pro)
- RadarChart

Follow existing component patterns for implementation.