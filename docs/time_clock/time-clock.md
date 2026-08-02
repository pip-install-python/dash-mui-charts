---
name: Time Clock
description: "TimeClock demos mirroring the MUI docs: basic usage, controlled vs uncontrolled values, disabled/readOnly, view configuration and 12h/24h format."
endpoint: /time-clock
package: dash_mui_charts
category: Date & Time Pickers
icon: mdi:clock-outline
---

.. llms_copy::Time Clock

.. toc::

### Overview

TimeClock demos mirroring the MUI docs: basic usage, controlled vs uncontrolled values, disabled/readOnly, view configuration and 12h/24h format.


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

### Usage

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

### Outputs

`value` (wall-time ISO), `view`, and `timeData`:
`{"hours", "minutes", "seconds", "formatted" ("HH:mm:ss"), "event_timestamp"}`.

```python
@callback(Output("out", "children"), Input("clock", "timeData"))
def show(td):
    return td["formatted"] if td else "-"
```

### Notes

- Function-only MUI props are omitted (not serializable across the Dash
  boundary): `shouldDisableTime`, `referenceDate`, `slots`/`slotProps`.
  `skipDisabled` is intentionally not exposed — it belongs to the digital
  clock variants, not the analog `TimeClock`.
- Recolour via `sx` using internal MUI class names: face `.MuiClock-clock`,
  hand `.MuiClockPointer-root` + `.MuiClockPointer-thumb` + centre
  `.MuiClock-pin`, digits `.MuiClockNumber-root` / `-selected`, meridiem
  `.MuiClock-amButton` / `-pmButton`.

### Related pages

- `/time-clock` — this demo (basic, controlled vs uncontrolled, form props,
  views, 12h/24h)
- `/time-clock-lab` — dynamic colours, liquid glass theme, stopwatch, and
  two-way pairings with dmc.TimeInput / TimePicker / TimeGrid / DateTimePicker

---

### Live examples

.. exec::docs.time_clock.demo
    :code: false

.. source::docs/time_clock/demo.py
    :defaultExpanded: false
    :withExpandedButton: true
