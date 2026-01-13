# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class PieChart(Component):
    """A PieChart component.
PieChart component wrapping MUI X Charts PieChart.
Renders pie and donut charts with customizable arcs, labels, and interactions.
Supports single series (via data prop) or multiple series (via series prop) for nested pies.
This is a free feature - no MUI X Pro license required.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- arcLabel (a value equal to: 'value', 'label', 'formattedValue'; optional):
    Type of label to display on arcs. - 'value': Shows the numeric
    value - 'label': Shows the label text - 'formattedValue': Shows
    formatted value.

- arcLabelMinAngle (number; optional):
    Minimum arc angle in degrees required to display a label. Prevents
    labels from appearing on very small slices.

- clickData (dict; optional):
    Data from the most recent click event. Read-only output property.
    Contains id, dataIndex, value, label, and timestamp.

- colors (list of strings; optional):
    Array of colors to use for the pie slices. If not provided, uses
    the default MUI color palette. Example: ['#1976d2', '#dc004e',
    '#ff9800', '#4caf50'].

- cornerRadius (number; optional):
    Corner radius of the arcs in pixels. Rounds the corners of each
    slice.

- cx (number | string; optional):
    X position of the pie center. Can be pixels or percentage string.
    Default is '50%' (centered).

- cy (number | string; optional):
    Y position of the pie center. Can be pixels or percentage string.
    Default is '50%' (centered).

- data (list of dicts; optional):
    Pie chart data as an array of objects (for single series). Each
    object should have: - id (number/string): Unique identifier for
    the slice - value (number): The numeric value (required) - label
    (string): Display label for the slice - color (string): Optional
    color override for this slice  Example: [   { id: 0, value: 35,
    label: 'Marketing' },   { id: 1, value: 25, label: 'Engineering',
    color: '#1976d2' }, ]  Note: Use either 'data' for single series
    or 'series' for multiple series (nested pies).

    `data` is a list of dicts with keys:

    - id (number | string; optional)

    - value (number; required)

    - label (string; optional)

    - color (string; optional)

- endAngle (number; optional):
    End angle of the last arc in degrees. Default is 360 (full
    circle). Use 90 with startAngle=-90 for a half-pie/gauge chart.

- height (number; optional):
    Chart height in pixels. Default is 300.

- hideLegend (boolean; optional):
    If True, the legend is hidden.

- highlightScope (dict; optional):
    Highlight scope configuration for slice highlighting behavior. -
    highlight: 'item' or 'none' - fade: 'global' or 'none'  Example: {
    highlight: 'item', fade: 'global' }.

    `highlightScope` is a dict with keys:

    - highlight (a value equal to: 'item', 'none'; optional)

    - fade (a value equal to: 'global', 'none'; optional)

- highlightedItem (dict; optional):
    Currently highlighted item. Read-only output property updated when
    the user hovers over a slice.

- innerRadius (number | string; optional):
    Inner radius of the pie in pixels or percentage string. Set to a
    value > 0 to create a donut chart. Examples: 50, '50%', '40%'.

- margin (dict; optional):
    Chart margins in pixels. Object with top, right, bottom, left
    keys.

    `margin` is a dict with keys:

    - top (number; optional)

    - right (number; optional)

    - bottom (number; optional)

    - left (number; optional)

- n_clicks (number; optional):
    Number of times the chart has been clicked. Increments on each
    click event.

- outerRadius (number | string; optional):
    Outer radius of the pie in pixels or percentage string. Examples:
    100, '80%'.

- paddingAngle (number; optional):
    Gap between arcs in degrees. Creates visual separation between
    slices.

- series (list of dicts; optional):
    Array of series configurations for multi-series/nested pie charts.
    Each series can have its own data, geometry, and styling. When
    provided, the 'data' prop and individual geometry props are
    ignored.  Example for nested pie: [   {     data: innerRingData,
    innerRadius: 0,     outerRadius: 80,     cornerRadius: 3,
    highlightScope: { fade: 'global', highlight: 'item' },   },   {
    data: outerRingData,     innerRadius: 90,     outerRadius: 120,
    cornerRadius: 3,     highlightScope: { fade: 'global', highlight:
    'item' },   }, ].

    `series` is a list of dicts with keys:

    - id (string; optional)

    - data (list of dicts; required)

        `data` is a list of dicts with keys:

        - id (number | string; optional)

        - value (number; required)

        - label (string; optional)

        - color (string; optional)

    - innerRadius (number | string; optional)

    - outerRadius (number | string; optional)

    - paddingAngle (number; optional)

    - cornerRadius (number; optional)

    - startAngle (number; optional)

    - endAngle (number; optional)

    - arcLabel (a value equal to: 'value', 'label', 'formattedValue'; optional)

    - arcLabelMinAngle (number; optional)

    - arcLabelRadius (number; optional)

    - highlightScope (dict; optional)

        `highlightScope` is a dict with keys:

        - highlight (a value equal to: 'item', 'none'; optional)

        - fade (a value equal to: 'global', 'none'; optional)

- skipAnimation (boolean; optional):
    If True, disables chart animations. Also respects
    prefers-reduced-motion.

- startAngle (number; optional):
    Start angle of the first arc in degrees. Default is 0 (3 o'clock
    position). Use -90 for 12 o'clock start position.

- tooltip (dict; optional):
    Tooltip configuration. - trigger (string): 'item' to show on slice
    hover, 'none' to disable.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'none'; optional)

- width (number; optional):
    Chart width in pixels. If not specified, the chart expands to fill
    the available space."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'PieChart'
    Data = TypedDict(
        "Data",
            {
            "id": NotRequired[typing.Union[NumberType, str]],
            "value": NumberType,
            "label": NotRequired[str],
            "color": NotRequired[str]
        }
    )

    SeriesData = TypedDict(
        "SeriesData",
            {
            "id": NotRequired[typing.Union[NumberType, str]],
            "value": NumberType,
            "label": NotRequired[str],
            "color": NotRequired[str]
        }
    )

    SeriesHighlightScope = TypedDict(
        "SeriesHighlightScope",
            {
            "highlight": NotRequired[Literal["item", "none"]],
            "fade": NotRequired[Literal["global", "none"]]
        }
    )

    Series = TypedDict(
        "Series",
            {
            "id": NotRequired[str],
            "data": typing.Sequence["SeriesData"],
            "innerRadius": NotRequired[typing.Union[NumberType, str]],
            "outerRadius": NotRequired[typing.Union[NumberType, str]],
            "paddingAngle": NotRequired[NumberType],
            "cornerRadius": NotRequired[NumberType],
            "startAngle": NotRequired[NumberType],
            "endAngle": NotRequired[NumberType],
            "arcLabel": NotRequired[Literal["value", "label", "formattedValue"]],
            "arcLabelMinAngle": NotRequired[NumberType],
            "arcLabelRadius": NotRequired[NumberType],
            "highlightScope": NotRequired["SeriesHighlightScope"]
        }
    )

    Margin = TypedDict(
        "Margin",
            {
            "top": NotRequired[NumberType],
            "right": NotRequired[NumberType],
            "bottom": NotRequired[NumberType],
            "left": NotRequired[NumberType]
        }
    )

    HighlightScope = TypedDict(
        "HighlightScope",
            {
            "highlight": NotRequired[Literal["item", "none"]],
            "fade": NotRequired[Literal["global", "none"]]
        }
    )

    Tooltip = TypedDict(
        "Tooltip",
            {
            "trigger": NotRequired[Literal["item", "none"]]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        data: typing.Optional[typing.Sequence["Data"]] = None,
        series: typing.Optional[typing.Sequence["Series"]] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        innerRadius: typing.Optional[typing.Union[NumberType, str]] = None,
        outerRadius: typing.Optional[typing.Union[NumberType, str]] = None,
        paddingAngle: typing.Optional[NumberType] = None,
        cornerRadius: typing.Optional[NumberType] = None,
        startAngle: typing.Optional[NumberType] = None,
        endAngle: typing.Optional[NumberType] = None,
        cx: typing.Optional[typing.Union[NumberType, str]] = None,
        cy: typing.Optional[typing.Union[NumberType, str]] = None,
        arcLabel: typing.Optional[Literal["value", "label", "formattedValue"]] = None,
        arcLabelMinAngle: typing.Optional[NumberType] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        hideLegend: typing.Optional[bool] = None,
        margin: typing.Optional["Margin"] = None,
        highlightScope: typing.Optional["HighlightScope"] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        skipAnimation: typing.Optional[bool] = None,
        clickData: typing.Optional[dict] = None,
        n_clicks: typing.Optional[NumberType] = None,
        highlightedItem: typing.Optional[dict] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'arcLabel', 'arcLabelMinAngle', 'clickData', 'colors', 'cornerRadius', 'cx', 'cy', 'data', 'endAngle', 'height', 'hideLegend', 'highlightScope', 'highlightedItem', 'innerRadius', 'margin', 'n_clicks', 'outerRadius', 'paddingAngle', 'series', 'skipAnimation', 'startAngle', 'tooltip', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'arcLabel', 'arcLabelMinAngle', 'clickData', 'colors', 'cornerRadius', 'cx', 'cy', 'data', 'endAngle', 'height', 'hideLegend', 'highlightScope', 'highlightedItem', 'innerRadius', 'margin', 'n_clicks', 'outerRadius', 'paddingAngle', 'series', 'skipAnimation', 'startAngle', 'tooltip', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PieChart, self).__init__(**args)

setattr(PieChart, "__init__", _explicitize_args(PieChart.__init__))
