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


class BarChart(Component):
    """A BarChart component.
BarChart — Dash wrapper for MUI X BarChart (Community) and BarChartPro (Pro).

Renders vertical or horizontal bar charts with support for stacking, bar labels,
dataset mode, color maps, reference lines, highlighting, and Pro features
(zoom, toolbar, brush).

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axisClickData (dict; optional):
    Fires on axis area click. Contains: {axisValue, dataIndex,
    seriesValues, timestamp}.

- axisHighlight (dict; optional):
    Axis highlight configuration: {x: 'band'|'line'|'none', y:
    'band'|'line'|'none'}.

    `axisHighlight` is a dict with keys:

    - x (a value equal to: 'band', 'line', 'none'; optional)

    - y (a value equal to: 'band', 'line', 'none'; optional)

- borderRadius (number; optional):
    Border radius for bar corners in pixels.

- brushConfig (dict; optional):
    Brush selection config (Pro): {enabled: bool, preventTooltip:
    bool, preventHighlight: bool}.

- clickData (dict; optional):
    Fires on bar click. Contains: {seriesId, dataIndex, timestamp}.

- colors (list of strings; optional):
    Color palette array for series colors.

- dataset (list of dicts; optional):
    Array of row objects for dataKey-based series. Example: [{month:
    'Jan', sales: 100}, {month: 'Feb', sales: 150}].

- grid (dict; optional):
    Background grid lines: {horizontal: bool, vertical: bool}.

    `grid` is a dict with keys:

    - horizontal (boolean; optional)

    - vertical (boolean; optional)

- height (number; optional):
    Chart height in pixels.

- hideLegend (boolean; optional):
    Hide the legend.

- highlightedItem (dict; optional):
    Controlled highlight state. Both input (to set highlight) and
    output (fires on hover). Object: {seriesId, dataIndex} or None.

- initialZoom (list of dicts; optional):
    Initial zoom state (Pro). Array of {axisId, start, end}.

- layout (a value equal to: 'vertical', 'horizontal'; optional):
    Bar direction: 'vertical' (default) or 'horizontal'.

- licenseKey (string; optional):
    MUI X Pro license key. Required for zoom, brush, and toolbar
    features.

- loading (boolean; optional):
    Show loading overlay.

- margin (dict; optional):
    Chart margins: {top, bottom, left, right} in pixels.

    `margin` is a dict with keys:

    - top (number; optional)

    - bottom (number; optional)

    - left (number; optional)

    - right (number; optional)

- n_clicks (number; optional):
    Number of times bars have been clicked.

- referenceLines (list of dicts; optional):
    Reference lines array. Each object: - x (string|number): Vertical
    line at this x value - y (number): Horizontal line at this y value
    - axisId (string): Which axis (when multiple) - label (string):
    Text label - labelAlign (string): 'start', 'middle', 'end' -
    lineStyle (object): SVG style for the line - labelStyle (object):
    SVG style for the label - spacing (object): Label offset.

- renderer (a value equal to: 'svg-single', 'svg-batch'; optional):
    Renderer strategy: 'svg-single' (default) or 'svg-batch' for large
    datasets.

- series (list of dicts; optional):
    Array of bar series objects. Each series can contain: - data
    (number[]): Bar values - dataKey (string): Column key when using
    dataset prop - label (string): Series label for legend/tooltip -
    color (string): Series color - stack (string): Stack group ID
    (series with same value are stacked) - stackOffset (string):
    'none', 'expand', 'diverging', 'silhouette', 'wiggle' - stackOrder
    (string): 'none', 'appearance', 'ascending', 'descending',
    'insideOut', 'reverse' - barLabel (string): 'value' or
    'formattedValue' to show labels on bars - barLabelPlacement
    (string): 'center' or 'outside' - highlightScope (object):
    {highlight, fade} highlight behavior - yAxisId (string): Y-axis
    binding for biaxial charts - id (string): Unique series
    identifier.

- showSlider (boolean; optional):
    Show zoom range slider below the chart (Pro).

- showToolbar (boolean; optional):
    Show zoom/export toolbar above the chart (Pro).

- skipAnimation (boolean; optional):
    Disable animations.

- tooltip (dict; optional):
    Tooltip configuration: {trigger: 'item'|'axis'|'none'}.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'axis', 'none'; optional)

- width (number; optional):
    Chart width in pixels. If not set, uses parent container width.

- xAxis (list of dicts; optional):
    X-axis configuration array. For bar charts, typically uses
    scaleType: 'band'. Each axis can contain: - data (array): Category
    labels - dataKey (string): Column key from dataset - scaleType
    (string): 'band' (required for bars), 'linear', 'log', etc. -
    label (string): Axis label text - categoryGapRatio (number): Gap
    between categories (0-1) - barGapRatio (number): Gap between bars
    in same category (-1 to Infinity) - tickPlacement (string):
    'start', 'end', 'middle', 'extremities' - tickLabelPlacement
    (string): 'tick' or 'middle' - colorMap (object): Color mapping
    configuration - zoom (object): Zoom config for Pro features - id
    (string): Axis identifier - position (string): 'top', 'bottom',
    'none' - min/max (number): Domain limits - reverse (bool): Reverse
    axis direction - tickNumber (number): Approximate tick count -
    tickMinStep/tickMaxStep (number): Control tick spacing -
    tickLabelStyle (object): CSS for tick labels - labelStyle
    (object): CSS for axis label - disableLine (bool): Hide axis line
    - disableTicks (bool): Hide tick marks - domainLimit (string):
    'nice' or 'strict' - height (number): Space reserved for axis.

- yAxis (list of dicts; optional):
    Y-axis configuration array. Same structure as xAxis.

- zoomData (list of dicts; optional):
    Zoom state output (Pro). Fires on zoom change.

- zoomInteractionConfig (dict; optional):
    Zoom interaction configuration (Pro). Controls drag, wheel, pinch,
    brush zoom behaviors."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'BarChart'
    Margin = TypedDict(
        "Margin",
            {
            "top": NotRequired[NumberType],
            "bottom": NotRequired[NumberType],
            "left": NotRequired[NumberType],
            "right": NotRequired[NumberType]
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
            "x": NotRequired[Literal["band", "line", "none"]],
            "y": NotRequired[Literal["band", "line", "none"]]
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
        series: typing.Optional[typing.Sequence[dict]] = None,
        dataset: typing.Optional[typing.Sequence[dict]] = None,
        xAxis: typing.Optional[typing.Sequence[dict]] = None,
        yAxis: typing.Optional[typing.Sequence[dict]] = None,
        layout: typing.Optional[Literal["vertical", "horizontal"]] = None,
        borderRadius: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        grid: typing.Optional["Grid"] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        skipAnimation: typing.Optional[bool] = None,
        loading: typing.Optional[bool] = None,
        hideLegend: typing.Optional[bool] = None,
        renderer: typing.Optional[Literal["svg-single", "svg-batch"]] = None,
        axisHighlight: typing.Optional["AxisHighlight"] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        highlightedItem: typing.Optional[dict] = None,
        referenceLines: typing.Optional[typing.Sequence[dict]] = None,
        licenseKey: typing.Optional[str] = None,
        initialZoom: typing.Optional[typing.Sequence[dict]] = None,
        showSlider: typing.Optional[bool] = None,
        showToolbar: typing.Optional[bool] = None,
        brushConfig: typing.Optional[dict] = None,
        zoomInteractionConfig: typing.Optional[dict] = None,
        clickData: typing.Optional[dict] = None,
        axisClickData: typing.Optional[dict] = None,
        zoomData: typing.Optional[typing.Sequence[dict]] = None,
        n_clicks: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'axisClickData', 'axisHighlight', 'borderRadius', 'brushConfig', 'clickData', 'colors', 'dataset', 'grid', 'height', 'hideLegend', 'highlightedItem', 'initialZoom', 'layout', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'renderer', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'tooltip', 'width', 'xAxis', 'yAxis', 'zoomData', 'zoomInteractionConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisClickData', 'axisHighlight', 'borderRadius', 'brushConfig', 'clickData', 'colors', 'dataset', 'grid', 'height', 'hideLegend', 'highlightedItem', 'initialZoom', 'layout', 'licenseKey', 'loading', 'margin', 'n_clicks', 'referenceLines', 'renderer', 'series', 'showSlider', 'showToolbar', 'skipAnimation', 'tooltip', 'width', 'xAxis', 'yAxis', 'zoomData', 'zoomInteractionConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(BarChart, self).__init__(**args)

setattr(BarChart, "__init__", _explicitize_args(BarChart.__init__))
