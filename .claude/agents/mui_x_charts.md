# MUI X Charts Agent

Reference guide for MUI X Charts library, including composition API and Pro features.

## Chart Types

- **LineChart** - Line and area charts
- **BarChart** - Vertical and horizontal bar charts
- **PieChart** - Pie and donut charts
- **ScatterChart** - Scatter plots
- **Sparkline** - Compact inline charts
- **Gauge** - Progress gauges
- **Heatmap** (Pro) - Heat map visualization

## Two API Approaches

### 1. Single Component API (Simple)

```javascript
import { LineChart } from '@mui/x-charts/LineChart';

<LineChart
    series={[{ data: [1, 2, 3, 4] }]}
    xAxis={[{ data: ['A', 'B', 'C', 'D'], scaleType: 'band' }]}
    height={300}
/>
```

### 2. Composition API (Flexible)

```javascript
import { ChartDataProvider } from '@mui/x-charts/ChartDataProvider';
import { ChartsSurface } from '@mui/x-charts/ChartsSurface';
import { LinePlot } from '@mui/x-charts/LineChart';
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts/ChartsYAxis';

<ChartDataProvider
    series={[{ type: 'line', data: [1, 2, 3, 4] }]}
    xAxis={[{ data: ['A', 'B', 'C', 'D'], scaleType: 'band' }]}
    height={300}
>
    <ChartsSurface>
        <LinePlot />
        <ChartsXAxis />
        <ChartsYAxis />
    </ChartsSurface>
</ChartDataProvider>
```

## Pro Composition API

For Pro features like zoom, use Pro-specific providers:

```javascript
import { ChartDataProviderPro } from '@mui/x-charts-pro/ChartDataProviderPro';
import { ChartsSurface } from '@mui/x-charts-pro/ChartsSurface';
import { LinePlot } from '@mui/x-charts-pro/LineChart';
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';
import { ChartsClipPath } from '@mui/x-charts-pro/ChartsClipPath';
```

## Series Configuration

### Line Series

```javascript
{
    id: 'series-1',        // Unique identifier
    type: 'line',          // Required for composition API
    data: [1, 2, 3, 4],    // Y values
    label: 'Revenue',      // Legend label
    color: '#1976d2',      // Line color
    area: true,            // Fill area under line
    stack: 'total',        // Stack identifier
    curve: 'monotoneX',    // Interpolation method
    showMark: true,        // Show data point markers
    connectNulls: false,   // Bridge null values
    yAxisId: 'left',       // Which Y-axis to use
    xAxisId: 'bottom',     // Which X-axis to use
}
```

### Curve Types

- `linear` - Straight lines between points
- `monotoneX` - Smooth curves preserving monotonicity in X
- `monotoneY` - Smooth curves preserving monotonicity in Y
- `natural` - Natural cubic spline
- `step` - Step at midpoint
- `stepBefore` - Step before point
- `stepAfter` - Step after point
- `catmullRom` - Catmull-Rom spline
- `bumpX` / `bumpY` - Bump curves

## Axis Configuration

### X-Axis

```javascript
xAxis: [{
    id: 'x-axis',              // Identifier for zoom/series reference
    data: [2020, 2021, 2022],  // Axis values
    label: 'Year',             // Axis label
    scaleType: 'point',        // Scale type
    position: 'bottom',        // 'top' or 'bottom'
    tickLabelStyle: { ... },   // Style for tick labels
    zoom: { ... },             // Pro: zoom configuration
}]
```

### Y-Axis

```javascript
yAxis: [{
    id: 'left-axis',
    label: 'Value',
    min: 0,                    // Fixed minimum
    max: 100,                  // Fixed maximum
    position: 'left',          // 'left' or 'right'
    width: 60,                 // Space allocated for axis
}]
```

### Scale Types

- `band` - Categorical with bands (for bar charts)
- `point` - Categorical discrete points
- `linear` - Continuous numeric
- `log` - Logarithmic
- `time` - Time/date values

## Zoom Configuration (Pro)

### Enable Zoom on Axis

```javascript
xAxis: [{
    id: 'x-axis',
    data: years,
    scaleType: 'point',
    zoom: {
        minSpan: 5,        // Minimum visible data points
        maxSpan: 100,      // Maximum span (100 = full range)
        panning: true,     // Enable drag panning
        minStart: 0,       // Minimum start position (0-100)
        maxEnd: 100,       // Maximum end position (0-100)
        step: 1,           // Zoom granularity
        slider: {
            enabled: true  // Show zoom slider
        }
    }
}]
```

### Zoom State Format

```javascript
// Zoom state is array of axis zoom states
[
    {
        axisId: 'x-axis',
        start: 0,      // Start percentage (0-100)
        end: 50        // End percentage (0-100)
    }
]
```

### Controlled Zoom Pattern

```javascript
const [zoom, setZoom] = useState([
    { axisId: 'x-axis', start: 0, end: 100 }
]);

<ChartDataProviderPro
    zoom={zoom}
    onZoomChange={setZoom}
    ...
>
```

### Initial Zoom (Uncontrolled)

```javascript
<ChartDataProviderPro
    initialZoom={[{ axisId: 'x-axis', start: 0, end: 50 }]}
    ...
>
```

## Zoom Slider Component

The zoom slider provides visual zoom control:

