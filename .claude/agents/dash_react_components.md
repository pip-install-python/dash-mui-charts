# Dash React Components Agent

Reference guide for building React components for Dash applications.

## Component Boilerplate

```javascript
import React, { useState, useEffect, useId, useMemo } from 'react';
import PropTypes from 'prop-types';

/**
 * MyComponent description for Dash auto-generated docs.
 */
export default function MyComponent(props) {
    const {
        id,
        // Input props
        value,
        options,
        disabled = false,
        // Output props (read by Dash callbacks)
        selectedValue,
        n_clicks = 0,
        // Dash callback function
        setProps,
    } = props;

    // Component implementation
    const handleClick = () => {
        if (setProps) {
            setProps({
                selectedValue: value,
                n_clicks: n_clicks + 1
            });
        }
    };

    return (
        <div id={id}>
            {/* Component JSX */}
        </div>
    );
}

MyComponent.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Input value for the component.
     */
    value: PropTypes.string,

    /**
     * Array of option objects.
     */
    options: PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.string,
        value: PropTypes.any,
    })),

    /**
     * If true, component is disabled.
     */
    disabled: PropTypes.bool,

    /**
     * Currently selected value. Read-only output.
     */
    selectedValue: PropTypes.any,

    /**
     * Number of times clicked.
     */
    n_clicks: PropTypes.number,

    /**
     * Dash-assigned callback for property updates.
     */
    setProps: PropTypes.func,
};
```

## Controlled Component Pattern

For components that need to sync between Dash props and internal state:

```javascript
export default function ControlledComponent(props) {
    const { value, setProps } = props;

    // Internal state mirrors prop
    const [internalValue, setInternalValue] = useState(value);

    // Track last prop value to detect external changes
    const [lastPropValue, setLastPropValue] = useState(JSON.stringify(value));

    // Sync external prop changes to internal state
    useEffect(() => {
        const currentPropStr = JSON.stringify(value);
        if (currentPropStr !== lastPropValue) {
            setLastPropValue(currentPropStr);
            setInternalValue(value);
        }
    }, [value, lastPropValue]);

    // Handle internal changes
    const handleChange = (newValue) => {
        setInternalValue(newValue);
        setLastPropValue(JSON.stringify(newValue));

        if (setProps) {
            setProps({ value: newValue });
        }
    };

    return <input value={internalValue} onChange={e => handleChange(e.target.value)} />;
}
```

## PropTypes Reference

### Basic Types

```javascript
PropTypes.string
PropTypes.number
PropTypes.bool
PropTypes.array
PropTypes.object
PropTypes.func
PropTypes.any
```

### Constrained Types

```javascript
// One of specific values
PropTypes.oneOf(['small', 'medium', 'large'])

// One of specific types
PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
])

// Array of specific type
PropTypes.arrayOf(PropTypes.number)

// Object with specific shape
PropTypes.shape({
    id: PropTypes.string.isRequired,
    label: PropTypes.string,
    value: PropTypes.any,
})

// Object with specific keys
PropTypes.objectOf(PropTypes.number)

// Required prop
PropTypes.string.isRequired
```

### Complex Shapes

```javascript
// Nested shape
PropTypes.shape({
    axis: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.array,
        zoom: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.shape({
                minSpan: PropTypes.number,
                maxSpan: PropTypes.number,
            }),
        ]),
    }),
})

// Array of shapes
PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string,
    data: PropTypes.arrayOf(PropTypes.number),
    label: PropTypes.string,
}))
```

## Event Handling Patterns

### Click Events

```javascript
const handleClick = (event, data) => {
    if (setProps) {
        setProps({
            clickData: {
                timestamp: new Date().toISOString(),
                ...data,
            },
            n_clicks: (props.n_clicks || 0) + 1,
        });
    }
};
```

### Change Events

```javascript
const handleChange = (newValue) => {
    if (setProps) {
        setProps({ value: newValue });
    }
};
```

### Debounced Events

```javascript
import { useMemo } from 'react';
import debounce from 'lodash/debounce';

const debouncedSetProps = useMemo(
    () => debounce((updates) => {
        if (setProps) setProps(updates);
    }, 300),
    [setProps]
);

const handleInput = (e) => {
    debouncedSetProps({ value: e.target.value });
};
```

## Loading States

```javascript
const { loading_state } = props;

return (
    <div className={loading_state?.is_loading ? 'loading' : ''}>
        {loading_state?.is_loading && <Spinner />}
        {/* Component content */}
    </div>
);
```

### PropTypes for Loading

```javascript
loading_state: PropTypes.shape({
    is_loading: PropTypes.bool,
    prop_name: PropTypes.string,
    component_name: PropTypes.string,
})
```

## Styling Patterns

