# Claude Code Project Guide - dash_mui_charts

## Project Overview

**dash_mui_charts** is a Dash component library that wraps [MUI X Charts](https://mui.com/x/react-charts/) for use in Plotly Dash applications. It provides 4 chart components with full Python type hints and interactive callbacks.

---

## Components

| Component | Purpose | License |
|-----------|---------|---------|
| **LineChart** | Line/area charts, biaxial, zoom/pan, brush, reference lines | Community / Pro |
| **PieChart** | Pie, donut, nested pies | Community |
| **Heatmap** | Matrix/grid visualization | Pro |
| **SparklineChart** | Compact inline charts | Community |

### LineChart Features (v0.0.5)
- **Reference Lines**: Horizontal (`y`) and vertical (`x`) markers for targets, thresholds, dates
- **Brush Selection** (Pro): Range selection with `'default'` or `'values'` overlay
- **Axis Highlight**: Configurable hover highlighting (`'none'`, `'line'`, `'band'`)

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