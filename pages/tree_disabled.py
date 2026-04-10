"""
Tree View - Disabled Items

Demonstrates disabling specific items, disabledItemsFocusable,
and interaction of disabled items with selection.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/tree-disabled', name='Tree Disabled')

from dash_mui_charts import TreeView

PRODUCTS = [
    {"id": "grid", "label": "Data Grid", "children": [
        {"id": "grid-com", "label": "@mui/x-data-grid (Free)"},
        {"id": "grid-pro", "label": "@mui/x-data-grid-pro (Pro)"},
        {"id": "grid-premium", "label": "@mui/x-data-grid-premium (Premium)"},
    ]},
    {"id": "pickers", "label": "Date and Time Pickers", "children": [
        {"id": "pickers-com", "label": "@mui/x-date-pickers (Free)"},
        {"id": "pickers-pro", "label": "@mui/x-date-pickers-pro (Pro)"},
    ]},
    {"id": "charts", "label": "Charts", "children": [
        {"id": "charts-com", "label": "@mui/x-charts (Free)"},
    ]},
    {"id": "tree", "label": "Tree View", "children": [
        {"id": "tree-com", "label": "@mui/x-tree-view (Free)"},
        {"id": "tree-pro", "label": "@mui/x-tree-view-pro (Pro)"},
    ]},
]

PRO_ITEMS = ["grid-pro", "grid-premium", "pickers-pro", "tree-pro"]

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
    html.H2("Tree View - Disabled Items"),
    html.P("Disable specific items to prevent selection and interaction.", style={'color': '#666'}),

    # --- 1. Disabled specific items ---
    html.Div([
        html.H3("1. Disabled Pro/Premium Items"),
        html.P(
            f"disabledItems={PRO_ITEMS} — these items appear greyed out and cannot be selected.",
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-dis-basic",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            disabledItems=PRO_ITEMS,
        ),
    ], style=section_style),

    # --- 2. Disabled with checkbox selection ---
    html.Div([
        html.H3("2. Disabled Items + Checkbox Selection"),
        html.P("Disabled items cannot be checked. Selection propagation skips disabled items.", style={'color': '#666'}),
        TreeView(
            id="tree-dis-checkbox",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers", "charts", "tree"],
            disabledItems=PRO_ITEMS,
            multiSelect=True,
            checkboxSelection=True,
            selectionPropagation={"parents": True, "descendants": True},
        ),
        html.Pre(id="tree-dis-checkbox-out", children="Check items...", style=output_style),
    ], style=section_style),

    # --- 3. disabledItemsFocusable ---
    html.Div([
        html.H3("3. Disabled Items Focusable"),
        html.P(
            "disabledItemsFocusable=True allows keyboard focus on disabled items "
            "(accessibility: screen readers can still read them).",
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-dis-focusable",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "pickers"],
            disabledItems=PRO_ITEMS,
            disabledItemsFocusable=True,
        ),
    ], style=section_style),

    # --- 4. Disable parent nodes ---
    html.Div([
        html.H3("4. Disable Parent Nodes"),
        html.P(
            'disabledItems=["pickers", "tree"] — disabling a parent also prevents expanding it.',
            style={'color': '#666'},
        ),
        TreeView(
            id="tree-dis-parents",
            items=PRODUCTS,
            defaultExpandedItems=["grid", "charts"],
            disabledItems=["pickers", "tree"],
        ),
    ], style=section_style),
])


@callback(
    Output("tree-dis-checkbox-out", "children"),
    Input("tree-dis-checkbox", "selectedItems"),
    prevent_initial_call=True,
)
def show_disabled_selection(sel):
    return json.dumps(sel, indent=2) if sel else "Check items..."
