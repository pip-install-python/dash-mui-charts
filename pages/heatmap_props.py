"""
Heatmap Props Playground

Interactive control panel for exploring and customizing Heatmap component properties.
Uses dash-mantine-components for the control panel UI.
"""
import os
import json
import dash
from dash import html, callback, Input, Output, State, dcc

import dash_mantine_components as dmc
from dash_mui_charts import Heatmap

dash.register_page(
    __name__,
    path='/heatmap-props',
    name='Heatmap Props'
)

# Get license key from environment
MUI_LICENSE_KEY = os.environ.get('MUI_PRO_API_KEY', '')

# Sample data - 5x5 grid
SAMPLE_DATA = [
    [0, 0, 2], [1, 0, 5], [2, 0, 8], [3, 0, 4], [4, 0, 6],
    [0, 1, 7], [1, 1, 3], [2, 1, 9], [3, 1, 1], [4, 1, 5],
    [0, 2, 4], [1, 2, 8], [2, 2, 2], [3, 2, 7], [4, 2, 3],
    [0, 3, 6], [1, 3, 1], [2, 3, 5], [3, 3, 9], [4, 3, 8],
    [0, 4, 3], [1, 4, 6], [2, 4, 4], [3, 4, 2], [4, 4, 7],
]
X_LABELS = ['A', 'B', 'C', 'D', 'E']
Y_LABELS = ['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5']

# Color swatches
COLOR_SWATCHES = [
    '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5',
    '#1976d2', '#1565c0', '#0d47a1', '#4fc3f7', '#00bcd4',
]
WARM_SWATCHES = [
    '#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726',
    '#ff9800', '#f57c00', '#ef6c00', '#e65100', '#ff5722',
]
COOL_SWATCHES = [
    '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a',
    '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20',
]


def create_control_card(title, children):
    """Helper to create a styled control card."""
    return dmc.Paper(
        shadow='sm',
        radius='md',
        p='md',
        children=[
            dmc.Text(title, fw=600, size='lg', mb='md'),
            dmc.Stack(gap='sm', children=children),
        ],
    )


