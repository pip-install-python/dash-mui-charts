"""
Tree View - Selection

Demonstrates single selection, multi-select, checkbox selection,
selection propagation, and controlled selection.
"""

import json
import dash
from dash import html, callback, Input, Output, State

dash.register_page(__name__, path='/tree-selection', name='Tree Selection')

from dash_mui_charts import TreeView

PRODUCTS = [
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
    html.H2("Tree View - Selection"),
    html.P("Various selection modes and propagation behaviors.", style={'color': '#666'}),

    # --- 1. Single selection (default) ---
    html.Div([
        html.H3("1. Single Selection (default)"),
        html.P("Click an item to select it. Only one item can be selected.", style={'color': '#666'}),
        TreeView(
            id="tree-sel-single",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
        ),
        html.Pre(id="tree-sel-single-out", children="Select an item...", style=output_style),
    ], style=section_style),

    # --- 2. Multi-select ---
    html.Div([
        html.H3("2. Multi-Select"),
        html.P("multiSelect=True. Hold Ctrl/Cmd to select multiple items.", style={'color': '#666'}),
        TreeView(
            id="tree-sel-multi",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            multiSelect=True,
        ),
        html.Pre(id="tree-sel-multi-out", children="Select items...", style=output_style),
    ], style=section_style),

    # --- 3. Checkbox selection ---
    html.Div([
        html.H3("3. Checkbox Selection"),
        html.P("checkboxSelection=True adds checkboxes to each item.", style={'color': '#666'}),
        TreeView(
            id="tree-sel-checkbox",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            multiSelect=True,
            checkboxSelection=True,
        ),
        html.Pre(id="tree-sel-checkbox-out", children="Check items...", style=output_style),
    ], style=section_style),

    # --- 4. Selection propagation ---
    html.Div([
        html.H3("4. Selection Propagation"),
        html.P(
            'selectionPropagation={parents: True, descendants: True}. '
            'Selecting a parent auto-selects all children. Selecting all children auto-selects the parent.',
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-sel-propagation",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            multiSelect=True,
            checkboxSelection=True,
            selectionPropagation={"parents": True, "descendants": True},
        ),
        html.Pre(id="tree-sel-propagation-out", children="Check items...", style=output_style),
    ], style=section_style),

    # --- 5. Disable selection ---
    html.Div([
        html.H3("5. Selection Disabled"),
        html.P("disableSelection=True prevents any item from being selected.", style={'color': '#666'}),
        TreeView(
            id="tree-sel-disabled",
            items=PRODUCTS,
            defaultExpandedItems=["grid"],
            disableSelection=True,
        ),
    ], style=section_style),

    # --- 6. Controlled selection ---
    html.Div([
        html.H3("6. Controlled Selection"),
        html.P("Use a button to programmatically set selectedItems.", style={'color': '#666'}),
        html.Div([
            html.Button("Select All Grid", id="tree-sel-btn-grid",
                        style={'marginRight': '8px', 'padding': '6px 12px'}),
            html.Button("Select All Pickers", id="tree-sel-btn-pickers",
                        style={'marginRight': '8px', 'padding': '6px 12px'}),
            html.Button("Clear", id="tree-sel-btn-clear",
                        style={'padding': '6px 12px'}),
        ], style={'marginBottom': '10px'}),
        TreeView(
            id="tree-sel-controlled",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            multiSelect=True,
            checkboxSelection=True,
            selectedItems=[],
        ),
        html.Pre(id="tree-sel-controlled-out", children="[]", style=output_style),
    ], style=section_style),
])


# --- Callbacks ---
@callback(
    Output("tree-sel-single-out", "children"),
    Input("tree-sel-single", "selectedItems"),
    prevent_initial_call=True,
)
def show_single(sel):
    return json.dumps(sel, indent=2) if sel else "Select an item..."


@callback(
    Output("tree-sel-multi-out", "children"),
    Input("tree-sel-multi", "selectedItems"),
    prevent_initial_call=True,
)
def show_multi(sel):
    return json.dumps(sel, indent=2) if sel else "Select items..."


@callback(
    Output("tree-sel-checkbox-out", "children"),
    Input("tree-sel-checkbox", "selectedItems"),
    prevent_initial_call=True,
)
def show_checkbox(sel):
    return json.dumps(sel, indent=2) if sel else "Check items..."


@callback(
    Output("tree-sel-propagation-out", "children"),
    Input("tree-sel-propagation", "selectedItems"),
    prevent_initial_call=True,
)
def show_propagation(sel):
    return json.dumps(sel, indent=2) if sel else "Check items..."


@callback(
    Output("tree-sel-controlled", "selectedItems"),
    Output("tree-sel-controlled-out", "children"),
    Input("tree-sel-btn-grid", "n_clicks"),
    Input("tree-sel-btn-pickers", "n_clicks"),
    Input("tree-sel-btn-clear", "n_clicks"),
    Input("tree-sel-controlled", "selectedItems"),
    prevent_initial_call=True,
)
def controlled_selection(grid_clicks, picker_clicks, clear_clicks, current):
    from dash import ctx
    trigger = ctx.triggered_id
    if trigger == "tree-sel-btn-grid":
        sel = ["grid-com", "grid-pro", "grid-premium"]
    elif trigger == "tree-sel-btn-pickers":
        sel = ["pickers-com", "pickers-pro"]
    elif trigger == "tree-sel-btn-clear":
        sel = []
    else:
        sel = current or []
    return sel, json.dumps(sel, indent=2)
