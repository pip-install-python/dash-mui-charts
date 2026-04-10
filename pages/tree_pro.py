"""
Tree View Pro - Pro Features

Demonstrates TreeViewPro with drag-and-drop reordering.
Requires MUI X Pro license key.
"""

import os
import json
import dash
from dash import html, callback, Input, Output, dcc

dash.register_page(__name__, path='/tree-pro', name='Tree Pro')

from dash_mui_charts import TreeViewPro

# Try to load license key from environment
LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

REORDER_ITEMS = [
    {"id": "backlog", "label": "Backlog", "children": [
        {"id": "task-1", "label": "Setup CI/CD"},
        {"id": "task-2", "label": "Write unit tests"},
        {"id": "task-3", "label": "Code review"},
    ]},
    {"id": "in-progress", "label": "In Progress", "children": [
        {"id": "task-4", "label": "Build dashboard"},
        {"id": "task-5", "label": "API integration"},
    ]},
    {"id": "done", "label": "Done", "children": [
        {"id": "task-6", "label": "Project setup"},
        {"id": "task-7", "label": "Database schema"},
    ]},
]

section_style = {'marginBottom': '40px'}
output_style = {
    'fontSize': '12px', 'margin': 0,
    'padding': '10px 14px', 'borderRadius': '6px',
    'backgroundColor': '#f5f5f5',
    'border': '1px solid #ddd',
    'whiteSpace': 'pre-wrap',
    'maxHeight': '200px',
    'overflow': 'auto',
}

layout = html.Div([
    html.H2("Tree View Pro"),
    html.P(
        "Pro features: drag-and-drop reordering. Requires MUI X Pro license key.",
        style={'color': '#666'},
    ),
    html.P(
        f"License key: {'Set' if LICENSE_KEY else 'Not set (set MUI_PRO_API_KEY env var)'}",
        style={'color': '#1976d2' if LICENSE_KEY else '#d32f2f', 'fontSize': '13px', 'fontStyle': 'italic'},
    ),

    # --- 1. Drag-and-drop reordering ---
    html.Div([
        html.H3("1. Drag-and-Drop Reordering"),
        html.P("itemsReordering=True enables drag-and-drop to move items between groups.", style={'color': '#666'}),
        TreeViewPro(
            id="tree-pro-reorder",
            items=REORDER_ITEMS,
            defaultExpandedItems=["backlog", "in-progress", "done"],
            itemsReordering=True,
            licenseKey=LICENSE_KEY,
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
        ),
        html.P("Last reorder event:", style={'marginTop': '10px', 'fontSize': '13px', 'color': '#666'}),
        html.Pre(id="tree-pro-reorder-out", children="Drag items to reorder...", style=output_style),
    ], style=section_style),

    # --- 2. Reorderable subset ---
    html.Div([
        html.H3("2. Reorderable Subset"),
        html.P(
            'reorderableItems=["task-1", "task-2", "task-3"] — only backlog tasks can be reordered.',
            style={'color': '#666'},
        ),
        TreeViewPro(
            id="tree-pro-reorder-subset",
            items=REORDER_ITEMS,
            defaultExpandedItems=["backlog", "in-progress", "done"],
            itemsReordering=True,
            reorderableItems=["task-1", "task-2", "task-3"],
            licenseKey=LICENSE_KEY,
        ),
    ], style=section_style),

    # --- 3. Pro with all features ---
    html.Div([
        html.H3("3. Pro with Selection + Editing + Reordering"),
        html.P("Combining multiple features on a single tree.", style={'color': '#666'}),
        TreeViewPro(
            id="tree-pro-combo",
            items=REORDER_ITEMS,
            defaultExpandedItems=["backlog", "in-progress", "done"],
            itemsReordering=True,
            isItemEditable=True,
            multiSelect=True,
            checkboxSelection=True,
            licenseKey=LICENSE_KEY,
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
        ),
        html.Div([
            html.Div([
                html.P("Selected:", style={'fontSize': '13px', 'color': '#666', 'margin': '0 0 4px'}),
                html.Pre(id="tree-pro-combo-sel", children="[]", style=output_style),
            ], style={'flex': '1', 'marginRight': '10px'}),
            html.Div([
                html.P("Last edit:", style={'fontSize': '13px', 'color': '#666', 'margin': '0 0 4px'}),
                html.Pre(id="tree-pro-combo-edit", children="...", style=output_style),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'marginTop': '10px'}),
    ], style=section_style),
])


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
    prevent_initial_call=True,
)
def show_combo_sel(sel):
    return json.dumps(sel, indent=2) if sel else "[]"


@callback(
    Output("tree-pro-combo-edit", "children"),
    Input("tree-pro-combo", "editedItemLabel"),
    prevent_initial_call=True,
)
def show_combo_edit(data):
    return json.dumps(data, indent=2) if data else "..."
