# MUI X Tree View — Complete API Reference for Implementation

This file contains the exhaustive prop/slot/CSS-class surface extracted from the official MUI X documentation. Use this as the source-of-truth when implementing the Dash wrappers.

---

## RichTreeView Props (Community)

Source: `@mui/x-tree-view/RichTreeView`

| Prop | Type | Default | Description |
|---|---|---|---|
| `apiRef` | object | - | Ref for imperative API. Methods: `focusItem`, `getItem`, `getItemDOMElement`, `getItemOrderedChildrenIds`, `getItemTree`, `getParentId`, `isItemExpanded`, `setEditedItem`, `setIsItemDisabled`, `setItemExpansion`, `setItemSelection`, `updateItemLabel` |
| `checkboxSelection` | bool | `false` | Render checkbox at left of label |
| `classes` | object | - | CSS class overrides |
| `defaultExpandedItems` | string[] | `[]` | Uncontrolled expanded items |
| `defaultSelectedItems` | string \| string[] | `[]` | Uncontrolled selected items |
| `disabledItemsFocusable` | bool | `false` | Allow focus on disabled items |
| `disableSelection` | bool | `false` | Disable all selection |
| `expandedItems` | string[] | - | Controlled expanded items |
| `expansionTrigger` | `'content'` \| `'iconContainer'` | `'content'` | What triggers expansion |
| `getItemChildren` | `(item) => item[]` | `(item) => item.children` | Extract children from item |
| `getItemId` | `(item) => string` | `(item) => item.id` | Extract ID from item |
| `getItemLabel` | `(item) => string` | `(item) => item.label` | Extract label from item |
| `id` | string | - | Accessibility ID |
| `isItemDisabled` | `(item) => bool` | - | Per-item disabled check |
| `isItemEditable` | `(item) => bool` \| bool | `() => false` | Per-item editable check |
| `isItemSelectionDisabled` | `(item) => bool` | - | Per-item selection disabled check |
| `itemChildrenIndentation` | number \| string | `'12px'` | Horizontal indent |
| `items` | object[] | **required** | The data items array |
| `multiSelect` | bool | `false` | Enable multi-select |
| `onExpandedItemsChange` | `(event, itemIds) => void` | - | Fired on expand/collapse |
| `onItemClick` | `(event, itemId) => void` | - | Fired on content click |
| `onItemExpansionToggle` | `(event, itemId, isExpanded) => void` | - | Fired per-item expansion toggle |
| `onItemFocus` | `(event, itemId) => void` | - | Fired on item focus |
| `onItemLabelChange` | `(itemId, newLabel) => void` | - | Fired after label edit |
| `onItemSelectionToggle` | `(event, itemId, isSelected) => void` | - | Fired per-item selection toggle |
| `onSelectedItemsChange` | `(event, itemIds) => void` | - | Fired on selection change |
| `selectedItems` | string \| string[] | - | Controlled selection |
| `selectionPropagation` | `{descendants?: bool, parents?: bool}` | `{parents: false, descendants: false}` | Auto-propagate selection |
| `slotProps` | object | `{}` | Props for component slots |
| `slots` | object | `{}` | Overridable component slots |
| `sx` | object | - | MUI sx styling |

### RichTreeView Slots

| Slot | Class | Default | Description |
|---|---|---|---|
| `root` | `.MuiRichTreeView-root` | `RichTreeViewRoot` | Root element |
| `collapseIcon` | - | - | Icon to collapse |
| `expandIcon` | - | - | Icon to expand |
| `endIcon` | - | - | Icon for leaf nodes |
| `item` | `.MuiRichTreeView-item` | `TreeItem` | Item component |

### RichTreeView CSS Classes

| Class | Description |
|---|---|
| `.MuiRichTreeView-itemCheckbox` | Checkbox element |
| `.MuiRichTreeView-itemContent` | Content element |
| `.MuiRichTreeView-itemGroupTransition` | Transition element |
| `.MuiRichTreeView-itemIconContainer` | Icon container |
| `.MuiRichTreeView-itemLabel` | Label element |
| `.MuiRichTreeView-itemLabelInput` | Label input (editing) |

---

## RichTreeViewPro Props (Pro)

Source: `@mui/x-tree-view-pro/RichTreeViewPro`

**Inherits all RichTreeView props, plus:**

| Prop | Type | Default | Description |
|---|---|---|---|
| `canMoveItemToNewPosition` | `({itemId, oldPosition, newPosition}) => bool` | - | Validate reorder moves |
| `dataSource` | `{getChildrenCount: func, getTreeItems: func}` | - | Lazy loading data source |
| `dataSourceCache` | `{clear, get, set}` | - | Cache for lazy loading |
| `isItemReorderable` | `(itemId) => bool` | `() => true` | Per-item reorder check |
| `itemsReordering` | bool | `false` | Enable drag-and-drop |
| `onItemPositionChange` | `({itemId, oldPosition, newPosition}) => void` | - | Fired after reorder |

**Additional apiRef methods:** `updateItemChildren`

### RichTreeViewPro Additional CSS Classes

