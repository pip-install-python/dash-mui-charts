"""
Home Page - Dash MUI Charts Examples
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path='/', name='Home')

# Card style
card_style = {
    'border': '1px solid #e0e0e0',
    'borderRadius': '8px',
    'padding': '24px',
    'marginBottom': '20px',
    'backgroundColor': 'white',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
}

link_card_style = {
    **card_style,
    'cursor': 'pointer',
    'transition': 'box-shadow 0.2s',
}

layout = html.Div([
    # Hero section
    html.Div([
        html.H1(
            "Dash MUI Charts",
            style={'marginBottom': '10px', 'color': '#1976d2'}
        ),
        html.P(
            "A Dash component library wrapping MUI X Charts Pro for creating "
            "beautiful, interactive charts with advanced features like zoom, pan, and more.",
            style={'fontSize': '18px', 'color': '#666', 'maxWidth': '700px'}
        ),
    ], style={'textAlign': 'center', 'padding': '40px 0'}),

    # Feature cards
    html.Div([
        html.H2("Examples", style={'marginBottom': '20px'}),

        # Basic LineChart Card
        dcc.Link([
            html.Div([
                html.H3("LineChart Basics", style={'color': '#1976d2', 'marginBottom': '10px'}),
                html.P(
                    "Learn the fundamentals of creating line charts including "
                    "multiple series, area charts, stacked areas, custom curves, "
                    "biaxial charts, and click event handling.",
                    style={'color': '#666', 'marginBottom': '15px'}
                ),
                html.Div([
                    html.Span("Multiple Series", style={'backgroundColor': '#e3f2fd', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Area Charts", style={'backgroundColor': '#e3f2fd', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Biaxial", style={'backgroundColor': '#e3f2fd', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Click Events", style={'backgroundColor': '#e3f2fd', 'padding': '4px 8px', 'borderRadius': '4px', 'fontSize': '12px'}),
                ]),
            ], style=link_card_style),
        ], href='/linechart-basic', style={'textDecoration': 'none'}),

        # Pro LineChart Card
        dcc.Link([
            html.Div([
                html.Div([
                    html.H3("LineChart Pro", style={'color': '#1976d2', 'marginBottom': '0', 'display': 'inline'}),
                    html.Span(
                        "PRO",
                        style={
                            'backgroundColor': '#ff9800',
                            'color': 'white',
                            'padding': '2px 8px',
                            'borderRadius': '4px',
                            'fontSize': '10px',
                            'fontWeight': 'bold',
                            'marginLeft': '10px',
                            'verticalAlign': 'middle',
                        }
                    ),
                ], style={'marginBottom': '10px'}),
                html.P(
                    "Explore advanced Pro features including zoom and pan functionality, "
                    "zoom slider control, Y-axis zoom, controlled/uncontrolled zoom states, "
                    "and zoom state callbacks.",
                    style={'color': '#666', 'marginBottom': '15px'}
                ),
                html.Div([
                    html.Span("Zoom Slider", style={'backgroundColor': '#fff3e0', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Pan", style={'backgroundColor': '#fff3e0', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Zoom Callbacks", style={'backgroundColor': '#fff3e0', 'padding': '4px 8px', 'borderRadius': '4px', 'marginRight': '8px', 'fontSize': '12px'}),
                    html.Span("Y-Axis Zoom", style={'backgroundColor': '#fff3e0', 'padding': '4px 8px', 'borderRadius': '4px', 'fontSize': '12px'}),
                ]),
            ], style=link_card_style),
        ], href='/linechart-pro', style={'textDecoration': 'none'}),

    ]),

    # Getting Started section
    html.Div([
        html.H2("Getting Started", style={'marginTop': '40px', 'marginBottom': '20px'}),
        html.Div([
            html.H4("Installation", style={'marginBottom': '10px'}),
            html.Pre(
                "pip install dash-mui-charts",
                style={
                    'backgroundColor': '#f5f5f5',
                    'padding': '15px',
                    'borderRadius': '4px',
                    'overflow': 'auto',
                }
            ),
            html.H4("Basic Usage", style={'marginTop': '20px', 'marginBottom': '10px'}),
            html.Pre(
                """from dash import Dash, html
from dash_mui_charts import LineChart

app = Dash(__name__)

app.layout = html.Div([
    LineChart(
        id='my-chart',
        height=400,
        series=[
            {'data': [1, 4, 2, 5, 7], 'label': 'Series A'},
        ],
        xAxis=[{'data': [1, 2, 3, 4, 5]}],
    )
])

if __name__ == '__main__':
    app.run(debug=True)""",
                style={
                    'backgroundColor': '#f5f5f5',
                    'padding': '15px',
                    'borderRadius': '4px',
                    'overflow': 'auto',
                    'fontSize': '13px',
                }
            ),
        ], style=card_style),
    ]),
])
