"""
Time Clock — inline time selection (no input / popper / modal).

A limited working example for the TimeClock component, wrapping MUI X
@mui/x-date-pickers TimeClock. Mirrors the official MUI demo sections:
basic usage, controlled vs uncontrolled, form props, views, and 12h/24h format.
"""

import json

import dash
import dash_mantine_components as dmc
from dash import html, callback, Input, Output, ctx, no_update

from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX

dash.register_page(
    __name__,
    path='/time-clock',
    name='Time Clock',
    title=PAGE_TITLE_PREFIX + 'TimeClock',
    description='TimeClock demos mirroring the MUI docs: basic usage, '
                'controlled vs uncontrolled values, disabled/readOnly, view '
                'configuration and 12h/24h format.',
    image_url=OG_IMAGE_URL,
)

LLMS_DOC = """# TimeClock

`TimeClock` is an inline clock-face time selector — no text input, popper, or
modal; the user drags the hand or clicks the numbers to pick hours, minutes,
and optionally seconds. It is a **Community (free)** component and the
library's first **Date & Time Pickers** component (wrapping
`@mui/x-date-pickers` 8.24.0 with the dayjs adapter), NOT a chart.

**String <-> dayjs boundary:** dayjs objects can't cross the Dash boundary, so
values are exchanged as strings — full wall-time ISO
(`"2022-04-17T15:30:00"`) or time-only (`"15:30"` / `"15:30:45"`). Strings are
parsed to dayjs on the way in; on the way out the value is formatted as local
wall-time `YYYY-MM-DDTHH:mm:ss` (not `toISOString()`, to avoid a UTC shift).

## Usage

```python
from dash_mui_charts import TimeClock

TimeClock(
    id="clock",
    value="15:30:00",                       # controlled, in/out (wall-time ISO out)
    defaultValue="15:30:00",                # uncontrolled initial (use instead of value)
    views=["hours", "minutes", "seconds"],  # default ["hours", "minutes"]
    view="hours",                           # controlled view, in/out
    ampm=False,                             # force 12h/24h (omit = locale default)
    minutesStep=5,
    minTime="09:00", maxTime="18:00",
    disabled=False, readOnly=False,
    showViewSwitcher=True,
)
```

## Outputs

`value` (wall-time ISO), `view`, and `timeData`:
`{"hours", "minutes", "seconds", "formatted" ("HH:mm:ss"), "event_timestamp"}`.

```python
@callback(Output("out", "children"), Input("clock", "timeData"))
def show(td):
    return td["formatted"] if td else "-"
```

## Notes

- Function-only MUI props are omitted (not serializable across the Dash
  boundary): `shouldDisableTime`, `referenceDate`, `slots`/`slotProps`.
  `skipDisabled` is intentionally not exposed — it belongs to the digital
  clock variants, not the analog `TimeClock`.
- Recolour via `sx` using internal MUI class names: face `.MuiClock-clock`,
  hand `.MuiClockPointer-root` + `.MuiClockPointer-thumb` + centre
  `.MuiClock-pin`, digits `.MuiClockNumber-root` / `-selected`, meridiem
  `.MuiClock-amButton` / `-pmButton`.

## Related pages

- `/time-clock` — this demo (basic, controlled vs uncontrolled, form props,
  views, 12h/24h)
- `/time-clock-lab` — dynamic colours, liquid glass theme, stopwatch, and
  two-way pairings with dmc.TimeInput / TimePicker / TimeGrid / DateTimePicker
"""

from dash_mui_charts import TimeClock


# --------------------------------------------------------------------------- #
# Small layout helpers (theme-aware via Mantine)
# --------------------------------------------------------------------------- #
def demo_item(label, component):
    """A labelled clock, like MUI's <DemoItem>."""
    return dmc.Stack(
        [
            dmc.Text(label, size="sm", fw=600, c="dimmed"),
            dmc.Paper(component, withBorder=True, radius="md", p="xs",
                      style={"width": "fit-content"}),
        ],
        gap=6,
    )


def section(title, description, *children):
    return dmc.Stack(
        [
            dmc.Title(title, order=3),
            dmc.Text(description, size="sm", c="dimmed"),
            *children,
        ],
        gap="sm",
        mb="xl",
    )


# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #
layout = dmc.Container(
    [
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Title("Time Clock", order=1),
                        dmc.Badge("Community", color="teal", variant="light"),
                    ],
                    align="center",
                ),
                dmc.Text(
                    "Select a time directly on a clock face — no text input, popper, "
                    "or modal. Values cross the Dash boundary as strings "
                    "(\"15:30\" or \"2022-04-17T15:30:00\").",
                    c="dimmed",
                ),
            ],
            gap=4,
            mb="lg",
        ),

        # --- 1. Basic usage --------------------------------------------------
        section(
            "1. Basic usage",
            "Uncontrolled — the component manages its own internal state.",
            dmc.Paper(
                TimeClock(id="tc-basic"),
                withBorder=True, radius="md", p="xs",
                style={"width": "fit-content"},
            ),
        ),

        # --- 2. Uncontrolled vs controlled ----------------------------------
        section(
            "2. Uncontrolled vs. controlled value",
            "Left clock is uncontrolled (defaultValue). Right clock is controlled — "
            "its value lives in Dash; the buttons push new values in, and every "
            "change flows back out.",
            dmc.Group(
                [
                    demo_item(
                        "Uncontrolled clock",
                        TimeClock(id="tc-uncontrolled",
                                  defaultValue="2022-04-17T15:30:00"),
                    ),
                    demo_item(
                        "Controlled clock",
                        TimeClock(id="tc-controlled",
                                  value="2022-04-17T15:30:00"),
                    ),
                ],
                align="flex-start",
                gap="xl",
            ),
            dmc.Group(
                [
                    dmc.Button("Set 09:00", id="tc-set-0900", size="xs",
                               variant="light"),
                    dmc.Button("Set 14:30", id="tc-set-1430", size="xs",
                               variant="light"),
                    dmc.Button("Set 18:45", id="tc-set-1845", size="xs",
                               variant="light"),
                ],
                gap="xs",
            ),
            dmc.Code(id="tc-controlled-out", block=True,
                     children="Pick a time on the controlled clock…"),
        ),

        # --- 3. Form props ---------------------------------------------------
        section(
            "3. Form props",
            "The component can be disabled or read-only.",
            dmc.Group(
                [
                    demo_item(
                        "disabled",
                        TimeClock(id="tc-disabled",
                                  defaultValue="2022-04-17T15:30:00",
                                  disabled=True),
                    ),
                    demo_item(
                        "readOnly",
                        TimeClock(id="tc-readonly",
                                  defaultValue="2022-04-17T15:30:00",
                                  readOnly=True),
                    ),
                ],
                align="flex-start",
                gap="xl",
            ),
        ),

        # --- 4. Views --------------------------------------------------------
        section(
            "4. Views",
            "Choose which views appear and in what order. By default only hours "
            "and minutes are enabled.",
            dmc.Group(
                [
                    demo_item(
                        '"hours", "minutes" and "seconds"',
                        TimeClock(id="tc-views-hms",
                                  views=["hours", "minutes", "seconds"]),
                    ),
                    demo_item(
                        '"hours"',
                        TimeClock(id="tc-views-h", views=["hours"]),
                    ),
                    demo_item(
                        '"minutes" and "seconds"',
                        TimeClock(id="tc-views-ms",
                                  views=["minutes", "seconds"]),
                    ),
                ],
                align="flex-start",
                gap="xl",
            ),
            dmc.Code(id="tc-views-out", block=True,
                     children="Pick on the hours/minutes/seconds clock…"),
        ),

        # --- 5. 12h / 24h format --------------------------------------------
        section(
            "5. 12h / 24h format",
            "The clock uses the locale's hour format by default. Force it with the "
            "ampm prop.",
            dmc.Group(
                [
                    demo_item(
                        "Locale default (enUS → 12h)",
                        TimeClock(id="tc-ampm-default",
                                  defaultValue="2022-04-17T15:30:00"),
                    ),
                    demo_item(
                        "AM/PM enabled",
                        TimeClock(id="tc-ampm-on",
                                  defaultValue="2022-04-17T15:30:00",
                                  ampm=True),
                    ),
                    demo_item(
                        "AM/PM disabled (24h)",
                        TimeClock(id="tc-ampm-off",
                                  defaultValue="2022-04-17T15:30:00",
                                  ampm=False),
                    ),
                ],
                align="flex-start",
                gap="xl",
            ),
        ),
    ],
    size="lg",
    px=0,
    py="md",
)


# --------------------------------------------------------------------------- #
# Callbacks
# --------------------------------------------------------------------------- #
@callback(
    Output("tc-controlled", "value"),
    Input("tc-set-0900", "n_clicks"),
    Input("tc-set-1430", "n_clicks"),
    Input("tc-set-1845", "n_clicks"),
    prevent_initial_call=True,
)
def set_controlled(_a, _b, _c):
    mapping = {
        "tc-set-0900": "09:00",
        "tc-set-1430": "14:30",
        "tc-set-1845": "18:45",
    }
    return mapping.get(ctx.triggered_id, no_update)


@callback(
    Output("tc-controlled-out", "children"),
    Input("tc-controlled", "value"),
    Input("tc-controlled", "timeData"),
    prevent_initial_call=True,
)
def show_controlled(value, time_data):
    return json.dumps({"value": value, "timeData": time_data}, indent=2)


@callback(
    Output("tc-views-out", "children"),
    Input("tc-views-hms", "timeData"),
    prevent_initial_call=True,
)
def show_views(time_data):
    if not time_data:
        return "Pick on the hours/minutes/seconds clock…"
    return json.dumps(time_data, indent=2)