| Class | Description |
|---|---|
| `.MuiRichTreeViewPro-itemDragAndDropOverlay` | DnD overlay |
| `.MuiRichTreeViewPro-itemErrorIcon` | Error icon (lazy load) |
| `.MuiRichTreeViewPro-itemLoadingIcon` | Loading icon (lazy load) |

---

## SimpleTreeView Props (Community)

Source: `@mui/x-tree-view/SimpleTreeView`

Same as RichTreeView but **without**: `items`, `getItemId`, `getItemLabel`, `getItemChildren`, `isItemDisabled`, `isItemEditable`, `isItemSelectionDisabled`, `selectionPropagation`.

Items are passed as `<TreeItem>` JSX children instead.

---

## TreeItem Props

Source: `@mui/x-tree-view/TreeItem`

| Prop | Type | Default | Description |
|---|---|---|---|
| `itemId`* | string | - | Unique item identifier |
| `children` | any | - | Nested TreeItem children |
| `classes` | object | - | CSS overrides |
| `disabled` | bool | `false` | Disable this item |
| `disableSelection` | bool | `false` | Disable selection for this item |
| `id` | string | - | DOM id attribute |
| `label` | node | - | Item label content |
| `onBlur` | func | - | Blur callback |
| `onKeyDown` | func | - | Keydown callback |
| `slotProps` | object | `{}` | Slot props |
| `slots` | object | `{}` | Overridable slots |
| `sx` | object | - | MUI sx styling |

### TreeItem Slots

| Slot | Class | Default | Description |
|---|---|---|---|
| `root` | `.MuiTreeItem-root` | `TreeItemRoot` | Root element |
| `content` | `.MuiTreeItem-content` | `TreeItemContent` | Content wrapper |
| `groupTransition` | `.MuiTreeItem-groupTransition` | `TreeItemGroupTransition` | Children container |
| `iconContainer` | `.MuiTreeItem-iconContainer` | `TreeItemIconContainer` | Icon wrapper |
| `checkbox` | `.MuiTreeItem-checkbox` | `TreeItemCheckbox` | Selection checkbox |
| `label` | `.MuiTreeItem-label` | `TreeItemLabel` | Label element |
| `labelInput` | `.MuiTreeItem-labelInput` | `TreeItemLabelInput` | Edit input |
| `dragAndDropOverlay` | `.MuiTreeItem-dragAndDropOverlay` | `TreeItemDragAndDropOverlay` | DnD overlay (Pro only) |
| `errorIcon` | `.MuiTreeItem-errorIcon` | `TreeItemErrorContainer` | Error state (Pro lazy) |
| `loadingIcon` | `.MuiTreeItem-loadingIcon` | `TreeItemLoadingContainer` | Loading state (Pro lazy) |
| `collapseIcon` | - | - | Collapse icon |
| `expandIcon` | - | - | Expand icon |
| `endIcon` | - | - | Leaf icon |
| `icon` | - | - | Item icon |

### TreeItem CSS State Classes

| Class | Attribute | Description |
|---|---|---|
| `.Mui-disabled` | `data-disabled` | Disabled state |
| `.Mui-expanded` | `data-expanded` | Expanded state |
| `.Mui-focused` | `data-focused` | Focused state |
| `.Mui-selected` | `data-selected` | Selected state |
| `.MuiTreeItem-editable` | `data-editable` | Editable state |
| `.MuiTreeItem-editing` | `data-editing` | Currently editing |

---

## Feature Matrix

| Feature | SimpleTreeView | RichTreeView | RichTreeViewPro |
|---|---|---|---|
| Static items (JSX) | ✅ | ❌ | ❌ |
| Data-driven items | ❌ | ✅ | ✅ |
| Selection (single/multi) | ✅ | ✅ | ✅ |
| Checkbox selection | ✅ | ✅ | ✅ |
| Selection propagation | Limited¹ | ✅ | ✅ |
| Expansion (controlled) | ✅ | ✅ | ✅ |
| Expansion trigger config | ✅ | ✅ | ✅ |
| Item disabled | ✅ | ✅ | ✅ |
| Focus management | ✅ | ✅ | ✅ |
| Keyboard navigation | ✅ | ✅ | ✅ |
| Label editing | ❌ | ✅ | ✅ |
| Custom icons | ✅ | ✅ | ✅ |
| Item indentation | ✅ | ✅ | ✅ |
| Imperative API | ❌ | ✅ | ✅ |
| Drag-and-drop ordering | ❌ | ❌ | ✅ |
| Lazy loading (dataSource) | ❌ | ❌ | ✅ |
| Virtualization | ❌ | ❌ | ✅ (v9) |
| Custom item rendering | Via slots | Via slots | Via slots |

¹ SimpleTreeView only considers expanded items for propagation.

---

## Accessibility (WAI-ARIA)

All Tree View components follow the WAI-ARIA tree view pattern:
- `role="tree"` on the root
- `role="treeitem"` on each item
- `aria-expanded` on expandable items
- `aria-selected` on selectable items
- Keyboard: Arrow keys for navigation, Enter to expand/select, Space for selection, Home/End for first/last, `*` to expand all siblings
- Type-ahead: typing a character focuses the next item starting with that character

The Dash wrapper MUST pass `aria-label` or `aria-labelledby` to the root component. Expose this as a Dash prop.
