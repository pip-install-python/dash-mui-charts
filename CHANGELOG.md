# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [1.2.0] - 2026-04-10

### Added

#### BarChart Component (New)
- **Vertical & Horizontal Bars**: `layout='vertical'` (default) or `layout='horizontal'`
- **Multi-Series**: Multiple data series with individual colors side by side
- **Stacking**: `stack` group ID on series, with `stackOffset` ('none', 'expand', 'diverging') and `stackOrder` ('none', 'appearance', 'ascending', 'descending', 'reverse')
- **Bar Labels**: `barLabel='value'` with `barLabelPlacement` ('center' or 'outside')
- **Border Radius**: Rounded bar corners via `borderRadius` prop
- **Dataset Mode**: `dataset` + `dataKey` pattern for table-format data (no duplication)
- **Bar Spacing**: `categoryGapRatio` and `barGapRatio` on band axis for gap control
- **Reference Lines**: Horizontal (`y`) and vertical (`x`) markers for targets, thresholds
- **Axis Highlight**: Configurable `axisHighlight` with 'band', 'line', or 'none'
- **Tooltip Modes**: `tooltip={'trigger': 'axis'}` or `tooltip={'trigger': 'item'}`
- **Highlighting**: `highlightedItem` prop (controlled, bidirectional) with per-series `highlightScope`
- **Custom Colors**: `colors` palette prop for series color override
- **Batch Renderer**: `renderer='svg-batch'` for large dataset performance
- **Click Events**: `clickData` (bar click) and `axisClickData` (axis area click) output props
- **Pro Features** (require `licenseKey`):
  - `initialZoom` + `showSlider` for zoom with range slider
  - `showToolbar` for zoom/export toolbar
  - `brushConfig` for brush selection
  - `zoomInteractionConfig` for pan/wheel/pinch behaviors
  - `zoomData` output prop for zoom state callbacks

#### CandlestickChart Component (New)
- **OHLC Candlestick Rendering**: Custom SVG candles (body + wicks) built on MUI X Charts Pro composition API
- **Array Format**: `series=[{data: [[open,high,low,close], ...], upColor, downColor}]`
- **Dataset Format**: `dataset` + `series=[{datasetKeys: {open, high, low, close}}]`
- **Volume Overlay**: Optional volume bars below candles via `showVolume=True` with `volumeKey` or `volume` array
- **Candle Styling**: `bodyWidthRatio` (0-1) and `wickWidth` (px) for custom candle appearance
- **OHLC Tooltip**: Built-in hover tooltip showing Open, High, Low, Close values
- **Reference Lines**: Support/resistance lines, moving averages markers
- **Click Events**: `clickData` with `{dataIndex, label, open, high, low, close, timestamp}`
- **Auto Y-Axis Domain**: Automatically computes min/max from OHLC data with 5% padding
- **Grid Support**: `grid={'horizontal': True, 'vertical': True}`
- **Pro Features**: Zoom, slider, toolbar (via composition API)
- **No Premium Dependency**: Works with existing `@mui/x-charts-pro` v8.24.0 (no `@mui/x-charts-premium` required)

#### Demo Pages (7 New)
- `/barchart-basic` — Multi-series, stacked, horizontal, bar labels, rounded corners, negative values
- `/barchart-dataset` — Dataset mode with dataKey, bar/category gap control
- `/barchart-stacking` — Stack offsets (none, expand, diverging), multiple stack groups, horizontal stacked
- `/barchart-interaction` — Click events, axis click, highlighting, axis highlight modes, tooltip triggers
- `/barchart-reference` — Target lines, min/avg/max refs, vertical refs, animation, legend, color palette
- `/barchart-pro` — Zoom+slider, toolbar, stacked zoom (Pro features)
- `/candlestick` — Array format, dataset mode, volume overlay, styling, support/resistance lines, click events

