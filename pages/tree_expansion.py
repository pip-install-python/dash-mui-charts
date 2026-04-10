"""
Tree View - Expansion

Demonstrates expansion triggers, controlled expansion,
and expand/collapse all.
"""

import json
import dash
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/tree-expansion', name='Tree Expansion')

from dash_mui_charts import TreeView

DEEP_TREE = [
    {"id": "root-a", "label": "Category A", "children": [
        {"id": "a-1", "label": "Sub A-1", "children": [
            {"id": "a-1-i", "label": "Item A-1-i"},
            {"id": "a-1-ii", "label": "Item A-1-ii"},
        ]},
        {"id": "a-2", "label": "Sub A-2", "children": [
            {"id": "a-2-i", "label": "Item A-2-i"},
        ]},
    ]},
    {"id": "root-b", "label": "Category B", "children": [
        {"id": "b-1", "label": "Sub B-1"},
        {"id": "b-2", "label": "Sub B-2", "children": [
            {"id": "b-2-i", "label": "Item B-2-i"},
            {"id": "b-2-ii", "label": "Item B-2-ii"},
        ]},
    ]},
    {"id": "root-c", "label": "Category C", "children": [
        {"id": "c-1", "label": "Sub C-1"},
    ]},
]

ALL_PARENT_IDS = ["root-a", "a-1", "a-2", "root-b", "b-2", "root-c"]

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
    html.H2("Tree View - Expansion"),
    html.P("Control how tree nodes expand and collapse.", style={'color': '#666'}),

    # --- 1. expansionTrigger="content" (default) ---
    html.Div([
        html.H3('1. Expansion Trigger: "content" (default)'),
        html.P("Click anywhere on the item row to expand/collapse.", style={'color': '#666'}),
        TreeView(
            id="tree-exp-content",
            items=DEEP_TREE,
            expansionTrigger="content",
        ),
    ], style=section_style),

    # --- 2. expansionTrigger="iconContainer" ---
    html.Div([
        html.H3('2. Expansion Trigger: "iconContainer"'),
        html.P("Only clicking the expand/collapse icon toggles the node.", style={'color': '#666'}),
        TreeView(
            id="tree-exp-icon",
            items=DEEP_TREE,
            expansionTrigger="iconContainer",
        ),
    ], style=section_style),

    # --- 3. Controlled expansion ---
    html.Div([
        html.H3("3. Controlled Expansion"),
        html.P("Use buttons to expand all or collapse all programmatically.", style={'color': '#666'}),
        html.Div([
            html.Button("Expand All", id="tree-exp-btn-all",
                        style={'marginRight': '8px', 'padding': '6px 12px'}),
            html.Button("Collapse All", id="tree-exp-btn-none",
                        style={'marginRight': '8px', 'padding': '6px 12px'}),
            html.Button("Expand Root Only", id="tree-exp-btn-root",
                        style={'padding': '6px 12px'}),
        ], style={'marginBottom': '10px'}),
        TreeView(
            id="tree-exp-controlled",
            items=DEEP_TREE,
            expandedItems=[],
        ),
        html.P("Expanded items:", style={'marginTop': '10px', 'fontSize': '13px', 'color': '#666'}),
        html.Pre(id="tree-exp-controlled-out", children="[]", style=output_style),
    ], style=section_style),

    # --- 4. Track expansion changes ---
    html.Div([
        html.H3("4. Track Expansion Changes"),
        html.P("expandedItems output updates whenever nodes are toggled.", style={'color': '#666'}),
        TreeView(
            id="tree-exp-track",
            items=DEEP_TREE,
            defaultExpandedItems=["root-a"],
        ),
        html.P("Currently expanded:", style={'marginTop': '10px', 'fontSize': '13px', 'color': '#666'}),
        html.Pre(id="tree-exp-track-out", children='["root-a"]', style=output_style),
    ], style=section_style),
])


@callback(
    Output("tree-exp-controlled", "expandedItems"),
    Output("tree-exp-controlled-out", "children"),
    Input("tree-exp-btn-all", "n_clicks"),
    Input("tree-exp-btn-none", "n_clicks"),
    Input("tree-exp-btn-root", "n_clicks"),
    Input("tree-exp-controlled", "expandedItems"),
    prevent_initial_call=True,
)
def controlled_expand(all_clicks, none_clicks, root_clicks, current):
    from dash import ctx
    trigger = ctx.triggered_id
    if trigger == "tree-exp-btn-all":
        items = ALL_PARENT_IDS
    elif trigger == "tree-exp-btn-none":
        items = []
    elif trigger == "tree-exp-btn-root":
        items = ["root-a", "root-b", "root-c"]
    else:
        items = current or []
    return items, json.dumps(items, indent=2)


@callback(
    Output("tree-exp-track-out", "children"),
    Input("tree-exp-track", "expandedItems"),
    prevent_initial_call=True,
)
def track_expansion(expanded):
    return json.dumps(expanded, indent=2) if expanded else "[]"
