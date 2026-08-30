---
name: Tree Basic
description: "TreeView basics for Dash: data-driven items, defaultExpandedItems, click and focus tracking, and custom getItemId/getItemLabel accessors."
endpoint: /tree-basic
package: dash_mui_charts
category: TreeView
order: 1
icon: mdi:file-tree
---

.. llms_copy::Tree Basic

.. toc::

### Overview

TreeView basics for Dash: data-driven items, defaultExpandedItems, click and focus tracking, and custom getItemId/getItemLabel accessors.

### TreeView

TreeView is the data-driven tree component in dash-mui-charts (Community
license — no key needed). It wraps MUI X `RichTreeView`: you pass one nested
`items` list and the component renders the whole tree, with controlled
selection, expansion, in-place label editing, and per-item disabling
available through props.

### Item shape

```python
items = [
    {"id": "docs", "label": "Documents", "children": [
        {"id": "docs-resume", "label": "resume.pdf"},
        {"id": "docs-cover", "label": "cover_letter.docx"},
    ]},
]
```

### Basic usage

```python
from dash_mui_charts import TreeView

TreeView(
    id="tree",
    items=items,
    defaultExpandedItems=["docs"],
)
```

### Key props

- `items` — nested list of `{id, label, children}` dicts (the whole tree).
- `defaultExpandedItems` — item ids expanded on load (uncontrolled).
- `expandedItems` / `selectedItems` — controlled equivalents, in/out.
- `getItemId` / `getItemLabel` / `getItemChildren` — string accessors for
  when your dicts use different keys, e.g. `getItemId="key"`,
  `getItemLabel="name"` maps `{"key": "a", "name": "Alpha"}` items.
- `expandIcon` / `collapseIcon` / `endIcon` — MUI icon names as strings.

### Outputs (use as callback Inputs)

- `clickedItem` — `{itemId, event_timestamp}` on every item click.
- `focusedItem` — fires when an item receives focus (click or keyboard nav).
- `expandedItems` / `selectedItems` — update as the user toggles/selects.
- `editedItemLabel` — `{itemId, newLabel}` after inline label editing.

```python
@callback(Output("out", "children"), Input("tree", "clickedItem"))
def show_click(data):
    return data["itemId"] if data else "Click an item..."
```

### Related pages

- /tree-selection — single, multi, checkbox and propagated selection
- /tree-expansion — expansion triggers and controlled expand/collapse
- /tree-editing — inline label editing
- /tree-icons — icons, indentation, height and sx styling
- /tree-disabled — disabled items and focusability
- /tree-simple — SimpleTreeView, the lighter JSX-driven tree
- /tree-pro — TreeViewPro: drag-reorder, lazy loading, per-item controls

---

### Live examples

.. exec::docs.tree_basic.demo
    :code: false

.. source::docs/tree_basic/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
