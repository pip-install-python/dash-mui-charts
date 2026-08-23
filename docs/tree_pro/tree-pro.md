---
name: Tree Pro
description: "TreeViewPro (MUI X Pro): drag-and-drop reordering, reorderable subsets, and per-item 0-100 sliders plus kebab action menus wired to Dash callbacks."
endpoint: /tree-pro
package: dash_mui_charts
category: TreeView
icon: mdi:diamond-outline
---

.. llms_copy::Tree Pro

.. toc::

### Overview

TreeViewPro (MUI X Pro): drag-and-drop reordering, reorderable subsets, and per-item 0-100 sliders plus kebab action menus wired to Dash callbacks.

### TreeViewPro

TreeViewPro extends `TreeView` with MUI X Pro features — it requires an
MUI X Pro license key, passed as the `licenseKey` prop (this demo reads it
from the `MUI_PRO_API_KEY` environment variable). It is designed for the
"tree paired with a map / canvas" pattern where each leaf is a layer with
a 0-100 value and a row-level actions menu.

### Pro features

```python
import os
from dash_mui_charts import TreeViewPro

TreeViewPro(
    id="layers",
    items=LAYER_ITEMS,
    licenseKey=os.environ["MUI_PRO_API_KEY"],
    itemsReordering=True,            # drag-and-drop reorder
    reorderableItems=["task-1"],     # optional subset that may be reordered
    lazyLoading=True,                # fire `lazyLoadRequest` on expand
    lazyLoadedChildren={...},        # parentId -> [child items]
)
```

Outputs from reorder / lazy loading:

- `itemPositionChanged` — `{itemId, oldPosition, newPosition,
  event_timestamp}` per move.
- `orderedItems` — the full live tree after each reorder, so Python can
  render the current nested order without re-applying deltas. Falls back
  to `items` until the first reorder.
- `lazyLoadRequest` — `{itemId, event_timestamp}` when an unloaded node
  is expanded.

### Per-item slider + kebab controls (`showItemControls=True`)

```python
TreeViewPro(
    showItemControls=True,
    controlsItems=LEAF_IDS,                  # optional subset (leaves only)
    sliderValues={"layer-a": 80},            # bidirectional {itemId: value}
    sliderMin=0, sliderMax=100, sliderStep=1,
    sliderColor="teal",                      # Mantine palette name, hex, or CSS
    kebabMenuItems=[
        {"label": "Duplicate", "value": "duplicate", "icon": "ContentCopy"},
        {"label": "Delete",    "value": "delete",    "icon": "Delete"},
    ],
)
```

- `sliderChange` output — `{itemId, value, event_timestamp}` on slider
  commit (mouse-up / touch-end); observe `sliderValues` for live mid-drag
  values.
- `kebabAction` output — `{itemId, action, event_timestamp}` when a menu
  item is picked; `action` is the chosen entry's `value`.
- `sliderColor` accepts Mantine palette names ("teal", "blue.5"), CSS
  literals ("#ff6b6b"), or CSS expressions ("var(--mantine-color-...)").

### Kebab submenus, dividers, and per-node menus (v1.4.0)

`kebabMenuItems` entries may be a leaf `{label, value, icon?}`, a
`{divider: True}` rule, or a submenu `{label, icon?, children: [entries]}`
that opens on hover/click (recursive nesting; a leaf anywhere in the chain
closes the whole menu and fires `kebabAction`). `kebabMenuItemsById`
(`{itemId: [entries]}`) overrides the global `kebabMenuItems` for that
node — same entry shape — so one tree can carry different action sets for
different node types.

### Also supported (inherited patterns)

Selection (`multiSelect`, `checkboxSelection`), controlled expansion,
inline label editing (`isItemEditable`, `editedItemLabel` output), and
custom icons work the same as on `TreeView`.

### Related pages

- /tree-basic — TreeView, the Community data-driven tree
- /tree-simple — SimpleTreeView, the lighter JSX-driven tree
- /tree-selection — selection modes
- /tree-expansion — expansion triggers and controlled expand/collapse
- /tree-editing — inline label editing
- /tree-icons — icons, indentation, height and sx styling
- /tree-disabled — disabled items and focusability

.. admonition::Pro component demos
    :icon: mdi:diamond-outline
    :color: orange

    The examples on this page read a **MUI X Pro license key** from the
    `MUI_PRO_API_KEY` environment variable and pass it as `licenseKey`.
    Without it the tree renders with the unlicensed watermark; the badge
    below reports the live posture.

---

### Live examples

.. exec::docs.tree_pro.demo
    :code: false

.. source::docs/tree_pro/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
