# dash-mui-charts

[![PyPI version](https://badge.fury.io/py/dash-mui-charts.svg)](https://badge.fury.io/py/dash-mui-charts)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Dash component library wrapping [MUI X Charts](https://mui.com/x/react-charts/) for creating beautiful, interactive data visualizations in Python.

## Features

- **LineChart** - Line and area charts with zoom/pan, multiple axes, and stacking
- **PieChart** - Pie, donut, and nested/concentric pie charts
- **ScatterChart** - Scatter/point charts with z-axis color mapping and voronoi interaction
- **CompositeChart** - Layer scatter + line plots on a single surface with zoom/pan
- **Heatmap** - Matrix visualizations with customizable color scales
- **SparklineChart** - Compact inline charts for dashboards and tables

## Installation

```bash
pip install dash-mui-charts
```

## Quick Start

```python
from dash import Dash, html
from dash_mui_charts import LineChart, PieChart

app = Dash(__name__)

app.layout = html.Div([
    # Simple Line Chart
    LineChart(
        series=[
            {'data': [2, 5, 3, 8, 1, 9], 'label': 'Sales'},
            {'data': [1, 3, 2, 5, 4, 6], 'label': 'Costs'},
        ],
        xAxis=[{'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'scaleType': 'band'}],
        height=300,
    ),

    # Simple Pie Chart
    PieChart(
        data=[
            {'id': 0, 'value': 35, 'label': 'Marketing'},
            {'id': 1, 'value': 25, 'label': 'Engineering'},
            {'id': 2, 'value': 20, 'label': 'Sales'},
            {'id': 3, 'value': 20, 'label': 'Support'},
        ],
        height=300,
    ),
])

if __name__ == '__main__':
    app.run(debug=True)
```

## Components

### LineChart

Create line and area charts with rich interactivity.

```python
from dash_mui_charts import LineChart

LineChart(
    id='my-line-chart',
    series=[
        {
            'data': [2, 5.5, 2, 8.5, 1.5, 5],
            'label': 'Series A',
            'color': '#1976d2',
            'area': True,  # Fill area under line
            'curve': 'monotoneX',  # Smooth curve
        },
    ],
    xAxis=[{'data': [1, 2, 3, 4, 5, 6], 'scaleType': 'linear'}],
    yAxis=[{'label': 'Value'}],
    height=400,
    grid={'horizontal': True, 'vertical': False},
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `series` | list | Array of line configurations (data, label, color, area, curve, stack) |
| `xAxis` | list | X-axis configurations (data, scaleType, label) |
| `yAxis` | list | Y-axis configurations (label, position, min, max) |
| `zoom` | list | Zoom state for controlled zoom (requires Pro license) |
| `showSlider` | bool | Show zoom slider below chart |
| `grid` | dict | Grid line configuration |
| `height` | int | Chart height in pixels |

**Output Props (for callbacks):**
- `clickData` - Data from click events
- `zoomData` - Current zoom state
- `n_clicks` - Click counter

---

### PieChart

Create pie, donut, and nested pie charts.

```python
from dash_mui_charts import PieChart

# Simple Donut Chart
PieChart(
    data=[
        {'id': 0, 'value': 35, 'label': 'Chrome'},
        {'id': 1, 'value': 25, 'label': 'Safari'},
        {'id': 2, 'value': 20, 'label': 'Firefox'},
        {'id': 3, 'value': 20, 'label': 'Edge'},
    ],
    innerRadius=60,  # Creates donut hole
    cornerRadius=5,
    paddingAngle=2,
    height=300,
)

# Nested Pie Chart (Multi-Series)
PieChart(
    series=[
        {
            'data': inner_ring_data,
            'innerRadius': 0,
            'outerRadius': 80,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
        {
            'data': outer_ring_data,
            'innerRadius': 90,
            'outerRadius': 120,
            'highlightScope': {'fade': 'global', 'highlight': 'item'},
        },
    ],
    height=400,
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `data` | list | Pie data for single series (id, value, label, color) |
| `series` | list | Multi-series config for nested pies |
| `innerRadius` | int/str | Inner radius (>0 creates donut) |
| `outerRadius` | int/str | Outer radius |
| `startAngle` | int | Start angle in degrees (default: 0) |
| `endAngle` | int | End angle in degrees (default: 360) |
| `arcLabel` | str | Label type: 'value', 'label', 'formattedValue' |
| `cornerRadius` | int | Rounded corners on slices |
| `paddingAngle` | int | Gap between slices in degrees |

**Output Props:**
- `clickData` - Clicked slice data (id, label, value, seriesIndex)
- `highlightedItem` - Currently hovered item
- `n_clicks` - Click counter

---

### ScatterChart

Create scatter/point charts with multi-series support and z-axis color mapping.

```python
from dash_mui_charts import ScatterChart

ScatterChart(
    id='my-scatter',
    series=[
        {
            'id': 'group-a',
            'label': 'Group A',
            'data': [
                {'x': 1, 'y': 5, 'id': 0},
                {'x': 2, 'y': 8, 'id': 1},
                {'x': 3, 'y': 6, 'id': 2},
            ],
            'color': '#1976d2',
            'markerSize': 6,
        },
    ],
    voronoiMaxRadius=30,
    height=400,
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `series` | list | Scatter series with data [{x, y, id}], color, markerSize |
| `zAxis` | list | Z-axis config for color mapping |
| `voronoiMaxRadius` | int | Proximity radius for hover interaction |
| `dataset` | list | Table-format data for datasetKeys pattern |
| `renderer` | str | 'svg' (default) or 'svg-batch' for large datasets |

**Output Props:**
- `clickData` - Click event with seriesId, dataIndex, x, y
- `highlightedItem` - Currently hovered item
- `n_clicks` - Click counter

---

### CompositeChart

Layer scatter and line plots on a single chart surface.

> **Note:** Zoom/pan features require MUI X Pro license.

```python
from dash_mui_charts import CompositeChart

CompositeChart(
    id='my-composite',
    series=[
        {
            'type': 'line',
            'id': 'baseline',
            'label': 'Baseline',
            'data': [50, 55, 48, 62, 58],
            'color': '#66bb6a',
            'area': True,
        },
        {
            'type': 'scatter',
            'id': 'anomalies',
            'label': 'Anomalies',
            'data': [{'x': 1, 'y': 80, 'id': 0}, {'x': 3, 'y': 25, 'id': 1}],
            'color': '#e53935',
            'markerSize': 6,
        },
    ],
    xAxis=[{'data': [0, 1, 2, 3, 4], 'scaleType': 'linear'}],
    height=400,
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `series` | list | Array of series with `type` ('scatter' or 'line') |
| `xAxis` | list | X-axis config (supports `scaleType: 'time'` with epoch ms) |
| `yAxis` | list | Y-axis config (supports multi-axis with `id` and `position`) |
| `referenceLines` | list | Horizontal/vertical reference markers |
| `initialZoom` | list | Initial zoom state (Pro) |
| `showSlider` | bool | Show zoom slider (Pro) |
| `showToolbar` | bool | Show toolbar (Pro) |

**Output Props:**
- `clickData` - Click event with type, seriesId, dataIndex
- `highlightedItem` - Currently hovered item
- `zoomData` - Current zoom state
- `n_clicks` - Click counter

---

### Heatmap

Create matrix visualizations with color-coded cells.

> **Note:** Requires MUI X Pro license for full functionality.

```python
from dash_mui_charts import Heatmap

Heatmap(
    data=[
        [0, 0, 10], [0, 1, 20], [0, 2, 30],
        [1, 0, 40], [1, 1, 50], [1, 2, 60],
        [2, 0, 70], [2, 1, 80], [2, 2, 90],
    ],
    xAxis={'data': ['Mon', 'Tue', 'Wed'], 'scaleType': 'band'},
    yAxis={'data': ['Morning', 'Afternoon', 'Evening'], 'scaleType': 'band'},
    colorScale={
        'type': 'continuous',
        'min': 0,
        'max': 100,
        'colors': ['#e3f2fd', '#1976d2'],
    },
    height=300,
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `data` | list | Array of [x, y, value] tuples |
| `xAxis` | dict | X-axis band scale configuration |
| `yAxis` | dict | Y-axis band scale configuration |
| `colorScale` | dict | Color mapping (continuous or piecewise) |
| `cellStyle` | str/dict | Cell styling ('rounded' or detailed config) |

**Output Props:**
- `clickData` - Clicked cell data (x, y, value, color)
- `highlightedItem` - Currently hovered cell
- `n_clicks` - Click counter

---

### SparklineChart

Create compact inline charts for dashboards.

```python
from dash_mui_charts import SparklineChart

SparklineChart(
    data=[1, 4, 2, 5, 7, 2, 4, 6],
    plotType='line',  # or 'bar'
    color='#1976d2',
    area=True,
    height=40,
    width=150,
    showTooltip=True,
)
```

**Key Props:**
| Prop | Type | Description |
|------|------|-------------|
| `data` | list | Numeric values (required) |
| `plotType` | str | 'line' or 'bar' |
| `color` | str | Line/bar color |
| `area` | bool | Fill area under line |
| `curve` | str | Curve interpolation method |
| `showTooltip` | bool | Enable hover tooltips |

**Output Props:**
- `highlightedItem` - Current highlight state
- `hoverIndex` - Index of hovered point
- `hoverValue` - Value at hovered point
- `n_hovers` - Hover counter

---

## License Requirements

| Component | Community (Free) | Pro License Required |
|-----------|------------------|---------------------|
| LineChart | Basic features | Zoom & Pan |
| PieChart | All features | - |
| ScatterChart | All features | - |
| CompositeChart | Basic layering | Zoom & Pan |
| Heatmap | - | All features |
| SparklineChart | All features | - |

To use Pro features, obtain a license from [MUI](https://mui.com/x/introduction/licensing/) and pass it via the `licenseKey` prop:

```python
LineChart(
    licenseKey='YOUR_MUI_X_PRO_LICENSE_KEY',
    # ... other props
)
```

## Interactive Examples

Run the demo application to explore all components:

```bash
git clone https://github.com/pip-install-python/dash-mui-charts.git
cd dash-mui-charts
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:8050` to see:
- Basic and advanced line chart examples
- Pie chart property explorer with nested pies
- Scatter chart with z-axis color mapping and voronoi interaction
- Composite charts layering scatter + line with zoom/pan
- Heatmap configuration playground
- Sparkline styling options

## Development

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Setup

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build components
npm run build

# Run development server
python app.py
```

### Build Process

```bash
# Full build (JS + Python wrappers)
npm run build

# Watch mode for development
npm run start
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Resources

- [MUI X Charts Documentation](https://mui.com/x/react-charts/)
- [Dash Documentation](https://dash.plotly.com)
- [Dash Component Boilerplate](https://github.com/plotly/dash-component-boilerplate)

## License

Pip Install Python LLC MIT License - see [LICENSE](LICENSE) for details.

## Author

**Pip Install Python**
- GitHub: [@pip-install-python](https://github.com/pip-install-python)