```javascript
import { ChartZoomSlider } from '@mui/x-charts-pro/ChartZoomSlider';

<ChartDataProviderPro ...>
    <ChartsSurface>
        {/* Chart content */}
        <ChartZoomSlider />
    </ChartsSurface>
</ChartDataProviderPro>
```

Enable slider via axis config:

```javascript
xAxis: [{
    zoom: {
        slider: { enabled: true }
    }
}]
```

## Clip Path for Zoomed Content

Prevent content from rendering outside chart area:

```javascript
import { ChartsClipPath } from '@mui/x-charts/ChartsClipPath';

const clipPathId = useId();

<ChartsSurface>
    <ChartsClipPath id={clipPathId} />
    <g clipPath={`url(#${clipPathId})`}>
        <LinePlot />
        <AreaPlot />
    </g>
    <ChartsXAxis />
</ChartsSurface>
```

## Composition Components

### Data Providers
- `ChartDataProvider` - Community, basic charts
- `ChartDataProviderPro` - Pro features (zoom, heatmap)

### Surface
- `ChartsSurface` - SVG container for chart elements

### Plot Components
- `LinePlot` - Line paths
- `AreaPlot` - Filled areas
- `MarkPlot` - Data point markers
- `BarPlot` - Bar elements
- `ScatterPlot` - Scatter points

### Axis Components
- `ChartsXAxis` - X-axis with ticks and labels
- `ChartsYAxis` - Y-axis with ticks and labels
- `ChartsGrid` - Grid lines

### Interactive Components
- `ChartsTooltip` - Hover tooltips
- `ChartsAxisHighlight` - Highlight line on hover
- `ChartsLegend` - Chart legend
- `ChartZoomSlider` - Zoom slider (Pro)

## Event Handling

### Click Events

```javascript
// Line click
<LinePlot onItemClick={(event, params) => {
    console.log('Clicked series:', params.seriesId);
}} />

// Mark (point) click
<MarkPlot onItemClick={(event, params) => {
    console.log('Clicked point:', params.dataIndex);
}} />

// Area click
<AreaPlot onItemClick={(event, params) => {
    console.log('Clicked area:', params.seriesId);
}} />
```

### Axis Click

```javascript
<ChartsAxisHighlight
    x="line"
    onAxisClick={(event, params) => {
        console.log('Axis value:', params.axisValue);
        console.log('Data index:', params.dataIndex);
    }}
/>
```

## Tooltip Configuration

```javascript
// Trigger modes
<ChartsTooltip trigger="axis" />   // Show on axis hover
<ChartsTooltip trigger="item" />   // Show on item hover
<ChartsTooltip trigger="none" />   // Disable tooltip

// Custom tooltip content
<ChartsTooltip
    content={({ series, dataIndex }) => (
        <div>Custom tooltip content</div>
    )}
/>
```

## Grid Configuration

```javascript
<ChartsGrid
    horizontal={true}   // Horizontal grid lines
    vertical={false}    // Vertical grid lines
/>
```

## Margin Configuration

```javascript
margin: {
    top: 20,
    right: 20,
    bottom: 30,
    left: 40
}
```

## Multiple Y-Axes (Biaxial Charts)

```javascript
series: [
    { data: [1, 2, 3], yAxisId: 'left', label: 'Series A' },
    { data: [100, 200, 300], yAxisId: 'right', label: 'Series B' }
],
yAxis: [
    { id: 'left', position: 'left', label: 'Left Axis' },
    { id: 'right', position: 'right', label: 'Right Axis' }
]
```

## Stacked Areas

```javascript
series: [
    { data: [1, 2, 3], area: true, stack: 'total', label: 'A' },
    { data: [2, 3, 4], area: true, stack: 'total', label: 'B' },
    { data: [1, 1, 1], area: true, stack: 'total', label: 'C' }
]
```

## Animation Control

```javascript
<LinePlot skipAnimation={false} />  // Enable animations
<LinePlot skipAnimation={true} />   // Disable animations

// Or on provider
<ChartDataProviderPro skipAnimation={true} ... />
```

## Common Issues and Solutions

### Zoom not responding to prop changes

Ensure you're using controlled mode correctly:

```javascript
const [zoom, setZoom] = useState([...]);

// Sync external prop changes
useEffect(() => {
    if (externalZoom) {
        setZoom(externalZoom);
    }
}, [externalZoom]);

// Handle internal changes
const handleZoomChange = (newZoom) => {
    const resolved = typeof newZoom === 'function'
        ? newZoom(zoom)
        : newZoom;
    setZoom(resolved);
};
```

### Chart not rendering

Check that:
1. Series has `type: 'line'` for composition API
2. `height` is set on provider
3. Axis data length matches series data length

### Tooltip not showing

Ensure `ChartsTooltip` is inside the provider but outside `ChartsSurface`:

```javascript
<ChartDataProviderPro>
    <ChartsSurface>
        <LinePlot />
    </ChartsSurface>
    <ChartsTooltip trigger="axis" />  {/* Outside surface */}
</ChartDataProviderPro>
```

## Resources

- [MUI X Charts Overview](https://mui.com/x/react-charts/)
- [Line Chart API](https://mui.com/x/api/charts/line-chart/)
- [Charts Pro Features](https://mui.com/x/react-charts/zoom-and-pan/)
- [Composition API Guide](https://mui.com/x/react-charts/composition/)