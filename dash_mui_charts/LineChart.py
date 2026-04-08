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


class LineChart(Component):
    """A LineChart component.
LineChart component wrapping MUI X Charts Pro with composition API.
Renders interactive line charts with support for multiple series,
customizable axes, tooltips, click event callbacks, and Pro features
like zoom, pan, and zoom slider.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axisHighlight (dict; optional):
    Axis highlight configuration. Controls how axes are highlighted on
    hover. - x (string): 'none', 'line', or 'band' - y (string):
    'none' or 'line'.

    `axisHighlight` is a dict with keys:

    - x (a value equal to: 'none', 'line', 'band'; optional)

    - y (a value equal to: 'none', 'line'; optional)

- brushConfig (dict; optional):
    Brush configuration for range selection. Object with: - enabled
    (boolean): Whether brush interaction is enabled (default: False) -
    preventTooltip (boolean): Prevent tooltip during brush (default:
    True) - preventHighlight (boolean): Prevent highlight during brush
    (default: True).

    `brushConfig` is a dict with keys:

    - enabled (boolean; optional)

    - preventTooltip (boolean; optional)

    - preventHighlight (boolean; optional)

- brushData (dict; optional):
    Current brush selection data. Read-only output property. Contains
    pixel coordinates of the brush selection.

    `brushData` is a dict with keys:

    - start (dict; optional)

        `start` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

    - current (dict; optional)

        `current` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

    - timestamp (string; optional)

- brushOverlay (a value equal to: 'none', 'default', 'values'; optional):
    Type of brush overlay to display: - 'none': No overlay (default) -
    'default': Standard MUI selection rectangle - 'values': Custom
    overlay showing start/end values with difference and percentage.

- brushSeriesId (string; optional):
    Series ID for the custom 'values' brush overlay to read data from.
    If not specified, uses the first series.

- clickData (dict; optional):
    Data from the most recent click event. Read-only output property.
    Contains type ('axis', 'mark', 'line', 'area'), relevant
    IDs/values, and timestamp.

- colors (list of strings; optional):
    Array of colors for the series palette.

- grid (dict; optional):
    Grid configuration. Object with vertical and horizontal boolean
    keys.

    `grid` is a dict with keys:

    - vertical (boolean; optional)

    - horizontal (boolean; optional)

- height (number; optional):
    Chart height in pixels. Default is 400.

- hideLegend (boolean; optional):
    If True, the legend is hidden.

- highlightedAxis (list of dicts; optional):
    Controlled axis highlight state. Array of objects specifying which
    axis values are highlighted. Each object has: - axisId
    (string|number): The axis identifier - dataIndex (number): The
    data index to highlight Set to empty array [] to clear highlights.

    `highlightedAxis` is a list of dicts with keys:

    - axisId (string | number; required)

    - dataIndex (number; required)

- highlightedItem (dict; optional):
    Controlled item highlight state. Specifies which data point is
    highlighted. Object with: - seriesId (string): The series
    identifier - dataIndex (number): The data index within the series
    (optional) Set to None to clear highlight.

    `highlightedItem` is a dict with keys:

    - seriesId (string; required)

    - dataIndex (number; optional)

- initialZoom (list of dicts; optional):
    Initial zoom state for uncontrolled mode. Array of objects with: -
    axisId (string): The axis identifier - start (number): Start
    position (0-100) - end (number): End position (0-100).

    `initialZoom` is a list of dicts with keys:

    - axisId (string; optional)

    - start (number; optional)

    - end (number; optional)

- licenseKey (string; optional):
    MUI X Pro license key. Required to enable Pro features like
    zoom/pan without watermarks. Get your license key from
    https://mui.com/x/introduction/licensing/.

- loading (boolean; optional):
    If True, a loading overlay is displayed.

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

- referenceLines (list of dicts; optional):
    Array of reference line configurations. Each reference line can be
    vertical (x) or horizontal (y). - x (string|number): X-axis value
    for a vertical reference line - y (number): Y-axis value for a
    horizontal reference line - axisId (string): The axis ID to use
    for the reference value - label (string): Label text displayed
    along the reference line - labelAlign (string): 'start', 'middle',
    or 'end' alignment - lineStyle (object): CSS style object for the
    line (e.g. {stroke: 'red', strokeDasharray: '4 4'}) - labelStyle
    (object): CSS style object for the label - spacing
    (number|object): Space around label in px, or {x, y} object.

    `referenceLines` is a list of dicts with keys:

    - x (string | number; optional)

    - y (string | number; optional)

    - axisId (string; optional)

    - label (string; optional)

    - labelAlign (a value equal to: 'start', 'middle', 'end'; optional)

    - lineStyle (dict; optional)

    - labelStyle (dict; optional)

    - spacing (number | dict; optional)

- series (list of dicts; optional):
    Array of series configurations. Each series represents a line in
    the chart. Each series object can have: - id (string): Unique
    identifier for the series - data (array of numbers): Y-axis
    values, supports None for gaps - label (string): Label shown in
    legend and tooltip - color (string): Custom color for this series
    - area (boolean): Fill area under the line - stack (string): Stack
    identifier for stacked area charts - curve (string): Interpolation
    method - 'linear', 'monotoneX', 'monotoneY',   'natural', 'step',
    'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY' -
    showMark (boolean): Whether to show data point markers -
    connectNulls (boolean): Whether to bridge gaps across None values
    - yAxisId (string): ID of the y-axis to use for this series (for
    biaxial charts) - xAxisId (string): ID of the x-axis to use for
    this series - highlightScope (object): Per-series highlight
    behavior with:   - highlight: 'none', 'item', or 'series'   -
    fade: 'none', 'series', or 'global'.

    `series` is a list of dicts with keys:

    - id (string; optional)

    - data (list of numbers; optional)

    - label (string; optional)

    - color (string; optional)

    - area (boolean; optional)

    - stack (string; optional)

    - curve (a value equal to: 'linear', 'monotoneX', 'monotoneY', 'natural', 'step', 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'; optional)

    - showMark (boolean; optional)

    - connectNulls (boolean; optional)

    - yAxisId (string; optional)

    - xAxisId (string; optional)

    - highlightScope (dict; optional)

        `highlightScope` is a dict with keys:

        - highlight (a value equal to: 'none', 'item', 'series'; optional)

        - fade (a value equal to: 'none', 'series', 'global'; optional)

- showSlider (boolean; optional):
    If True, shows a zoom slider below the chart for easy zoom
    control. The slider allows users to select a range and pan through
    the data.

- showToolbar (boolean; optional):
    Show chart toolbar with zoom/export controls. This is a Pro
    feature that requires a valid licenseKey.

- skipAnimation (boolean; optional):
    If True, animations are skipped.

- tooltip (dict; optional):
    Tooltip configuration. Object with trigger key. - trigger
    (string): 'item', 'axis', or 'none'.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'axis', 'none'; optional)

- tooltipItem (dict; optional):
    Controlled tooltip item state. Used to synchronize tooltips across
    multiple charts. Object with: - type (string): Chart type ('line',
    'bar', 'pie', etc.) - seriesId (string): The series identifier -
    dataIndex (number): The data index within the series Set to None
    to hide tooltip.

    `tooltipItem` is a dict with keys:

    - type (string; optional)

    - seriesId (string; optional)

    - dataIndex (number; optional)

- width (number; optional):
    Chart width in pixels. If not specified, the chart expands to fill
    the available space.

- xAxis (list of dicts; optional):
    X-axis configuration. Array of axis config objects. Each axis
    object can have: - data (array): X-axis values (timestamps in ms
    for 'time' scaleType) - dataKey (string): Key to use from dataset
    for axis values - label (string): Axis label - scaleType (string):
    'band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt'
    - position (string): 'top', 'bottom', or 'none' (hidden but still
    computed) - id (string): Axis identifier for referencing in series
    and zoom - min (number): Minimum domain value - max (number):
    Maximum domain value - reverse (boolean): Reverse axis direction -
    tickNumber (number): Approximate number of ticks - tickMinStep
    (number): Minimum step between ticks (ms for time axes) -
    tickMaxStep (number): Maximum step between ticks - tickSize
    (number): Tick mark length in pixels (default: 6) - tickSpacing
    (number): Minimum spacing in px between ticks (ordinal axes only)
    - tickInterval (array): Fixed tick positions as array of values -
    tickLabelStyle (object): CSS style for tick labels (e.g. {angle:
    45, fontSize: 12}) - tickLabelPlacement (string): 'middle' or
    'tick' (band scale only) - tickPlacement (string): 'end',
    'extremities', 'middle', 'start' (band scale only) -
    tickLabelMinGap (number): Minimum gap in px between tick labels
    (default: 4) - labelStyle (object): CSS style for the axis label -
    height (number): Space reserved for this x-axis in pixels -
    disableLine (boolean): Hide the axis line - disableTicks
    (boolean): Hide tick marks - domainLimit (string): 'nice'
    (default, rounds to friendly values) or 'strict' -
    categoryGapRatio (number): Gap ratio between bands (0-1, band
    scale only) - barGapRatio (number): Gap ratio between bars within
    a band (band scale only) - colorMap (object): Axis color mapping
    configuration - zoom (boolean or object): Enable zoom on this
    axis. Can be True or object with:   - minStart (number): Minimum
    start position (0-100)   - maxEnd (number): Maximum end position
    (0-100)   - minSpan (number): Minimum zoom span   - maxSpan
    (number): Maximum zoom span   - step (number): Zoom step size   -
    panning (boolean): Enable panning   - filterMode (string): 'keep'
    or 'discard'   - slider (object): Slider config with { enabled,
    preview, size, showTooltip }.

    `xAxis` is a list of dicts with keys:

    - data (list; optional)

    - dataKey (string; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt'; optional)

    - position (a value equal to: 'top', 'bottom', 'none'; optional)

    - id (string; optional)

    - min (number; optional)

    - max (number; optional)

    - reverse (boolean; optional)

    - tickNumber (number; optional)

    - tickMinStep (number; optional)

    - tickMaxStep (number; optional)

    - tickSize (number; optional)

    - tickSpacing (number; optional)

    - tickInterval (list; optional)

    - tickLabelStyle (dict; optional)

    - tickLabelPlacement (a value equal to: 'middle', 'tick'; optional)

    - tickPlacement (a value equal to: 'end', 'extremities', 'middle', 'start'; optional)

    - tickLabelMinGap (number; optional)

    - labelStyle (dict; optional)

    - height (number; optional)

    - dateFormat (string; optional)

    - dateTickFormat (string; optional)

    - disableLine (boolean; optional)

    - disableTicks (boolean; optional)

    - domainLimit (a value equal to: 'nice', 'strict'; optional)

    - categoryGapRatio (number; optional)

    - barGapRatio (number; optional)

    - colorMap (dict; optional)

    - zoom (boolean | dict; optional)

    - valueFormatter (dict; optional)

        `valueFormatter` is a dict with keys:

        - function (string; required)

        - options (dict; optional)

- yAxis (list of dicts; optional):
    Y-axis configuration. Array of axis config objects. Each axis
    object can have: - data (array): Y-axis values (for horizontal bar
    charts) - dataKey (string): Key to use from dataset for axis
    values - label (string): Axis label - scaleType (string): 'band',
    'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt' -
    position (string): 'left', 'right', or 'none' (hidden but still
    computed) - id (string): Axis identifier for referencing in series
    - min (number): Minimum domain value - max (number): Maximum
    domain value - width (number): Width allocated for axis in pixels
    - reverse (boolean): Reverse axis direction - tickNumber (number):
    Approximate number of ticks - tickMinStep (number): Minimum step
    between ticks - tickMaxStep (number): Maximum step between ticks -
    tickSize (number): Tick mark length in pixels (default: 6) -
    tickSpacing (number): Minimum spacing in px between ticks (ordinal
    axes only) - tickInterval (array): Fixed tick positions as array
    of values - tickLabelStyle (object): CSS style for tick labels
    (e.g. {angle: 45, fontSize: 12}) - tickLabelPlacement (string):
    'middle' or 'tick' (band scale only) - tickPlacement (string):
    'end', 'extremities', 'middle', 'start' (band scale only) -
    tickLabelMinGap (number): Minimum gap in px between tick labels
    (default: 4) - labelStyle (object): CSS style for the axis label -
    height (number): Space reserved for this y-axis in pixels -
    disableLine (boolean): Hide the axis line - disableTicks
    (boolean): Hide tick marks - domainLimit (string): 'nice'
    (default, rounds to friendly values) or 'strict' -
    categoryGapRatio (number): Gap ratio between bands (0-1, band
    scale only) - barGapRatio (number): Gap ratio between bars within
    a band (band scale only) - colorMap (object): Axis color mapping
    configuration - zoom (boolean or object): Enable zoom on this axis
    (same options as xAxis).

    `yAxis` is a list of dicts with keys:

    - data (list; optional)

    - dataKey (string; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'band', 'point', 'linear', 'log', 'time', 'utc', 'symlog', 'sqrt'; optional)

    - position (a value equal to: 'left', 'right', 'none'; optional)

    - id (string; optional)

    - min (number; optional)

    - max (number; optional)

    - width (number; optional)

    - reverse (boolean; optional)

    - dateFormat (string; optional)

    - dateTickFormat (string; optional)

    - tickNumber (number; optional)

    - tickMinStep (number; optional)

    - tickMaxStep (number; optional)

    - tickSize (number; optional)

    - tickSpacing (number; optional)

    - tickInterval (list; optional)

    - tickLabelStyle (dict; optional)

    - tickLabelPlacement (a value equal to: 'middle', 'tick'; optional)

    - tickPlacement (a value equal to: 'end', 'extremities', 'middle', 'start'; optional)

    - tickLabelMinGap (number; optional)

    - labelStyle (dict; optional)

    - height (number; optional)

    - disableLine (boolean; optional)

    - disableTicks (boolean; optional)

    - domainLimit (a value equal to: 'nice', 'strict'; optional)

    - categoryGapRatio (number; optional)

    - barGapRatio (number; optional)

    - colorMap (dict; optional)

    - zoom (boolean | dict; optional)

    - valueFormatter (dict; optional)

        `valueFormatter` is a dict with keys:

        - function (string; required)

        - options (dict; optional)

- zoom (list of dicts; optional):
    Controlled zoom state for the chart. Array of objects with: -
    axisId (string): The axis identifier - start (number): Start
    position (0-100) - end (number): End position (0-100).

    `zoom` is a list of dicts with keys:

    - axisId (string; optional)

    - start (number; optional)

    - end (number; optional)

- zoomData (list of dicts; optional):
    Current zoom state. Read-only output property updated when zoom
    changes. Array of objects with axisId, start, and end values.

    `zoomData` is a list of dicts with keys:

    - axisId (string; optional)

    - start (number; optional)

    - end (number; optional) | boolean | number | string | dict | list

- zoomInteractionConfig (dict; optional):
    Zoom interaction configuration. Controls which interactions are
    enabled for zooming and panning. Object with: - zoom (array): Zoom
    interactions - 'wheel', 'pinch', 'tapAndDrag', 'brush',
    'doubleTapReset',   or objects with { type, requiredKeys,
    pointerMode } - pan (array): Pan interactions - 'drag',
    'pressAndDrag', 'wheel',   or objects with { type, requiredKeys,
    pointerMode }.

    `zoomInteractionConfig` is a dict with keys:

    - zoom (list of dicts; optional)

        `zoom` is a list of string

      Or dict with keys:

        - type (string; optional)

        - requiredKeys (list of strings; optional)

        - pointerMode (a value equal to: 'mouse', 'touch'; optional)s

    - pan (list of dicts; optional)

        `pan` is a list of string | dict with keys:

        - type (string; optional)

        - requiredKeys (list of strings; optional)

        - pointerMode (a value equal to: 'mouse', 'touch'; optional)s"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'LineChart'
    SeriesHighlightScope = TypedDict(
        "SeriesHighlightScope",
            {
            "highlight": NotRequired[Literal["none", "item", "series"]],
            "fade": NotRequired[Literal["none", "series", "global"]]
        }
    )

    Series = TypedDict(
        "Series",
            {
            "id": NotRequired[str],
            "data": NotRequired[typing.Sequence[NumberType]],
            "label": NotRequired[str],
            "color": NotRequired[str],
            "area": NotRequired[bool],
            "stack": NotRequired[str],
            "curve": NotRequired[Literal["linear", "monotoneX", "monotoneY", "natural", "step", "stepBefore", "stepAfter", "catmullRom", "bumpX", "bumpY"]],
            "showMark": NotRequired[bool],
            "connectNulls": NotRequired[bool],
            "yAxisId": NotRequired[str],
            "xAxisId": NotRequired[str],
            "highlightScope": NotRequired["SeriesHighlightScope"]
        }
    )

    XAxisValueFormatter = TypedDict(
        "XAxisValueFormatter",
            {
            "function": str,
            "options": NotRequired[dict]
        }
    )

    XAxis = TypedDict(
        "XAxis",
            {
            "data": NotRequired[typing.Sequence],
            "dataKey": NotRequired[str],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["band", "point", "linear", "log", "time", "utc", "symlog", "sqrt"]],
            "position": NotRequired[Literal["top", "bottom", "none"]],
            "id": NotRequired[str],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "reverse": NotRequired[bool],
            "tickNumber": NotRequired[NumberType],
            "tickMinStep": NotRequired[NumberType],
            "tickMaxStep": NotRequired[NumberType],
            "tickSize": NotRequired[NumberType],
            "tickSpacing": NotRequired[NumberType],
            "tickInterval": NotRequired[typing.Sequence],
            "tickLabelStyle": NotRequired[dict],
            "tickLabelPlacement": NotRequired[Literal["middle", "tick"]],
            "tickPlacement": NotRequired[Literal["end", "extremities", "middle", "start"]],
            "tickLabelMinGap": NotRequired[NumberType],
            "labelStyle": NotRequired[dict],
            "height": NotRequired[NumberType],
            "dateFormat": NotRequired[str],
            "dateTickFormat": NotRequired[str],
            "disableLine": NotRequired[bool],
            "disableTicks": NotRequired[bool],
            "domainLimit": NotRequired[Literal["nice", "strict"]],
            "categoryGapRatio": NotRequired[NumberType],
            "barGapRatio": NotRequired[NumberType],
            "colorMap": NotRequired[dict],
            "zoom": NotRequired[typing.Union[bool, dict]],
            "valueFormatter": NotRequired[typing.Union[typing.Any, "XAxisValueFormatter"]]
        }
    )

    YAxisValueFormatter = TypedDict(
        "YAxisValueFormatter",
            {
            "function": str,
            "options": NotRequired[dict]
        }
    )

    YAxis = TypedDict(
        "YAxis",
            {
            "data": NotRequired[typing.Sequence],
            "dataKey": NotRequired[str],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["band", "point", "linear", "log", "time", "utc", "symlog", "sqrt"]],
            "position": NotRequired[Literal["left", "right", "none"]],
            "id": NotRequired[str],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "width": NotRequired[NumberType],
            "reverse": NotRequired[bool],
            "dateFormat": NotRequired[str],
            "dateTickFormat": NotRequired[str],
            "tickNumber": NotRequired[NumberType],
            "tickMinStep": NotRequired[NumberType],
            "tickMaxStep": NotRequired[NumberType],
            "tickSize": NotRequired[NumberType],
            "tickSpacing": NotRequired[NumberType],
            "tickInterval": NotRequired[typing.Sequence],
            "tickLabelStyle": NotRequired[dict],
            "tickLabelPlacement": NotRequired[Literal["middle", "tick"]],
            "tickPlacement": NotRequired[Literal["end", "extremities", "middle", "start"]],
            "tickLabelMinGap": NotRequired[NumberType],
            "labelStyle": NotRequired[dict],
            "height": NotRequired[NumberType],
            "disableLine": NotRequired[bool],
            "disableTicks": NotRequired[bool],
            "domainLimit": NotRequired[Literal["nice", "strict"]],
            "categoryGapRatio": NotRequired[NumberType],
            "barGapRatio": NotRequired[NumberType],
            "colorMap": NotRequired[dict],
            "zoom": NotRequired[typing.Union[bool, dict]],
            "valueFormatter": NotRequired[typing.Union[typing.Any, "YAxisValueFormatter"]]
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
            "vertical": NotRequired[bool],
            "horizontal": NotRequired[bool]
        }
    )

    Tooltip = TypedDict(
        "Tooltip",
            {
            "trigger": NotRequired[Literal["item", "axis", "none"]]
        }
    )

    Zoom = TypedDict(
        "Zoom",
            {
            "axisId": NotRequired[str],
            "start": NotRequired[NumberType],
            "end": NotRequired[NumberType]
        }
    )

    InitialZoom = TypedDict(
        "InitialZoom",
            {
            "axisId": NotRequired[str],
            "start": NotRequired[NumberType],
            "end": NotRequired[NumberType]
        }
    )

    ZoomInteractionConfigZoom = TypedDict(
        "ZoomInteractionConfigZoom",
            {
            "type": NotRequired[str],
            "requiredKeys": NotRequired[typing.Sequence[str]],
            "pointerMode": NotRequired[Literal["mouse", "touch"]]
        }
    )

    ZoomInteractionConfigPan = TypedDict(
        "ZoomInteractionConfigPan",
            {
            "type": NotRequired[str],
            "requiredKeys": NotRequired[typing.Sequence[str]],
            "pointerMode": NotRequired[Literal["mouse", "touch"]]
        }
    )

    ZoomInteractionConfig = TypedDict(
        "ZoomInteractionConfig",
            {
            "zoom": NotRequired[typing.Sequence[typing.Union[str, "ZoomInteractionConfigZoom"]]],
            "pan": NotRequired[typing.Sequence[typing.Union[str, "ZoomInteractionConfigPan"]]]
        }
    )

    ReferenceLines = TypedDict(
        "ReferenceLines",
            {
            "x": NotRequired[typing.Union[str, NumberType]],
            "y": NotRequired[typing.Union[str, NumberType]],
            "axisId": NotRequired[str],
            "label": NotRequired[str],
            "labelAlign": NotRequired[Literal["start", "middle", "end"]],
            "lineStyle": NotRequired[dict],
            "labelStyle": NotRequired[dict],
            "spacing": NotRequired[typing.Union[NumberType, dict]]
        }
    )

    BrushConfig = TypedDict(
        "BrushConfig",
            {
            "enabled": NotRequired[bool],
            "preventTooltip": NotRequired[bool],
            "preventHighlight": NotRequired[bool]
        }
    )

    BrushDataStart = TypedDict(
        "BrushDataStart",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    BrushDataCurrent = TypedDict(
        "BrushDataCurrent",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    BrushData = TypedDict(
        "BrushData",
            {
            "start": NotRequired["BrushDataStart"],
            "current": NotRequired["BrushDataCurrent"],
            "timestamp": NotRequired[str]
        }
    )

    AxisHighlight = TypedDict(
        "AxisHighlight",
            {
            "x": NotRequired[Literal["none", "line", "band"]],
            "y": NotRequired[Literal["none", "line"]]
        }
    )

    HighlightedAxis = TypedDict(
        "HighlightedAxis",
            {
            "axisId": typing.Union[str, NumberType],
            "dataIndex": NumberType
        }
    )

    HighlightedItem = TypedDict(
        "HighlightedItem",
            {
            "seriesId": str,
            "dataIndex": NotRequired[NumberType]
        }
    )

    TooltipItem = TypedDict(
        "TooltipItem",
            {
            "type": NotRequired[str],
            "seriesId": NotRequired[str],
            "dataIndex": NotRequired[NumberType]
        }
    )

    ZoomData = TypedDict(
        "ZoomData",
            {
            "axisId": NotRequired[str],
            "start": NotRequired[NumberType],
            "end": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        licenseKey: typing.Optional[str] = None,
        series: typing.Optional[typing.Sequence["Series"]] = None,
        xAxis: typing.Optional[typing.Sequence["XAxis"]] = None,
        yAxis: typing.Optional[typing.Sequence["YAxis"]] = None,
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        grid: typing.Optional["Grid"] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        hideLegend: typing.Optional[bool] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        skipAnimation: typing.Optional[bool] = None,
        loading: typing.Optional[bool] = None,
        zoom: typing.Optional[typing.Sequence["Zoom"]] = None,
        initialZoom: typing.Optional[typing.Sequence["InitialZoom"]] = None,
        showSlider: typing.Optional[bool] = None,
        zoomInteractionConfig: typing.Optional["ZoomInteractionConfig"] = None,
        referenceLines: typing.Optional[typing.Sequence["ReferenceLines"]] = None,
        brushConfig: typing.Optional["BrushConfig"] = None,
        brushOverlay: typing.Optional[Literal["none", "default", "values"]] = None,
        brushSeriesId: typing.Optional[str] = None,
        brushData: typing.Optional["BrushData"] = None,
        axisHighlight: typing.Optional["AxisHighlight"] = None,
        highlightedAxis: typing.Optional[typing.Sequence["HighlightedAxis"]] = None,
        highlightedItem: typing.Optional["HighlightedItem"] = None,
        showToolbar: typing.Optional[bool] = None,
        tooltipItem: typing.Optional["TooltipItem"] = None,
        zoomData: typing.Optional[typing.Union[typing.Sequence["ZoomData"], typing.Any]] = None,
        clickData: typing.Optional[dict] = None,
        n_clicks: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'axisHighlight', 'brushConfig', 'brushData', 'brushOverlay', 'brushSeriesId', 'clickData', 'colors', 'grid', 'height', 'hideLegend', 'highlightedAxis', 'highlightedItem', 'initialZoom', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'tooltip', 'tooltipItem', 'width', 'xAxis', 'yAxis', 'zoom', 'zoomData', 'zoomInteractionConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisHighlight', 'brushConfig', 'brushData', 'brushOverlay', 'brushSeriesId', 'clickData', 'colors', 'grid', 'height', 'hideLegend', 'highlightedAxis', 'highlightedItem', 'initialZoom', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'tooltip', 'tooltipItem', 'width', 'xAxis', 'yAxis', 'zoom', 'zoomData', 'zoomInteractionConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LineChart, self).__init__(**args)

setattr(LineChart, "__init__", _explicitize_args(LineChart.__init__))
