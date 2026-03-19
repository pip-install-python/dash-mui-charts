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


class Heatmap(Component):
    """A Heatmap component.
Heatmap component wrapping MUI X Charts Pro Heatmap.
Renders a matrix visualization where color intensity represents values.
This is a Pro feature - requires MUI X Pro license key.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cellStyle (dict; optional):
    Custom cell style. Use 'rounded' for default rounded corners with
    gap, or provide an object for detailed configuration: - gap
    (number): Spacing between cells in pixels (default: 4) -
    borderRadius (number): Corner radius in pixels (default: 10) -
    showValue (boolean): Display value text in cells (default: True) -
    fontSize (number): Font size for value text (default: 12) -
    fontWeight (number): Font weight for value text (default: 500) -
    textColor (string): Color for value text (default: '#ffffff').

    `cellStyle` is a a value equal to: 'rounded' | dict with keys:

    - gap (number; optional)

    - borderRadius (number; optional)

    - showValue (boolean; optional)

    - fontSize (number; optional)

    - fontWeight (number; optional)

    - textColor (string; optional)

- clickData (dict; optional):
    Data from the most recent click event. Read-only output property.
    Contains x, y, value, seriesId, and timestamp.

- colorScale (dict; optional):
    Color scale configuration for mapping values to colors.
    Continuous scale (interpolates between colors): { type:
    'continuous', min: 0, max: 100, colors: ['#e3f2fd', '#1565c0'] }
    Piecewise scale (discrete color bands): { type: 'piecewise',
    thresholds: [20, 40, 60, 80],   colors: ['#color1', '#color2',
    '#color3', '#color4', '#color5'] }  Note: For piecewise, you need
    n+1 colors for n thresholds.

    `colorScale` is a dict with keys:

    - type (a value equal to: 'continuous', 'piecewise'; optional)

    - min (number; optional)

    - max (number; optional)

    - colors (list of strings; optional)

    - thresholds (list of numbers; optional)

- data (list of list of numberss; optional):
    Heatmap data as an array of [x, y, value] tuples. - x: X-axis
    index (0-based) - y: Y-axis index (0-based) - value: Numeric value
    for the cell (mapped to color)  Example: [[0, 0, 25], [0, 1, 45],
    [1, 0, 30], [1, 1, 60]].

- height (number; optional):
    Chart height in pixels. Default is 400.

- hideLegend (boolean; optional):
    If True, the color legend is hidden.

- highlightScope (dict; optional):
    Highlight scope configuration for cell highlighting behavior. -
    highlight: 'item' or 'none' - fade: 'global' or 'none'.

    `highlightScope` is a dict with keys:

    - highlight (a value equal to: 'item', 'none'; optional)

    - fade (a value equal to: 'global', 'none'; optional)

- highlightedItem (dict; optional):
    Currently highlighted item. Read-only output property updated when
    the user hovers over a cell.

- licenseKey (string; optional):
    MUI X Pro license key. Required to enable Pro features without
    watermarks. Get your license key from
    https://mui.com/x/introduction/licensing/.

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

- slotProps (dict; optional):
    Props passed to internal slot components for customization.

- tooltip (dict; optional):
    Tooltip configuration. - trigger (string): 'item' to show on cell
    hover, 'none' to disable.

    `tooltip` is a dict with keys:

    - trigger (a value equal to: 'item', 'none'; optional)

- width (number; optional):
    Chart width in pixels. If not specified, the chart expands to fill
    the available space.

- xAxis (dict; optional):
    X-axis configuration object. - data (array): Category labels for
    x-axis - label (string): Axis label - scaleType (string): Scale
    type, defaults to 'band' for heatmaps - zoom (boolean or object):
    Enable zoom on this axis. Can be True or object with:   - minStart
    (number): Minimum start position (0-100)   - maxEnd (number):
    Maximum end position (0-100)   - minSpan (number): Minimum zoom
    span   - maxSpan (number): Maximum zoom span   - step (number):
    Zoom step size   - panning (boolean): Enable panning   -
    filterMode (string): 'keep' or 'discard'   - slider (object):
    Slider config with { enabled, preview, size, showTooltip }.

    `xAxis` is a dict with keys:

    - data (list; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'band', 'point'; optional)

    - zoom (boolean | dict; optional)

- yAxis (dict; optional):
    Y-axis configuration object. - data (array): Category labels for
    y-axis - label (string): Axis label - scaleType (string): Scale
    type, defaults to 'band' for heatmaps - zoom (boolean or object):
    Enable zoom on this axis (same options as xAxis).

    `yAxis` is a dict with keys:

    - data (list; optional)

    - label (string; optional)

    - scaleType (a value equal to: 'band', 'point'; optional)

    - zoom (boolean | dict; optional)"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'Heatmap'
    XAxis = TypedDict(
        "XAxis",
            {
            "data": NotRequired[typing.Sequence],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["band", "point"]],
            "zoom": NotRequired[typing.Union[bool, dict]]
        }
    )

    YAxis = TypedDict(
        "YAxis",
            {
            "data": NotRequired[typing.Sequence],
            "label": NotRequired[str],
            "scaleType": NotRequired[Literal["band", "point"]],
            "zoom": NotRequired[typing.Union[bool, dict]]
        }
    )

    ColorScale = TypedDict(
        "ColorScale",
            {
            "type": NotRequired[Literal["continuous", "piecewise"]],
            "min": NotRequired[NumberType],
            "max": NotRequired[NumberType],
            "colors": NotRequired[typing.Sequence[str]],
            "thresholds": NotRequired[typing.Sequence[NumberType]]
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

    Tooltip = TypedDict(
        "Tooltip",
            {
            "trigger": NotRequired[Literal["item", "none"]]
        }
    )

    HighlightScope = TypedDict(
        "HighlightScope",
            {
            "highlight": NotRequired[Literal["item", "none"]],
            "fade": NotRequired[Literal["global", "none"]]
        }
    )

    CellStyle = TypedDict(
        "CellStyle",
            {
            "gap": NotRequired[NumberType],
            "borderRadius": NotRequired[NumberType],
            "showValue": NotRequired[bool],
            "fontSize": NotRequired[NumberType],
            "fontWeight": NotRequired[NumberType],
            "textColor": NotRequired[str]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        licenseKey: typing.Optional[str] = None,
        data: typing.Optional[typing.Sequence[typing.Sequence[NumberType]]] = None,
        xAxis: typing.Optional["XAxis"] = None,
        yAxis: typing.Optional["YAxis"] = None,
        colorScale: typing.Optional["ColorScale"] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        margin: typing.Optional["Margin"] = None,
        hideLegend: typing.Optional[bool] = None,
        tooltip: typing.Optional["Tooltip"] = None,
        highlightScope: typing.Optional["HighlightScope"] = None,
        cellStyle: typing.Optional[typing.Union[Literal["rounded"], "CellStyle"]] = None,
        slotProps: typing.Optional[dict] = None,
        highlightedItem: typing.Optional[dict] = None,
        clickData: typing.Optional[dict] = None,
        n_clicks: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'cellStyle', 'clickData', 'colorScale', 'data', 'height', 'hideLegend', 'highlightScope', 'highlightedItem', 'licenseKey', 'margin', 'n_clicks', 'slotProps', 'tooltip', 'width', 'xAxis', 'yAxis']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cellStyle', 'clickData', 'colorScale', 'data', 'height', 'hideLegend', 'highlightScope', 'highlightedItem', 'licenseKey', 'margin', 'n_clicks', 'slotProps', 'tooltip', 'width', 'xAxis', 'yAxis']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Heatmap, self).__init__(**args)

setattr(Heatmap, "__init__", _explicitize_args(Heatmap.__init__))
