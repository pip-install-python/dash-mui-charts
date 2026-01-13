"""
Dash MUI Charts - Example Application

Multi-page Dash application demonstrating the LineChart component
with basic and Pro features.
"""

import os
from dash import Dash, html, dcc, page_container, page_registry

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load MUI X Pro license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

# Store license key in app config for pages to access
app.server.config['MUI_LICENSE_KEY'] = MUI_LICENSE_KEY

# Navigation styles
nav_style = {
    'backgroundColor': '#1976d2',
    'padding': '15px 20px',
    'marginBottom': '20px',
}

nav_link_style = {
    'color': 'white',
    'textDecoration': 'none',
    'padding': '8px 16px',
    'marginRight': '10px',
    'borderRadius': '4px',
    'display': 'inline-block',
}

nav_link_hover_style = {
    **nav_link_style,
    'backgroundColor': 'rgba(255,255,255,0.1)',
}

app.layout = html.Div([
    # Navigation header
    html.Nav([
        html.Div([
            html.Span(
                "Dash MUI Charts",
                style={
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '20px',
                    'marginRight': '30px',
                }
            ),
            *[
                dcc.Link(
                    page['name'],
                    href=page['path'],
                    style=nav_link_style,
                )
                for page in page_registry.values()
            ],
        ], style={'maxWidth': '1200px', 'margin': '0 auto'}),
    ], style=nav_style),

    # Page content
    html.Div([
        page_container,
    ], style={'maxWidth': '1000px', 'margin': '0 auto', 'padding': '0 20px 40px'}),

    # Store license key for pages
    dcc.Store(id='license-key-store', data=MUI_LICENSE_KEY),
])


if __name__ == '__main__':
    app.run(debug=True, port=7666)
