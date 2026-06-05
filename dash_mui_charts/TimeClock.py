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


class TimeClock(Component):
    """A TimeClock component.
TimeClock lets the user pick a time on an inline clock face (hours, minutes,
and optionally seconds) without any input, popper, or modal. Values are
exchanged with Dash as strings; on change it emits `value` (wall-time ISO),
the current `view`, and a parsed `timeData` convenience object.

Keyword arguments:

- id (string; optional):
    Dash component id.

- ampm (boolean; optional):
    Force 12h (True) or 24h (False). Omit to use the locale default.

- autoFocus (boolean; default False):
    Auto-focus the clock on mount.

- className (string; optional):
    CSS class applied to the wrapping div.

- defaultValue (string; optional):
    Uncontrolled initial value (same string formats as `value`).

- disableFuture (boolean; default False):
    Disable times in the future (relative to now).

- disableIgnoringDatePartForTimeValidation (boolean; default False):
    When True, min/max time comparisons include the date part. When
    False (default), only the time-of-day is compared.

- disablePast (boolean; default False):
    Disable times in the past (relative to now).

- disabled (boolean; default False):
    Disable the whole clock.

- maxTime (string; optional):
    Maximum selectable time (ISO or time-only string).

- minTime (string; optional):
    Minimum selectable time (ISO or time-only string).

- minutesStep (number; optional):
    Step (in minutes) between selectable minute values.

- openTo (a value equal to: 'hours', 'minutes', 'seconds'; optional):
    Which view to open first (uncontrolled).

- readOnly (boolean; default False):
    Make the clock read-only (no editing).

- showViewSwitcher (boolean; default False):
    Show the hours/minutes/seconds view-switch arrow buttons.

- sx (dict; optional):
    MUI sx styling object applied to the TimeClock.

- timeData (dict; optional):
    Parsed convenience output, updated on every change: { hours,
    minutes, seconds, formatted (\"HH:mm:ss\"), event_timestamp }.

    `timeData` is a dict with keys:

    - hours (number; optional)

    - minutes (number; optional)

    - seconds (number; optional)

    - formatted (string; optional)

    - event_timestamp (number; optional)

- value (string; optional):
    Controlled value. Full wall-time ISO (\"2022-04-17T15:30:00\") or
    time-only (\"15:30\" / \"15:30:45\"). Also an OUTPUT: updated on
    every change with a full wall-time ISO string.

- view (a value equal to: 'hours', 'minutes', 'seconds'; optional):
    Controlled visible view. Also an OUTPUT — updated when the view
    changes.

- views (list of a value equal to: 'hours', 'minutes', 'seconds's; default ['hours', 'minutes']):
    Which views to render, in order. Default [\"hours\", \"minutes\"]."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_mui_charts'
    _type = 'TimeClock'
    TimeData = TypedDict(
        "TimeData",
            {
            "hours": NotRequired[NumberType],
            "minutes": NotRequired[NumberType],
            "seconds": NotRequired[NumberType],
            "formatted": NotRequired[str],
            "event_timestamp": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        value: typing.Optional[str] = None,
        defaultValue: typing.Optional[str] = None,
        views: typing.Optional[typing.Sequence[Literal["hours", "minutes", "seconds"]]] = None,
        view: typing.Optional[Literal["hours", "minutes", "seconds"]] = None,
        openTo: typing.Optional[Literal["hours", "minutes", "seconds"]] = None,
        ampm: typing.Optional[bool] = None,
        disabled: typing.Optional[bool] = None,
        readOnly: typing.Optional[bool] = None,
        autoFocus: typing.Optional[bool] = None,
        minutesStep: typing.Optional[NumberType] = None,
        minTime: typing.Optional[str] = None,
        maxTime: typing.Optional[str] = None,
        disableFuture: typing.Optional[bool] = None,
        disablePast: typing.Optional[bool] = None,
        disableIgnoringDatePartForTimeValidation: typing.Optional[bool] = None,
        showViewSwitcher: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        sx: typing.Optional[dict] = None,
        timeData: typing.Optional["TimeData"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ampm', 'autoFocus', 'className', 'defaultValue', 'disableFuture', 'disableIgnoringDatePartForTimeValidation', 'disablePast', 'disabled', 'maxTime', 'minTime', 'minutesStep', 'openTo', 'readOnly', 'showViewSwitcher', 'sx', 'timeData', 'value', 'view', 'views']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ampm', 'autoFocus', 'className', 'defaultValue', 'disableFuture', 'disableIgnoringDatePartForTimeValidation', 'disablePast', 'disabled', 'maxTime', 'minTime', 'minutesStep', 'openTo', 'readOnly', 'showViewSwitcher', 'sx', 'timeData', 'value', 'view', 'views']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(TimeClock, self).__init__(**args)

setattr(TimeClock, "__init__", _explicitize_args(TimeClock.__init__))