### Inline Styles

```javascript
const { style } = props;

return (
    <div style={{ padding: '10px', ...style }}>
        {/* Content */}
    </div>
);

// PropType
style: PropTypes.object
```

### Class Names

```javascript
const { className } = props;

return (
    <div className={`my-component ${className || ''}`}>
        {/* Content */}
    </div>
);

// PropType
className: PropTypes.string
```

## Children Pattern

```javascript
const { children } = props;

return (
    <div className="wrapper">
        {children}
    </div>
);

// PropType
children: PropTypes.node
```

## Refs and DOM Access

```javascript
import { useRef, useEffect } from 'react';

export default function ChartComponent(props) {
    const containerRef = useRef(null);

    useEffect(() => {
        if (containerRef.current) {
            // Access DOM element
            const width = containerRef.current.offsetWidth;
        }
    }, []);

    return <div ref={containerRef}>{/* Content */}</div>;
}
```

## Memoization

```javascript
import { useMemo, useCallback } from 'react';

// Memoize computed values
const processedData = useMemo(() => {
    return data.map(item => ({
        ...item,
        computed: item.value * 2,
    }));
}, [data]);

// Memoize callbacks
const handleClick = useCallback((e) => {
    if (setProps) {
        setProps({ clicked: true });
    }
}, [setProps]);
```

## Third-Party Library Integration

### Pattern for wrapping external libraries:

```javascript
import React, { useEffect, useRef } from 'react';
import ExternalLibrary from 'external-library';

export default function WrappedComponent(props) {
    const { config, setProps } = props;
    const containerRef = useRef(null);
    const instanceRef = useRef(null);

    // Initialize library on mount
    useEffect(() => {
        if (containerRef.current && !instanceRef.current) {
            instanceRef.current = new ExternalLibrary(containerRef.current, {
                ...config,
                onChange: (value) => {
                    if (setProps) setProps({ value });
                },
            });
        }

        // Cleanup on unmount
        return () => {
            if (instanceRef.current) {
                instanceRef.current.destroy();
            }
        };
    }, []);

    // Update library when config changes
    useEffect(() => {
        if (instanceRef.current) {
            instanceRef.current.update(config);
        }
    }, [config]);

    return <div ref={containerRef} />;
}
```

## Build Configuration

### webpack.config.js essentials

```javascript
module.exports = {
    entry: './src/lib/index.js',
    output: {
        path: path.resolve(__dirname, 'dash_component_name'),
        filename: 'dash_component_name.min.js',
        library: 'dash_component_name',
        libraryTarget: 'window',
    },
    externals: {
        react: 'React',
        'react-dom': 'ReactDOM',
    },
    // ... rest of config
};
```

### package.json scripts

```json
{
    "scripts": {
        "build:js": "webpack --mode production",
        "build:backends": "dash-generate-components ./src/lib/components component_name",
        "build": "npm run build:js && npm run build:backends",
        "watch": "webpack --mode development --watch"
    }
}
```

## Testing Components

### Basic test with pytest

```python
# tests/test_component.py
from dash import Dash, html
from dash.testing.application_runners import import_app

def test_component_renders(dash_duo):
    app = Dash(__name__)
    app.layout = html.Div([
        MyComponent(id='test', value='hello')
    ])

    dash_duo.start_server(app)
    dash_duo.wait_for_element('#test')
```

### Callback test

```python
def test_callback(dash_duo):
    app = Dash(__name__)
    app.layout = html.Div([
        MyComponent(id='input', value=''),
        html.Div(id='output')
    ])

    @app.callback(
        Output('output', 'children'),
        Input('input', 'value')
    )
    def update(value):
        return f'Value: {value}'

    dash_duo.start_server(app)
    # Test interaction
```

## Common Pitfalls

### 1. Missing setProps check

```javascript
// Bad - will crash if setProps is undefined
setProps({ value: newValue });

// Good - always check
if (setProps) {
    setProps({ value: newValue });
}
```

### 2. Mutating props directly

```javascript
// Bad - mutating prop
props.data.push(newItem);

// Good - create new reference
const newData = [...props.data, newItem];
if (setProps) setProps({ data: newData });
```

### 3. Missing PropTypes

All props must be defined in PropTypes for Dash to generate Python bindings.

### 4. Stale closures in useEffect

```javascript
// Bad - controlledValue might be stale
useEffect(() => {
    console.log(controlledValue);
}, [someProp]); // Missing controlledValue in deps

// Good - include all dependencies or use refs
```

### 5. Infinite loops with useEffect

```javascript
// Bad - causes infinite loop
useEffect(() => {
    setProps({ value: processedValue });
}, [processedValue]); // processedValue changes, triggers effect, changes value...

// Good - use condition or separate tracking state
```