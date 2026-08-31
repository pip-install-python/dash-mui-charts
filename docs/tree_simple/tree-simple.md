---
name: Tree Simple
description: "SimpleTreeView examples: itemId/label items, checkbox multi-select, per-item disabled flags, custom icons, and the iconContainer expansion trigger."
endpoint: /tree-simple
package: dash_mui_charts
nav: Simple
category: TreeView
order: 2
icon: mdi:view-list-outline
---

.. llms_copy::Tree Simple

.. toc::

### Overview

SimpleTreeView examples: itemId/label items, checkbox multi-select, per-item disabled flags, custom icons, and the iconContainer expansion trigger.

### SimpleTreeView

SimpleTreeView is the lightweight, JSX-driven tree in dash-mui-charts
(Community license — no key needed). Unlike the data-driven `TreeView`
(a `RichTreeView` wrapper with an MUI store), SimpleTreeView renders its
items as `TreeItem` JSX children — a lighter alternative that suits
navigation sidebars and small static trees. This documentation site
dogfoods it: the site's own sidebar navigation is a SimpleTreeView
(`NAV_ITEMS` in app.py).

### Item shape — itemId, not id

```python
items = [
    {"itemId": "1", "label": "Applications", "children": [
        {"itemId": "1.1", "label": "Calendar"},
        {"itemId": "1.2", "label": "Chrome"},
    ]},
]
```

Items also support per-item flags directly on the dict:

- `disabled: True` — item is greyed out and inert.
- `disableSelection: True` — item renders normally but cannot be selected.
- `icon` — an MUI icon name, resolved through the library's icon resolver.

### Basic usage

```python
from dash_mui_charts import SimpleTreeView

SimpleTreeView(
    id="nav",
    items=items,
    defaultExpandedItems=["1"],
)
```

### Key props

- `multiSelect=True` + `checkboxSelection=True` — checkbox multi-select.
- `expandIcon` / `collapseIcon` / `endIcon` — MUI icon names, e.g.
  `expandIcon="ChevronRight"`, `collapseIcon="ExpandMore"`,
  `endIcon="Description"`.
- `expansionTrigger="iconContainer"` — only clicking the expand/collapse
  icon toggles the node (default `"content"` toggles on the whole row).

### Outputs (use as callback Inputs)

- `selectedItems` — the current selection (string or list with multiSelect).

```python
@callback(Output("out", "children"), Input("nav", "selectedItems"))
def show_selection(sel):
    return json.dumps(sel) if sel else "Select an item..."
```

### Related pages

- /tree-basic — TreeView, the data-driven RichTreeView wrapper
- /tree-selection — selection modes on TreeView
- /tree-expansion — expansion triggers and controlled expand/collapse
- /tree-editing — inline label editing
- /tree-icons — icons, indentation, height and sx styling
- /tree-disabled — disabled items and focusability
- /tree-pro — TreeViewPro: drag-reorder, lazy loading, per-item controls

---

### The docs sidebar, dogfooded

Before the boilerplate migration this site's navigation WAS a
SimpleTreeView. The tree below is generated from the site's real
navigation map (`components/navbar.py`), and clicking a leaf genuinely
navigates — the component driving its own documentation, as it always did.

.. exec::docs.tree_simple.sidebar_example
    :code: false

.. source::docs/tree_simple/sidebar_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Live examples

.. exec::docs.tree_simple.demo
    :code: false

.. source::docs/tree_simple/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
