"""
PieChart Props Playground

Interactive control panel for exploring and customizing PieChart component properties.
Features nested/multi-series pie charts with inner and outer rings.
Based on MUI X Charts Titanic survival statistics example.
"""
import json
import dash
from dash import html, callback, Input, Output, dcc, ctx

import dash_mantine_components as dmc
from dash_mui_charts import PieChart

dash.register_page(
    __name__,
    path='/pie-props',
    name='Pie Chart Props'
)

# =============================================================================
# TITANIC DATA
# =============================================================================
# https://en.wikipedia.org/wiki/Passengers_of_the_Titanic
TITANIC_RAW = [
    {'Class': '1st', 'Survived': 'No', 'Count': 123},
    {'Class': '1st', 'Survived': 'Yes', 'Count': 202},
    {'Class': '2nd', 'Survived': 'No', 'Count': 167},
    {'Class': '2nd', 'Survived': 'Yes', 'Count': 118},
    {'Class': '3rd', 'Survived': 'No', 'Count': 528},
    {'Class': '3rd', 'Survived': 'Yes', 'Count': 178},
    {'Class': 'Crew', 'Survived': 'No', 'Count': 696},
    {'Class': 'Crew', 'Survived': 'Yes', 'Count': 212},
]

CLASSES = ['1st', '2nd', '3rd', 'Crew']
TOTAL_COUNT = sum(item['Count'] for item in TITANIC_RAW)

# Colors for each class
CLASS_COLORS = {
    '1st': '#fa938e',
    '2nd': '#98bf45',
    '3rd': '#51cbcf',
    'Crew': '#d397ff',
}

# Opacity map for class breakdown
OPACITY_MAP = {
    '1st': 0.9,
    '2nd': 0.7,
    '3rd': 0.5,
    'Crew': 0.3,
}


def hex_to_rgba(hex_color, alpha):
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'


# =============================================================================
# BUILD DATA STRUCTURES
# =============================================================================

# Inner ring - Class totals
CLASS_DATA = []
for pclass in CLASSES:
    class_total = sum(
        item['Count'] for item in TITANIC_RAW if item['Class'] == pclass
    )
    CLASS_DATA.append({
        'id': pclass,
        'label': f'{pclass} Class',
        'value': class_total,
        'color': CLASS_COLORS[pclass],
    })

# Outer ring - Survival within each class (grouped by class)
CLASS_SURVIVAL_DATA = []
for pclass in CLASSES:
    base_color = CLASS_COLORS[pclass]
    for item in sorted(
        [x for x in TITANIC_RAW if x['Class'] == pclass],
        key=lambda x: x['Survived'],
        reverse=True  # Yes first, then No
    ):
        # Full color for survived, 50% opacity for not survived
        color = base_color if item['Survived'] == 'Yes' else f'{base_color}80'
        CLASS_SURVIVAL_DATA.append({
            'id': f"{pclass}-{item['Survived']}",
            'label': 'Survived' if item['Survived'] == 'Yes' else 'Did not survive',
            'value': item['Count'],
            'color': color,
        })

# Inner ring - Survival status totals
survived_total = sum(x['Count'] for x in TITANIC_RAW if x['Survived'] == 'Yes')
not_survived_total = sum(x['Count'] for x in TITANIC_RAW if x['Survived'] == 'No')

SURVIVAL_DATA = [
    {'id': 'Yes', 'label': 'Survived', 'value': survived_total, 'color': '#51cbcf'},
    {'id': 'No', 'label': 'Did not survive', 'value': not_survived_total, 'color': '#fa938e'},
]

# Outer ring - Class breakdown within survival status
SURVIVAL_CLASS_DATA = []
# First add all survivors by class
for pclass in CLASSES:
    count = next(
        (x['Count'] for x in TITANIC_RAW if x['Class'] == pclass and x['Survived'] == 'Yes'),
        0
    )
    SURVIVAL_CLASS_DATA.append({
        'id': f'{pclass}-Yes',
        'label': f'{pclass} Class',
        'value': count,
        'color': hex_to_rgba('#51cbcf', OPACITY_MAP[pclass]),
    })
