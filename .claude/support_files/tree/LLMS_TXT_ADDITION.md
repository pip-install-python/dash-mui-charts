# Tree View Components — llms.txt Addition

Append this section to the existing `llms.txt` for dash_mui_charts.

---

## Tree View

| Component | License | Key Features |
|:----------|:--------|:-------------|
| **TreeView** | Free | Data-driven tree, selection (single/multi/checkbox), expansion, label editing, focus, disabled items, custom icons |
| **TreeViewPro** | Pro | All Free features + drag-and-drop reordering, lazy loading, virtualization |
| **SimpleTreeView** | Free | Static item definition, selection, expansion, focus — lighter alternative |

### TreeView Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `items` | list | Required | Array of `{id, label, children?, ...}` objects |
| `getItemId` | string | `"id"` | Property name for item ID |
| `getItemLabel` | string | `"label"` | Property name for item label |
| `getItemChildren` | string | `"children"` | Property name for item children |
| `selectedItems` | string \| list | `None` | Controlled selected item(s) — string if single, list if multi |
| `defaultSelectedItems` | string \| list | `[]` | Default selection (uncontrolled) |
| `multiSelect` | bool | `False` | Allow multiple item selection |
| `checkboxSelection` | bool | `False` | Show selection checkboxes |
| `disableSelection` | bool | `False` | Disable all selection |
| `selectionPropagation` | dict | `None` | `{parents: bool, descendants: bool}` — auto-propagate selection |
| `expandedItems` | list | `None` | Controlled expanded item IDs |
| `defaultExpandedItems` | list | `[]` | Default expanded items (uncontrolled) |
| `expansionTrigger` | string | `"content"` | `"content"` or `"iconContainer"` |
| `isItemEditable` | bool | `False` | Enable label editing on all items |
| `editableItems` | list | `None` | Item IDs that are editable |
| `disabledItems` | list | `None` | Item IDs that are disabled |
| `disabledItemsFocusable` | bool | `False` | Allow focus on disabled items |
| `itemChildrenIndentation` | number \| string | `"12px"` | Horizontal indent |
| `height` | number \| string | `None` | Container height |
| `collapseIcon` | string | `None` | MUI icon name for collapse |
| `expandIcon` | string | `None` | MUI icon name for expand |
| `endIcon` | string | `None` | MUI icon name for leaf nodes |
| `clickedItem` | dict | Output | `{itemId, event_timestamp}` |
| `focusedItem` | dict | Output | `{itemId, event_timestamp}` |
| `editedItemLabel` | dict | Output | `{itemId, newLabel, event_timestamp}` |

### TreeViewPro Properties (inherits all TreeView props)

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `licenseKey` | string | `""` | MUI Pro license key |
| `itemsReordering` | bool | `False` | Enable drag-and-drop reordering |
| `reorderableItems` | list | `None` | Item IDs that can be reordered |
| `lazyLoading` | bool | `False` | Enable lazy loading mode |
| `lazyLoadedChildren` | dict | `None` | `{parentId: [children]}` — loaded by callback |
| `lazyLoadRequest` | dict | Output | `{itemId, event_timestamp}` — fires when unloaded node expands |
| `itemPositionChanged` | dict | Output | `{itemId, oldPosition, newPosition, event_timestamp}` |

### SimpleTreeView Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `items` | list | Required | Array of `{itemId, label, children?, disabled?, disableSelection?}` |
| Same selection/expansion/icon props as TreeView | | | |
