# Claude Code Project Guide - dash_mui_charts

## Project Overview

**dash_mui_charts** is a Dash component library that wraps [MUI X Charts](https://mui.com/x/react-charts/) for use in Plotly Dash applications. It provides 9 chart components with full Python type hints and interactive callbacks.

---

## Components

| Component | Purpose | License |
|-----------|---------|---------|
| **LineChart** | Line/area charts, biaxial, zoom/pan, brush, reference lines | Community / Pro |
| **BarChart** | Vertical/horizontal bars, stacking, labels, dataset mode, zoom/brush | Community / Pro |
| **CandlestickChart** | OHLC candlestick charts with volume overlay, reference lines | Community / Pro |
| **PieChart** | Pie, donut, nested pies | Community |
| **ScatterChart** | Scatter/point charts, z-axis color mapping, voronoi interaction | Community |
| **CompositeChart** | Layer scatter + line plots on a single surface | Community / Pro |
| **Heatmap** | Matrix/grid visualization | Pro |
| **SparklineChart** | Compact inline charts | Community |
| **LiveTradingChart** | Real-time streaming charts | Community / Pro |

### BarChart Features (v1.2.0)
- **Vertical & Horizontal**: `layout='vertical'` (default) or `layout='horizontal'`
- **Stacking**: `stack` group ID, `stackOffset` ('none', 'expand', 'diverging'), `stackOrder`
- **Bar Labels**: `barLabel='value'` with `barLabelPlacement` ('center', 'outside')
- **Border Radius**: `borderRadius` prop for rounded bar corners
- **Dataset Mode**: `dataset` + `dataKey` pattern for table-format data
- **Bar Spacing**: `categoryGapRatio` (0-1) and `barGapRatio` (-1 to Inf) on band axis
- **Reference Lines**: Horizontal and vertical markers (same API as LineChart)
- **Axis Highlight**: `axisHighlight` with 'band', 'line', or 'none'
- **Tooltip Modes**: `tooltip={'trigger': 'axis'}` or `{'trigger': 'item'}`
- **Highlighting**: Controlled `highlightedItem` prop, per-series `highlightScope`
- **Click Events**: `clickData` (bar click) and `axisClickData` (axis area click)
- **Custom Colors**: `colors` palette prop, `renderer='svg-batch'` for performance
- **Pro Features** (require `licenseKey`): `initialZoom`, `showSlider`, `showToolbar`, `brushConfig`, `zoomData` output
- **Architecture**: Uses `BarChart` from `@mui/x-charts` and `BarChartPro` from `@mui/x-charts-pro` — auto-switches based on Pro feature usage

### CandlestickChart Features (v1.2.0)
- **Custom OHLC Rendering**: Built on MUI X Charts Pro composition API with custom SVG candles
- **Array Format**: `series=[{data: [[open,high,low,close], ...], upColor, downColor}]`
- **Dataset Format**: `dataset` + `series=[{datasetKeys: {open, high, low, close}}]`
- **Volume Overlay**: `showVolume=True` with `volumeKey` (dataset) or `volume` array (series)
- **Candle Styling**: `bodyWidthRatio` (0-1, default 0.6), `wickWidth` (px, default 2)
- **OHLC Tooltip**: Built-in hover tooltip showing O/H/L/C values with vertical crosshair
- **Reference Lines**: Support/resistance levels, moving average markers
- **Click Events**: `clickData` with full OHLC values
- **Auto Y-Domain**: Computes min/max from data with 5% padding
- **Architecture**: Uses `ChartDataProviderPro` + custom `CandlePlot` SVG component (no `@mui/x-charts-premium` needed)
- **Pro Features**: Zoom, slider, toolbar via composition API

### LineChart & CompositeChart Features (v1.1.0)
- **Built-in Date Formatting**: `dateFormat` / `dateTickFormat` props on xAxis/yAxis for time-scale axes
  - `dateFormat='M/d HH:mm'` for tooltip labels, `dateTickFormat='M/d'` for compact tick labels
  - Tokens: `YYYY`, `MMM`, `MM`, `M`, `dd`, `d`, `HH`, `mm`
- **Functions-as-Props**: `valueFormatter` on xAxis/yAxis accepts DMC-style `{'function': 'name', 'options': {...}}`
  - Resolves from `window.dashMuiChartsFunctions` registry (users define in `assets/*.js`)
  - Mirrors Dash Mantine Components pattern for JS function serialization
- **Axis Processing**: `processedXAxis` always runs (no longer skips when `showSlider=false`)

### LineChart Features (v0.0.7)
- **Reference Lines**: Horizontal (`y`) and vertical (`x`) markers for targets, thresholds, dates
- **Brush Selection** (Pro): Range selection with `'default'` or `'values'` overlay
- **Axis Highlight**: Configurable hover highlighting (`'none'`, `'line'`, `'band'`)
- **Controlled Axis Highlight**: `highlightedAxis` prop for programmatic control of axis highlights
- **Controlled Item Highlight**: `highlightedItem` prop for programmatic control of data point highlights
- **Per-Series highlightScope**: Configure highlight/fade behavior per series
- **Toolbar** (Pro): `showToolbar=True` for zoom/export controls
- **Synchronized Tooltips**: Custom overlay pattern for showing tooltips on multiple charts simultaneously

### ScatterChart Features (v0.0.8)
- **Multi-Series**: Multiple scatter series with individual colors and marker sizes
- **Z-Axis Color Mapping**: Color points by a third variable (continuous, piecewise, ordinal)
- **Voronoi Interaction**: `voronoiMaxRadius` for proximity-based hover/click
- **Dataset-Driven**: `dataset` + `datasetKeys` pattern for table-format data
- **Batch Renderer**: `renderer='svg-batch'` for large datasets
- **Click Events**: `clickData` with seriesId, dataIndex, x, y coordinates
- **Log/Sqrt Scales**: Full axis scaleType support

### CompositeChart Features (v0.0.8)
- **Chart Layering**: Mix `type: 'scatter'` and `type: 'line'` series on one surface
- **Reference Lines**: Horizontal and vertical markers
- **Multi-Axis**: Scatter on left axis, line on right axis
- **Zoom/Pan** (Pro): `initialZoom`, `showSlider`, `zoomInteractionConfig`
- **Toolbar** (Pro): `showToolbar=True` for zoom/export controls

### PieChart Features (v0.0.7)
- **Controlled Item Highlight**: `highlightedItem` now works as both input and output for synchronized highlighting

### Synchronized Highlighting (v0.0.7)
- **Custom Tooltip Overlays**: Solution for MUI's limitation where tooltips only appear on hovered chart
- Use `tooltip={'trigger': 'none'}` + custom HTML divs for true synchronized tooltips
- See `pages/highlighting_sync.py` for complete implementation

---

## Technology Stack

### Frontend
- **React 18+** - UI rendering
- **@mui/x-charts v8.24.0** - Community charts
- **@mui/x-charts-pro v8.24.0** - Pro charts
- **@mui/material v6.5.0** - Material UI
- **Webpack 5** - Bundling

### Backend
- **Python 3.8+** - Runtime
- **Dash 3.x** - Web framework
- **dash-generate-components** - Python wrapper generation

---

## Quick Commands

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build components
npm run build

# Run demo app
python app.py

# Run standalone example
python usage.py
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/lib/components/*.react.js` | React component source |
| `dash_mui_charts/*.py` | Auto-generated Python wrappers |
| `assets/muiChartsFunctions.js` | Functions-as-props registry (formatDate, etc.) |
| `pages/*.py` | Demo page examples |
| `app.py` | Main Dash application |
| `setup.py` | Python package configuration |

---

## Important Notes

1. **MUI X Charts uses `seriesId`** not `seriesIndex` in callbacks - React components convert this
2. **Rebuild after changes**: Always run `npm run build` after modifying React components
3. **Unique IDs in multi-page apps**: Prefix component IDs with page name to avoid conflicts
4. **Pro features**: Require MUI X Pro license key via `licenseKey` prop

---

## Resources

- **MUI X Charts**: https://mui.com/x/react-charts/
- **Dash Documentation**: https://dash.plotly.com
- **Project README**: See `README.md` for usage examples
- **Detailed Guide**: See `.claude/SKILLS.md` for implementation details