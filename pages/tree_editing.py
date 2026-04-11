"""
Tree View - Label Editing

Demonstrates inline label editing: edit all items, edit specific items,
and tracking edit events via callbacks.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/tree-editing', name='Tree Editing')

from dash_mui_charts import TreeView

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

section_style = {'marginBottom': '40px'}
output_style = {
    'fontSize': '12px', 'margin': 0,
    'padding': '10px 14px', 'borderRadius': '6px',
    'backgroundColor': 'var(--mantine-color-default)',
    'border': '1px solid var(--mantine-color-default-border)',
    'whiteSpace': 'pre-wrap',
    'maxHeight': '200px',
    'overflow': 'auto',
}

layout = html.Div([
    html.H2("Tree View - Label Editing"),
    html.P("Double-click an item label to edit. Press Enter to save, Esc to cancel.", style={'color': 'var(--mantine-color-dimmed)'}),

    # --- 1. All items editable ---
    html.Div([
        html.H3("1. All Items Editable"),
        html.P("isItemEditable=True makes every item's label editable.", style={'color': 'var(--mantine-color-dimmed)'}),
        TreeView(
            id="tree-edit-all",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "src"],
            isItemEditable=True,
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
            endIcon="InsertDriveFile",
        ),
        html.P("Last edit:", style={'marginTop': '10px', 'fontSize': '13px', 'color': 'var(--mantine-color-dimmed)'}),
        html.Pre(id="tree-edit-all-out", children="Double-click to edit...", style=output_style),
    ], style=section_style),

    # --- 2. Specific items editable ---
    html.Div([
        html.H3("2. Specific Items Editable"),
        html.P(
            'editableItems=["docs-resume", "docs-cover", "src-main"] — only those 3 items can be edited.',
            style={'color': 'var(--mantine-color-dimmed)'},
        ),
        TreeView(
            id="tree-edit-specific",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "src"],
            editableItems=["docs-resume", "docs-cover", "src-main"],
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
            endIcon="InsertDriveFile",
        ),
        html.P("Last edit:", style={'marginTop': '10px', 'fontSize': '13px', 'color': 'var(--mantine-color-dimmed)'}),
        html.Pre(id="tree-edit-specific-out", children="Double-click an editable item...", style=output_style),
    ], style=section_style),

    # --- 3. Edit history log ---
    html.Div([
        html.H3("3. Edit History"),
        html.P("Each edit appends to a log showing itemId and newLabel.", style={'color': 'var(--mantine-color-dimmed)'}),
        TreeView(
            id="tree-edit-log",
            items=[
                {"id": "fruits", "label": "Fruits", "children": [
                    {"id": "apple", "label": "Apple"},
                    {"id": "banana", "label": "Banana"},
                    {"id": "cherry", "label": "Cherry"},
                ]},
                {"id": "vegs", "label": "Vegetables", "children": [
                    {"id": "carrot", "label": "Carrot"},
                    {"id": "potato", "label": "Potato"},
                ]},
            ],
            defaultExpandedItems=["fruits", "vegs"],
            isItemEditable=True,
        ),
        html.P("Edit log:", style={'marginTop': '10px', 'fontSize': '13px', 'color': 'var(--mantine-color-dimmed)'}),
        html.Pre(id="tree-edit-log-out", children="No edits yet...", style=output_style),
    ], style=section_style),
])


@callback(
    Output("tree-edit-all-out", "children"),
    Input("tree-edit-all", "editedItemLabel"),
    prevent_initial_call=True,
)
def show_edit_all(data):
    if not data:
        return "Double-click to edit..."
    return json.dumps(data, indent=2)


@callback(
    Output("tree-edit-specific-out", "children"),
    Input("tree-edit-specific", "editedItemLabel"),
    prevent_initial_call=True,
)
def show_edit_specific(data):
    if not data:
        return "Double-click an editable item..."
    return json.dumps(data, indent=2)


@callback(
    Output("tree-edit-log-out", "children"),
    Input("tree-edit-log", "editedItemLabel"),
    prevent_initial_call=True,
)
def edit_log(data):
    if not data:
        return "No edits yet..."
    return f"Renamed '{data['itemId']}' -> '{data['newLabel']}'"
