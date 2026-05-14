# MUI X Tree View — Dash Integration Plan

## Overview

Extend `dash-mui-charts` to include MUI X Tree View components, following the same patterns used for chart components (license key gating, output props for Dash callbacks, controlled/uncontrolled state).

The MUI X Tree View has **three component tiers**:

| Component | Package | License | Key Features |
|---|---|---|---|
| `SimpleTreeView` | `@mui/x-tree-view` | Community (Free) | JSX children-based, hardcoded items |
| `RichTreeView` | `@mui/x-tree-view` | Community (Free) | Data-driven items, label editing, selection propagation |
| `RichTreeViewPro` | `@mui/x-tree-view-pro` | Pro | Drag-and-drop ordering, lazy loading, virtualization, dataSource |

---

## Phase 1: `RichTreeView` (Community — Free)

This is the primary component. Data-driven, supports all core features, and maps cleanly to Dash's prop-driven model.

### Dash Component: `TreeView`

**File:** `src/lib/components/TreeView.react.js`

#### Props → MUI Mapping

**Data Props (Input):**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `id` | string | `id` | Standard Dash id |
| `items` | list[dict] | `items` | Array of `{id, label, children?, ...custom}` |
| `getItemId` | string | `getItemId` | Property name to use as id (default: `"id"`) — converted to function in JS |
| `getItemLabel` | string | `getItemLabel` | Property name for label (default: `"label"`) — converted to function in JS |
| `getItemChildren` | string | `getItemChildren` | Property name for children (default: `"children"`) — converted to function in JS |

**Selection Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `selectedItems` | string \| list[string] | `selectedItems` | Controlled selection |
| `defaultSelectedItems` | string \| list[string] | `defaultSelectedItems` | Uncontrolled default |
| `multiSelect` | bool | `multiSelect` | Enable multi-select (default: `false`) |
| `checkboxSelection` | bool | `checkboxSelection` | Render checkboxes (default: `false`) |
| `disableSelection` | bool | `disableSelection` | Disable all selection |
| `selectionPropagation` | dict | `selectionPropagation` | `{parents: bool, descendants: bool}` |

**Expansion Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `expandedItems` | list[string] | `expandedItems` | Controlled expansion |
| `defaultExpandedItems` | list[string] | `defaultExpandedItems` | Uncontrolled default |
| `expansionTrigger` | string | `expansionTrigger` | `"content"` or `"iconContainer"` |

**Editing Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `isItemEditable` | bool | `isItemEditable` | Enable editing on all items |
| `editableItems` | list[string] | — | Custom: list of item IDs that are editable (converted to function in JS) |

**Disabled Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `disabledItems` | list[string] | — | Custom: list of disabled item IDs (converted to `isItemDisabled` function) |
| `disabledItemsFocusable` | bool | `disabledItemsFocusable` | Allow focusing disabled items |

**Appearance Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `itemChildrenIndentation` | number \| string | `itemChildrenIndentation` | e.g. `24`, `"24px"`, `"2rem"` |
| `height` | number | — | CSS height on wrapper |
| `sx` | dict | `sx` | MUI sx styling object |

**Slot/Icon Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `collapseIcon` | string | `slots.collapseIcon` | Icon name string → resolved in JS |
| `expandIcon` | string | `slots.expandIcon` | Icon name string → resolved in JS |
| `endIcon` | string | `slots.endIcon` | Icon name string → resolved in JS |

**Output Props (for Dash callbacks):**

| Dash Prop | Type | Fires On | Notes |
|---|---|---|---|
| `selectedItems` | string \| list[string] | Selection change | Controlled + output |
| `expandedItems` | list[string] | Expansion change | Controlled + output |
| `clickedItem` | dict | Item click | `{itemId, event_timestamp}` |
| `focusedItem` | dict | Item focus | `{itemId, event_timestamp}` |
| `editedItemLabel` | dict | Label edit complete | `{itemId, newLabel, event_timestamp}` |

---

## Phase 2: `RichTreeViewPro` (Pro — License Key)

### Dash Component: `TreeViewPro`

**File:** `src/lib/components/TreeViewPro.react.js`

Inherits ALL props from `TreeView` plus:

**Pro-Only Props:**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `licenseKey` | string | — | MUI Pro license key |
| `itemsReordering` | bool | `itemsReordering` | Enable drag-and-drop reordering |
| `reorderableItems` | list[string] | — | Custom: item IDs that can be reordered (→ `isItemReorderable`) |

**Pro Output Props:**

