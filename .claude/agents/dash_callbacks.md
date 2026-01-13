# Dash Callbacks Agent

Reference guide for Dash callbacks, patterns, and advanced features including Dash 3.3.0 enhancements.

## Basic Callback Pattern

```python
from dash import Dash, html, dcc, callback, Input, Output

@callback(
    Output('output-id', 'children'),
    Input('input-id', 'value')
)
def update_output(value):
    return f'You entered: {value}'
```

## Multiple Outputs

```python
@callback(
    Output('output-1', 'children'),
    Output('output-2', 'style'),
    Input('input-id', 'value')
)
def update_multiple(value):
    return f'Value: {value}', {'color': 'blue'}
```

## State vs Input

- **Input**: Triggers callback when value changes
- **State**: Provides value but does NOT trigger callback

```python
@callback(
    Output('output', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('text-input', 'value'),
    prevent_initial_call=True
)
def submit_form(n_clicks, text_value):
    return f'Submitted: {text_value}'
```

## Context (ctx) - Determine What Triggered

```python
from dash import ctx

@callback(
    Output('output', 'children'),
    Input('btn-1', 'n_clicks'),
    Input('btn-2', 'n_clicks'),
)
def handle_buttons(btn1, btn2):
    triggered_id = ctx.triggered_id
    if triggered_id == 'btn-1':
        return 'Button 1 clicked'
    elif triggered_id == 'btn-2':
        return 'Button 2 clicked'
    return 'No button clicked yet'
```

### ctx Properties

- `ctx.triggered_id` - ID of component that triggered (string or dict for pattern-matching)
- `ctx.triggered` - List of changed props with values
- `ctx.inputs` - Dict of all input values
- `ctx.states` - Dict of all state values
- `ctx.args_grouping` - Arguments grouped by Input/State

## Preventing Initial Call

```python
@callback(
    Output('output', 'children'),
    Input('input', 'value'),
    prevent_initial_call=True  # Don't fire on page load
)
```

## no_update - Skip Output Updates

```python
from dash import no_update

@callback(
    Output('output-1', 'children'),
    Output('output-2', 'children'),
    Input('input', 'value')
)
def selective_update(value):
    if not value:
        return no_update, no_update
    return value, no_update  # Only update first output
```

## Patch - Partial Updates (Dash 3.3.0+)

For large data or complex state, use `Patch()` to update only specific parts:

```python
from dash import Patch

@callback(
    Output('figure-graph', 'figure'),
    Input('color-picker', 'value')
)
def update_color(color):
    patched = Patch()
    patched['layout']['paper_bgcolor'] = color
    return patched
```

### Patch Operations

```python
# Update nested value
patched = Patch()
patched['data'][0]['marker']['color'] = 'red'

# Append to list
patched['data'].append(new_trace)

# Prepend to list
patched['data'].prepend(new_trace)

# Insert at index
patched['data'].insert(1, new_trace)

# Extend list
patched['data'].extend([trace1, trace2])

# Remove item
patched['data'].remove(existing_trace)

# Delete key
del patched['layout']['title']

# Reverse list
patched['data'].reverse()

# Clear list
patched['data'].clear()
```

## set_props - Direct Property Updates (Dash 3.3.0+)

Update component properties without traditional callback:

```python
from dash import set_props

@callback(
    Output('main-output', 'children'),
    Input('trigger', 'n_clicks')
)
def update_multiple_components(n):
    # Update another component directly
    set_props('status-indicator', {'children': 'Processing...', 'style': {'color': 'orange'}})

    # Do some work...

    set_props('status-indicator', {'children': 'Complete!', 'style': {'color': 'green'}})

    return f'Processed {n} times'
```

### set_props with Component IDs

```python
# Simple string ID
set_props('my-component', {'value': 42})

# Pattern-matching ID (dict)
set_props({'type': 'dynamic', 'index': 0}, {'children': 'Updated'})
```

## Running Callback States

Track long-running callbacks:

