"""
Tree View - Icons & Appearance

Demonstrates custom icons, indentation, height, and sx styling.
"""

import dash
from dash import html

dash.register_page(__name__, path='/tree-icons', name='Tree Icons')

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
    ]},
]

section_style = {'marginBottom': '40px'}

layout = html.Div([
    html.H2("Tree View - Icons & Appearance"),
    html.P("Customize icons, indentation, height, and styling.", style={'color': 'var(--mantine-color-dimmed)'}),

    # --- 1. Default icons ---
    html.Div([
        html.H3("1. Default Icons"),
        html.P("No icon props set — uses MUI defaults.", style={'color': 'var(--mantine-color-dimmed)'}),
        TreeView(
            id="tree-icon-default",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs"],
        ),
    ], style=section_style),

    # --- 2. File explorer icons ---
    html.Div([
        html.H3("2. File Explorer Icons"),
        html.P(
            'expandIcon="ChevronRight", collapseIcon="ExpandMore", endIcon="InsertDriveFile"',
            style={'color': 'var(--mantine-color-dimmed)'},
        ),
        TreeView(
            id="tree-icon-file",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "src"],
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
            endIcon="InsertDriveFile",
        ),
    ], style=section_style),

    # --- 3. Add/Remove icons ---
    html.Div([
        html.H3("3. Add/Remove Style Icons"),
        html.P(
            'expandIcon="Add", collapseIcon="Remove"',
            style={'color': 'var(--mantine-color-dimmed)'},
        ),
        TreeView(
            id="tree-icon-addremove",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs"],
            expandIcon="Add",
            collapseIcon="Remove",
        ),
    ], style=section_style),

    # --- 4. Arrow icons ---
    html.Div([
        html.H3("4. Arrow Drop Down Icons"),
        html.P(
            'expandIcon="ArrowRight", collapseIcon="ArrowDropDown"',
            style={'color': 'var(--mantine-color-dimmed)'},
        ),
        TreeView(
            id="tree-icon-arrow",
            items=FILE_SYSTEM,
            defaultExpandedItems=["images"],
            expandIcon="ArrowRight",
            collapseIcon="ArrowDropDown",
        ),
    ], style=section_style),

    # --- 5. Custom indentation ---
    html.Div([
        html.H3("5. Custom Indentation"),
        html.P("Compare different itemChildrenIndentation values.", style={'color': 'var(--mantine-color-dimmed)'}),
        html.Div([
            html.Div([
                html.P("indentation=8", style={'fontSize': '13px', 'fontWeight': 'bold'}),
                TreeView(
                    id="tree-icon-indent-8",
                    items=FILE_SYSTEM,
                    defaultExpandedItems=["docs", "docs-projects"],
                    itemChildrenIndentation=8,
                ),
            ], style={'flex': '1', 'marginRight': '20px'}),
            html.Div([
                html.P("indentation=24 (default-ish)", style={'fontSize': '13px', 'fontWeight': 'bold'}),
                TreeView(
                    id="tree-icon-indent-24",
                    items=FILE_SYSTEM,
                    defaultExpandedItems=["docs", "docs-projects"],
                    itemChildrenIndentation=24,
                ),
            ], style={'flex': '1', 'marginRight': '20px'}),
            html.Div([
                html.P("indentation=48", style={'fontSize': '13px', 'fontWeight': 'bold'}),
                TreeView(
                    id="tree-icon-indent-48",
                    items=FILE_SYSTEM,
                    defaultExpandedItems=["docs", "docs-projects"],
                    itemChildrenIndentation=48,
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex'}),
    ], style=section_style),

    # --- 6. Fixed height with scroll ---
    html.Div([
        html.H3("6. Fixed Height with Scroll"),
        html.P("height=200 constrains the tree and adds scrolling.", style={'color': 'var(--mantine-color-dimmed)'}),
        TreeView(
            id="tree-icon-height",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "docs-projects", "images", "src"],
            height=200,
            sx={"overflow": "auto"},
        ),
    ], style=section_style),

    # --- 7. SX styling ---
    html.Div([
        html.H3("7. SX Styling"),
        html.P("Custom styles via the sx prop.", style={'color': 'var(--mantine-color-dimmed)'}),
        TreeView(
            id="tree-icon-sx",
            items=FILE_SYSTEM,
            defaultExpandedItems=["docs", "src"],
            expandIcon="ChevronRight",
            collapseIcon="ExpandMore",
            endIcon="InsertDriveFile",
            sx={
                "border": "1px solid #1976d2",
                "borderRadius": "8px",
                "padding": "12px",
                "backgroundColor": "#f8f9ff",
                "& .MuiTreeItem-label": {
                    "fontSize": "14px",
                },
                "& .MuiTreeItem-iconContainer": {
                    "color": "#1976d2",
                },
            },
        ),
    ], style=section_style),
])
