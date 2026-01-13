"""
SparklineChart Styling Playground
Interactive control board for customizing sparkline appearance using dash-mantine-components.
"""
import dash
from dash import html, callback, Input, Output, State, dcc, no_update
import dash_mantine_components as dmc
from dash_mui_charts import SparklineChart

dash.register_page(__name__, path='/sparkline-style', name='Sparkline Style')

# Sample data for preview
PREVIEW_DATA = [
    23, 25, 22, 28, 32, 30, 35, 33, 38, 42,
    40, 45, 43, 48, 52, 50, 55, 53, 58, 62
]

# Color swatches
COLOR_SWATCHES = [
    '#1976d2', '#4caf50', '#ff9800', '#f44336', '#9c27b0',
    '#00bcd4', '#795548', '#607d8b', '#e91e63', '#3f51b5',
]

BACKGROUND_SWATCHES = [
    '#ffffff', '#f5f5f5', '#e3f2fd', '#e8f5e9',
    '#fff3e0', '#fce4ec', '#1a1a2e', '#2d2d2d',
]

# Curve options
CURVE_OPTIONS = [
    {'value': 'linear', 'label': 'Linear'},
    {'value': 'natural', 'label': 'Natural'},
    {'value': 'monotoneX', 'label': 'Monotone X'},
    {'value': 'monotoneY', 'label': 'Monotone Y'},
    {'value': 'step', 'label': 'Step'},
    {'value': 'stepBefore', 'label': 'Step Before'},
    {'value': 'stepAfter', 'label': 'Step After'},
    {'value': 'catmullRom', 'label': 'Catmull-Rom'},
]

# Axis highlight options
AXIS_HIGHLIGHT_OPTIONS = [
    {'value': 'none', 'label': 'None'},
    {'value': 'line', 'label': 'Line'},
    {'value': 'band', 'label': 'Band'},
]

# Baseline options
BASELINE_OPTIONS = [
    {'value': 'min', 'label': 'Min (default)'},
    {'value': 'max', 'label': 'Max'},
    {'value': '0', 'label': 'Zero (0)'},
]

