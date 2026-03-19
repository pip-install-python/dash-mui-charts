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
│   ├── ScatterChart.react.js       # Scatter/point charts
│   ├── CompositeChart.react.js     # Layered scatter + line charts
│   ├── Heatmap.react.js            # Heatmap with Pro features
│   └── SparklineChart.react.js     # Compact inline sparklines
├── dash_mui_charts/                 # Python package (auto-generated)
│   ├── __init__.py                 # Package initialization
│   ├── LineChart.py                # Python wrapper for LineChart
│   ├── PieChart.py                 # Python wrapper for PieChart
│   ├── ScatterChart.py             # Python wrapper for ScatterChart
│   ├── CompositeChart.py           # Python wrapper for CompositeChart
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
│   ├── scatter.py                  # Scatter chart examples
│   ├── composite.py                # Composite chart examples
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

## Components (6 Total)

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

### 3. ScatterChart

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

### 4. CompositeChart

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

### 5. Heatmap (unchanged)

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

### 6. SparklineChart

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
| `/linechart-highlighting` | Controlled item/axis highlights, per-series highlightScope |
| `/linechart-zoom-preview` | Biaxial chart with zoom slider preview |
| `/highlighting-sync` | Synchronized highlights across charts |
| `/pie` | Pie chart examples |
| `/pie-props` | Nested pie property explorer |
| `/scatter` | ScatterChart examples (multi-series, z-axis, voronoi, dataset) |
| `/composite` | CompositeChart examples (scatter+line, zoom, reference lines) |
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
| `dash_mui_charts/dash_mui_charts.min.js` | Bundled component JS (~603KB) |
| `dash_mui_charts/dash_mui_charts.min.js.map` | Source map |
| `dash_mui_charts/*.py` | Generated Python wrappers |
| `dash_mui_charts/metadata.json` | Component metadata |

---

## License Requirements Summary

| Component | Community (Free) | Pro Required |
|-----------|------------------|--------------|
| LineChart | Basic features, Reference Lines | Zoom, Pan, Brush |
| PieChart | All features | - |
| ScatterChart | All features | - |
| CompositeChart | Basic layering, Reference Lines | Zoom, Pan, Toolbar |
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
- GaugeChart (Pro)
- TreemapChart (Pro)
- RadarChart

Follow existing component patterns for implementation.