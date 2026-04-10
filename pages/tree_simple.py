"""
Tree View - SimpleTreeView

Demonstrates the SimpleTreeView component which uses a different
item structure (itemId/label) and renders TreeItem JSX children.
Lighter alternative to the data-driven TreeView.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/tree-simple', name='Tree Simple')

from dash_mui_charts import SimpleTreeView

# SimpleTreeView uses itemId (not id) and label
SIMPLE_ITEMS = [
    {"itemId": "1", "label": "Applications", "children": [
        {"itemId": "1.1", "label": "Calendar"},
        {"itemId": "1.2", "label": "Chrome"},
        {"itemId": "1.3", "label": "Webstorm"},
    ]},
    {"itemId": "2", "label": "Documents", "children": [
        {"itemId": "2.1", "label": "OSS", "children": [
            {"itemId": "2.1.1", "label": "MUI", "children": [
                {"itemId": "2.1.1.1", "label": "index.js"},
            ]},
        ]},
        {"itemId": "2.2", "label": "Personal", "children": [
            {"itemId": "2.2.1", "label": "resume.pdf"},
        ]},
    ]},
    {"itemId": "3", "label": "Bookmarks", "children": [
        {"itemId": "3.1", "label": "GitHub"},
        {"itemId": "3.2", "label": "Stack Overflow"},
    ]},
]

# Per-item disabled/disableSelection example
DISABLED_ITEMS = [
    {"itemId": "d1", "label": "Available", "children": [
        {"itemId": "d1.1", "label": "Item A"},
        {"itemId": "d1.2", "label": "Item B (disabled)", "disabled": True},
        {"itemId": "d1.3", "label": "Item C"},
    ]},
    {"itemId": "d2", "label": "Mixed", "children": [
        {"itemId": "d2.1", "label": "Selectable"},
        {"itemId": "d2.2", "label": "Not selectable", "disableSelection": True},
        {"itemId": "d2.3", "label": "Disabled", "disabled": True},
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
    html.H2("SimpleTreeView"),
    html.P(
        "Lighter alternative using itemId/label structure. Items are rendered as TreeItem JSX children.",
        style={'color': '#666'},
    ),

    # --- 1. Basic ---
    html.Div([
        html.H3("1. Basic SimpleTreeView"),
        html.P("Nested items with itemId and label fields.", style={'color': '#666'}),
        SimpleTreeView(
            id="tree-simple-basic",
            items=SIMPLE_ITEMS,
            defaultExpandedItems=["1", "2"],
        ),
    ], style=section_style),

    # --- 2. Selection ---
    html.Div([
        html.H3("2. Selection with Click Tracking"),
        html.P("Single selection with click output.", style={'color': '#666'}),
        SimpleTreeView(
            id="tree-simple-select",
            items=SIMPLE_ITEMS,
            defaultExpandedItems=["1", "2", "3"],
        ),
        html.Pre(id="tree-simple-select-out", children="Select an item...", style=output_style),
    ], style=section_style),

    # --- 3. Multi-select with checkboxes ---
    html.Div([
        html.H3("3. Checkbox Multi-Select"),
        html.P("multiSelect + checkboxSelection on SimpleTreeView.", style={'color': '#666'}),
        SimpleTreeView(
            id="tree-simple-checkbox",
            items=SIMPLE_ITEMS,
            defaultExpandedItems=["1", "2", "3"],
            multiSelect=True,
            checkboxSelection=True,
        ),
        html.Pre(id="tree-simple-checkbox-out", children="Check items...", style=output_style),
    ], style=section_style),

    # --- 4. Per-item disabled/disableSelection ---
    html.Div([
        html.H3("4. Per-Item Disabled & disableSelection"),
        html.P(
            "SimpleTreeView supports per-item disabled and disableSelection flags directly on items.",
            style={'color': '#666'},
        ),
        SimpleTreeView(
            id="tree-simple-disabled",
            items=DISABLED_ITEMS,
            defaultExpandedItems=["d1", "d2"],
        ),
    ], style=section_style),

    # --- 5. Custom icons ---
    html.Div([
        html.H3("5. Custom Icons"),
        html.P('expandIcon="Add", collapseIcon="Remove", endIcon="Description"', style={'color': '#666'}),
        SimpleTreeView(
            id="tree-simple-icons",
            items=SIMPLE_ITEMS,
            defaultExpandedItems=["1"],
            expandIcon="Add",
            collapseIcon="Remove",
            endIcon="Description",
        ),
    ], style=section_style),

    # --- 6. Icon container expansion ---
    html.Div([
        html.H3("6. Icon Container Expansion Trigger"),
        html.P('expansionTrigger="iconContainer" — only icon click expands.', style={'color': '#666'}),
        SimpleTreeView(
            id="tree-simple-icon-trigger",
            items=SIMPLE_ITEMS,
            defaultExpandedItems=["2"],
            expansionTrigger="iconContainer",
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
        ),
    ], style=section_style),
])


@callback(
    Output("tree-simple-select-out", "children"),
    Input("tree-simple-select", "selectedItems"),
    prevent_initial_call=True,
)
def show_simple_select(sel):
    return json.dumps(sel, indent=2) if sel else "Select an item..."


@callback(
    Output("tree-simple-checkbox-out", "children"),
    Input("tree-simple-checkbox", "selectedItems"),
    prevent_initial_call=True,
)
def show_simple_checkbox(sel):
    return json.dumps(sel, indent=2) if sel else "Check items..."
