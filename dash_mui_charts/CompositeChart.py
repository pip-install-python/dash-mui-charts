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


class CompositeChart(Component):
    """A CompositeChart component.
CompositeChart component for layering multiple chart types together.
Uses MUI X Charts composition API to render scatter, line, and area plots
on a single chart surface. Each series must specify its type ('scatter' or 'line').
Supports Pro features like zoom/pan with a license key.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axisHighlight (dict; optional):
    Axis highlight configuration.

    `axisHighlight` is a dict with keys:

    - x (a value equal to: 'none', 'line', 'band'; optional)

    - y (a value equal to: 'none', 'line', 'band'; optional)

- clickData (dict; optional):
    Data from the most recent click event. Contains type
    ('scatter'|'line'), seriesId, dataIndex, and timestamp.

- colors (list of strings; optional):
    Color palette array.

- dataset (list of dicts; optional):
    Dataset array for datasetKeys-driven series.

- disableVoronoi (boolean; optional):
    If True, disables Voronoi cell interaction.

- grid (dict; optional):
    Grid configuration.

    `grid` is a dict with keys:

    - horizontal (boolean; optional)

    - vertical (boolean; optional)

- height (number; optional):
    Chart height in pixels. Default is 400.

- hideLegend (boolean; optional):
    If True, the legend is hidden.

- highlightedItem (dict; optional):
    Currently highlighted item (controlled input/output).

- initialZoom (list of dicts; optional):
    Initial zoom configuration (Pro). Array of {axisId, start, end}
    objects. start/end are percentages (0-100) of the axis range.

    `initialZoom` is a list of dicts with keys:

    - axisId (string | number; optional)

    - start (number; optional)

    - end (number; optional)

- licenseKey (string; optional):
    MUI X Pro license key. Required for zoom/pan/toolbar features.

- loading (boolean; optional):
    If True, shows a loading overlay.

- margin (dict; optional):
    Chart margins in pixels.

    `margin` is a dict with keys:

    - top (number; optional)

    - right (number; optional)

    - bottom (number; optional)

    - left (number; optional)

- n_clicks (number; optional):
    Number of times the chart has been clicked.

- referenceLines (list of dicts; optional):
    Reference lines to display on the chart. Array of objects with: -
    x (number|string): Vertical reference line at x value - y
    (number): Horizontal reference line at y value - label (string):
    Label text - lineStyle (object): CSS for line element - labelStyle
    (object): CSS for label text - labelAlign (string): 'start',
    'middle', 'end'.

    `referenceLines` is a list of dicts with keys:

    - x (number | string; optional)

    - y (number; optional)

    - label (string; optional)

    - lineStyle (dict; optional)

    - labelStyle (dict; optional)

    - labelAlign (a value equal to: 'start', 'middle', 'end'; optional)

    - spacing (dict; optional)

- series (list of dicts; optional):
    Array of series to display. Each series MUST include a 'type'
    field.  Scatter series: {type: 'scatter', id, label, color,
    markerSize, data: [{x, y, id}], highlightScope}  Line series:
    {type: 'line', id, label, color, data: [...], area, curve,
    showMark, highlightScope, yAxisId}.

    `series` is a list of dicts with keys:

    - type (a value equal to: 'scatter', 'line'; required)

    - id (string; optional)

    - label (string; optional)

    - color (string; optional)

    - data (list of dicts; optional)

        `data` is a list of numbers | list of dicts with keys:

        - x (number; optional)

        - y (number; optional)

        - id (string | number; optional)

    - datasetKeys (dict; optional)

        `datasetKeys` is a dict with keys:

        - x (string; optional)

        - y (string; optional)

    - markerSize (number; optional)

    - preview (dict; optional)

        `preview` is a dict with keys:

        - markerSize (number; optional)

    - area (boolean; optional)

    - curve (a value equal to: 'linear', 'monotoneX', 'monotoneY', 'natural', 'step', 'stepBefore', 'stepAfter', 'catmullRom', 'bumpX', 'bumpY'; optional)

    - showMark (boolean; optional)

    - yAxisId (string; optional)

    - xAxisId (string; optional)

    - highlightScope (dict; optional)

        `highlightScope` is a dict with keys:

        - highlight (a value equal to: 'item', 'series', 'none'; optional)

        - fade (a value equal to: 'global', 'series', 'none'; optional)

    - stack (string; optional)

    - connectNulls (boolean; optional)

- showSlider (boolean; optional):
    If True, shows the zoom slider below the chart. Injects
    zoom.slider.enabled into x-axis config.

- showToolbar (boolean; optional):
    If True, shows the Pro toolbar for zoom/export controls.

- skipAnimation (boolean; optional):
    If True, animations are disabled.

- slotProps (dict; optional):
    Props passed to internal slot components.

- tooltip (dict; optional):
    Tooltip configuration.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'axis', 'none'; optional)

- voronoiMaxRadius (number | a value equal to: 'item'; optional):
    Maximum distance for Voronoi scatter interaction.

- width (number; optional):
    Chart width in pixels. If not set, fills available space.

- xAxis (list of dicts; optional):
    X-axis configuration. Array of axis config objects.

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

    - zoom (boolean | dict; optional)

- yAxis (list of dicts; optional):
    Y-axis configuration. Array of axis config objects.

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

    - zoom (boolean | dict; optional)

- zAxis (list of dicts; optional):
    Z-axis configuration for color mapping scatter points.

    `zAxis` is a list of dicts with keys:

    - id (string; optional)

    - data (list; optional)

    - dataKey (string; optional)

    - min (number; optional)

    - max (number; optional)

    - colorMap (dict; optional)

- zoomData (list of dicts; optional):
    Current zoom state. Read-only output updated on zoom/pan. Array of
    {axisId, start, end} objects.

    `zoomData` is a list of dicts with keys:

    - axisId (string | number; optional)

    - start (number; optional)

    - end (number; optional)

- zoomInteractionConfig (dict; optional):
    Fine-grained control over zoom/pan interactions (Pro). - zoom:
    Array of interaction types ['wheel', 'pinch', 'brush',
    'tapAndDrag', 'doubleTapReset'] - pan: Array of interaction types
    ['drag', 'pressAndDrag', 'wheel'].

    `zoomInteractionConfig` is a dict with keys:

    - zoom (list; optional)

    - pan (list; optional)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'CompositeChart'
    SeriesData = TypedDict(
        "SeriesData",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "id": NotRequired[typing.Union[str, NumberType]]
        }
    )

    SeriesDatasetKeys = TypedDict(
        "SeriesDatasetKeys",
            {
            "x": NotRequired[str],
            "y": NotRequired[str]
        }
    )

    SeriesPreview = TypedDict(
        "SeriesPreview",
            {
            "markerSize": NotRequired[NumberType]
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
            "type": Literal["scatter", "line"],
            "id": NotRequired[str],
            "label": NotRequired[str],
            "color": NotRequired[str],
            "data": NotRequired[typing.Union[typing.Sequence[NumberType], typing.Sequence["SeriesData"]]],
            "datasetKeys": NotRequired["SeriesDatasetKeys"],
            "markerSize": NotRequired[NumberType],
            "preview": NotRequired["SeriesPreview"],
            "area": NotRequired[bool],
            "curve": NotRequired[Literal["linear", "monotoneX", "monotoneY", "natural", "step", "stepBefore", "stepAfter", "catmullRom", "bumpX", "bumpY"]],
            "showMark": NotRequired[bool],
            "yAxisId": NotRequired[str],
            "xAxisId": NotRequired[str],
            "highlightScope": NotRequired["SeriesHighlightScope"],
            "stack": NotRequired[str],
            "connectNulls": NotRequired[bool]
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
            "zoom": NotRequired[typing.Union[bool, dict]]
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
            "domainLimit": NotRequired[Literal["nice", "strict"]],
            "zoom": NotRequired[typing.Union[bool, dict]]
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

    ReferenceLines = TypedDict(
        "ReferenceLines",
            {
            "x": NotRequired[typing.Union[NumberType, str]],
            "y": NotRequired[NumberType],
            "label": NotRequired[str],
            "lineStyle": NotRequired[dict],
            "labelStyle": NotRequired[dict],
            "labelAlign": NotRequired[Literal["start", "middle", "end"]],
            "spacing": NotRequired[dict]
        }
    )

    InitialZoom = TypedDict(
        "InitialZoom",
            {
            "axisId": NotRequired[typing.Union[str, NumberType]],
            "start": NotRequired[NumberType],
            "end": NotRequired[NumberType]
        }
    )

    ZoomInteractionConfig = TypedDict(
        "ZoomInteractionConfig",
            {
            "zoom": NotRequired[typing.Sequence],
            "pan": NotRequired[typing.Sequence]
        }
    )

    ZoomData = TypedDict(
        "ZoomData",
            {
            "axisId": NotRequired[typing.Union[str, NumberType]],
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
        slotProps: typing.Optional[dict] = None,
        referenceLines: typing.Optional[typing.Sequence["ReferenceLines"]] = None,
        initialZoom: typing.Optional[typing.Sequence["InitialZoom"]] = None,
        showToolbar: typing.Optional[bool] = None,
        showSlider: typing.Optional[bool] = None,
        zoomInteractionConfig: typing.Optional["ZoomInteractionConfig"] = None,
        highlightedItem: typing.Optional[dict] = None,
        clickData: typing.Optional[dict] = None,
        n_clicks: typing.Optional[NumberType] = None,
        zoomData: typing.Optional[typing.Sequence["ZoomData"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'axisHighlight', 'clickData', 'colors', 'dataset', 'disableVoronoi', 'grid', 'height', 'hideLegend', 'highlightedItem', 'initialZoom', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'slotProps', 'tooltip', 'voronoiMaxRadius', 'width', 'xAxis', 'yAxis', 'zAxis', 'zoomData', 'zoomInteractionConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisHighlight', 'clickData', 'colors', 'dataset', 'disableVoronoi', 'grid', 'height', 'hideLegend', 'highlightedItem', 'initialZoom', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'slotProps', 'tooltip', 'voronoiMaxRadius', 'width', 'xAxis', 'yAxis', 'zAxis', 'zoomData', 'zoomInteractionConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CompositeChart, self).__init__(**args)

setattr(CompositeChart, "__init__", _explicitize_args(CompositeChart.__init__))
