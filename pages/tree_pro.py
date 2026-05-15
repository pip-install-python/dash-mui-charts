"""
Tree View Pro - Pro Features

Demonstrates TreeViewPro with drag-and-drop reordering, plus per-item
Slider (0-100) and kebab action menu on each row.

Section 3 is designed as the "map companion" pattern: a tree on the left where
each row carries a 0-100 progress slider and a ⋮ actions menu, paired with a
companion panel on the right that mirrors the selected layer's state. Slider
moves and menu picks are surfaced via dmc.Text so callback wiring is visible.

IDs are derived from labels at startup (spaces → "-", duplicates get "-1",
"-2", ...). The right column shows the live reordered tree as nested JSON.

Requires MUI X Pro license key.
"""

import copy
import os
import json
import re

import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, no_update
from dash_iconify import DashIconify

dash.register_page(__name__, path='/tree-pro', name='Tree Pro')

from dash_mui_charts import TreeViewPro

# Try to load license key from environment
LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# --- Raw tree data: labels only — IDs are derived below --------------------
RAW_TREE = [
    {"label": "Planning Layers", "children": [
        {"label": "Site survey overlay"},
        {"label": "Soil sample points"},
        {"label": "Access roads"},
    ]},
    {"label": "Active Layers", "children": [
        {"label": "Drone imagery 2026-Q1"},
        {"label": "Equipment GPS"},
    ]},
    {"label": "Reference Layers", "children": [
        {"label": "Parcel boundaries"},
        {"label": "Topographic base"},
    ]},
]

# Suggested initial slider values keyed by *label* — IDs aren't generated yet.
DEFAULT_BY_LABEL = {
    "Site survey overlay": 80,
    "Soil sample points": 25,
    "Access roads": 10,
    "Drone imagery 2026-Q1": 55,
    "Equipment GPS": 40,
    "Parcel boundaries": 100,
    "Topographic base": 100,
}


def slugify_label(label: str) -> str:
    """Turn a human label into a URL-safe slug.

    "Site survey overlay" -> "site-survey-overlay"
    "Drone imagery 2026-Q1" -> "drone-imagery-2026-q1"
    """
    base = re.sub(r"[^a-z0-9]+", "-", (label or "").lower()).strip("-")
    return base or "item"


def assign_ids(items):
    """Walk the tree and assign each node an id derived from its label.

    Duplicate slugs get suffixed -1, -2, -3 ... so every id stays unique
    across the whole tree (siblings or not). The input is not mutated.
    """
    tree = copy.deepcopy(items)
    seen = {}

    def walk(nodes):
        for node in nodes:
            base = slugify_label(node["label"])
            count = seen.get(base, 0)
            node["id"] = base if count == 0 else f"{base}-{count}"
            seen[base] = count + 1
            if node.get("children"):
                walk(node["children"])

    walk(tree)
    return tree


LAYER_ITEMS = assign_ids(RAW_TREE)

# After ID assignment: build the leaf-only lookups that feed the demo.
ITEM_LABELS = {}
DEFAULT_SLIDER_VALUES = {}


def _index_leaves(items):
    for it in items:
        if it.get("children"):
            _index_leaves(it["children"])
        else:
            ITEM_LABELS[it["id"]] = it["label"]
            if it["label"] in DEFAULT_BY_LABEL:
                DEFAULT_SLIDER_VALUES[it["id"]] = DEFAULT_BY_LABEL[it["label"]]


_index_leaves(LAYER_ITEMS)
LEAF_IDS = list(ITEM_LABELS.keys())

# id -> label for *every* node (groups + leaves), used to render labels
# instead of raw ids in the readouts.
ALL_LABELS = {}


def _index_all(items):
    for it in items:
        ALL_LABELS[it["id"]] = it["label"]
        if it.get("children"):
            _index_all(it["children"])


_index_all(LAYER_ITEMS)


def label_for(item_id, overrides=None):
    """Resolve an item id to its current label.

    Edited labels (from `editedItemLabel`) take priority via `overrides`,
    then the static tree labels, then the id itself as a last resort.
    """
    if not item_id:
        return item_id
    return (overrides or {}).get(item_id) or ALL_LABELS.get(item_id, item_id)


# --- Helpers used by the JSON readout --------------------------------------
def build_nested_view(items, slider_values):
    """Return a tree shaped like the input, with `value` injected on leaves.

    The structure preserves the live reorder so the JSON visibly reflects
    what the user sees in the tree.
    """
    out = []
    sv = slider_values or {}
    for it in items or []:
        node = {"id": it.get("id"), "label": it.get("label")}
        kids = it.get("children")
        if kids:
            node["children"] = build_nested_view(kids, sv)
        else:
            node["value"] = sv.get(it.get("id"), 0)
        out.append(node)
    return out