layout = dmc.MantineProvider(
    html.Div([
        # Header
        html.Div([
            html.H1('Heatmap Props Playground'),
            html.P(
                'Interactively explore and customize Heatmap component properties. '
                'Changes are reflected in real-time.',
                style={'color': '#666', 'marginBottom': '30px'}
            ),
        ]),

        # Pro License Warning (if no key)
        html.Div([
            dmc.Paper(
                shadow='xs',
                radius='md',
                p='md',
                style={'backgroundColor': '#fff3e0', 'borderLeft': '4px solid #ff9800'},
                children=[
                    dmc.Text(
                        'This feature requires an MUI X Pro license key. '
                        'Set MUI_PRO_API_KEY environment variable.',
                        size='sm',
                        c='orange',
                    ),
                ],
            ),
        ], style={'marginBottom': '20px'}) if not MUI_LICENSE_KEY else None,

        # Live Preview Section
        dmc.Paper(
            shadow='sm',
            radius='md',
            p='lg',
            mb='lg',
            children=[
                dmc.Text('Live Preview', fw=600, size='lg', mb='md'),
                html.Div(
                    id='heatmap-preview-container',
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'minHeight': '350px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '8px',
                        'padding': '20px',
                        'transition': 'background-color 0.3s ease',
                    },
                    children=[
                        html.Div(id='heatmap-preview'),
                    ],
                ),
                # Interaction Info
                dmc.SimpleGrid(
                    cols=2,
                    spacing='md',
                    mt='md',
                    children=[
                        dmc.Paper(
                            p='sm',
                            radius='sm',
                            style={'backgroundColor': '#e3f2fd'},
                            children=[
                                dmc.Text('Hover Info', size='xs', c='dimmed', mb='xs'),
                                html.Div(
                                    id='heatmap-hover-info',
                                    children='Hover over a cell',
                                    style={'fontFamily': 'monospace', 'fontSize': '13px'},
                                ),
                            ],
                        ),
                        dmc.Paper(
                            p='sm',
                            radius='sm',
                            style={'backgroundColor': '#e8f5e9'},
                            children=[
                                dmc.Text('Click Data', size='xs', c='dimmed', mb='xs'),
                                html.Div(
                                    id='heatmap-click-info',
                                    children='Click on a cell',
                                    style={'fontFamily': 'monospace', 'fontSize': '13px'},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Control Panel Grid
        dmc.SimpleGrid(
            cols={'base': 1, 'sm': 2, 'lg': 3},
            spacing='lg',
            mb='lg',
            children=[
                # Color Scale Card
                create_control_card('Color Scale', [
                    dmc.Text('Scale Type', size='sm', fw=500, mb='xs'),
                    dmc.SegmentedControl(
                        id='ctrl-scale-type',
                        data=[
                            {'value': 'continuous', 'label': 'Continuous'},
                            {'value': 'piecewise', 'label': 'Piecewise'},
                        ],
                        value='continuous',
                        fullWidth=True,
                        mb='md',
                    ),
                    dmc.ColorInput(
                        id='ctrl-min-color',
                        label='Min Color',
                        value='#e3f2fd',
                        format='hex',
                        swatches=COLOR_SWATCHES,
                        mb='sm',
                    ),
                    dmc.ColorInput(
                        id='ctrl-max-color',
                        label='Max Color',
                        value='#1565c0',
                        format='hex',
                        swatches=COLOR_SWATCHES,
                        mb='sm',
                    ),
                    dmc.NumberInput(
                        id='ctrl-min-value',
                        label='Min Value',
                        value=0,
                        min=-100,
                        max=100,
                        mb='sm',
                    ),
                    dmc.NumberInput(
                        id='ctrl-max-value',
                        label='Max Value',
                        value=10,
                        min=-100,
                        max=100,
                    ),
                ]),

                # Dimensions Card
                create_control_card('Dimensions', [
                    dmc.Text('Width', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='ctrl-width',
                        value=400,
                        min=200,
                        max=600,
                        step=10,
                        marks=[
                            {'value': 200, 'label': '200'},
                            {'value': 400, 'label': '400'},
                            {'value': 600, 'label': '600'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Height', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='ctrl-height',
                        value=300,
                        min=200,
                        max=500,
                        step=10,
                        marks=[
                            {'value': 200, 'label': '200'},
                            {'value': 350, 'label': '350'},
                            {'value': 500, 'label': '500'},
                        ],
                        mb='md',
                    ),
                ]),

                # Cell Style Card
                create_control_card('Cell Style', [
                    dmc.Text('Style', size='sm', fw=500, mb='xs'),
                    dmc.SegmentedControl(
                        id='ctrl-cell-style',
                        data=[
                            {'value': 'default', 'label': 'Default'},
                            {'value': 'rounded', 'label': 'Rounded'},
                        ],
                        value='default',
                        fullWidth=True,
                        mb='md',
                    ),
                    dmc.Text('Gap (px)', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='ctrl-gap',
                        value=4,
                        min=0,
                        max=10,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 5, 'label': '5'},
                            {'value': 10, 'label': '10'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Border Radius (px)', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='ctrl-border-radius',
                        value=10,
                        min=0,
                        max=20,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 10, 'label': '10'},
                            {'value': 20, 'label': '20'},
                        ],
                        mb='lg',
                    ),
                    dmc.Switch(
                        id='ctrl-show-values',
                        label='Show Values in Cells',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Text('Font Size (px)', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='ctrl-font-size',
                        value=12,
                        min=8,
                        max=18,
                        step=1,
                        marks=[
                            {'value': 8, 'label': '8'},
                            {'value': 12, 'label': '12'},
                            {'value': 18, 'label': '18'},
                        ],
                        mb='lg',
                    ),
                    dmc.ColorInput(
                        id='ctrl-text-color',
                        label='Text Color',
                        value='#ffffff',
                        format='hex',
                        swatches=['#ffffff', '#000000', '#333333', '#666666'],
                    ),
                ]),

                # Interactions Card
                create_control_card('Interactions', [
                    dmc.Switch(
                        id='ctrl-highlight',
                        label='Highlight on Hover',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Switch(
                        id='ctrl-hide-legend',
                        label='Hide Legend',
                        checked=False,
                        mb='sm',
                    ),
                ]),

                # Margins Card
                create_control_card('Margins', [
                    dmc.SimpleGrid(
                        cols=2,
                        spacing='sm',
                        children=[
                            dmc.NumberInput(
                                id='ctrl-margin-top',
                                label='Top',
                                value=20,
                                min=0,
                                max=100,
                            ),
                            dmc.NumberInput(
                                id='ctrl-margin-right',
                                label='Right',
                                value=20,
                                min=0,
                                max=100,
                            ),
                            dmc.NumberInput(
                                id='ctrl-margin-bottom',
                                label='Bottom',
                                value=50,
                                min=0,
                                max=100,
                            ),
                            dmc.NumberInput(
                                id='ctrl-margin-left',
                                label='Left',
                                value=80,
                                min=0,
                                max=100,
                            ),
                        ],
                    ),
                ]),
            ],
        ),

        # Generated Code Section
        dmc.Paper(
            shadow='sm',
            radius='md',
            p='lg',
            children=[
                dmc.Group(
                    justify='space-between',
                    mb='md',
                    children=[
                        dmc.Text('Generated Code', fw=600, size='lg'),
                        dmc.Group(
                            gap='sm',
                            children=[
                                dmc.Button(
                                    'Reset to Defaults',
                                    id='reset-heatmap-btn',
                                    variant='outline',
                                    size='sm',
                                ),
                                dcc.Clipboard(
                                    target_id='generated-heatmap-code',
                                    style={
                                        'display': 'inline-block',
                                        'backgroundColor': '#1976d2',
                                        'color': 'white',
                                        'padding': '6px 12px',
                                        'borderRadius': '4px',
                                        'cursor': 'pointer',
                                        'fontSize': '14px',
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Pre(
                    id='generated-heatmap-code',
                    style={
                        'backgroundColor': '#1e1e1e',
                        'color': '#d4d4d4',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'fontSize': '13px',
                        'lineHeight': '1.5',
                        'overflowX': 'auto',
                        'margin': 0,
                    },
                ),
            ],
        ),

    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}),
)


@callback(
    Output('heatmap-preview', 'children'),
    Output('generated-heatmap-code', 'children'),
    Input('ctrl-scale-type', 'value'),
    Input('ctrl-min-color', 'value'),
    Input('ctrl-max-color', 'value'),
    Input('ctrl-min-value', 'value'),
    Input('ctrl-max-value', 'value'),
    Input('ctrl-width', 'value'),
    Input('ctrl-height', 'value'),
    Input('ctrl-cell-style', 'value'),
    Input('ctrl-gap', 'value'),
    Input('ctrl-border-radius', 'value'),
    Input('ctrl-show-values', 'checked'),
    Input('ctrl-font-size', 'value'),
    Input('ctrl-text-color', 'value'),
    Input('ctrl-highlight', 'checked'),
    Input('ctrl-hide-legend', 'checked'),
    Input('ctrl-margin-top', 'value'),
    Input('ctrl-margin-right', 'value'),
    Input('ctrl-margin-bottom', 'value'),
    Input('ctrl-margin-left', 'value'),
)
def update_heatmap(
    scale_type, min_color, max_color, min_value, max_value,
    width, height, cell_style, gap, border_radius,
    show_values, font_size, text_color, highlight, hide_legend,
    margin_top, margin_right, margin_bottom, margin_left,
):
    """Update heatmap preview and generated code."""

    # Build color scale
    color_scale = {
        'type': scale_type,
        'min': min_value or 0,
        'max': max_value or 10,
        'colors': [min_color, max_color],
    }

    # Build cell style (only for rounded)
    cell_style_prop = None
    if cell_style == 'rounded':
        cell_style_prop = {
            'gap': gap,
            'borderRadius': border_radius,
            'showValue': show_values,
            'fontSize': font_size,
            'textColor': text_color,
        }

    # Build highlight scope
    highlight_scope = {'highlight': 'item'} if highlight else None

    # Build margin
    margin = {
        'top': margin_top or 20,
        'right': margin_right or 20,
        'bottom': margin_bottom or 50,
        'left': margin_left or 80,
    }

    # Create heatmap component
    heatmap = Heatmap(
        id='preview-heatmap',
        licenseKey=MUI_LICENSE_KEY,
        data=SAMPLE_DATA,
        xAxis={'data': X_LABELS},
        yAxis={'data': Y_LABELS},
        width=width,
        height=height,
        colorScale=color_scale,
        cellStyle=cell_style_prop,
        highlightScope=highlight_scope,
        hideLegend=hide_legend,
        margin=margin,
    )

    # Generate code string
    code_lines = ['Heatmap(']
    code_lines.append('    data=data,')
    code_lines.append(f"    xAxis={{'data': {X_LABELS}}},")
    code_lines.append(f"    yAxis={{'data': {Y_LABELS}}},")
    code_lines.append(f'    width={width},')
    code_lines.append(f'    height={height},')
    code_lines.append(f'    colorScale={{')
    code_lines.append(f"        'type': '{scale_type}',")
    code_lines.append(f"        'min': {min_value},")
    code_lines.append(f"        'max': {max_value},")
    code_lines.append(f"        'colors': ['{min_color}', '{max_color}'],")
    code_lines.append(f'    }},')

    if cell_style_prop:
        code_lines.append(f'    cellStyle={{')
        code_lines.append(f"        'gap': {gap},")
        code_lines.append(f"        'borderRadius': {border_radius},")
        code_lines.append(f"        'showValue': {show_values},")
        code_lines.append(f"        'fontSize': {font_size},")
        code_lines.append(f"        'textColor': '{text_color}',")
        code_lines.append(f'    }},')

    if highlight_scope:
        code_lines.append(f"    highlightScope={{'highlight': 'item'}},")

    if hide_legend:
        code_lines.append(f'    hideLegend=True,')

    code_lines.append(f'    margin={{')
    code_lines.append(f"        'top': {margin_top}, 'right': {margin_right},")
    code_lines.append(f"        'bottom': {margin_bottom}, 'left': {margin_left},")
    code_lines.append(f'    }},')
    code_lines.append(')')

    code = '\n'.join(code_lines)

    return heatmap, code


@callback(
    Output('heatmap-hover-info', 'children'),
    Input('preview-heatmap', 'highlightedItem'),
    prevent_initial_call=True
)
def update_hover_info(highlighted_item):
    """Display current hover info."""
    if highlighted_item:
        return json.dumps(highlighted_item, indent=2)
    return 'Hover over a cell'


@callback(
    Output('heatmap-click-info', 'children'),
    Input('preview-heatmap', 'clickData'),
    prevent_initial_call=True
)
def update_click_info(click_data):
    """Display click data."""
    if click_data:
        return f"Cell ({click_data.get('x')}, {click_data.get('y')}) = {click_data.get('value')}"
    return 'Click on a cell'


@callback(
    Output('ctrl-scale-type', 'value'),
    Output('ctrl-min-color', 'value'),
    Output('ctrl-max-color', 'value'),
    Output('ctrl-min-value', 'value'),
    Output('ctrl-max-value', 'value'),
    Output('ctrl-width', 'value'),
    Output('ctrl-height', 'value'),
    Output('ctrl-cell-style', 'value'),
    Output('ctrl-gap', 'value'),
    Output('ctrl-border-radius', 'value'),
    Output('ctrl-show-values', 'checked'),
    Output('ctrl-font-size', 'value'),
    Output('ctrl-text-color', 'value'),
    Output('ctrl-highlight', 'checked'),
    Output('ctrl-hide-legend', 'checked'),
    Output('ctrl-margin-top', 'value'),
    Output('ctrl-margin-right', 'value'),
    Output('ctrl-margin-bottom', 'value'),
    Output('ctrl-margin-left', 'value'),
    Input('reset-heatmap-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_controls(n_clicks):
    """Reset all controls to defaults."""
    return (
        'continuous',  # scale type
        '#e3f2fd',     # min color
        '#1565c0',     # max color
        0,             # min value
        10,            # max value
        400,           # width
        300,           # height
        'default',     # cell style
        4,             # gap
        10,            # border radius
        True,          # show values
        12,            # font size
        '#ffffff',     # text color
        True,          # highlight
        False,         # hide legend
        20,            # margin top
        20,            # margin right
        50,            # margin bottom
        80,            # margin left
    )
