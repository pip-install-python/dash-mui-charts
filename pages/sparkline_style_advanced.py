"""
Advanced Sparkline with Liquid Glass Theme
Apple-inspired glassmorphism design with interactive hover effects.

Features:
- Liquid glass (glassmorphism) card design
- Left-to-right reveal animation on page load
- Hover effect: left side 100% opacity, right side 40% opacity
- X-axis highlight line follows cursor
- Real-time value display
"""
import dash
from dash import html, callback, Input, Output, State

from dash_mui_charts import SparklineChart

dash.register_page(
    __name__,
    path='/sparkline-style-advanced',
    name='Sparkline Advanced'
)

# Stock-like data with realistic movement
STOCK_DATA = [
    142.50, 143.20, 141.80, 144.50, 146.20, 145.80, 147.90, 149.20,
    148.50, 150.10, 151.80, 150.90, 152.40, 154.20, 153.80, 155.50,
    157.20, 156.80, 158.40, 160.10, 159.50, 161.20, 162.80, 164.50
]

# Calculate stats
START_VALUE = STOCK_DATA[0]
END_VALUE = STOCK_DATA[-1]
CHANGE = END_VALUE - START_VALUE
CHANGE_PERCENT = (CHANGE / START_VALUE) * 100

layout = html.Div(
    className='liquid-glass-background',
    children=[
        html.Div(
            className='liquid-glass-card',
            children=[
                # Header
                html.Div([
                    html.Span(className='status-dot'),
                    html.Span('Live', style={
                        'color': 'rgba(255, 255, 255, 0.7)',
                        'fontSize': '12px',
                        'fontWeight': '500',
                    }),
                ], style={'marginBottom': '15px'}),

                html.H1('AAPL Stock Price', className='glass-title'),
                html.P(
                    'Interactive sparkline with liquid glass design',
                    className='glass-subtitle'
                ),

                # Sparkline Container
                html.Div(
                    id='sparkline-container',
                    className='sparkline-container',
                    children=[
                        SparklineChart(
                            id='glass-sparkline',
                            data=STOCK_DATA,
                            width=500,
                            height=100,
                            color='rgba(79, 195, 247, 1)',
                            area=True,
                            curve='monotoneX',
                            showTooltip=True,
                            showHighlight=True,
                            axisHighlight={'x': 'line'},
                            xAxis={'id': 'x-axis'},
                            strokeWidth=2,
                            baseline='min',
                            slotProps={
                                'lineHighlight': {'r': 6},
                                'tooltip': {'disablePortal': True},
                            },
                            clipAreaOffset={'top': 10, 'right': 10, 'bottom': 10, 'left': 10},
                        ),
                    ],
                ),

                # Value Display Panel
                html.Div(
                    className='value-display-panel',
                    children=[
                        # Current/Hover Value
                        html.Div(
                            className='value-display',
                            children=[
                                html.Div('VALUE', className='value-label'),
                                html.Div(
                                    id='hover-value-display',
                                    className='value-number',
                                    children=f'${END_VALUE:.2f}'
                                ),
                            ]
                        ),

                        # Index/Position
                        html.Div(
                            className='value-display',
                            children=[
                                html.Div('POSITION', className='value-label'),
                                html.Div(
                                    id='hover-index-display',
                                    className='value-number',
                                    children=f'{len(STOCK_DATA)}/{len(STOCK_DATA)}'
                                ),
                            ]
                        ),

                        # Change
                        html.Div(
                            className='value-display',
                            children=[
                                html.Div('CHANGE', className='value-label'),
                                html.Div(
                                    id='change-display',
                                    className=f'value-number {"positive" if CHANGE >= 0 else "negative"}',
                                    children=f'{"+$" if CHANGE >= 0 else "-$"}{abs(CHANGE):.2f}'
                                ),
                            ]
                        ),
                    ]
                ),

                # Hover instruction
                html.P(
                    id='hover-instruction',
                    className='hover-instruction',
                    children='Hover over the chart to explore values'
                ),
            ]
        ),
    ]
)


@callback(
    Output('sparkline-container', 'style'),
    Output('sparkline-container', 'className'),
    Output('hover-value-display', 'children'),
    Output('hover-index-display', 'children'),
    Output('change-display', 'children'),
    Output('change-display', 'className'),
    Output('hover-instruction', 'className'),
    Input('glass-sparkline', 'hoverIndex'),
    Input('glass-sparkline', 'hoverValue'),
)
def update_hover_effect(hover_index, hover_value):
    data_length = len(STOCK_DATA)

    # Base style for container
    base_style = {}

    if hover_index is not None and hover_value is not None:
        # Calculate hover position as percentage
        hover_percent = ((hover_index + 1) / data_length) * 100

        # Update style with CSS custom property for mask position
        new_style = {
            **base_style,
            '--hover-percent': f'{hover_percent}%',
        }

        # Add hovering class for mask effect
        class_name = 'sparkline-container hovering'

        # Format value display
        value_text = f'${hover_value:.2f}'
        index_text = f'{hover_index + 1}/{data_length}'

        # Calculate change from start
        change_from_start = hover_value - START_VALUE
        change_text = f'{"+$" if change_from_start >= 0 else "-$"}{abs(change_from_start):.2f}'
        change_class = f'value-number {"positive" if change_from_start >= 0 else "negative"}'

        # Hide instruction when hovering
        instruction_class = 'hover-instruction hidden'
    else:
        # Default state (not hovering)
        new_style = base_style
        class_name = 'sparkline-container'

        # Show end values
        value_text = f'${END_VALUE:.2f}'
        index_text = f'{data_length}/{data_length}'
        change_text = f'{"+$" if CHANGE >= 0 else "-$"}{abs(CHANGE):.2f}'
        change_class = f'value-number {"positive" if CHANGE >= 0 else "negative"}'

        # Show instruction
        instruction_class = 'hover-instruction'

    return (
        new_style,
        class_name,
        value_text,
        index_text,
        change_text,
        change_class,
        instruction_class,
    )
