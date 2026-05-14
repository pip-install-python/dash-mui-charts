# File: docs/dash_mui_charts/tree_basic.py
"""Tree View — Basic examples showing items, expansion, selection, editing, and callbacks."""

import json
import dash_mantine_components as dmc
from dash import html, callback, Input, Output
from dash_mui_charts import TreeView

GLASS = {
    "background": "light-dark(rgba(255,255,255,0.55), rgba(30,30,30,0.55))",
    "backdropFilter": "blur(16px) saturate(1.8)",
    "WebkitBackdropFilter": "blur(16px) saturate(1.8)",
    "border": "1px solid light-dark(rgba(255,255,255,0.5), rgba(255,255,255,0.08))",
}

MUI_X_PRODUCTS = [
    {"id": "grid", "label": "Data Grid", "children": [
        {"id": "grid-com", "label": "@mui/x-data-grid"},
        {"id": "grid-pro", "label": "@mui/x-data-grid-pro"},
        {"id": "grid-premium", "label": "@mui/x-data-grid-premium"},
    ]},
    {"id": "pickers", "label": "Date and Time Pickers", "children": [
        {"id": "pickers-com", "label": "@mui/x-date-pickers"},
        {"id": "pickers-pro", "label": "@mui/x-date-pickers-pro"},
    ]},
    {"id": "charts", "label": "Charts", "children": [
        {"id": "charts-com", "label": "@mui/x-charts"},
    ]},
    {"id": "tree", "label": "Tree View", "children": [
        {"id": "tree-com", "label": "@mui/x-tree-view"},
        {"id": "tree-pro", "label": "@mui/x-tree-view-pro"},
    ]},
]

FILE_SYSTEM = [
    {"id": "docs", "label": "Documents", "children": [
        {"id": "docs-resume", "label": "resume.pdf"},
        {"id": "docs-cover", "label": "cover_letter.docx"},
        {"id": "docs-projects", "label": "Projects", "children": [
            {"id": "docs-proj-a", "label": "project_a.md"},
            {"id": "docs-proj-b", "label": "project_b.md"},
        ]},
    ]},
    {"id": "images", "label": "Images", "children": [
        {"id": "img-photo", "label": "photo.jpg"},
        {"id": "img-diagram", "label": "diagram.png"},
    ]},
    {"id": "src", "label": "Source Code", "children": [
        {"id": "src-main", "label": "main.py"},
        {"id": "src-utils", "label": "utils.py"},
        {"id": "src-tests", "label": "tests/", "children": [
            {"id": "src-test1", "label": "test_main.py"},
        ]},
    ]},
]

component = dmc.Stack([
    dmc.Text("Tree View", fw=700, size="xl"),
    dmc.Text("Hierarchical data display with selection, expansion, editing, and keyboard navigation.", size="sm", c="dimmed"),

    # --- Basic Tree ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Basic Tree View", fw=600),
            dmc.Text("Data-driven tree with default expansion. Click items to expand/collapse.", size="sm", c="dimmed"),
            TreeView(
                id="mc-tree-basic",
                items=MUI_X_PRODUCTS,
                defaultExpandedItems=["grid", "pickers"],
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Checkbox Multi-Select with Propagation ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Checkbox Selection with Propagation", fw=600),
            dmc.Text(
                "multiSelect + checkboxSelection + selectionPropagation: selecting a parent auto-selects children.",
                size="sm", c="dimmed",
            ),
            TreeView(
                id="mc-tree-checkbox",
                items=MUI_X_PRODUCTS,
                defaultExpandedItems=["grid", "pickers", "charts", "tree"],
                multiSelect=True,
                checkboxSelection=True,
                selectionPropagation={"parents": True, "descendants": True},
            ),
            dmc.Text("Selected items:", size="xs", c="dimmed"),
            html.Pre(
                id="mc-tree-checkbox-out",
                children="Select items...",
                style={
                    "fontSize": "11px", "margin": 0,
                    "padding": "8px 12px", "borderRadius": "6px",
                    "background": "light-dark(#f8f9fa, #1a1b1e)",
                    "border": "1px solid light-dark(#dee2e6, #373a40)",
                },
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Editable Labels ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Editable Labels", fw=600),
            dmc.Text("Double-click any item to edit its label. Press Enter to save, Esc to cancel.", size="sm", c="dimmed"),
            TreeView(
                id="mc-tree-editable",
                items=FILE_SYSTEM,
                defaultExpandedItems=["docs", "src"],
                isItemEditable=True,
                expandIcon="ChevronRight",
                collapseIcon="ExpandMore",
                endIcon="InsertDriveFile",
            ),
            dmc.Text("Last edit:", size="xs", c="dimmed"),
            html.Pre(
                id="mc-tree-edit-out",
                children="Edit an item...",
                style={
                    "fontSize": "11px", "margin": 0,
                    "padding": "8px 12px", "borderRadius": "6px",
                    "background": "light-dark(#f8f9fa, #1a1b1e)",
                    "border": "1px solid light-dark(#dee2e6, #373a40)",
                },
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Disabled Items ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Disabled Items", fw=600),
            dmc.Text("Specific items disabled via disabledItems prop.", size="sm", c="dimmed"),
            TreeView(
                id="mc-tree-disabled",
                items=MUI_X_PRODUCTS,
                defaultExpandedItems=["grid"],
                disabledItems=["grid-premium", "pickers-pro", "tree-pro"],
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),

    # --- Click Tracking ---
    dmc.Paper(
        dmc.Stack([
            dmc.Text("Click & Focus Tracking", fw=600),
            dmc.Text("clickedItem and focusedItem output props fire on interaction.", size="sm", c="dimmed"),
            TreeView(
                id="mc-tree-clicks",
                items=FILE_SYSTEM,
                defaultExpandedItems=["docs", "images", "src"],
            ),
            dmc.Text("Last click:", size="xs", c="dimmed"),
            html.Pre(
                id="mc-tree-click-out",
                children="Click an item...",
                style={
                    "fontSize": "11px", "margin": 0,
                    "padding": "8px 12px", "borderRadius": "6px",
                    "background": "light-dark(#f8f9fa, #1a1b1e)",
                    "border": "1px solid light-dark(#dee2e6, #373a40)",
                },
            ),
        ], gap="sm"),
        p="lg", radius="md", style=GLASS,
    ),
], gap="lg")


# --- Callbacks ---
@callback(
    Output("mc-tree-checkbox-out", "children"),
    Input("mc-tree-checkbox", "selectedItems"),
    prevent_initial_call=True,
)
def show_selection(selected):
    if not selected:
        return "No items selected"
    return json.dumps(selected, indent=2)


@callback(
    Output("mc-tree-edit-out", "children"),
    Input("mc-tree-editable", "editedItemLabel"),
    prevent_initial_call=True,
)
def show_edit(edit_data):
    if not edit_data:
        return "Edit an item..."
    return json.dumps(edit_data, indent=2)


@callback(
    Output("mc-tree-click-out", "children"),
    Input("mc-tree-clicks", "clickedItem"),
    prevent_initial_call=True,
)
def show_click(data):
    if not data:
        return "Click an item..."
    return json.dumps(data, indent=2)
