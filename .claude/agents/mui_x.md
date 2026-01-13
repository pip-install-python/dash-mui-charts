# MUI X Agent

Reference guide for MUI X component library, licensing, and general patterns.

## MUI X Overview

MUI X is a collection of advanced React components built on top of Material UI:

- **Data Grid** - Advanced data table with sorting, filtering, grouping
- **Charts** - Line, bar, pie, scatter, and other chart types
- **Date/Time Pickers** - Date, time, and datetime selection
- **Tree View** - Hierarchical data display

## Licensing

MUI X has three tiers:

### Community (Free)
- Basic features, MIT license
- No license key required

### Pro ($249/dev/year)
- Advanced features like export, multi-filtering
- Requires license key

### Premium ($588/dev/year)
- All Pro features plus premium-only features
- Requires license key

## License Key Setup

### Setting the License Key

```javascript
import { LicenseInfo } from '@mui/x-license';

// Set once at app initialization
LicenseInfo.setLicenseKey('YOUR_LICENSE_KEY');
```

### In Dash Components

```javascript
// Track if already set to avoid multiple calls
let licenseKeySet = false;

export default function MyComponent({ licenseKey, ...props }) {
    if (licenseKey && !licenseKeySet) {
        LicenseInfo.setLicenseKey(licenseKey);
        licenseKeySet = true;
    }
    // ... rest of component
}
```

### Environment Variable Pattern

```python
# Python (load from environment)
import os
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Pass to component
LineChart(licenseKey=MUI_LICENSE_KEY, ...)
```

## MUI X Package Structure

### Installation

```bash
# Community packages
npm install @mui/x-charts
npm install @mui/x-data-grid
npm install @mui/x-date-pickers
npm install @mui/x-tree-view

# Pro packages (requires license)
npm install @mui/x-charts-pro
npm install @mui/x-data-grid-pro
npm install @mui/x-date-pickers-pro

# Premium packages
npm install @mui/x-data-grid-premium
```

### Import Patterns

```javascript
// Community imports
import { LineChart } from '@mui/x-charts/LineChart';
import { DataGrid } from '@mui/x-data-grid';

// Pro imports (different package path)
import { LineChart } from '@mui/x-charts-pro/LineChart';
import { DataGridPro } from '@mui/x-data-grid-pro';

// Individual component imports (tree-shaking)
import { LinePlot } from '@mui/x-charts/LineChart';
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis';
```

## Pro Features by Component

### Data Grid Pro
- Column pinning
- Row reordering
- Multi-filtering
- Tree data
- Excel/CSV export
- Lazy loading

### Charts Pro
- Zoom and pan
- Zoom slider
- Heatmap charts
- Animation control

### Date Pickers Pro
- Date range picker
- Time range picker

## Controlled vs Uncontrolled Components

MUI X components support both patterns:

### Uncontrolled (with initial value)
```javascript
// Component manages its own state after initial render
<DataGrid
    initialState={{
        sorting: { sortModel: [{ field: 'name', sort: 'asc' }] }
    }}
/>
```

### Controlled (external state management)
```javascript
// Parent manages state
const [sortModel, setSortModel] = useState([]);

<DataGrid
    sortModel={sortModel}
    onSortModelChange={setSortModel}
/>
```

## Theming

MUI X components inherit from Material UI theme:

```javascript
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: { main: '#1976d2' },
    },
    components: {
        MuiChartsAxis: {
            styleOverrides: {
                root: {
                    // Custom axis styles
                }
            }
        }
    }
});

<ThemeProvider theme={theme}>
    <LineChart ... />
</ThemeProvider>
```

## Common Patterns for Dash Integration

### Prop Validation

```javascript
import PropTypes from 'prop-types';

MyComponent.propTypes = {
    // Required for Dash
    id: PropTypes.string,
    setProps: PropTypes.func,

    // Component props
    data: PropTypes.arrayOf(PropTypes.object),
    licenseKey: PropTypes.string,
};
```

### Event Handling for Dash

```javascript
const handleClick = (event, params) => {
    if (setProps) {
        setProps({
            clickData: {
                type: 'item',
                itemId: params.id,
                timestamp: new Date().toISOString()
            },
            n_clicks: (n_clicks || 0) + 1
        });
    }
};
```

### Loading States

```javascript
{loading && (
    <div style={{
        position: 'absolute',
        top: 0, left: 0, right: 0, bottom: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(255,255,255,0.7)'
    }}>
        Loading...
    </div>
)}
```

## Resources

- [MUI X Documentation](https://mui.com/x/)
- [MUI X GitHub](https://github.com/mui/mui-x)
- [Licensing Info](https://mui.com/x/introduction/licensing/)
- [API Reference](https://mui.com/x/api/)