# Then add all non-survivors by class
for pclass in CLASSES:
    count = next(
        (x['Count'] for x in TITANIC_RAW if x['Class'] == pclass and x['Survived'] == 'No'),
        0
    )
    SURVIVAL_CLASS_DATA.append({
        'id': f'{pclass}-No',
        'label': f'{pclass} Class',
        'value': count,
        'color': hex_to_rgba('#fa938e', OPACITY_MAP[pclass]),
    })

# Simple demo data for basic examples
SIMPLE_DATA = [
    {'id': 'a', 'label': 'Marketing', 'value': 35, 'color': '#1976d2'},
    {'id': 'b', 'label': 'Engineering', 'value': 25, 'color': '#dc004e'},
    {'id': 'c', 'label': 'Sales', 'value': 20, 'color': '#ff9800'},
    {'id': 'd', 'label': 'Support', 'value': 15, 'color': '#4caf50'},
    {'id': 'e', 'label': 'Other', 'value': 5, 'color': '#9c27b0'},
]

SIMPLE_BREAKDOWN_DATA = [
    # Marketing breakdown
    {'id': 'a1', 'label': 'Digital', 'value': 20, 'color': '#1976d2'},
    {'id': 'a2', 'label': 'Traditional', 'value': 15, 'color': '#1976d280'},
    # Engineering breakdown
    {'id': 'b1', 'label': 'Frontend', 'value': 15, 'color': '#dc004e'},
    {'id': 'b2', 'label': 'Backend', 'value': 10, 'color': '#dc004e80'},
    # Sales breakdown
    {'id': 'c1', 'label': 'Direct', 'value': 12, 'color': '#ff9800'},
    {'id': 'c2', 'label': 'Channel', 'value': 8, 'color': '#ff980080'},
    # Support breakdown
    {'id': 'd1', 'label': 'Technical', 'value': 10, 'color': '#4caf50'},
    {'id': 'd2', 'label': 'Customer', 'value': 5, 'color': '#4caf5080'},
    # Other
    {'id': 'e1', 'label': 'Other', 'value': 5, 'color': '#9c27b0'},
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


# =============================================================================
# LAYOUT
# =============================================================================
layout = dmc.MantineProvider(
    html.Div([
        # Header
        html.Div([
            html.H1('PieChart Props Playground'),
            html.P(
                'Interactive demo of nested/multi-series pie charts. '
                'Visualize hierarchical data with inner and outer rings. '
                'Based on MUI X Charts Titanic survival statistics example.',
                style={'color': '#666', 'marginBottom': '30px'}
            ),
        ]),

        # Live Preview Section
        dmc.Paper(
            shadow='sm',
            radius='md',
            p='lg',
            mb='lg',
            children=[
                dmc.Group(
                    justify='space-between',
                    mb='md',
                    children=[
                        dmc.Text('Live Preview', fw=600, size='lg'),
                        dmc.SegmentedControl(
                            id='pie-view-toggle',
                            data=[
                                {'value': 'class', 'label': 'View by Class'},
                                {'value': 'survival', 'label': 'View by Survival'},
                                {'value': 'simple', 'label': 'Simple Demo'},
                            ],
                            value='class',
                        ),
                    ],
                ),
                html.Div(
                    id='pie-preview-container',
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'minHeight': '450px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '8px',
                        'padding': '20px',
                        'transition': 'background-color 0.3s ease',
                    },
                    children=[
                        html.Div(id='pie-preview'),
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
                                    id='pie-hover-info',
                                    children='Hover over a slice',
                                    style={'fontFamily': 'monospace', 'fontSize': '12px'},
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
                                    id='pie-click-info',
                                    children='Click on a slice',
                                    style={'fontFamily': 'monospace', 'fontSize': '12px'},
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
                # Chart Dimensions
                create_control_card('Chart Dimensions', [
                    dmc.Text('Width (px)', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-width',
                        value=450,
                        min=300,
                        max=600,
                        step=10,
                        marks=[
                            {'value': 300, 'label': '300'},
                            {'value': 450, 'label': '450'},
                            {'value': 600, 'label': '600'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Height (px)', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-height',
                        value=400,
                        min=300,
                        max=500,
                        step=10,
                        marks=[
                            {'value': 300, 'label': '300'},
                            {'value': 400, 'label': '400'},
                            {'value': 500, 'label': '500'},
                        ],
                        mb='md',
                    ),
                ]),

                # Inner Ring Settings
                create_control_card('Inner Ring', [
                    dmc.Text('Inner Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-inner-inner-radius',
                        value=50,
                        min=0,
                        max=80,
                        step=5,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 40, 'label': '40'},
                            {'value': 80, 'label': '80'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Outer Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-inner-outer-radius',
                        value=100,
                        min=60,
                        max=140,
                        step=5,
                        marks=[
                            {'value': 60, 'label': '60'},
                            {'value': 100, 'label': '100'},
                            {'value': 140, 'label': '140'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Corner Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-inner-corner-radius',
                        value=3,
                        min=0,
                        max=15,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 5, 'label': '5'},
                            {'value': 10, 'label': '10'},
                            {'value': 15, 'label': '15'},
                        ],
                        mb='md',
                    ),
                    dmc.Text('Padding Angle', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-inner-padding-angle',
                        value=0,
                        min=0,
                        max=5,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0°'},
                            {'value': 2, 'label': '2°'},
                            {'value': 5, 'label': '5°'},
                        ],
                        mb='md',
                    ),
                ]),

                # Outer Ring Settings
                create_control_card('Outer Ring', [
                    dmc.Text('Inner Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-outer-inner-radius',
                        value=110,
                        min=80,
                        max=150,
                        step=5,
                        marks=[
                            {'value': 80, 'label': '80'},
                            {'value': 115, 'label': '115'},
                            {'value': 150, 'label': '150'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Outer Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-outer-outer-radius',
                        value=140,
                        min=100,
                        max=180,
                        step=5,
                        marks=[
                            {'value': 100, 'label': '100'},
                            {'value': 140, 'label': '140'},
                            {'value': 180, 'label': '180'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Corner Radius', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-outer-corner-radius',
                        value=3,
                        min=0,
                        max=15,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 5, 'label': '5'},
                            {'value': 10, 'label': '10'},
                            {'value': 15, 'label': '15'},
                        ],
                        mb='md',
                    ),
                    dmc.Text('Padding Angle', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-outer-padding-angle',
                        value=0,
                        min=0,
                        max=5,
                        step=1,
                        marks=[
                            {'value': 0, 'label': '0°'},
                            {'value': 2, 'label': '2°'},
                            {'value': 5, 'label': '5°'},
                        ],
                        mb='md',
                    ),
                ]),

                # Ring Gap Control
                create_control_card('Ring Gap & Labels', [
                    dmc.Text('Gap Between Rings', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-ring-gap',
                        value=10,
                        min=0,
                        max=30,
                        step=2,
                        marks=[
                            {'value': 0, 'label': '0'},
                            {'value': 10, 'label': '10'},
                            {'value': 20, 'label': '20'},
                            {'value': 30, 'label': '30'},
                        ],
                        mb='lg',
                    ),
                    dmc.Text('Arc Label (Inner Ring)', size='sm', fw=500, mb='xs'),
                    dmc.Select(
                        id='pie-ctrl-arc-label',
                        data=[
                            {'value': 'none', 'label': 'None'},
                            {'value': 'value', 'label': 'Value'},
                            {'value': 'label', 'label': 'Label'},
                            {'value': 'formattedValue', 'label': 'Formatted'},
                        ],
                        value='none',
                        mb='md',
                    ),
                    dmc.Text('Min Angle for Label', size='sm', fw=500, mb='xs'),
                    dmc.Slider(
                        id='pie-ctrl-arc-label-min-angle',
                        value=20,
                        min=0,
                        max=45,
                        step=5,
                        marks=[
                            {'value': 0, 'label': '0°'},
                            {'value': 20, 'label': '20°'},
                            {'value': 45, 'label': '45°'},
                        ],
                        mb='md',
                    ),
                ]),

                # Interactions & Style
                create_control_card('Interactions', [
                    dmc.Switch(
                        id='pie-ctrl-highlight',
                        label='Enable Highlight on Hover',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Switch(
                        id='pie-ctrl-fade-others',
                        label='Fade Other Slices',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Switch(
                        id='pie-ctrl-show-tooltip',
                        label='Show Tooltip',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Switch(
                        id='pie-ctrl-hide-legend',
                        label='Hide Legend',
                        checked=True,
                        mb='sm',
                    ),
                    dmc.Switch(
                        id='pie-ctrl-skip-animation',
                        label='Skip Animation',
                        checked=False,
                        mb='sm',
                    ),
                ]),

                # Margins
                create_control_card('Margins', [
                    dmc.SimpleGrid(
                        cols=2,
                        spacing='sm',
                        children=[
                            dmc.NumberInput(
                                id='pie-ctrl-margin-top',
                                label='Top',
                                value=10,
                                min=0,
                                max=50,
                            ),
                            dmc.NumberInput(
                                id='pie-ctrl-margin-right',
                                label='Right',
                                value=10,
                                min=0,
                                max=50,
                            ),
                            dmc.NumberInput(
                                id='pie-ctrl-margin-bottom',
                                label='Bottom',
                                value=10,
                                min=0,
                                max=50,
                            ),
                            dmc.NumberInput(
                                id='pie-ctrl-margin-left',
                                label='Left',
                                value=10,
                                min=0,
                                max=50,
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
                                    id='pie-reset-btn',
                                    variant='outline',
                                    size='sm',
                                ),
                                dcc.Clipboard(
                                    target_id='pie-generated-code',
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
                    id='pie-generated-code',
                    style={
                        'backgroundColor': '#1e1e1e',
                        'color': '#d4d4d4',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'fontSize': '12px',
                        'lineHeight': '1.5',
                        'overflowX': 'auto',
                        'margin': 0,
                        'maxHeight': '400px',
                    },
                ),
            ],
        ),

    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}),
)


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output('pie-preview', 'children'),
    Output('pie-generated-code', 'children'),
    Input('pie-view-toggle', 'value'),
    Input('pie-ctrl-width', 'value'),
    Input('pie-ctrl-height', 'value'),
    Input('pie-ctrl-inner-inner-radius', 'value'),
    Input('pie-ctrl-inner-outer-radius', 'value'),
    Input('pie-ctrl-inner-corner-radius', 'value'),
    Input('pie-ctrl-inner-padding-angle', 'value'),
    Input('pie-ctrl-outer-inner-radius', 'value'),
    Input('pie-ctrl-outer-outer-radius', 'value'),
    Input('pie-ctrl-outer-corner-radius', 'value'),
    Input('pie-ctrl-outer-padding-angle', 'value'),
    Input('pie-ctrl-ring-gap', 'value'),
    Input('pie-ctrl-arc-label', 'value'),
    Input('pie-ctrl-arc-label-min-angle', 'value'),
    Input('pie-ctrl-highlight', 'checked'),
    Input('pie-ctrl-fade-others', 'checked'),
    Input('pie-ctrl-show-tooltip', 'checked'),
    Input('pie-ctrl-hide-legend', 'checked'),
    Input('pie-ctrl-skip-animation', 'checked'),
    Input('pie-ctrl-margin-top', 'value'),
    Input('pie-ctrl-margin-right', 'value'),
    Input('pie-ctrl-margin-bottom', 'value'),
    Input('pie-ctrl-margin-left', 'value'),
)
def update_pie_chart(
    view, width, height,
    inner_inner_radius, inner_outer_radius, inner_corner_radius, inner_padding_angle,
    outer_inner_radius, outer_outer_radius, outer_corner_radius, outer_padding_angle,
    ring_gap, arc_label, arc_label_min_angle,
    highlight, fade_others, show_tooltip, hide_legend, skip_animation,
    margin_top, margin_right, margin_bottom, margin_left,
):
    """Update nested pie chart preview and generated code."""

    # Get data based on view
    if view == 'class':
        inner_data = CLASS_DATA
        outer_data = CLASS_SURVIVAL_DATA
        data_desc = 'Titanic by Class'
    elif view == 'survival':
        inner_data = SURVIVAL_DATA
        outer_data = SURVIVAL_CLASS_DATA
        data_desc = 'Titanic by Survival'
    else:
        inner_data = SIMPLE_DATA
        outer_data = SIMPLE_BREAKDOWN_DATA
        data_desc = 'Simple Budget Demo'

    # Calculate outer ring inner radius based on inner ring outer radius + gap
    effective_outer_inner = inner_outer_radius + ring_gap

    # Build highlight scope
    highlight_scope = None
    if highlight:
        highlight_scope = {
            'highlight': 'item',
            'fade': 'global' if fade_others else 'none',
        }

    # Build margin
    margin = {
        'top': margin_top or 10,
        'right': margin_right or 10,
        'bottom': margin_bottom or 10,
        'left': margin_left or 10,
    }

    # Build series configuration
    inner_series = {
        'data': inner_data,
        'innerRadius': inner_inner_radius,
        'outerRadius': inner_outer_radius,
        'cornerRadius': inner_corner_radius,
    }
    if inner_padding_angle > 0:
        inner_series['paddingAngle'] = inner_padding_angle
    if highlight_scope:
        inner_series['highlightScope'] = highlight_scope
    if arc_label and arc_label != 'none':
        inner_series['arcLabel'] = arc_label
        if arc_label_min_angle > 0:
            inner_series['arcLabelMinAngle'] = arc_label_min_angle

    outer_series = {
        'data': outer_data,
        'innerRadius': effective_outer_inner,
        'outerRadius': outer_outer_radius,
        'cornerRadius': outer_corner_radius,
    }
    if outer_padding_angle > 0:
        outer_series['paddingAngle'] = outer_padding_angle
    if highlight_scope:
        outer_series['highlightScope'] = highlight_scope

    series = [inner_series, outer_series]

    # Build tooltip config
    tooltip = {'trigger': 'item' if show_tooltip else 'none'}

    # Create pie chart
    pie_chart = PieChart(
        id='pie-preview-chart',
        series=series,
        width=width,
        height=height,
        hideLegend=hide_legend,
        skipAnimation=skip_animation,
        tooltip=tooltip,
        margin=margin,
    )

    # Generate code
    code = generate_code(
        series, width, height, hide_legend, skip_animation, tooltip, margin, data_desc
    )

    return pie_chart, code


def generate_code(series, width, height, hide_legend, skip_animation, tooltip, margin, data_desc):
    """Generate Python code from current configuration."""
    lines = [
        'from dash_mui_charts import PieChart',
        '',
        f'# {data_desc}',
        '# Define your inner and outer ring data...',
        '',
        'PieChart(',
        '    series=[',
    ]

    # Inner series
    inner = series[0]
    lines.append('        {  # Inner ring')
    lines.append('            "data": inner_ring_data,')
    lines.append(f'            "innerRadius": {inner.get("innerRadius", 0)},')
    lines.append(f'            "outerRadius": {inner.get("outerRadius", 80)},')
    if inner.get('cornerRadius', 0) > 0:
        lines.append(f'            "cornerRadius": {inner["cornerRadius"]},')
    if inner.get('paddingAngle', 0) > 0:
        lines.append(f'            "paddingAngle": {inner["paddingAngle"]},')
    if inner.get('highlightScope'):
        hs = inner['highlightScope']
        lines.append(f'            "highlightScope": {{"highlight": "{hs["highlight"]}", "fade": "{hs["fade"]}"}},')
    if inner.get('arcLabel'):
        lines.append(f'            "arcLabel": "{inner["arcLabel"]}",')
        if inner.get('arcLabelMinAngle', 0) > 0:
            lines.append(f'            "arcLabelMinAngle": {inner["arcLabelMinAngle"]},')
    lines.append('        },')

    # Outer series
    outer = series[1]
    lines.append('        {  # Outer ring')
    lines.append('            "data": outer_ring_data,')
    lines.append(f'            "innerRadius": {outer.get("innerRadius", 90)},')
    lines.append(f'            "outerRadius": {outer.get("outerRadius", 120)},')
    if outer.get('cornerRadius', 0) > 0:
        lines.append(f'            "cornerRadius": {outer["cornerRadius"]},')
    if outer.get('paddingAngle', 0) > 0:
        lines.append(f'            "paddingAngle": {outer["paddingAngle"]},')
    if outer.get('highlightScope'):
        hs = outer['highlightScope']
        lines.append(f'            "highlightScope": {{"highlight": "{hs["highlight"]}", "fade": "{hs["fade"]}"}},')
    lines.append('        },')

    lines.append('    ],')
    lines.append(f'    width={width},')
    lines.append(f'    height={height},')

    if hide_legend:
        lines.append('    hideLegend=True,')
    if skip_animation:
        lines.append('    skipAnimation=True,')

    if tooltip.get('trigger') != 'item':
        lines.append(f'    tooltip={{"trigger": "{tooltip["trigger"]}"}},')

    default_margin = {'top': 10, 'right': 10, 'bottom': 10, 'left': 10}
    if margin != default_margin:
        lines.append(f'    margin={margin},')

    lines.append(')')

    return '\n'.join(lines)


@callback(
    Output('pie-hover-info', 'children'),
    Input('pie-preview-chart', 'highlightedItem'),
    prevent_initial_call=True
)
def update_hover_info(highlighted_item):
    """Display current hover info."""
    if highlighted_item:
        # MUI X Charts returns { seriesId, dataIndex } for highlighted item
        series_id = highlighted_item.get('seriesId', '')
        data_index = highlighted_item.get('dataIndex', 0)
        ring = 'Inner ring' if series_id == 'series-0' else 'Outer ring'
        return f'{ring}, slice index: {data_index}'
    return 'Hover over a slice'


@callback(
    Output('pie-click-info', 'children'),
    Input('pie-preview-chart', 'clickData'),
    prevent_initial_call=True
)
def update_click_info(click_data):
    """Display click data."""
    if click_data:
        series_idx = click_data.get('seriesIndex', 0)
        ring = 'Inner ring' if series_idx == 0 else 'Outer ring'
        label = click_data.get('label', 'Unknown')
        value = click_data.get('value', 0)
        item_id = click_data.get('id', '')
        return f'{ring}: {label} = {value} (id: {item_id})'
    return 'Click on a slice'


# Reset button callback
@callback(
    Output('pie-view-toggle', 'value'),
    Output('pie-ctrl-width', 'value'),
    Output('pie-ctrl-height', 'value'),
    Output('pie-ctrl-inner-inner-radius', 'value'),
    Output('pie-ctrl-inner-outer-radius', 'value'),
    Output('pie-ctrl-inner-corner-radius', 'value'),
    Output('pie-ctrl-inner-padding-angle', 'value'),
    Output('pie-ctrl-outer-inner-radius', 'value'),
    Output('pie-ctrl-outer-outer-radius', 'value'),
    Output('pie-ctrl-outer-corner-radius', 'value'),
    Output('pie-ctrl-outer-padding-angle', 'value'),
    Output('pie-ctrl-ring-gap', 'value'),
    Output('pie-ctrl-arc-label', 'value'),
    Output('pie-ctrl-arc-label-min-angle', 'value'),
    Output('pie-ctrl-highlight', 'checked'),
    Output('pie-ctrl-fade-others', 'checked'),
    Output('pie-ctrl-show-tooltip', 'checked'),
    Output('pie-ctrl-hide-legend', 'checked'),
    Output('pie-ctrl-skip-animation', 'checked'),
    Output('pie-ctrl-margin-top', 'value'),
    Output('pie-ctrl-margin-right', 'value'),
    Output('pie-ctrl-margin-bottom', 'value'),
    Output('pie-ctrl-margin-left', 'value'),
    Input('pie-reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_controls(n_clicks):
    """Reset all controls to defaults."""
    return (
        'class',    # view toggle
        450,        # width
        400,        # height
        50,         # inner inner radius
        100,        # inner outer radius
        3,          # inner corner radius
        0,          # inner padding angle
        110,        # outer inner radius
        140,        # outer outer radius
        3,          # outer corner radius
        0,          # outer padding angle
        10,         # ring gap
        'none',     # arc label
        20,         # arc label min angle
        True,       # highlight
        True,       # fade others
        True,       # show tooltip
        True,       # hide legend
        False,      # skip animation
        10,         # margin top
        10,         # margin right
        10,         # margin bottom
        10,         # margin left
    )