#### Application UI/UX Redesign
- **DMC AppShell Layout**: Replaced flat blue top-bar with `dmc.AppShell` (header + sidebar navbar + main content area)
- **Sidebar Tree Navigation**: `SimpleTreeView` organizes all 37 demo pages into 11 component groups with expand/collapse
- **Dark/Light Mode**: `dmc.ColorSchemeToggle` (DMC 2.6.1) with `dmc.pre_render_color_scheme()` to prevent theme flash on load
- **MUI Charts Dark Mode**: Global CSS overrides for axis labels, tick marks, grid lines, legend labels, tooltips, bar labels, and reference lines — all auto-switch via `[data-mantine-color-scheme="dark"]`
- **Theme-Aware Loading Screen**: Animated liquid-blob splash screen with 2plot logo, swaps between light/dark assets based on saved preference (`localStorage`)
- **Page Loading Overlay**: `/composite-render-bp` uses deferred content loading via callback with `dmc.LoadingOverlay` — shows logo + blur overlay while heavy chart sections build server-side
- **Home Page Redesign**: Responsive 3-column component card grid with `dmc.Paper`, `dmc.Badge`, `dmc.CodeHighlight` for installation and usage examples

### Changed
- **CompositeChart**: Custom tooltip components (`MuiAxisTooltip`, `ExternalAxisTooltip`) now use Mantine CSS variables (`--mantine-color-body`, `--mantine-color-text`, `--mantine-color-default-border`) instead of hardcoded `white`/`#e0e0e0` — tooltips auto-adapt to dark mode
- **SimpleTreeView**: Replaced `Component.defaultProps` with JavaScript default parameters to eliminate React 18 deprecation warning
- **Composite Render BP page**: Deferred chart section building to a callback (from static layout) for instant page load with loading overlay
- Updated component count from 7 to 9
- `src/lib/index.js` exports BarChart and CandlestickChart
- Auto-generated Python wrappers for both components via `dash-generate-components`
- Upgraded `dash-mantine-components` from `>=1.0.0` to `>=2.6.0` in `requirements.txt`
- All demo pages updated with Mantine CSS variables for dark mode support (card backgrounds, text colors, code blocks, tooltips, borders)
- Pages with `dmc.MantineProvider` wrappers (8 files) unwrapped — single root provider in `app.py`

### Fixed
- **Legend labels not switching in dark mode**: Added CSS selectors for `.MuiChartsLegend-label` and `.MuiChartsLabel-root` (HTML span elements used by MUI X Charts v8)
- **Custom tooltip dark mode** in crosshair, highlighting sync, composite, and composite render pages — replaced hardcoded `white`/`#333`/`#e0e0e0` with theme-adaptive CSS variables
- **Highlighting demo**: Per-Series Highlight Scope example now uses 3 series with distinct `highlightScope` configs to clearly demonstrate `series` vs `item` highlight and `global` vs `none` fade behaviors
- **Circular dependency**: Replaced server-side nav callbacks with clientside `window.location` navigation to break `url.pathname ↔ nav-tree.selectedItems` cycle

### Documentation
- Updated CLAUDE.md with BarChart and CandlestickChart features
- Updated SKILLS.md with implementation details, prop references, and usage patterns
- Updated README.md with new component listings and examples

---

## [1.1.0] - 2026-04-08

### Added

#### Functions-as-Props Pattern (LineChart, CompositeChart)
- **`resolveFunctionProp` utility** — Mirrors Dash Mantine Components' `dashMantineFunctions` pattern
  - Python passes `{'function': 'name', 'options': {...}}` as a prop value
  - React component resolves from `window.dashMuiChartsFunctions` registry
  - Users define custom JS functions in `assets/*.js` files
- **`valueFormatter` support on xAxis/yAxis** — Control how axis values are displayed
  - Accepts DMC-style function reference objects or native JS functions
  - Enables custom date formatting, number formatting, and label rendering
  - Works with all scale types (time, linear, point, band, etc.)

#### Built-in Date Formatting (LineChart, CompositeChart)
- **`dateFormat` prop on xAxis/yAxis** — Format string for tooltip date labels (e.g. `'M/d HH:mm'`)
- **`dateTickFormat` prop on xAxis/yAxis** — Separate shorter format for tick labels (e.g. `'M/d'`)
  - Prevents label truncation by using compact tick labels while keeping full format in tooltips
  - Supported tokens: `YYYY`, `MMM`, `MM`, `M`, `dd`, `d`, `HH`, `mm`
  - Automatically creates a `valueFormatter` internally — no external JS file required

#### LiveTradingChart Component (New)
- Real-time streaming chart component for live data visualization

