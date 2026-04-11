"""
Changelog Page - Rendered from CHANGELOG.md
"""

import os
import dash
import dash_mantine_components as dmc
from dash import html, dcc

dash.register_page(__name__, path='/changelog', name='Changelog')

# Read the changelog file
_changelog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CHANGELOG.md')
with open(_changelog_path, encoding='utf-8') as _f:
    _changelog_md = _f.read()

layout = html.Div([
    dmc.Title("Changelog", order=2, mb="md"),
    dmc.Text("All notable changes to dash-mui-charts.", size="lg", c="dimmed", mb="lg"),
    dmc.Paper(
        dcc.Markdown(
            _changelog_md,
            style={'fontSize': '14px', 'lineHeight': '1.7'},
            className='changelog-content',
        ),
        p="xl",
        radius="md",
        withBorder=True,
    ),
], style={'maxWidth': '900px', 'margin': '0 auto'})