# Kebab menu options shared across items
KEBAB_MENU = [
    {"label": "Duplicate layer", "value": "duplicate", "icon": "ContentCopy"},
    {"label": "Assign to me",    "value": "assign",    "icon": "PersonAdd"},
    {"label": "Mark complete",   "value": "complete",  "icon": "CheckCircle"},
    {"label": "Archive",         "value": "archive",   "icon": "Archive"},
    {"label": "Delete",          "value": "delete",    "icon": "Delete"},
]
KEBAB_LABEL_BY_VALUE = {m["value"]: m["label"] for m in KEBAB_MENU}

# Slider color — picks up Mantine's teal palette so it adapts to the theme.
# Accepts theme names ("teal", "blue.5"), hex/rgb literals, or CSS expressions.
SLIDER_COLOR = "teal"

section_style = {'marginBottom': '40px'}
output_style = {
    'fontSize': '12px', 'margin': 0,
    'padding': '10px 14px', 'borderRadius': '6px',
    'backgroundColor': 'var(--mantine-color-default)',
    'border': '1px solid var(--mantine-color-default-border)',
    'whiteSpace': 'pre-wrap',
    'maxHeight': '320px',
    'overflow': 'auto',
}


def _stat_card(label, value_id, initial, icon):
    """Tile that lights up when something updates — used for live readouts."""
    return dmc.Paper(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    variant="light",
                    color=SLIDER_COLOR,
                    radius="md",
                    size="lg",
                ),
                dmc.Stack(
                    [
                        dmc.Text(label, size="xs", c="dimmed", fw=600, tt="uppercase"),
                        dmc.Text(initial, id=value_id, size="lg", fw=700),
                    ],
                    gap=2,
                ),
            ],
            gap="md",
            wrap="nowrap",
            align="center",
        ),
        p="md",
        withBorder=True,
        radius="md",
        shadow="xs",
    )


