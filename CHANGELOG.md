# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- BarChart component
- ScatterChart component

---

## [0.0.5] - 2025-01-26

### Added

#### LineChart - Reference Lines
- Full support for `ChartsReferenceLine` API
- Horizontal reference lines via `y` prop (targets, thresholds, averages)
- Vertical reference lines via `x` prop (dates, events, milestones)
- Props: `x`, `y`, `axisId`, `label`, `labelAlign`, `lineStyle`, `labelStyle`, `spacing`
- Support for string/number/Date values on both axes
- Multi-axis support with `axisId` for biaxial charts
- New demo page: `/linechart-referencelines`

#### LineChart - Brush Selection (Pro)
- New brush interaction for range selection on charts
- `brushConfig` prop: `{enabled, preventTooltip, preventHighlight}`
- `brushOverlay` prop: `'none'` | `'default'` | `'values'`
  - `'default'`: Standard MUI selection rectangle
  - `'values'`: Custom overlay showing start/end values with difference and percentage change
- `brushSeriesId` prop: Specify which series to use for value calculations
- `brushData` output prop: Selection coordinates for callbacks
- New demo page: `/linechart-brush`

#### LineChart - Axis Highlight Configuration
- New `axisHighlight` prop to configure hover highlighting
- Options: `{x: 'none'|'line'|'band', y: 'none'|'line'}`
- Default: `{x: 'line', y: 'none'}`

### Changed
- `referenceLines.y` now accepts `string | number` (previously only `number`)
- Enables Date string values for time-based reference lines

### Documentation
- New demo page: `pages/linechart_brush.py`
- New demo page: `pages/linechart_referencelines.py`
- Updated SKILLS.md with brush and reference line documentation
- Updated CLAUDE.md with new LineChart features

---

## [0.0.1] - 2025-01-10

### Added

#### Components
- **LineChart** - Full-featured line and area charts
  - Multiple series support with independent Y-axes (biaxial charts)
  - Interactive zoom & pan (requires MUI X Pro license)
  - Line, area, and stacked area visualizations
  - 10+ curve interpolation options (linear, monotone, natural, step, catmull-rom, bump, etc.)
  - Configurable grid, legend, and margins
  - Click events for axis, mark, line, and area interactions
  - Zoom slider for range selection
  - Loading state overlay
  - Animation controls with prefers-reduced-motion support

- **PieChart** - Pie, donut, and nested pie charts
  - Single series (simple pie/donut) or multiple series (nested/concentric pies)
  - Customizable arc geometry (inner/outer radius, corners, padding)
  - Arc labels with value, label, or formattedValue display
  - Configurable start/end angles for half-pie and gauge charts
  - Highlight interactions with global fade effects
  - Click and hover event handling
  - Full animation support

- **Heatmap** - Matrix/grid visualization (requires MUI X Pro license)
  - Color-coded cell visualization
  - Continuous or piecewise color scales
  - Custom cell styling (rounded corners, gaps, value display)
  - Band-scale axes for categorical data
  - Cell click detection with coordinates
  - Highlight interactions

- **SparklineChart** - Compact inline charts
  - Ultra-compact design (36px default height)
  - Line or bar plot types
  - Area fill support
  - Tooltip and highlight interactions
  - Controlled highlight index for component synchronization
  - Curve interpolation options

#### Features
- Full TypeScript-like type safety with Python TypedDict
- Auto-generated Python wrappers from React PropTypes
- Comprehensive prop documentation
- Click event data with timestamps
- Dash 3.x compatibility
- React 18+ support

#### Documentation
- Basic usage examples in `usage.py`
- Multi-page demo application with interactive examples
- Property explorer pages for Pie, Heatmap, and Sparkline components

### Technical
- Webpack 5 build configuration
- MUI X Charts v8.24.0 integration
- MUI X Charts Pro v8.24.0 for advanced features
- Emotion styling support

---

## Component License Requirements

| Component | License Required |
|-----------|-----------------|
| LineChart (zoom/pan) | MUI X Pro |
| PieChart | Community (Free) |
| Heatmap | MUI X Pro |
| SparklineChart | Community (Free) |

---

[Unreleased]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.5...HEAD
[0.0.5]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.1...v0.0.5
[0.0.1]: https://github.com/pip-install-python/dash-mui-charts/releases/tag/v0.0.1