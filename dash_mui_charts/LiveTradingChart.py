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


class LiveTradingChart(Component):
    """A LiveTradingChart component.
LiveTradingChart simulates real-time candlestick trading data with volume bars,
forecast line with uncertainty bands, alert labels, and optional price labels.
Uses an internal React timer for smooth high-speed updates.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alertDownColor (string; optional):
    Alert label color for downward moves. Default '#f44336'.

- alertFilter (dict; optional):
    Functions-as-props: custom alert detection. {function: 'name',
    options: {...}}.

    `alertFilter` is a dict with keys:

    - function (string; required)

    - options (dict; optional)

- alertFormatter (dict; optional):
    Functions-as-props: custom alert label formatting. {function:
    'name', options: {...}}.

    `alertFormatter` is a dict with keys:

    - function (string; required)

    - options (dict; optional)

- alertHistory (list; optional):
    Recent alert history (read-only output).

- alertLookback (number; optional):
    Number of candles on each side to confirm a swing high/low.
    Default 5.

- alertMinDistance (number; optional):
    Minimum ticks between consecutive alerts to prevent clustering.
    Default 10.

- alertProbability (number; optional):
    (Legacy) Probability of alert per tick — unused by default swing
    detection.

- alertThresholdPct (number; optional):
    (Legacy) Minimum % change to flag as alert — unused by default
    swing detection.

- alertUpColor (string; optional):
    Alert label color for upward moves. Default '#4caf50'.

- candleDownColor (string; optional):
    Candle color for downward (close < open) moves. Default '#f44336'.

- candleUpColor (string; optional):
    Candle color for upward (close >= open) moves. Default '#4caf50'.

- currentPrice (number; optional):
    Current price (read-only output).

- drift (number; optional):
    Price drift/trend factor. Default 0.001.

- forecastColor (string; optional):
    Forecast line/area color. Default '#ff9800'.

- forecastSize (number; optional):
    Number of forecast points beyond the window. Default 15.

- forecastVolatility (number; optional):
    Forecast uncertainty multiplier. Default 1.5.

- grid (dict; optional):
    Grid configuration.

    `grid` is a dict with keys:

    - horizontal (boolean; optional)

    - vertical (boolean; optional)

- height (number; optional):
    Chart height in pixels. Default 500.

- hideLegend (boolean; optional):
    Hide the legend. Default True.

- initialPrice (number; optional):
    Starting price. Default 100.

- intervalMs (number; optional):
    Tick interval in milliseconds. Default 300.

- licenseKey (string; optional):
    MUI X Pro license key.

- margin (dict; optional):
    Chart margins.

    `margin` is a dict with keys:

    - top (number; optional)

    - right (number; optional)

    - bottom (number; optional)

    - left (number; optional)

- maxVisibleAlerts (number; optional):
    Maximum number of alert labels visible in the window. Default 6.

- resetTrigger (number; optional):
    Increment this to reset the simulation.

- running (boolean; optional):
    Whether the simulation is running. Default False.

- seed (number; optional):
    RNG seed for reproducible randomness. Default 42.

- showGrid (boolean; optional):
    Show grid lines. Default True.

- showLabels (boolean; optional):
    Show price labels on candles. Default False.

- showSlider (boolean; optional):
    Show zoom slider below the chart (Pro). Default False.

- showVolume (boolean; optional):
    Show volume bars. Default True.

- tickCount (number; optional):
    Total ticks elapsed (read-only output).

- uncertaintyOpacity (number; optional):
    Opacity of the forecast uncertainty shaded area. Default 0.15.

- volatility (number; optional):
    Price volatility factor. Default 0.02.

- volumeHeightPct (number; optional):
    Volume bars height as percentage of chart area. Default 20.

- width (number; optional):
    Chart width in pixels. If not set, fills available space.

- windowSize (number; optional):
    Number of visible candles in the sliding window. Default 60.

- xAxisLabel (string; optional):
    X-axis label text. Default 'Tick'.

- yAxisLabel (string; optional):
    Y-axis label text. Default 'Price'.

- zoomData (list of dicts; optional):
    Current zoom state (read-only output).

    `zoomData` is a list of dicts with keys:

    - axisId (string | number; optional)

    - start (number; optional)

    - end (number; optional)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'LiveTradingChart'
    Margin = TypedDict(
        "Margin",
            {
            "top": NotRequired[NumberType],
            "right": NotRequired[NumberType],
            "bottom": NotRequired[NumberType],
            "left": NotRequired[NumberType]
        }
    )

    AlertFilter = TypedDict(
        "AlertFilter",
            {
            "function": str,
            "options": NotRequired[dict]
        }
    )

    AlertFormatter = TypedDict(
        "AlertFormatter",
            {
            "function": str,
            "options": NotRequired[dict]
        }
    )

    Grid = TypedDict(
        "Grid",
            {
            "horizontal": NotRequired[bool],
            "vertical": NotRequired[bool]
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
        height: typing.Optional[NumberType] = None,
        width: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        windowSize: typing.Optional[NumberType] = None,
        forecastSize: typing.Optional[NumberType] = None,
        running: typing.Optional[bool] = None,
        intervalMs: typing.Optional[NumberType] = None,
        seed: typing.Optional[NumberType] = None,
        resetTrigger: typing.Optional[NumberType] = None,
        initialPrice: typing.Optional[NumberType] = None,
        volatility: typing.Optional[NumberType] = None,
        drift: typing.Optional[NumberType] = None,
        forecastVolatility: typing.Optional[NumberType] = None,
        alertProbability: typing.Optional[NumberType] = None,
        alertThresholdPct: typing.Optional[NumberType] = None,
        alertLookback: typing.Optional[NumberType] = None,
        alertMinDistance: typing.Optional[NumberType] = None,
        maxVisibleAlerts: typing.Optional[NumberType] = None,
        alertFilter: typing.Optional["AlertFilter"] = None,
        alertFormatter: typing.Optional["AlertFormatter"] = None,
        candleUpColor: typing.Optional[str] = None,
        candleDownColor: typing.Optional[str] = None,
        forecastColor: typing.Optional[str] = None,
        alertUpColor: typing.Optional[str] = None,
        alertDownColor: typing.Optional[str] = None,
        uncertaintyOpacity: typing.Optional[NumberType] = None,
        showVolume: typing.Optional[bool] = None,
        showLabels: typing.Optional[bool] = None,
        volumeHeightPct: typing.Optional[NumberType] = None,
        showGrid: typing.Optional[bool] = None,
        showSlider: typing.Optional[bool] = None,
        hideLegend: typing.Optional[bool] = None,
        grid: typing.Optional["Grid"] = None,
        xAxisLabel: typing.Optional[str] = None,
        yAxisLabel: typing.Optional[str] = None,
        currentPrice: typing.Optional[NumberType] = None,
        tickCount: typing.Optional[NumberType] = None,
        alertHistory: typing.Optional[typing.Sequence] = None,
        zoomData: typing.Optional[typing.Sequence["ZoomData"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'alertDownColor', 'alertFilter', 'alertFormatter', 'alertHistory', 'alertLookback', 'alertMinDistance', 'alertProbability', 'alertThresholdPct', 'alertUpColor', 'candleDownColor', 'candleUpColor', 'currentPrice', 'drift', 'forecastColor', 'forecastSize', 'forecastVolatility', 'grid', 'height', 'hideLegend', 'initialPrice', 'intervalMs', 'licenseKey', 'margin', 'maxVisibleAlerts', 'resetTrigger', 'running', 'seed', 'showGrid', 'showLabels', 'showSlider', 'showVolume', 'tickCount', 'uncertaintyOpacity', 'volatility', 'volumeHeightPct', 'width', 'windowSize', 'xAxisLabel', 'yAxisLabel', 'zoomData']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alertDownColor', 'alertFilter', 'alertFormatter', 'alertHistory', 'alertLookback', 'alertMinDistance', 'alertProbability', 'alertThresholdPct', 'alertUpColor', 'candleDownColor', 'candleUpColor', 'currentPrice', 'drift', 'forecastColor', 'forecastSize', 'forecastVolatility', 'grid', 'height', 'hideLegend', 'initialPrice', 'intervalMs', 'licenseKey', 'margin', 'maxVisibleAlerts', 'resetTrigger', 'running', 'seed', 'showGrid', 'showLabels', 'showSlider', 'showVolume', 'tickCount', 'uncertaintyOpacity', 'volatility', 'volumeHeightPct', 'width', 'windowSize', 'xAxisLabel', 'yAxisLabel', 'zoomData']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LiveTradingChart, self).__init__(**args)

setattr(LiveTradingChart, "__init__", _explicitize_args(LiveTradingChart.__init__))
