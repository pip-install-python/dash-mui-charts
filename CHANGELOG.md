# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- PyPI package preparation and documentation

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

[Unreleased]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/pip-install-python/dash-mui-charts/releases/tag/v0.0.1