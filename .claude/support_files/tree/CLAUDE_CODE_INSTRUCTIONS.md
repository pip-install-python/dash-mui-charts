# Claude Code — Tree View Implementation Instructions

## Context

You are implementing MUI X Tree View components within the `dash-mui-charts` Dash component library. The project already has chart components (LineChart, PieChart, ScatterChart, etc.) — follow the same patterns.

## Files Provided

- `IMPLEMENTATION_PLAN.md` — Full architecture, phases, prop mappings, callback patterns
- `API_REFERENCE.md` — Exhaustive MUI X Tree View API surface (props, slots, CSS classes)
- `stubs/TreeView.react.js` — Near-complete React stub for RichTreeView wrapper
- `stubs/TreeViewPro.react.js` — Near-complete React stub for RichTreeViewPro wrapper
- `stubs/SimpleTreeView.react.js` — React stub for SimpleTreeView wrapper
- `stubs/fragments/iconResolver.js` — Icon name → MUI component resolver

## Execution Steps

### 1. Check existing project structure
```bash
ls src/lib/components/         # See existing chart component files
cat package.json               # Check existing MUI dependencies
cat src/lib/index.js           # See how components are exported
cat dash_mui_charts/__init__.py # See Python exports
```

### 2. Install new dependencies
```bash
npm install @mui/x-tree-view @mui/x-tree-view-pro @mui/icons-material
```

Note: Check if `@mui/material`, `@emotion/react`, `@emotion/styled` are already installed. If not, install them too. Also check version compatibility — the tree view v9 requires MUI v6+, v8 works with MUI v5+.

### 3. Copy stub files into project
- Copy `TreeView.react.js` → `src/lib/components/TreeView.react.js`
- Copy `TreeViewPro.react.js` → `src/lib/components/TreeViewPro.react.js`
- Copy `SimpleTreeView.react.js` → `src/lib/components/SimpleTreeView.react.js`
- Copy `fragments/iconResolver.js` → `src/lib/components/fragments/iconResolver.js`

### 4. Complete the stubs

The stubs are ~80% complete. Key items to finish:

**TreeView.react.js:**
- Verify the MUI import paths match the installed version
- Test that `getItemId`/`getItemLabel`/`getItemChildren` string→function conversion works
- Add `isItemSelectionDisabled` support (list of item IDs, same pattern as `disabledItems`)
- Ensure the license key is NOT needed for this component (it's Community)

**TreeViewPro.react.js:**
- Implement the lazy loading bridge:
  1. Maintain internal state `mergedItems` that starts as `props.items`
  2. On expansion of a node where `getItemChildren(item)` is empty/null, fire `setProps({lazyLoadRequest: {itemId, event_timestamp}})`
  3. When `props.lazyLoadedChildren` changes, deep-merge the new children into `mergedItems`
  4. Pass `mergedItems` to `RichTreeViewPro` instead of `props.items`
- Add license key activation (look at how existing Pro chart components like Heatmap do it — likely `import { LicenseInfo } from '@mui/x-license'` + `LicenseInfo.setLicenseKey(key)`)
- Wire `canMoveItemToNewPosition` if you want to expose it (optional for v1)

**SimpleTreeView.react.js:**
- Verify the recursive `renderItems` function handles edge cases (empty arrays, undefined children)
- Add `onItemFocus` callback

**iconResolver.js:**
- Expand with more icons as needed
- Consider whether to use dynamic imports for tree-shaking

### 5. Register components

**`src/lib/index.js`:**
```js
export {default as TreeView} from './components/TreeView.react';
export {default as TreeViewPro} from './components/TreeViewPro.react';
export {default as SimpleTreeView} from './components/SimpleTreeView.react';
```

### 6. Build
```bash
npm run build
```
This generates the Python class files in `dash_mui_charts/`.

### 7. Verify Python classes
```bash
cat dash_mui_charts/TreeView.py
cat dash_mui_charts/TreeViewPro.py
cat dash_mui_charts/SimpleTreeView.py
```

### 8. Update `__init__.py`
Add the new components to the `__all__` list and imports.

### 9. Write usage tests
Create `usage_tree.py`:
```python
import dash
from dash import html, callback, Input, Output
from dash_mui_charts import TreeView

app = dash.Dash(__name__)
app.layout = html.Div([
    TreeView(
        id="test-tree",
        items=[
            {"id": "1", "label": "Node 1", "children": [
                {"id": "1.1", "label": "Child 1.1"},
                {"id": "1.2", "label": "Child 1.2"},
            ]},
            {"id": "2", "label": "Node 2"},
        ],
        defaultExpandedItems=["1"],
        multiSelect=True,
        checkboxSelection=True,
    ),
    html.Pre(id="output"),
])

@callback(Output("output", "children"), Input("test-tree", "selectedItems"))
def show(sel):
    return str(sel)

if __name__ == "__main__":
    app.run(debug=True)
```

### 10. Write docs
Create documentation files following the existing pattern in `docs/dash_mui_charts/`:
- `tree_basic.py` — Basic usage, items, expansion, selection
- `tree_selection.py` — Multi-select, checkbox, propagation
- `tree_editing.py` — Label editing, callbacks
- `tree_pro.py` — Pro features: ordering, lazy load

## Key Gotchas

1. **MUI version compatibility**: Tree View v9 (latest) may require MUI v6. Check `package.json` for what version of `@mui/material` is already installed. If it's v5, use `@mui/x-tree-view@^7` or `@mui/x-tree-view@^8`.

2. **Emotion/styled-components**: The project likely uses Emotion already for charts. Make sure there's no conflict.

3. **Bundle size**: `@mui/icons-material` is large. Only import the specific icons used in `iconResolver.js`. Do NOT import the entire package.

4. **Controlled vs uncontrolled**: Both `selectedItems` and `expandedItems` work as both input AND output props in Dash. When Dash sends a new value, it's controlled input. When the user interacts, the callback fires `setProps` to update the value as output. This is the standard Dash pattern.

5. **License key**: Follow the exact same pattern used by the existing Pro chart components (Heatmap, LineChart zoom/brush). Look at how `licenseKey` is consumed there.

6. **`selectionPropagation` only works with `multiSelect=true`**: Document this clearly.

7. **Virtualization (v9+)**: Requires the parent to have explicit height/width. The `height` prop on the Dash component sets this on the wrapper div.