| Dash Prop | Type | Fires On | Notes |
|---|---|---|---|
| `itemPositionChanged` | dict | After reorder | `{itemId, oldPosition: {parentId, index}, newPosition: {parentId, index}}` |

**Lazy Loading Props (Pro):**

| Dash Prop | Type | MUI Prop | Notes |
|---|---|---|---|
| `lazyLoading` | bool | — | If true, enables dataSource mode |
| `lazyLoadedChildren` | dict | — | Dash-managed: `{parentItemId: [children]}` — written by callbacks |

> **Note on lazy loading:** MUI's `dataSource` API expects async JS functions. For Dash, we implement a pattern where: expanding an unloaded node fires an output prop `lazyLoadRequest` with the parent item ID, a Dash callback responds by updating `lazyLoadedChildren`, and the JS component merges the children into the tree. This is the same pattern used for server-side callbacks in DataTable.

**Lazy Loading Output Props:**

| Dash Prop | Type | Fires On | Notes |
|---|---|---|---|
| `lazyLoadRequest` | dict | Expand unloaded node | `{itemId, event_timestamp}` |

---

## Phase 3: `SimpleTreeView` (Community — Free)

### Dash Component: `SimpleTreeView`

**File:** `src/lib/components/SimpleTreeView.react.js`

This component uses JSX children (`TreeItem`). For Dash, we convert a flat/nested data structure into TreeItem children internally — the user passes data, not JSX.

**Props:** Same selection/expansion/focus/disabled props as `TreeView`, but `items` uses a simpler structure since it maps to `<TreeItem>` children:

```python
items=[
    {"itemId": "1", "label": "Parent", "children": [
        {"itemId": "1.1", "label": "Child"},
    ]},
]
```

The `itemId` and `label` props map directly to `<TreeItem itemId={...} label={...}>`.

**Additional TreeItem-level props exposed per item:**

| Per-Item Field | Type | Maps To |
|---|---|---|
| `disabled` | bool | `<TreeItem disabled>` |
| `disableSelection` | bool | `<TreeItem disableSelection>` |

---

## File Structure

```
src/lib/components/
├── TreeView.react.js          # RichTreeView wrapper (Community)
├── TreeViewPro.react.js       # RichTreeViewPro wrapper (Pro)
├── SimpleTreeView.react.js    # SimpleTreeView wrapper (Community)
├── fragments/
│   ├── TreeViewBase.js        # Shared logic (selection, expansion, focus, callbacks)
│   ├── TreeItemRenderer.js    # Recursive TreeItem renderer for SimpleTreeView
│   └── iconResolver.js        # Maps icon name strings to MUI icons
```

```
dash_mui_charts/
├── TreeView.py                # Auto-generated Python class
├── TreeViewPro.py             # Auto-generated Python class
├── SimpleTreeView.py          # Auto-generated Python class
```

```
docs/dash_mui_charts/
├── tree_basic.py              # Basic RichTreeView demo
├── tree_selection.py          # Selection modes demo
├── tree_editing.py            # Label editing demo
├── tree_pro.py                # Pro features (ordering, lazy load)
```

---

## npm Dependencies

Add to `package.json`:

```json
{
  "dependencies": {
    "@mui/x-tree-view": "^7.x || ^8.x || ^9.x",
    "@mui/x-tree-view-pro": "^7.x || ^8.x || ^9.x",
    "@mui/material": "^5.x || ^6.x",
    "@emotion/react": "^11.x",
    "@emotion/styled": "^11.x"
  }
}
```

Check the existing `package.json` — `@mui/material` and `@emotion/*` are likely already present from the chart components. The tree-view packages are the new additions.

---

## Implementation Order

### Step 1 — Scaffold & Shared Logic
1. Create `fragments/TreeViewBase.js` with shared prop-to-MUI conversion utilities
2. Create `fragments/iconResolver.js` for icon string → component mapping
3. Add npm dependencies

### Step 2 — `TreeView` (RichTreeView Community)
1. Create `TreeView.react.js` with full prop surface
2. Wire selection (controlled + output), expansion (controlled + output), click, focus callbacks
3. Wire label editing with `editedItemLabel` output prop
4. Add `isItemDisabled` / `isItemEditable` function conversion from list props
5. Run `npm run build` to generate Python class
6. Write `tree_basic.py` and `tree_selection.py` docs

### Step 3 — `SimpleTreeView`
1. Create `SimpleTreeView.react.js`
2. Create `fragments/TreeItemRenderer.js` for recursive `<TreeItem>` rendering from items data
3. Wire same selection/expansion/focus outputs
4. Build + test

