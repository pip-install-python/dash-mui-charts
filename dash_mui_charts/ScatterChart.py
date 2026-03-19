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


class ScatterChart(Component):
    """A ScatterChart component.
ScatterChart component wrapping MUI X Charts ScatterChart.
Renders scatter/point charts showing relationships between two variables.
Supports multiple series, z-axis color mapping, voronoi interaction,
custom marker sizes, and click/highlight callbacks.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axisHighlight (dict; optional):
    Axis highlight configuration on hover. - x: 'none', 'line', or
    'band' - y: 'none', 'line', or 'band'.

    `axisHighlight` is a dict with keys:

    - x (a value equal to: 'none', 'line', 'band'; optional)

    - y (a value equal to: 'none', 'line', 'band'; optional)

- clickData (dict; optional):
    Data from the most recent click event. Read-only output property.
    Contains seriesId, dataIndex, x, y, and timestamp.

- colors (list of strings; optional):
    Color palette array for multiple series.

- dataset (list of dicts; optional):
    Dataset array for datasetKeys-driven series. Array of objects
    where keys map to series datasetKeys. Example: [{x1: 10, y1: 20,
    x2: 30, y2: 40}, ...].

- disableVoronoi (boolean; optional):
    If True, disables Voronoi cell interaction and falls back to hover
    events.

- grid (dict; optional):
    Grid configuration. Object with horizontal and vertical boolean
    keys.

    `grid` is a dict with keys:

    - horizontal (boolean; optional)

    - vertical (boolean; optional)

- height (number; optional):
    Chart height in pixels. Default is 400.

- hideLegend (boolean; optional):
    If True, the legend is hidden.

- highlightedItem (dict; optional):
    Currently highlighted item. Works as both input (controlled) and
    output. Object with seriesId and dataIndex.

- loading (boolean; optional):
    If True, shows a loading overlay.

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

- renderer (a value equal to: 'svg-single', 'svg-batch'; optional):
    Renderer type for performance optimization. - 'svg-single':
    Default, renders each point as a <circle> element - 'svg-batch':
    Batch renders points in <path> elements for large datasets   Note:
    svg-batch has limitations (no CSS per-point, no custom markers).

- series (list of dicts; optional):
    Array of scatter series to display. Each series contains: - id
    (string): Unique series identifier - label (string): Display label
    for legend/tooltip - color (string): Series color - data (array):
    Array of {x, y, id, z?} point objects - datasetKeys (object): {x,
    y, id?, z?} keys mapping to dataset columns - markerSize (number):
    Radius of scatter markers in pixels - highlightScope (object):
    {highlight, fade} highlighting behavior.

    `series` is a list of dicts with keys:

    - id (string; optional)

    - label (string; optional)

    - color (string; optional)

    - data (list of dicts; optional)

        `data` is a list of dicts with keys:

        - x (number; optional)

        - y (number; optional)

        - id (string | number; optional)

        - z (number; optional)

    - datasetKeys (dict; optional)

        `datasetKeys` is a dict with keys:

        - x (string; optional)

        - y (string; optional)

        - id (string; optional)

        - z (string; optional)

    - markerSize (number; optional)

    - highlightScope (dict; optional)

        `highlightScope` is a dict with keys:

        - highlight (a value equal to: 'item', 'series', 'none'; optional)

        - fade (a value equal to: 'global', 'series', 'none'; optional)

    - xAxisId (string; optional)

    - yAxisId (string; optional)

- skipAnimation (boolean; optional):
    If True, animations are disabled.

- slotProps (dict; optional):
    Props passed to internal slot components for customization.

- tooltip (dict; optional):
    Tooltip configuration. - trigger: 'item' (on point hover), 'axis'
    (all at x position), 'none' (disabled).

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'axis', 'none'; optional)

- voronoiMaxRadius (number | a value equal to: 'item'; optional):
    Maximum distance between pointer and scatter point for
    interaction. - number: Distance in pixels - 'item': Only trigger
    on direct hover over marker - undefined: Infinite radius
    (default).

- width (number; optional):
    Chart width in pixels. If not set, fills available space.

- xAxis (list of dicts; optional):
    X-axis configuration. Array of axis config objects. - id (string):
    Axis identifier - label (string): Axis label - scaleType (string):
    'linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc'
    - min/max (number): Domain bounds - data (array): Axis data values
    - dataKey (string): Key for dataset-driven axis - position
    (string): 'top', 'bottom', 'none' - reverse (bool): Reverse axis
    direction - colorMap (object): Color mapping configuration -
    tickLabelStyle (object): CSS for tick labels - labelStyle
    (object): CSS for axis label - tickMinStep (number): Minimum step
    between ticks - tickMaxStep (number): Maximum step between ticks -
    tickNumber (number): Approximate tick count - tickSize (number):
    Tick mark length in pixels - height (number): Space reserved for
    axis - disableLine (bool): Hide axis line - disableTicks (bool):
    Hide tick marks - domainLimit (string): 'nice' or 'strict'.

    `xAxis` is a list of dicts with keys:

    - id (string | number; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc', 'pow'; optional)

    - min (number; optional)

    - max (number; optional)

    - data (list; optional)

    - dataKey (string; optional)

    - position (a value equal to: 'top', 'bottom', 'none'; optional)

    - reverse (boolean; optional)

    - colorMap (dict; optional)

    - tickLabelStyle (dict; optional)

    - labelStyle (dict; optional)

    - tickMinStep (number; optional)

    - tickMaxStep (number; optional)

    - tickNumber (number; optional)

    - tickSize (number; optional)

    - tickSpacing (number; optional)

    - tickLabelMinGap (number; optional)

    - tickLabelPlacement (a value equal to: 'middle', 'tick'; optional)

    - tickPlacement (a value equal to: 'start', 'end', 'middle', 'extremities'; optional)

    - height (number; optional)

    - disableLine (boolean; optional)

    - disableTicks (boolean; optional)

    - domainLimit (a value equal to: 'nice', 'strict'; optional)

    - categoryGapRatio (number; optional)

    - barGapRatio (number; optional)

    - width (number; optional)

- yAxis (list of dicts; optional):
    Y-axis configuration. Array of axis config objects. Same
    properties as xAxis, plus: - width (number): Space reserved for
    axis - position (string): 'left', 'right', 'none'.

    `yAxis` is a list of dicts with keys:

    - id (string | number; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'linear', 'log', 'time', 'band', 'point', 'sqrt', 'symlog', 'utc', 'pow'; optional)

    - min (number; optional)

    - max (number; optional)

    - data (list; optional)

    - dataKey (string; optional)

    - position (a value equal to: 'left', 'right', 'none'; optional)

    - reverse (boolean; optional)

    - colorMap (dict; optional)

    - tickLabelStyle (dict; optional)

    - labelStyle (dict; optional)

    - tickMinStep (number; optional)

    - tickMaxStep (number; optional)

    - tickNumber (number; optional)

    - tickSize (number; optional)

    - tickSpacing (number; optional)

    - tickLabelMinGap (number; optional)

    - tickLabelPlacement (a value equal to: 'middle', 'tick'; optional)

    - tickPlacement (a value equal to: 'start', 'end', 'middle', 'extremities'; optional)

    - width (number; optional)

    - disableLine (boolean; optional)

    - disableTicks (boolean; optional)

    - domainLimit (a value equal to: 'nice', 'strict'; optional)

- zAxis (list of dicts; optional):
    Z-axis configuration for color mapping scatter points. Color
    priority: z-axis > y-axis > x-axis > series color. - data (array):
    Z-axis values - dataKey (string): Key for dataset-driven z values
    - id (string): Axis identifier - min/max (number): Domain bounds -
    colorMap (object): Color mapping - continuous, piecewise, or
    ordinal   Continuous: {type: 'continuous', min, max, color:
    ['#start', '#end']}   Piecewise: {type: 'piecewise', thresholds:
    [...], colors: [...]}   Ordinal: {type: 'ordinal', values: [...],
    colors: [...]}.

    `zAxis` is a list of dicts with keys:

    - id (string; optional)

    - data (list; optional)

    - dataKey (string; optional)

    - min (number; optional)

    - max (number; optional)

    - colorMap (dict; optional)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'ScatterChart'
    SeriesData = TypedDict(
        "SeriesData",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "id": NotRequired[typing.Union[str, NumberType]],
            "z": NotRequired[NumberType]
        }
    )

    SeriesDatasetKeys = TypedDict(
        "SeriesDatasetKeys",
            {
            "x": NotRequired[str],
            "y": NotRequired[str],
            "id": NotRequired[str],
            "z": NotRequired[str]
        }
    )

    SeriesHighlightScope = TypedDict(
        "SeriesHighlightScope",
            {
            "highlight": NotRequired[Literal["item", "series", "none"]],
            "fade": NotRequired[Literal["global", "series", "none"]]
        }
    )

    Series = TypedDict(
        "Series",
            {
            "id": NotRequired[str],
            "label": NotRequired[str],
            "color": NotRequired[str],
            "data": NotRequired[typing.Sequence["SeriesData"]],
            "datasetKeys": NotRequired["SeriesDatasetKeys"],
            "markerSize": NotRequired[NumberType],
            "highlightScope": NotRequired["SeriesHighlightScope"],
            "xAxisId": NotRequired[str],
            "yAxisId": NotRequired[str]
        }
    )

    XAxis = TypedDict(
        "XAxis",
            {
            "id": NotRequired[typing.Union[str, NumberType]],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["linear", "log", "time", "band", "point", "sqrt", "symlog", "utc", "pow"]],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "data": NotRequired[typing.Sequence],
            "dataKey": NotRequired[str],
            "position": NotRequired[Literal["top", "bottom", "none"]],
            "reverse": NotRequired[bool],
            "colorMap": NotRequired[dict],
            "tickLabelStyle": NotRequired[dict],
            "labelStyle": NotRequired[dict],
            "tickMinStep": NotRequired[NumberType],
            "tickMaxStep": NotRequired[NumberType],
            "tickNumber": NotRequired[NumberType],
            "tickSize": NotRequired[NumberType],
            "tickSpacing": NotRequired[NumberType],
            "tickLabelMinGap": NotRequired[NumberType],
            "tickLabelPlacement": NotRequired[Literal["middle", "tick"]],
            "tickPlacement": NotRequired[Literal["start", "end", "middle", "extremities"]],
            "height": NotRequired[NumberType],
            "disableLine": NotRequired[bool],
            "disableTicks": NotRequired[bool],
            "domainLimit": NotRequired[Literal["nice", "strict"]],
            "categoryGapRatio": NotRequired[NumberType],
            "barGapRatio": NotRequired[NumberType],
            "width": NotRequired[NumberType]
        }
    )

    YAxis = TypedDict(
        "YAxis",
            {
            "id": NotRequired[typing.Union[str, NumberType]],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["linear", "log", "time", "band", "point", "sqrt", "symlog", "utc", "pow"]],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "data": NotRequired[typing.Sequence],
            "dataKey": NotRequired[str],
            "position": NotRequired[Literal["left", "right", "none"]],
            "reverse": NotRequired[bool],
            "colorMap": NotRequired[dict],
            "tickLabelStyle": NotRequired[dict],
            "labelStyle": NotRequired[dict],
            "tickMinStep": NotRequired[NumberType],
            "tickMaxStep": NotRequired[NumberType],
            "tickNumber": NotRequired[NumberType],
            "tickSize": NotRequired[NumberType],
            "tickSpacing": NotRequired[NumberType],
            "tickLabelMinGap": NotRequired[NumberType],
            "tickLabelPlacement": NotRequired[Literal["middle", "tick"]],
            "tickPlacement": NotRequired[Literal["start", "end", "middle", "extremities"]],
            "width": NotRequired[NumberType],
            "disableLine": NotRequired[bool],
            "disableTicks": NotRequired[bool],
            "domainLimit": NotRequired[Literal["nice", "strict"]]
        }
    )

    ZAxis = TypedDict(
        "ZAxis",
            {
            "id": NotRequired[str],
            "data": NotRequired[typing.Sequence],
            "dataKey": NotRequired[str],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "colorMap": NotRequired[dict]
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

    Grid = TypedDict(
        "Grid",
            {
            "horizontal": NotRequired[bool],
            "vertical": NotRequired[bool]
        }
    )

    AxisHighlight = TypedDict(
        "AxisHighlight",
            {
            "x": NotRequired[Literal["none", "line", "band"]],
            "y": NotRequired[Literal["none", "line", "band"]]
        }
    )

    Tooltip = TypedDict(
        "Tooltip",
            {
            "trigger": NotRequired[Literal["item", "axis", "none"]]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        series: typing.Optional[typing.Sequence["Series"]] = None,
        xAxis: typing.Optional[typing.Sequence["XAxis"]] = None,
        yAxis: typing.Optional[typing.Sequence["YAxis"]] = None,
        zAxis: typing.Optional[typing.Sequence["ZAxis"]] = None,
        dataset: typing.Optional[typing.Sequence[dict]] = None,
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        grid: typing.Optional["Grid"] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        voronoiMaxRadius: typing.Optional[typing.Union[NumberType, Literal["item"]]] = None,
        disableVoronoi: typing.Optional[bool] = None,
        axisHighlight: typing.Optional["AxisHighlight"] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        hideLegend: typing.Optional[bool] = None,
        skipAnimation: typing.Optional[bool] = None,
        loading: typing.Optional[bool] = None,
        renderer: typing.Optional[Literal["svg-single", "svg-batch"]] = None,
        slotProps: typing.Optional[dict] = None,
        highlightedItem: typing.Optional[dict] = None,
        clickData: typing.Optional[dict] = None,
        n_clicks: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'axisHighlight', 'clickData', 'colors', 'dataset', 'disableVoronoi', 'grid', 'height', 'hideLegend', 'highlightedItem', 'loading', 'margin', 'n_clicks', 'renderer', 'series', 'skipAnimation', 'slotProps', 'tooltip', 'voronoiMaxRadius', 'width', 'xAxis', 'yAxis', 'zAxis']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisHighlight', 'clickData', 'colors', 'dataset', 'disableVoronoi', 'grid', 'height', 'hideLegend', 'highlightedItem', 'loading', 'margin', 'n_clicks', 'renderer', 'series', 'skipAnimation', 'slotProps', 'tooltip', 'voronoiMaxRadius', 'width', 'xAxis', 'yAxis', 'zAxis']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ScatterChart, self).__init__(**args)

setattr(ScatterChart, "__init__", _explicitize_args(ScatterChart.__init__))