#### Demo Pages
- New `/linechart-tick-hover` page — Comprehensive tick, hover, and axis configuration guide
  - Section 1-4: Date range best practices (week, quarter, year) with point and linear scales
  - Section 5a: Angled labels with `dateFormat`/`dateTickFormat` on time scale
  - Section 5b: Zoom with slider — tick behavior during zoom/pan interactions (Pro)
  - Section 5c: Pro zoom with slider preview, brush select, toolbar, and `zoomInteractionConfig`
  - Section 6: Interactive hover events with click data callbacks
  - Section 7: Best practices summary reference table
- New `/live-trading` page — LiveTradingChart demo

#### Assets
- New `assets/muiChartsFunctions.js` — Ships a reusable `formatDate` function for the functions-as-props pattern
  - Supports format tokens: `YYYY`, `MMM`, `MM`, `M`, `dd`, `d`, `HH`, `mm`
  - Context-aware: uses `tickFormat` option for tick labels, `format` for tooltips

### Changed
- **LineChart** — `processedXAxis` no longer short-circuits when `showSlider` is false
  - Previously skipped all axis processing (including valueFormatter resolution) when slider was disabled
  - Now always processes axes for dateFormat and valueFormatter resolution
- **CompositeChart** — Same `processedXAxis` improvement as LineChart

### Documentation
- Updated CLAUDE.md with new component features and axis formatting documentation
- Key Tick & Zoom Props reference table in the tick-hover demo page

---

## [1.0.0] - 2026-03-19

### Added
- **Stable release** — 6 chart components ready for production use

### Changed
- Version bump to 1.0.0 to reflect API stability
- Fixed `package-info.json` version tracking (was stuck at `0.0.1`, causing stale JS bundle caching)

---

## [0.0.8] - 2026-03-12

### Added

#### ScatterChart (New Component)
- **Multi-Series**: Multiple scatter series with individual colors and marker sizes
- **Z-Axis Color Mapping**: Color points by a third variable (continuous, piecewise, ordinal)
- **Voronoi Interaction**: `voronoiMaxRadius` for proximity-based hover/click
- **Dataset-Driven**: `dataset` + `datasetKeys` pattern for table-format data
- **Batch Renderer**: `renderer='svg-batch'` for large datasets
- **Click Events**: `clickData` with seriesId, dataIndex, x, y coordinates
- **Log/Sqrt Scales**: Full axis scaleType support

#### CompositeChart (New Component)
- **Chart Layering**: Mix `type: 'scatter'` and `type: 'line'` series on a single surface
- **Custom Composite Tooltip**: Axis tooltip shows both line and scatter data via proximity search
  - Handles MUI's poor scatter tooltip formatting in composite charts
  - Auto-computes proximity threshold from x-axis data spacing
- **Reference Lines**: Horizontal and vertical markers
- **Multi-Axis**: Scatter on left axis, line on right axis
- **Zoom/Pan** (Pro): `initialZoom`, `showSlider`, `zoomInteractionConfig`
- **Toolbar** (Pro): `showToolbar=True` for zoom/export controls
- **Zoom Slider Preview**: `preview: {markerSize}` on scatter series for slider preview markers
- **Time Scale Support**: Automatic epoch ms to Date object conversion for `scaleType: 'time'`
- **Controlled Highlighting**: `highlightedItem` prop for programmatic control
- **Click Events**: Separate click handlers for scatter and line series

#### Demo Pages
- New `/scatter` page with multi-series, z-axis color mapping, voronoi, and dataset-driven examples
- New `/composite` page with scatter+trend, reference lines, multi-axis, and zoom-enabled examples
  - DMC sliders for interactive marker size control (chart and preview)
  - Multi-color anomaly scatter (red critical / yellow warning)

### Changed
- Updated component count from 4 to 6
- `src/lib/index.js` exports ScatterChart and CompositeChart

### Documentation
- Updated CLAUDE.md with ScatterChart and CompositeChart features
- Updated SKILLS.md with new component documentation and patterns
- Updated README.md with new component listings

---

## [0.0.7] - 2025-01-30

### Added

#### Synchronized Tooltips with Custom Overlays
- **Custom tooltip overlay system** for true synchronized tooltips across multiple charts
  - MUI X Charts limitation: native tooltips only appear on the hovered chart
  - Solution: Custom Dash HTML divs positioned absolutely over each chart
  - Both charts show tooltips simultaneously when hovering on either one
