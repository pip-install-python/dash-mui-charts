"""
Tree View - Basic Usage

Demonstrates the core TreeView component with data-driven items,
default expansion, and click tracking.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/tree-basic', name='Tree Basic')

from dash_mui_charts import TreeView

# --- Sample Data ---
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

section_style = {'marginBottom': '40px'}
output_style = {
    'fontSize': '12px', 'margin': 0,
    'padding': '10px 14px', 'borderRadius': '6px',
    'backgroundColor': '#f5f5f5',
    'border': '1px solid #ddd',
    'whiteSpace': 'pre-wrap',
    'maxHeight': '150px',
    'overflow': 'auto',
}

layout = html.Div([
    html.H2("Tree View - Basic Usage"),
    html.P("Data-driven tree using the RichTreeView component.", style={'color': '#666'}),

    # --- 1. Minimal tree ---
    html.Div([
        html.H3("1. Minimal Tree"),
        html.P("Just pass items. Click nodes to expand/collapse.", style={'color': '#666'}),
        TreeView(
            id="tree-basic-minimal",
            items=MUI_X_PRODUCTS,
        ),
    ], style=section_style),

    # --- 2. Default expanded ---
    html.Div([
        html.H3("2. Default Expanded Items"),
        html.P(
            'defaultExpandedItems=["grid", "pickers"] opens those nodes on load.',
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-basic-expanded",
            items=MUI_X_PRODUCTS,
            defaultExpandedItems=["grid", "pickers"],
        ),
    ], style=section_style),

    # --- 3. File system tree with click tracking ---
    html.Div([
        html.H3("3. Click Tracking"),
        html.P("clickedItem output fires on each click with {itemId, event_timestamp}.", style={'color': '#666'}),
        TreeView(
            id="tree-basic-clicks",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "src"],
        ),
        html.P("Last click:", style={'marginTop': '10px', 'fontSize': '13px', 'color': '#666'}),
        html.Pre(id="tree-basic-click-out", children="Click an item...", style=output_style),
    ], style=section_style),

    # --- 4. Focus tracking ---
    html.Div([
        html.H3("4. Focus Tracking"),
        html.P("focusedItem fires when an item receives focus (click or keyboard nav).", style={'color': '#666'}),
        TreeView(
            id="tree-basic-focus",
            items=FILE_SYSTEM,
            defaultExpandedItems=["images"],
        ),
        html.P("Last focused:", style={'marginTop': '10px', 'fontSize': '13px', 'color': '#666'}),
        html.Pre(id="tree-basic-focus-out", children="Focus an item...", style=output_style),
    ], style=section_style),

    # --- 5. Custom accessor keys ---
    html.Div([
        html.H3("5. Custom Item Keys"),
        html.P(
            'Items use "name" instead of "label" and "key" instead of "id". '
            'getItemId="key" and getItemLabel="name" map them correctly.',
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-basic-custom-keys",
            items=[
                {"key": "a", "name": "Alpha", "children": [
                    {"key": "a1", "name": "Alpha-One"},
                    {"key": "a2", "name": "Alpha-Two"},
                ]},
                {"key": "b", "name": "Beta", "children": [
                    {"key": "b1", "name": "Beta-One"},
                ]},
            ],
            getItemId="key",
            getItemLabel="name",
            defaultExpandedItems=["a"],
        ),
    ], style=section_style),
])


@callback(
    Output("tree-basic-click-out", "children"),
    Input("tree-basic-clicks", "clickedItem"),
    prevent_initial_call=True,
)
def show_click(data):
    if not data:
        return "Click an item..."
    return json.dumps(data, indent=2)


@callback(
    Output("tree-basic-focus-out", "children"),
    Input("tree-basic-focus", "focusedItem"),
    prevent_initial_call=True,
)
def show_focus(data):
    if not data:
        return "Focus an item..."
    return json.dumps(data, indent=2)
