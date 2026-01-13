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


class SparklineChart(Component):
    """A SparklineChart component.
SparklineChart component wrapping MUI X Charts SparkLineChart.
Renders compact, inline charts perfect for dashboards, tables, and KPI cards.
This is a Community feature - no license key required.

Supports both controlled and uncontrolled highlight states for interactive
dashboards where hovering on a sparkline updates other components.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- area (boolean; optional):
    If True, fills the area under the line. Only applies when plotType
    is 'line'.

- axisHighlight (dict; optional):
    Axis highlight configuration. Controls how the axis is highlighted
    on hover. - x: 'line' | 'band' | 'none' - highlight style for
    x-axis - y: 'line' | 'band' | 'none' - highlight style for y-axis.

    `axisHighlight` is a dict with keys:

    - x (a value equal to: 'line', 'band', 'none'; optional)

    - y (a value equal to: 'line', 'band', 'none'; optional)

- baseline (a value equal to: 'min', 'max' | number; optional):
    Baseline for area charts. Determines where the area fill starts. -
    'min': fills from minimum value (default) - 'max': fills from
    maximum value - number: fills from a specific value.

- clipAreaOffset (dict; optional):
    Offset for the clip area to prevent cutting off elements at edges.
    Object with top, right, bottom, left keys (in pixels).

    `clipAreaOffset` is a dict with keys:

    - top (number; optional)

    - right (number; optional)

    - bottom (number; optional)

    - left (number; optional)

- color (string; optional):
    Single color for the sparkline. Can be any valid CSS color string.
    Example: '#1976d2', 'rgb(25, 118, 210)', 'blue'.

- colors (list of strings; optional):
    Array of colors for the sparkline. Use this for multi-color
    configurations.

- curve (a value equal to: 'linear', 'monotoneX', 'monotoneY', 'natural', 'step', 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'; optional):
    Curve interpolation method for line charts. Options: 'linear',
    'monotoneX', 'monotoneY', 'natural', 'step', 'stepBefore',
    'stepAfter', 'catmullRom', 'bumpX', 'bumpY'.

- data (list of numbers; required):
    Array of numeric values to display in the sparkline. This is the
    primary data for the chart.

- disableClipping (boolean; optional):
    If True, disables clipping of the chart content. Useful when
    elements extend beyond the chart boundaries.

- height (number; optional):
    Chart height in pixels. Default is 36 for compact inline display.

- highlightedIndex (number; optional):
    Controlled highlight index. Set this to programmatically highlight
    a specific data point. Requires xAxis.id to be set.

- highlightedItem (dict; optional):
    Currently highlighted item. Read-only output property updated when
    the user hovers over a data point (requires showHighlight=True).
    Contains the data index of the highlighted point.

- hoverIndex (number; optional):
    Index of the currently hovered data point. Read-only output. Use
    this to sync hover state with other components.

- hoverValue (number; optional):
    Value at the currently hovered data point. Read-only output. Use
    this to display the hovered value in other components.

- margin (dict; optional):
    Chart margins in pixels. Object with top, right, bottom, left
    keys. Default is { top: 5, right: 5, bottom: 5, left: 5 }.

    `margin` is a dict with keys:

    - top (number; optional)

    - right (number; optional)

    - bottom (number; optional)

    - left (number; optional)

- n_hovers (number; optional):
    Number of hover events. Increments each time a data point is
    hovered.

- plotType (a value equal to: 'line', 'bar'; optional):
    Type of plot to render. - 'line': Renders a line chart (default) -
    'bar': Renders a bar chart.

- showHighlight (boolean; optional):
    If True, shows a visual highlight on the hovered data point. For
    line charts, shows a dot. For bar charts, shows a band.

- showTooltip (boolean; optional):
    If True, shows a tooltip on hover displaying the value.

- slotProps (dict; optional):
    Props passed to internal slot components for customization. -
    lineHighlight: { r: number } - radius of the highlight dot -
    tooltip: tooltip configuration.

- strokeWidth (number; optional):
    Stroke width for the line in pixels. Only applies when plotType is
    'line'. Default is 2. Higher values create thicker lines.

- width (number; optional):
    Chart width in pixels. If not specified, the chart will expand to
    fill the available space.

- xAxis (dict; optional):
    X-axis configuration object. Unlike LineChart, this is a single
    object, not an array. The axis is hidden by default for compact
    display. - id (string): Axis identifier for controlled
    highlighting - data (array): X-axis labels/values - scaleType
    (string): Scale type.

    `xAxis` is a dict with keys:

    - id (string; optional)

    - data (list; optional)

    - scaleType (a value equal to: 'band', 'point', 'linear', 'log', 'time'; optional)

- yAxis (dict; optional):
    Y-axis configuration object. Unlike LineChart, this is a single
    object, not an array. The axis is hidden by default for compact
    display.

    `yAxis` is a dict with keys:

    - min (number; optional)

    - max (number; optional)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'SparklineChart'
    Margin = TypedDict(
        "Margin",
            {
            "top": NotRequired[NumberType],
            "right": NotRequired[NumberType],
            "bottom": NotRequired[NumberType],
            "left": NotRequired[NumberType]
        }
    )

    XAxis = TypedDict(
        "XAxis",
            {
            "id": NotRequired[str],
            "data": NotRequired[typing.Sequence],
            "scaleType": NotRequired[Literal["band", "point", "linear", "log", "time"]]
        }
    )

    YAxis = TypedDict(
        "YAxis",
            {
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType]
        }
    )

    AxisHighlight = TypedDict(
        "AxisHighlight",
            {
            "x": NotRequired[Literal["line", "band", "none"]],
            "y": NotRequired[Literal["line", "band", "none"]]
        }
    )

    ClipAreaOffset = TypedDict(
        "ClipAreaOffset",
            {
            "top": NotRequired[NumberType],
            "right": NotRequired[NumberType],
            "bottom": NotRequired[NumberType],
            "left": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        data: typing.Optional[typing.Sequence[NumberType]] = None,
        plotType: typing.Optional[Literal["line", "bar"]] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        area: typing.Optional[bool] = None,
        curve: typing.Optional[Literal["linear", "monotoneX", "monotoneY", "natural", "step", "stepBefore", "stepAfter", "catmullRom", "bumpX", "bumpY"]] = None,
        showTooltip: typing.Optional[bool] = None,
        showHighlight: typing.Optional[bool] = None,
        margin: typing.Optional["Margin"] = None,
        xAxis: typing.Optional["XAxis"] = None,
        yAxis: typing.Optional["YAxis"] = None,
        axisHighlight: typing.Optional["AxisHighlight"] = None,
        slotProps: typing.Optional[dict] = None,
        clipAreaOffset: typing.Optional["ClipAreaOffset"] = None,
        baseline: typing.Optional[typing.Union[Literal["min", "max"], NumberType]] = None,
        strokeWidth: typing.Optional[NumberType] = None,
        disableClipping: typing.Optional[bool] = None,
        highlightedIndex: typing.Optional[NumberType] = None,
        highlightedItem: typing.Optional[dict] = None,
        hoverIndex: typing.Optional[NumberType] = None,
        hoverValue: typing.Optional[NumberType] = None,
        n_hovers: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'area', 'axisHighlight', 'baseline', 'clipAreaOffset', 'color', 'colors', 'curve', 'data', 'disableClipping', 'height', 'highlightedIndex', 'highlightedItem', 'hoverIndex', 'hoverValue', 'margin', 'n_hovers', 'plotType', 'showHighlight', 'showTooltip', 'slotProps', 'strokeWidth', 'width', 'xAxis', 'yAxis']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'area', 'axisHighlight', 'baseline', 'clipAreaOffset', 'color', 'colors', 'curve', 'data', 'disableClipping', 'height', 'highlightedIndex', 'highlightedItem', 'hoverIndex', 'hoverValue', 'margin', 'n_hovers', 'plotType', 'showHighlight', 'showTooltip', 'slotProps', 'strokeWidth', 'width', 'xAxis', 'yAxis']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SparklineChart, self).__init__(**args)

setattr(SparklineChart, "__init__", _explicitize_args(SparklineChart.__init__))