### Step 4 — `TreeViewPro` (Pro)
1. Create `TreeViewPro.react.js` extending TreeView logic
2. Add license key gating (same pattern as chart Pro components)
3. Wire `itemsReordering`, `onItemPositionChange` → `itemPositionChanged` output
4. Implement lazy loading bridge pattern (`lazyLoadRequest` output → `lazyLoadedChildren` input)
5. Write `tree_pro.py` docs

### Step 5 — Polish & Docs
1. Update `llms.txt` with TreeView component documentation
2. Add TreeView to the main `__init__.py` exports
3. Write comprehensive property tables in docs
4. Bump version

---

## Callback Patterns (Python Usage Examples)

### Basic TreeView

```python
from dash_mui_charts import TreeView

TreeView(
    id="my-tree",
    items=[
        {"id": "grid", "label": "Data Grid", "children": [
            {"id": "grid-com", "label": "@mui/x-data-grid"},
            {"id": "grid-pro", "label": "@mui/x-data-grid-pro"},
        ]},
        {"id": "pickers", "label": "Date Pickers"},
        {"id": "charts", "label": "Charts"},
    ],
    defaultExpandedItems=["grid"],
    multiSelect=True,
    checkboxSelection=True,
    selectionPropagation={"parents": True, "descendants": True},
)
```

### Controlled Selection via Callback

```python
@callback(
    Output("selected-display", "children"),
    Input("my-tree", "selectedItems"),
)
def show_selection(selected):
    return f"Selected: {selected}"
```

### Label Editing

```python
TreeView(
    id="editable-tree",
    items=[...],
    isItemEditable=True,
)

@callback(
    Output("edit-log", "children"),
    Input("editable-tree", "editedItemLabel"),
)
def on_edit(edit_data):
    if not edit_data:
        return "No edits yet"
    return f"Item {edit_data['itemId']} → {edit_data['newLabel']}"
```

### Pro: Drag-and-Drop Ordering

```python
from dash_mui_charts import TreeViewPro

TreeViewPro(
    id="reorderable-tree",
    licenseKey=os.getenv("MUI_PRO_API_KEY", ""),
    items=[...],
    itemsReordering=True,
    defaultExpandedItems=["grid", "pickers"],
)

@callback(
    Output("reorder-log", "children"),
    Input("reorderable-tree", "itemPositionChanged"),
)
def on_reorder(pos):
    if not pos:
        return "No reorders yet"
    return f"{pos['itemId']} moved from {pos['oldPosition']} to {pos['newPosition']}"
```

### Pro: Lazy Loading

```python
TreeViewPro(
    id="lazy-tree",
    licenseKey=os.getenv("MUI_PRO_API_KEY", ""),
    items=[
        {"id": "root", "label": "Root", "children": []},  # empty = unloaded
    ],
    lazyLoading=True,
)

@callback(
    Output("lazy-tree", "lazyLoadedChildren"),
    Input("lazy-tree", "lazyLoadRequest"),
    prevent_initial_call=True,
)
def load_children(request):
    parent_id = request["itemId"]
    # Fetch from DB, API, etc.
    children = fetch_children_from_server(parent_id)
    return {parent_id: children}
```

---

## Key Architecture Decisions

1. **`getItemId` / `getItemLabel` / `getItemChildren` as strings, not functions.**
   Dash can't serialize JS functions. We pass the property name as a string (e.g. `"name"`) and convert to `(item) => item.name` in the React wrapper.

2. **`isItemDisabled` / `isItemEditable` / `isItemReorderable` as lists of IDs.**
   Instead of passing functions, Dash users pass `disabledItems=["id1", "id2"]` and the React wrapper converts to `(item) => disabledItems.includes(getItemId(item))`. Boolean `isItemEditable=True` enables editing for all items.

3. **Lazy loading via Dash callback bridge.**
   MUI's `dataSource.getTreeItems` is async JS. We bridge this by: the JS component detects an expansion of a node with no children → fires `lazyLoadRequest` output → Dash callback fetches data → writes `lazyLoadedChildren` → JS component merges into tree state.

4. **License key gating follows the existing chart pattern.**
   `TreeViewPro` accepts `licenseKey` prop, imports from `@mui/x-tree-view-pro`, and the component is a separate file to enable tree-shaking.

5. **Virtualization (Pro v9+).**
   `RichTreeViewPro` supports virtualization in v9. Since this requires the parent container to have intrinsic dimensions, we expose a `height` prop that sets the container style. This is gated behind `licenseKey`.