layout = dmc.Stack(
    [
        dmc.Stack(
            [
                dmc.Title("Tree View Pro", order=2),
                dmc.Text(
                    "Pro features: drag-and-drop reordering, plus per-item Slider (0–100) and kebab actions menu, "
                    "designed for pairing with a map / canvas as the layer list.",
                    c="dimmed",
                ),
                dmc.Badge(
                    f"License key: {'Set' if LICENSE_KEY else 'Not set (set MUI_PRO_API_KEY)'}",
                    color="blue" if LICENSE_KEY else "red",
                    variant="light",
                    size="sm",
                ),
            ],
            gap=4,
        ),

        # --- 1. Drag-and-drop reordering ---
        dmc.Stack(
            [
                dmc.Title("1. Drag-and-Drop Reordering", order=3),
                dmc.Text(
                    "itemsReordering=True enables drag-and-drop to move items between groups.",
                    c="dimmed",
                    size="sm",
                ),
                TreeViewPro(
                    id="tree-pro-reorder",
                    items=LAYER_ITEMS,
                    defaultExpandedItems=[i["id"] for i in LAYER_ITEMS],
                    itemsReordering=True,
                    licenseKey=LICENSE_KEY,
                    expandIcon="ChevronRight",
                    collapseIcon="ExpandMore",
                ),
                dmc.Text("Last reorder event:", size="sm", c="dimmed"),
                html.Pre(id="tree-pro-reorder-out", children="Drag items to reorder...", style=output_style),
            ],
            gap="xs",
            style=section_style,
        ),

        # --- 2. Reorderable subset ---
        dmc.Stack(
            [
                dmc.Title("2. Reorderable Subset", order=3),
                dmc.Text(
                    'reorderableItems = the Planning leaf IDs — only Planning layers can be reordered.',
                    c="dimmed",
                    size="sm",
                ),
                TreeViewPro(
                    id="tree-pro-reorder-subset",
                    items=LAYER_ITEMS,
                    defaultExpandedItems=[i["id"] for i in LAYER_ITEMS],
                    itemsReordering=True,
                    reorderableItems=[
                        c["id"] for c in LAYER_ITEMS[0].get("children", [])
                    ],
                    licenseKey=LICENSE_KEY,
                ),
            ],
            gap="xs",
            style=section_style,
        ),

        # --- 3. Pro with selection + editing + reordering + slider + kebab ---
        dmc.Stack(
            [
                dmc.Title(
                    "3. Pro with Selection + Editing + Reordering + Slider + Kebab",
                    order=3,
                ),
                dmc.Text(
                    "Each row exposes a 0–100 Slider and a ⋮ actions menu directly after the label. "
                    "Drag the slider to set layer opacity, double-click a label to rename, or pick an action "
                    "from the kebab — every change is captured by Dash callbacks and reflected live in the "
                    "panel on the right.",
                    c="dimmed",
                    size="sm",
                ),

                # Two-column layout: tree on the left, live readouts on the right
                dmc.Grid(
                    [
                        # --- LEFT: the tree ---
                        dmc.GridCol(
                            dmc.Paper(
                                TreeViewPro(
                                    id="tree-pro-combo",
                                    items=LAYER_ITEMS,
                                    defaultExpandedItems=[i["id"] for i in LAYER_ITEMS],
                                    itemsReordering=True,
                                    isItemEditable=True,
                                    multiSelect=True,
                                    checkboxSelection=True,
                                    licenseKey=LICENSE_KEY,
                                    expandIcon="ChevronRight",
                                    collapseIcon="ExpandMore",
                                    # Per-item controls
                                    showItemControls=True,
                                    controlsItems=LEAF_IDS,
                                    sliderValues=DEFAULT_SLIDER_VALUES,
                                    sliderMin=0,
                                    sliderMax=100,
                                    sliderStep=1,
                                    sliderColor=SLIDER_COLOR,
                                    kebabMenuItems=KEBAB_MENU,
                                    sx={
                                        "& .MuiTreeItem-content": {"paddingY": "4px"},
                                        "& .MuiTreeItem-label": {"width": "100%"},
                                    },
                                ),
                                p="sm",
                                withBorder=True,
                                radius="md",
                                shadow="xs",
                            ),
                            span={"base": 12, "md": 7},
                        ),

                        # --- RIGHT: live readouts (the "map" companion in a real app) ---
                        dmc.GridCol(
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            _stat_card(
                                                "Last slider",
                                                "tree-pro-combo-slider-label",
                                                "Drag a slider…",
                                                "material-symbols:tune",
                                            ),
                                            _stat_card(
                                                "Last menu",
                                                "tree-pro-combo-menu-label",
                                                "Open a ⋮ menu…",
                                                "material-symbols:more-vert",
                                            ),
                                        ],
                                        grow=True,
                                        gap="sm",
                                    ),
                                    dmc.Paper(
                                        dmc.Stack(
                                            [
                                                dmc.Text(
                                                    "Map companion (state mirror)",
                                                    size="xs",
                                                    c="dimmed",
                                                    fw=700,
                                                    tt="uppercase",
                                                ),
                                                dmc.Text(
                                                    "In a real map view this column would render the layers. "
                                                    "Here it mirrors the tree state so you can confirm every "
                                                    "control is captured by a callback.",
                                                    size="sm",
                                                    c="dimmed",
                                                ),
                                                dmc.Divider(),
                                                dmc.Text("Selected:", size="xs", c="dimmed", fw=600, tt="uppercase"),
                                                html.Pre(
                                                    id="tree-pro-combo-sel",
                                                    children="[]",
                                                    style=output_style,
                                                ),
                                                dmc.Text("Last label edit:", size="xs", c="dimmed", fw=600, tt="uppercase"),
                                                html.Pre(
                                                    id="tree-pro-combo-edit",
                                                    children="...",
                                                    style=output_style,
                                                ),
                                                dmc.Text(
                                                    "Slider values and nested order:",
                                                    size="xs",
                                                    c="dimmed",
                                                    fw=600,
                                                    tt="uppercase",
                                                ),
                                                html.Pre(
                                                    id="tree-pro-combo-sliders",
                                                    children=json.dumps(
                                                        build_nested_view(LAYER_ITEMS, DEFAULT_SLIDER_VALUES),
                                                        indent=2,
                                                    ),
                                                    style=output_style,
                                                ),
                                                dmc.Text("Action log:", size="xs", c="dimmed", fw=600, tt="uppercase"),
                                                dmc.Stack(
                                                    id="tree-pro-combo-action-log",
                                                    children=[
                                                        dmc.Text(
                                                            "Pick a kebab menu item to start the log.",
                                                            size="sm",
                                                            c="dimmed",
                                                            fs="italic",
                                                        )
                                                    ],
                                                    gap=4,
                                                ),
                                            ],
                                            gap="xs",
                                        ),
                                        p="md",
                                        withBorder=True,
                                        radius="md",
                                        shadow="xs",
                                    ),
                                ],
                                gap="sm",
                            ),
                            span={"base": 12, "md": 5},
                        ),
                    ],
                    gutter="md",
                ),
            ],
            gap="sm",
            style=section_style,
        ),

        # Client-side state used to keep the readouts in sync. Label overrides
        # let "Last slider" / "Last menu" / "Selected" reflect renamed cells.
        dcc.Store(id="tps-label-overrides", data={}),
        dcc.Store(id="tps-last-slider", data=None),
        dcc.Store(id="tps-last-kebab", data=None),
    ],
    gap="lg",
)


