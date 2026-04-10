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


class CandlestickChart(Component):
    """A CandlestickChart component.
CandlestickChart — Dash wrapper that renders OHLC candlestick charts
using MUI X Charts Pro composition API with custom SVG candle rendering.

Supports:
- Array format: series[0].data = [[open, high, low, close], ...]
- Dataset format: dataset + series[0].datasetKeys = {open, high, low, close}
- Volume overlay (optional)
- Reference lines
- Grid, axes, zoom (Pro), toolbar (Pro)
- Click events

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- bodyWidthRatio (number; optional):
    Candle body width as a ratio of the band width (0-1). Default:
    0.6.

- clickData (dict; optional):
    Fires on candle click. Contains: {dataIndex, label, open, high,
    low, close, timestamp}.

- dataset (list of dicts; optional):
    Dataset for datasetKeys mode. Array of row objects. Example:
    [{date: '2025-01-02', open: 100, high: 110, low: 95, close: 105,
    volume: 1000}, ...].

- grid (dict; optional):
    Background grid lines: {horizontal: bool, vertical: bool}.

    `grid` is a dict with keys:

    - horizontal (boolean; optional)

    - vertical (boolean; optional)

- height (number; optional):
    Chart height in pixels.

- hideLegend (boolean; optional):
    Hide the legend (default: True for candlestick).

- hoverData (dict; optional):
    Hover data output (reserved for future use).

- initialZoom (list of dicts; optional):
    Initial zoom state (Pro). Array of {axisId, start, end}.

- licenseKey (string; optional):
    MUI X Pro license key. Required for zoom, slider, and toolbar.

- margin (dict; optional):
    Chart margins: {top, bottom, left, right} in pixels.

    `margin` is a dict with keys:

    - top (number; optional)

    - bottom (number; optional)

    - left (number; optional)

    - right (number; optional)

- referenceLines (list of dicts; optional):
    Reference lines array. Same format as BarChart/LineChart.

- series (list of dicts; optional):
    OHLC candlestick series. Typically a single series with two data
    formats:  Array format:   series=[{data: [[open,high,low,close],
    ...], upColor: '#4caf50', downColor: '#f44336'}]  Dataset format
    (use with dataset prop):   series=[{datasetKeys: {open:'open',
    high:'high', low:'low', close:'close'},            upColor:
    '#4caf50', downColor: '#f44336'}]  Optional volume:
    series=[{..., volume: [100, 200, ...]}]  (array format)
    series=[{..., volumeKey: 'volume'}]       (dataset format)  Series
    properties: - data (array): Array of [open, high, low, close]
    tuples or {open, high, low, close} objects - datasetKeys (object):
    {open, high, low, close} mapping to dataset columns - upColor
    (string): Color when close >= open (default: '#4caf50') -
    downColor (string): Color when close < open (default: '#f44336') -
    volume (array): Volume values for each candle - volumeKey
    (string): Dataset column name for volume data.

- showSlider (boolean; optional):
    Show zoom range slider (Pro).

- showToolbar (boolean; optional):
    Show toolbar (Pro).

- showVolume (boolean; optional):
    Show volume bars below candles. Requires volume data in series.

- skipAnimation (boolean; optional):
    Disable animations.

- tooltip (dict; optional):
    Tooltip configuration: {trigger: 'item'|'none'}. Set trigger to
    'none' to disable the OHLC tooltip.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'none'; optional)

- volumeHeightRatio (number; optional):
    Volume bars maximum height as ratio of chart height (0-1).
    Default: 0.2.

- wickWidth (number; optional):
    Wick (shadow) line width in pixels. Default: 2.

- width (number; optional):
    Chart width in pixels. If not set, uses parent container width.

- xAxis (list of dicts; optional):
    X-axis configuration. Typically band scale with dates/labels. -
    data (array): Category labels (dates, day names, etc.) - dataKey
    (string): Column from dataset for labels - label (string): Axis
    label text - scaleType (string): Always 'band' for candlestick
    (set automatically) - zoom (object): Zoom config for Pro features
    - tickLabelStyle (object): CSS for tick labels - tickPlacement
    (string): 'start', 'end', 'middle', 'extremities'.

- yAxis (list of dicts; optional):
    Y-axis configuration for price values. - label (string): Axis
    label (e.g., 'Price ($)') - min/max (number): Override
    auto-computed domain from OHLC data - position (string): 'left' or
    'right'.

- zoomData (list of dicts; optional):
    Zoom state output (Pro).

- zoomInteractionConfig (dict; optional):
    Zoom interaction configuration (Pro)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'CandlestickChart'
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

    Tooltip = TypedDict(
        "Tooltip",
            {
            "trigger": NotRequired[Literal["item", "none"]]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        series: typing.Optional[typing.Sequence[dict]] = None,
        dataset: typing.Optional[typing.Sequence[dict]] = None,
        xAxis: typing.Optional[typing.Sequence[dict]] = None,
        yAxis: typing.Optional[typing.Sequence[dict]] = None,
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        grid: typing.Optional["Grid"] = None,
        skipAnimation: typing.Optional[bool] = None,
        hideLegend: typing.Optional[bool] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        bodyWidthRatio: typing.Optional[NumberType] = None,
        wickWidth: typing.Optional[NumberType] = None,
        showVolume: typing.Optional[bool] = None,
        volumeHeightRatio: typing.Optional[NumberType] = None,
        referenceLines: typing.Optional[typing.Sequence[dict]] = None,
        licenseKey: typing.Optional[str] = None,
        initialZoom: typing.Optional[typing.Sequence[dict]] = None,
        showSlider: typing.Optional[bool] = None,
        showToolbar: typing.Optional[bool] = None,
        zoomInteractionConfig: typing.Optional[dict] = None,
        clickData: typing.Optional[dict] = None,
        hoverData: typing.Optional[dict] = None,
        zoomData: typing.Optional[typing.Sequence[dict]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'bodyWidthRatio', 'clickData', 'dataset', 'grid', 'height', 'hideLegend', 'hoverData', 'initialZoom', 'licenseKey', 'margin', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'showVolume', 'skipAnimation', 'tooltip', 'volumeHeightRatio', 'wickWidth', 'width', 'xAxis', 'yAxis', 'zoomData', 'zoomInteractionConfig']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'bodyWidthRatio', 'clickData', 'dataset', 'grid', 'height', 'hideLegend', 'hoverData', 'initialZoom', 'licenseKey', 'margin', 'referenceLines', 'series', 'showSlider', 'showToolbar', 'showVolume', 'skipAnimation', 'tooltip', 'volumeHeightRatio', 'wickWidth', 'width', 'xAxis', 'yAxis', 'zoomData', 'zoomInteractionConfig']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CandlestickChart, self).__init__(**args)

setattr(CandlestickChart, "__init__", _explicitize_args(CandlestickChart.__init__))
