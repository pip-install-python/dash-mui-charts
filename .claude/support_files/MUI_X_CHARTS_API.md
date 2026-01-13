# MUI X Charts LineChart API Reference

## Essential Props

### Data Props
- **series** (Array): Array of series configurations
  - `data` (Array<number>): Y-axis values
  - `label` (string): Series label
  - `color` (string): Custom color
  - `area` (boolean): Fill area under line
  - `stack` (string): Stack identifier
  - `curve` (string): Interpolation method
  - `showMark` (boolean): Show data point markers
  - `connectNulls` (boolean): Bridge null values

### Axis Props
- **xAxis** (Array): X-axis configuration
  - `data` (Array): X-axis values
  - `label` (string): Axis label
  - `scaleType` ('band' | 'point' | 'linear' | 'log' | 'time')
  - `position` ('top' | 'bottom')

- **yAxis** (Array): Y-axis configuration
  - `label` (string): Axis label
  - `min/max` (number): Domain range
  - `width` (number): Axis width
  - `position` ('left' | 'right')

### Layout Props
- **height** (number, required): Chart height in pixels
- **width** (number): Chart width in pixels
- **margin** (object): { top, right, bottom, left }
- **grid** (object): { vertical, horizontal }

### Style Props
- **colors** (Array<string>): Color palette
- **hideLegend** (boolean): Hide legend
- **skipAnimation** (boolean): Disable animations
- **loading** (boolean): Show loading overlay

### Events
- **onAxisClick**: (event, params) => void
- **onLineClick**: (event, params) => void
- **onMarkClick**: (event, params) => void
- **onAreaClick**: (event, params) => void

## Curve Types
- 'linear', 'monotoneX', 'monotoneY', 'natural'
- 'step', 'stepBefore', 'stepAfter'
- 'catmullRom', 'bumpX', 'bumpY'

## Tooltip Trigger Types
- 'item': Show data for specific element
- 'axis': Show all series at x-position
- 'none': Disable tooltip