- New demo implementation in `/highlighting-sync` page showing:
  - Revenue + Expenses dual LineChart with synchronized custom tooltips
  - Tooltips positioned using CSS `calc()` for responsive layouts
  - Visual highlighting (marks, axis bands) continues to sync via `highlightedItem`

#### LineChart Highlighting Improvements
- Improved callback patterns for highlight synchronization
- Better handling of highlight state when mouse leaves chart area
- Custom tooltip content generation for each chart in sync scenarios

### Changed
- **Highlighting Sync Demo**: Updated to use custom tooltip overlays instead of `tooltipItem`
  - Disabled MUI's built-in tooltips: `tooltip={'trigger': 'none'}`
  - Added absolutely-positioned custom tooltip divs
  - Tooltip x-position calculated from data index and chart margins
- Callback now listens to `highlightedItem` (more reliable than `tooltipItem` for sync)

### Documentation
- Updated SKILLS.md with custom synchronized tooltip pattern
- Documented MUI X Charts tooltip limitation (GitHub issues #14455, #17555)
- Added code examples for custom tooltip positioning

---

## [0.0.6] - 2025-01-29

### Added

#### LineChart - Controlled Highlighting
- New `highlightedItem` prop for controlled item highlight state
  - Programmatically highlight specific data points
  - Bidirectional: updates on hover and accepts external values
  - Object format: `{'seriesId': 'series-id', 'dataIndex': 0}`
- New `highlightedAxis` prop for controlled axis highlight state
  - Programmatically highlight specific axis positions
  - Array format: `[{'axisId': 'x-axis', 'dataIndex': 2}]`
- New `onHighlightChange` and `onHighlightedAxisChange` callbacks (internal)

#### LineChart - Per-Series Highlight Scope
- Series-level `highlightScope` configuration
  - `highlight`: `'none'` | `'item'` | `'series'`
  - `fade`: `'none'` | `'series'` | `'global'`
- Different highlight/fade behaviors per series

#### LineChart - Toolbar (Pro)
- New `showToolbar` prop to display chart toolbar
- Provides zoom/export controls
- Requires MUI X Pro license

#### LineChart - Synchronized Tooltips
- New `tooltipItem` prop for controlled tooltip state
  - Enables synchronized tooltips across multiple charts
  - Object format: `{'type': 'line', 'seriesId': 'series-id', 'dataIndex': 0}`
  - Bidirectional: updates on hover and accepts external values
- Combined with `highlightedItem` for full visual synchronization

#### PieChart - Controlled Highlighting
- `highlightedItem` prop now works as both input and output
- Enables synchronized highlighting across multiple charts
- Object format: `{'seriesId': 'auto-generated-id-0', 'dataIndex': 0}`

#### Demo Pages
- New `/linechart-highlighting` page demonstrating:
  - Controlled item highlights with buttons
  - Controlled axis highlights
  - Per-series highlightScope configuration
- New `/highlighting-sync` page demonstrating:
  - LineChart + PieChart synchronization
  - Dual LineChart axis synchronization
  - Cross-chart highlight coordination

### Changed
- LineChart now uses controlled mode for highlighting by default
  - Always passes `highlightedItem` (as `null` when not set)
  - Ensures proper MUI controlled mode initialization
- Callback patterns improved to avoid echo issues
  - Separated button-triggered and display callbacks
  - Use `dash.no_update` to prevent callback loops in sync scenarios

### Fixed
- Item highlighting not triggering callbacks in composition API
- Controlled highlight state not syncing with MUI internal state
- Echo issues in highlight synchronization callbacks

### Documentation
- Updated CLAUDE.md with v0.0.6 features
- Updated SKILLS.md with highlighting patterns and examples

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
| BarChart (zoom/brush) | MUI X Pro |
| CandlestickChart (zoom) | MUI X Pro |
| PieChart | Community (Free) |
| ScatterChart | Community (Free) |
| CompositeChart (zoom/pan) | MUI X Pro |
| Heatmap | MUI X Pro |
| SparklineChart | Community (Free) |
| LiveTradingChart | Community (Free) |

---

[Unreleased]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.8...v1.0.0
[0.0.8]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.1...v0.0.5
[0.0.1]: https://github.com/pip-install-python/dash-mui-charts/releases/tag/v0.0.1