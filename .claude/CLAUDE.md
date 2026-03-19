# Claude Code Project Guide - dash_mui_charts

## Project Overview

**dash_mui_charts** is a Dash component library that wraps [MUI X Charts](https://mui.com/x/react-charts/) for use in Plotly Dash applications. It provides 6 chart components with full Python type hints and interactive callbacks.

---

## Components

| Component | Purpose | License |
|-----------|---------|---------|
| **LineChart** | Line/area charts, biaxial, zoom/pan, brush, reference lines | Community / Pro |
| **PieChart** | Pie, donut, nested pies | Community |
| **ScatterChart** | Scatter/point charts, z-axis color mapping, voronoi interaction | Community |
| **CompositeChart** | Layer scatter + line plots on a single surface | Community / Pro |
| **Heatmap** | Matrix/grid visualization | Pro |
| **SparklineChart** | Compact inline charts | Community |

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