# Card style
card_style = {
    'padding': '20px',
    'marginBottom': '15px',
}


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
    children=[
        html.Div(
            style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'},
            children=[
                # Header
                html.H1('SparklineChart Styling Playground', style={'marginBottom': '10px'}),
                html.P(
                    'Interactive control board for customizing sparkline appearance. '
                    'Adjust the controls below to see real-time changes.',
                    style={'color': '#666', 'marginBottom': '30px'}
                ),

                # Live Preview Section
                dmc.Paper(
                    shadow='md',
                    radius='lg',
                    p='xl',
                    mb='xl',
                    children=[
                        dmc.Text('Live Preview', fw=600, size='xl', mb='md'),
                        html.Div(
                            id='preview-container',
                            style={
                                'padding': '30px',
                                'borderRadius': '8px',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'minHeight': '120px',
                                'backgroundColor': '#ffffff',
                                'transition': 'background-color 0.3s ease',
                            },
                            children=[
                                html.Div(id='sparkline-preview'),
                            ]
                        ),
                        # Hover info display
                        html.Div(
                            id='hover-info',
                            style={
                                'marginTop': '15px',
                                'padding': '10px',
                                'backgroundColor': '#f5f5f5',
                                'borderRadius': '4px',
                                'textAlign': 'center',
                                'fontFamily': 'monospace',
                            },
                            children='Hover over the chart to see interaction data'
                        ),
                    ]
                ),

                # Control Panels
                dmc.SimpleGrid(
                    cols={'base': 1, 'sm': 2, 'lg': 3},
                    spacing='lg',
                    children=[
                        # Colors Card
                        create_control_card('Colors', [
                            dmc.ColorInput(
                                id='color-line',
                                label='Chart Color',
                                value='#1976d2',
                                format='hex',
                                swatches=COLOR_SWATCHES,
                            ),
                            dmc.ColorInput(
                                id='color-background',
                                label='Background Color',
                                value='#ffffff',
                                format='hex',
                                swatches=BACKGROUND_SWATCHES,
                            ),
                        ]),

                        # Chart Type Card
                        create_control_card('Chart Type', [
                            dmc.Text('Plot Type', size='sm', fw=500, mb=5),
                            dmc.SegmentedControl(
                                id='plot-type',
                                data=[
                                    {'value': 'line', 'label': 'Line'},
                                    {'value': 'bar', 'label': 'Bar'},
                                ],
                                value='line',
                                fullWidth=True,
                            ),
                            dmc.Select(
                                id='curve-type',
                                label='Curve Type (line only)',
                                data=CURVE_OPTIONS,
                                value='linear',
                            ),
                            dmc.Text('Stroke Width (line only)', size='sm', fw=500),
                            dmc.Slider(
                                id='stroke-width',
                                min=1,
                                max=5,
                                value=2,
                                step=1,
                                marks=[
                                    {'value': 1, 'label': '1'},
                                    {'value': 2, 'label': '2'},
                                    {'value': 3, 'label': '3'},
                                    {'value': 4, 'label': '4'},
                                    {'value': 5, 'label': '5'},
                                ],
                                mb='md',
                            ),
                            dmc.Switch(
                                id='show-area',
                                label='Show Area Fill',
                                checked=False,
                            ),
                            dmc.Select(
                                id='baseline',
                                label='Baseline (area only)',
                                data=BASELINE_OPTIONS,
                                value='min',
                            ),
                        ]),

                        # Dimensions Card
                        create_control_card('Dimensions', [
                            dmc.Text('Width (px)', size='sm', fw=500),
                            dmc.Slider(
                                id='chart-width',
                                min=100,
                                max=500,
                                value=300,
                                marks=[
                                    {'value': 100, 'label': '100'},
                                    {'value': 300, 'label': '300'},
                                    {'value': 500, 'label': '500'},
                                ],
                                mb='lg',
                            ),
                            dmc.Text('Height (px)', size='sm', fw=500),
                            dmc.Slider(
                                id='chart-height',
                                min=20,
                                max=100,
                                value=50,
                                marks=[
                                    {'value': 20, 'label': '20'},
                                    {'value': 50, 'label': '50'},
                                    {'value': 100, 'label': '100'},
                                ],
                                mb='lg',
                            ),
                        ]),

                        # Interactive Features Card
                        create_control_card('Interactive Features', [
                            dmc.Switch(
                                id='show-tooltip',
                                label='Show Tooltip',
                                checked=True,
                            ),
                            dmc.Switch(
                                id='show-highlight',
                                label='Show Highlight',
                                checked=True,
                            ),
                            dmc.Select(
                                id='axis-highlight-x',
                                label='X-Axis Highlight',
                                data=AXIS_HIGHLIGHT_OPTIONS,
                                value='line',
                            ),
                            dmc.Text('Highlight Dot Size', size='sm', fw=500),
                            dmc.Slider(
                                id='highlight-dot-size',
                                min=2,
                                max=10,
                                value=4,
                                marks=[
                                    {'value': 2, 'label': '2'},
                                    {'value': 6, 'label': '6'},
                                    {'value': 10, 'label': '10'},
                                ],
                            ),
                        ]),

                        # Margins Card
                        create_control_card('Margins', [
                            dmc.SimpleGrid(
                                cols=2,
                                spacing='sm',
                                children=[
                                    dmc.NumberInput(
                                        id='margin-top',
                                        label='Top',
                                        value=5,
                                        min=0,
                                        max=50,
                                    ),
                                    dmc.NumberInput(
                                        id='margin-right',
                                        label='Right',
                                        value=5,
                                        min=0,
                                        max=50,
                                    ),
                                    dmc.NumberInput(
                                        id='margin-bottom',
                                        label='Bottom',
                                        value=5,
                                        min=0,
                                        max=50,
                                    ),
                                    dmc.NumberInput(
                                        id='margin-left',
                                        label='Left',
                                        value=5,
                                        min=0,
                                        max=50,
                                    ),
                                ]
                            ),
                        ]),

                        # Advanced Card
                        create_control_card('Advanced', [
                            dmc.Switch(
                                id='disable-clipping',
                                label='Disable Clipping',
                                checked=False,
                            ),
                            dmc.Text('Clip Area Offset', size='sm', fw=500, mb='xs', mt='sm'),
                            dmc.SimpleGrid(
                                cols=2,
                                spacing='sm',
                                children=[
                                    dmc.NumberInput(
                                        id='clip-top',
                                        label='Top',
                                        value=0,
                                        min=0,
                                        max=20,
                                    ),
                                    dmc.NumberInput(
                                        id='clip-right',
                                        label='Right',
                                        value=0,
                                        min=0,
                                        max=20,
                                    ),
                                    dmc.NumberInput(
                                        id='clip-bottom',
                                        label='Bottom',
                                        value=0,
                                        min=0,
                                        max=20,
                                    ),
                                    dmc.NumberInput(
                                        id='clip-left',
                                        label='Left',
                                        value=0,
                                        min=0,
                                        max=20,
                                    ),
                                ]
                            ),
                        ]),
                    ]
                ),

                # Generated Code Section
                dmc.Paper(
                    shadow='sm',
                    radius='md',
                    p='xl',
                    mt='xl',
                    children=[
                        dmc.Group(
                            justify='space-between',
                            mb='md',
                            children=[
                                dmc.Text('Generated Code', fw=600, size='xl'),
                                dmc.Group(
                                    gap='sm',
                                    children=[
                                        dmc.Button(
                                            'Reset to Defaults',
                                            id='reset-button',
                                            variant='outline',
                                            size='sm',
                                        ),
                                        dcc.Clipboard(
                                            target_id='generated-code',
                                            style={
                                                'display': 'inline-block',
                                                'fontSize': '14px',
                                                'cursor': 'pointer',
                                                'padding': '5px 10px',
                                                'backgroundColor': '#1976d2',
                                                'color': 'white',
                                                'border': 'none',
                                                'borderRadius': '4px',
                                            }
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dmc.Code(
                            id='generated-code',
                            block=True,
                            style={
                                'backgroundColor': '#1e1e1e',
                                'color': '#d4d4d4',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'fontSize': '13px',
                                'lineHeight': '1.5',
                                'overflowX': 'auto',
                            },
                            children='# Adjust controls above to generate code'
                        ),
                    ]
                ),
            ]
        ),
    ]
)


@callback(
    Output('sparkline-preview', 'children'),
    Output('preview-container', 'style'),
    Output('generated-code', 'children'),
    Input('color-line', 'value'),
    Input('color-background', 'value'),
    Input('plot-type', 'value'),
    Input('curve-type', 'value'),
    Input('stroke-width', 'value'),
    Input('show-area', 'checked'),
    Input('baseline', 'value'),
    Input('chart-width', 'value'),
    Input('chart-height', 'value'),
    Input('show-tooltip', 'checked'),
    Input('show-highlight', 'checked'),
    Input('axis-highlight-x', 'value'),
    Input('highlight-dot-size', 'value'),
    Input('margin-top', 'value'),
    Input('margin-right', 'value'),
    Input('margin-bottom', 'value'),
    Input('margin-left', 'value'),
    Input('disable-clipping', 'checked'),
    Input('clip-top', 'value'),
    Input('clip-right', 'value'),
    Input('clip-bottom', 'value'),
    Input('clip-left', 'value'),
)
def update_preview(
    color, bg_color, plot_type, curve, stroke_width, show_area, baseline,
    width, height, show_tooltip, show_highlight, axis_highlight_x, dot_size,
    margin_top, margin_right, margin_bottom, margin_left,
    disable_clipping, clip_top, clip_right, clip_bottom, clip_left
):
    # Build sparkline props
    sparkline_props = {
        'id': 'styled-sparkline',
        'data': PREVIEW_DATA,
        'color': color or '#1976d2',
        'width': width or 300,
        'height': height or 50,
        'plotType': plot_type or 'line',
        'showTooltip': show_tooltip,
        'showHighlight': show_highlight,
    }

    # Line-specific props
    if plot_type == 'line':
        sparkline_props['curve'] = curve or 'linear'
        sparkline_props['area'] = show_area

        # Stroke width for line chart
        if stroke_width and stroke_width != 2:
            sparkline_props['strokeWidth'] = stroke_width

        if show_area and baseline:
            if baseline == '0':
                sparkline_props['baseline'] = 0
            elif baseline != 'min':
                sparkline_props['baseline'] = baseline

    # Disable clipping
    if disable_clipping:
        sparkline_props['disableClipping'] = True

    # Margins
    margins = {
        'top': margin_top or 5,
        'right': margin_right or 5,
        'bottom': margin_bottom or 5,
        'left': margin_left or 5,
    }
    sparkline_props['margin'] = margins

    # Axis highlight
    if show_highlight and axis_highlight_x != 'none':
        sparkline_props['axisHighlight'] = {'x': axis_highlight_x}
        sparkline_props['xAxis'] = {'id': 'x-axis'}

    # Slot props for highlight dot size
    if show_highlight and dot_size and dot_size != 4:
        sparkline_props['slotProps'] = {'lineHighlight': {'r': dot_size}}

    # Clip area offset
    clip_offset = {
        'top': clip_top or 0,
        'right': clip_right or 0,
        'bottom': clip_bottom or 0,
        'left': clip_left or 0,
    }
    if any(v > 0 for v in clip_offset.values()):
        sparkline_props['clipAreaOffset'] = clip_offset

    # Create sparkline
    sparkline = SparklineChart(**sparkline_props)

    # Update container style
    container_style = {
        'padding': '30px',
        'borderRadius': '8px',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'minHeight': '120px',
        'backgroundColor': bg_color or '#ffffff',
        'transition': 'background-color 0.3s ease',
    }

    # Generate code
    code = generate_code(sparkline_props, bg_color)

    return sparkline, container_style, code


def generate_code(props, bg_color):
    """Generate Python code from current props."""
    lines = ['from dash_mui_charts import SparklineChart', '', 'SparklineChart(']

    # Data (abbreviated)
    lines.append(f'    data=[23, 25, 22, ...],  # {len(PREVIEW_DATA)} values')

    # Color
    if props.get('color') != '#1976d2':
        lines.append(f"    color='{props['color']}',")

    # Dimensions
    if props.get('width') != 300:
        lines.append(f"    width={props['width']},")
    if props.get('height') != 50:
        lines.append(f"    height={props['height']},")

    # Plot type
    if props.get('plotType') != 'line':
        lines.append(f"    plotType='{props['plotType']}',")

    # Line-specific
    if props.get('plotType') == 'line':
        if props.get('curve') != 'linear':
            lines.append(f"    curve='{props['curve']}',")
        if props.get('strokeWidth') and props.get('strokeWidth') != 2:
            lines.append(f"    strokeWidth={props['strokeWidth']},")
        if props.get('area'):
            lines.append('    area=True,')
        if props.get('baseline') and props.get('baseline') != 'min':
            if isinstance(props['baseline'], int):
                lines.append(f"    baseline={props['baseline']},")
            else:
                lines.append(f"    baseline='{props['baseline']}',")

    # Disable clipping
    if props.get('disableClipping'):
        lines.append('    disableClipping=True,')

    # Interactive
    if props.get('showTooltip'):
        lines.append('    showTooltip=True,')
    if props.get('showHighlight'):
        lines.append('    showHighlight=True,')

    # Axis highlight
    if props.get('axisHighlight'):
        lines.append(f"    axisHighlight={props['axisHighlight']},")
    if props.get('xAxis'):
        lines.append(f"    xAxis={props['xAxis']},")

    # Slot props
    if props.get('slotProps'):
        lines.append(f"    slotProps={props['slotProps']},")

    # Margins (only if non-default)
    margin = props.get('margin', {})
    if margin != {'top': 5, 'right': 5, 'bottom': 5, 'left': 5}:
        lines.append(f"    margin={margin},")

    # Clip area offset
    if props.get('clipAreaOffset'):
        lines.append(f"    clipAreaOffset={props['clipAreaOffset']},")

    lines.append(')')

    # Add container style comment if background is not white
    if bg_color and bg_color != '#ffffff':
        lines.append('')
        lines.append(f"# Container background: '{bg_color}'")

    return '\n'.join(lines)


@callback(
    Output('hover-info', 'children'),
    Input('styled-sparkline', 'hoverIndex'),
    Input('styled-sparkline', 'hoverValue'),
    prevent_initial_call=True
)
def update_hover_info(hover_index, hover_value):
    if hover_index is not None and hover_value is not None:
        return f'Hover Index: {hover_index} | Value: {hover_value}'
    return 'Hover over the chart to see interaction data'


# Reset button callback - resets all controls to defaults
@callback(
    Output('color-line', 'value'),
    Output('color-background', 'value'),
    Output('plot-type', 'value'),
    Output('curve-type', 'value'),
    Output('stroke-width', 'value'),
    Output('show-area', 'checked'),
    Output('baseline', 'value'),
    Output('chart-width', 'value'),
    Output('chart-height', 'value'),
    Output('show-tooltip', 'checked'),
    Output('show-highlight', 'checked'),
    Output('axis-highlight-x', 'value'),
    Output('highlight-dot-size', 'value'),
    Output('margin-top', 'value'),
    Output('margin-right', 'value'),
    Output('margin-bottom', 'value'),
    Output('margin-left', 'value'),
    Output('disable-clipping', 'checked'),
    Output('clip-top', 'value'),
    Output('clip-right', 'value'),
    Output('clip-bottom', 'value'),
    Output('clip-left', 'value'),
    Input('reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_controls(n_clicks):
    return (
        '#1976d2',  # color-line
        '#ffffff',  # color-background
        'line',     # plot-type
        'linear',   # curve-type
        2,          # stroke-width
        False,      # show-area
        'min',      # baseline
        300,        # chart-width
        50,         # chart-height
        True,       # show-tooltip
        True,       # show-highlight
        'line',     # axis-highlight-x
        4,          # highlight-dot-size
        5,          # margin-top
        5,          # margin-right
        5,          # margin-bottom
        5,          # margin-left
        False,      # disable-clipping
        0,          # clip-top
        0,          # clip-right
        0,          # clip-bottom
        0,          # clip-left
    )