```python
@callback(
    Output('output', 'children'),
    Input('trigger', 'n_clicks'),
    running=[
        (Output('trigger', 'disabled'), True, False),  # Disable button while running
        (Output('status', 'children'), 'Running...', 'Ready'),
    ],
    prevent_initial_call=True
)
def long_running_task(n):
    import time
    time.sleep(5)
    return 'Done!'
```

## Progress Updates

```python
@callback(
    Output('output', 'children'),
    Input('trigger', 'n_clicks'),
    progress=[Output('progress-bar', 'value')],
    prevent_initial_call=True
)
def task_with_progress(set_progress, n):
    for i in range(10):
        set_progress((i + 1) * 10)
        time.sleep(0.5)
    return 'Complete!'
```

## Circular Callbacks (Dash 2.9+)

Allow callbacks that form circular dependencies:

```python
@callback(
    Output('input-a', 'value'),
    Input('input-b', 'value'),
    prevent_initial_call=True
)
def sync_a_from_b(b_value):
    return b_value * 2

@callback(
    Output('input-b', 'value'),
    Input('input-a', 'value'),
    prevent_initial_call=True
)
def sync_b_from_a(a_value):
    return a_value / 2
```

**Important**: Must use `prevent_initial_call=True` to avoid infinite loops.

## Pattern Matching Callbacks

Dynamic callbacks for components with dict IDs:

```python
from dash import ALL, MATCH, ALLSMALLER

# ALL - Target all components matching pattern
@callback(
    Output('output', 'children'),
    Input({'type': 'button', 'index': ALL}, 'n_clicks')
)
def handle_all_buttons(all_clicks):
    return f'Total clicks: {sum(c or 0 for c in all_clicks)}'

# MATCH - Target same index
@callback(
    Output({'type': 'output', 'index': MATCH}, 'children'),
    Input({'type': 'input', 'index': MATCH}, 'value')
)
def sync_matched(value):
    return f'Value: {value}'
```

## Background Callbacks

For long-running tasks without blocking:

```python
from dash import DiskcacheManager
import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, background_callback_manager=background_callback_manager)

@callback(
    Output('output', 'children'),
    Input('trigger', 'n_clicks'),
    background=True,
    prevent_initial_call=True
)
def long_task(n):
    import time
    time.sleep(10)
    return f'Completed task {n}'
```

## Clientside Callbacks

Run JavaScript in browser for performance:

```python
from dash import clientside_callback, ClientsideFunction

# Inline JavaScript
clientside_callback(
    """
    function(value) {
        return value * 2;
    }
    """,
    Output('output', 'children'),
    Input('input', 'value')
)

# External JS file (assets/callbacks.js)
clientside_callback(
    ClientsideFunction(
        namespace='my_functions',
        function_name='multiply_by_two'
    ),
    Output('output', 'children'),
    Input('input', 'value')
)
```

## Component Property Patterns for Dash-React

When building React components for Dash:

### setProps Pattern

```javascript
// React component
export default function MyComponent({ id, value, setProps }) {
    const handleChange = (newValue) => {
        if (setProps) {
            setProps({ value: newValue });
        }
    };

    return <input value={value} onChange={e => handleChange(e.target.value)} />;
}

MyComponent.propTypes = {
    id: PropTypes.string,
    value: PropTypes.string,
    setProps: PropTypes.func,
};
```

### Controlled Component Pattern

For components with internal state that sync with Dash:

```javascript
const [internalState, setInternalState] = useState(props.value);

// Sync external prop changes to internal state
useEffect(() => {
    if (props.value !== internalState) {
        setInternalState(props.value);
    }
}, [props.value]);

// Update both internal state and Dash
const handleChange = (newValue) => {
    setInternalState(newValue);
    if (setProps) {
        setProps({ value: newValue });
    }
};
```

## Best Practices

1. **Use `prevent_initial_call=True`** when callback doesn't need to run on page load
2. **Use `no_update`** to skip unnecessary updates
3. **Use `Patch()`** for large data updates instead of returning full objects
4. **Use `set_props`** for side-effect updates to other components
5. **Use `ctx.triggered_id`** to determine which input fired
6. **Avoid circular callbacks** unless absolutely necessary
7. **Use clientside callbacks** for simple transformations that don't need server