@callback(
    Output("tree-pro-reorder-out", "children"),
    Input("tree-pro-reorder", "itemPositionChanged"),
    prevent_initial_call=True,
)
def show_reorder(data):
    if not data:
        return "Drag items to reorder..."
    return json.dumps(data, indent=2)


@callback(
    Output("tree-pro-combo-sel", "children"),
    Input("tree-pro-combo", "selectedItems"),
    Input("tps-label-overrides", "data"),
    prevent_initial_call=True,
)
def show_combo_sel(sel, overrides):
    if not sel:
        return "[]"
    ids = [sel] if isinstance(sel, str) else list(sel)
    labels = [label_for(i, overrides) for i in ids]
    return json.dumps(labels, indent=2)


@callback(
    Output("tree-pro-combo-edit", "children"),
    Output("tps-label-overrides", "data"),
    Input("tree-pro-combo", "editedItemLabel"),
    State("tps-label-overrides", "data"),
    prevent_initial_call=True,
)
def show_combo_edit(data, overrides):
    if not data:
        return "...", no_update
    overrides = dict(overrides or {})
    if data.get("itemId") and data.get("newLabel"):
        overrides[data["itemId"]] = data["newLabel"]
    return json.dumps(data, indent=2), overrides


@callback(
    Output("tree-pro-combo-sliders", "children"),
    Output("tps-last-slider", "data"),
    Input("tree-pro-combo", "sliderValues"),
    Input("tree-pro-combo", "sliderChange"),
    Input("tree-pro-combo", "orderedItems"),
    prevent_initial_call=True,
)
def show_combo_sliders(values, change, ordered):
    tree = ordered if ordered else LAYER_ITEMS
    nested = build_nested_view(tree, values or {})
    pretty = json.dumps(nested, indent=2)

    last = no_update
    if change:
        last = {"itemId": change.get("itemId"), "value": change.get("value")}
    elif values:
        diff = {k: v for k, v in values.items() if v != DEFAULT_SLIDER_VALUES.get(k)}
        if diff:
            k = next(iter(diff))
            last = {"itemId": k, "value": diff[k]}

    return pretty, last


@callback(
    Output("tree-pro-combo-action-log", "children"),
    Output("tps-last-kebab", "data"),
    Input("tree-pro-combo", "kebabAction"),
    State("tree-pro-combo-action-log", "children"),
    State("tps-label-overrides", "data"),
    prevent_initial_call=True,
)
def show_combo_kebab(action, log, overrides):
    if not action:
        return no_update, no_update

    action_label = KEBAB_LABEL_BY_VALUE.get(action.get("action"), action.get("action") or "—")
    item_label = label_for(action.get("itemId"), overrides)

    entry = dmc.Group(
        [
            dmc.ThemeIcon(
                DashIconify(icon="material-symbols:arrow-right-alt", width=14),
                size="sm",
                variant="light",
                color=SLIDER_COLOR,
                radius="xl",
            ),
            dmc.Text(action_label, size="sm", fw=600),
            dmc.Text(item_label, size="sm", c="dimmed"),
        ],
        gap="xs",
        wrap="nowrap",
    )

    log_list = list(log or [])
    if log_list and isinstance(log_list[0], dict):
        first_props = log_list[0].get("props", {}) or {}
        if first_props.get("fs") == "italic":
            log_list = []

    log_list.insert(0, entry)
    log_list = log_list[:6]
    return log_list, {"itemId": action.get("itemId"), "action": action.get("action")}


@callback(
    Output("tree-pro-combo-slider-label", "children"),
    Output("tree-pro-combo-menu-label", "children"),
    Input("tps-last-slider", "data"),
    Input("tps-last-kebab", "data"),
    Input("tps-label-overrides", "data"),
    prevent_initial_call=True,
)
def render_readouts(last_slider, last_kebab, overrides):
    """Render the two summary tiles from stored state.

    Driven by the label-overrides store too, so renaming a cell immediately
    refreshes "Last slider" / "Last menu" with the new label.
    """
    if last_slider and last_slider.get("itemId"):
        slider_text = f"{label_for(last_slider['itemId'], overrides)}: {last_slider.get('value')}"
    else:
        slider_text = "Drag a slider…"

    if last_kebab and last_kebab.get("itemId"):
        action_label = KEBAB_LABEL_BY_VALUE.get(
            last_kebab.get("action"), last_kebab.get("action") or "—"
        )
        menu_text = f"{action_label} · {label_for(last_kebab['itemId'], overrides)}"
    else:
        menu_text = "Open a ⋮ menu…"

    return slider_text, menu_text
