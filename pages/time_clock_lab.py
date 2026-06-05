"""
TimeClock Lab — dynamic theming, a stopwatch, and two-way pairings with
dash-mantine-components time inputs.

Shows the dash-mui-charts TimeClock working hand-in-hand with DMC. Each
example carries a syntax-highlighted "View code" panel (dmc.CodeHighlightTabs):
  1. dmc.ColorPicker/Input → recolor face (with opacity) + hand + digits live
  2. Liquid glass clock    → CSS glassmorphism + magnifying-lens handle
  3. dcc.Interval          → start/stop/restart stopwatch (seconds→minutes→hours)
  4. dmc.TimeInput         → two-way sync + reset buttons
  5. dmc.TimePicker        → two-way sync (dropdown, seconds)
  6. dmc.TimeGrid          → two-way sync against preset half-hour slots
  7. dmc.DateTimePicker    → the clock drives the time portion of a datetime
"""

import datetime as _dt

import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, ctx, no_update
from dash_iconify import DashIconify

dash.register_page(__name__, path='/time-clock-lab', name='TimeClock Lab')

from dash_mui_charts import TimeClock


# --------------------------------------------------------------------------- #
# Value helpers — normalise the many string formats to canonical "HH:MM:SS"
# --------------------------------------------------------------------------- #
def to_hms(value):
    """Any time-ish string (ISO, 'HH:mm', 'HH:mm:ss') -> 'HH:MM:SS' or None."""
    if not value or not isinstance(value, str):
        return None
    part = value.split('T')[-1] if 'T' in value else value
    bits = part.split(':')
    if len(bits) < 2:
        return None
    try:
        h, m = int(bits[0]), int(bits[1])
        s = int(bits[2]) if len(bits) > 2 else 0
    except ValueError:
        return None
    return f'{h:02d}:{m:02d}:{s:02d}'


def date_part(iso, fallback=None):
    """Extract the 'YYYY-MM-DD' date from an ISO datetime string."""
    if iso and len(iso) >= 10 and iso[4] == '-':
        return iso[:10]
    return fallback or _dt.date.today().isoformat()


# --------------------------------------------------------------------------- #
# Layout helpers
# --------------------------------------------------------------------------- #
def clock_paper(component):
    return dmc.Paper(component, withBorder=True, radius="md", p="xs",
                     style={"width": "fit-content"})


def lab_section(icon, title, description, *body):
    return dmc.Card(
        [
            dmc.Group(
                [
                    dmc.ThemeIcon(DashIconify(icon=icon, width=20),
                                  variant="light", size="lg", radius="md"),
                    dmc.Title(title, order=3),
                ],
                gap="sm",
            ),
            dmc.Text(description, size="sm", c="dimmed", mt=4),
            dmc.Divider(my="md"),
            *body,
        ],
        withBorder=True, radius="md", shadow="sm", p="lg", mb="xl",
    )


SWATCHES = [
    "#25262b", "#868e96", "#fa5252", "#e64980", "#be4bdb", "#7950f2",
    "#4c6ef5", "#228be6", "#15aabf", "#12b886", "#40c057", "#82c91e",
    "#fab005", "#fd7e14",
]

_TODAY = _dt.date.today().isoformat()

# Preset half-hour slots for the TimeGrid pairing (06:00 … 22:00)
TG_DATA = []
for _h in range(6, 23):
    TG_DATA.append(f"{_h:02d}:00")
    if _h < 22:
        TG_DATA.append(f"{_h:02d}:30")


# --------------------------------------------------------------------------- #
# "View code" — professional, syntax-highlighted snippets via CodeHighlightTabs
# --------------------------------------------------------------------------- #
_PY_ICON = DashIconify(icon="vscode-icons:file-type-python", width=18)
_CSS_ICON = DashIconify(icon="vscode-icons:file-type-css", width=18)


def _code_blocks(tabs):
    return dmc.CodeHighlightTabs(
        code=[
            {"fileName": name, "code": code, "language": lang,
             "icon": _CSS_ICON if lang == "css" else _PY_ICON}
            for name, code, lang in tabs
        ],
        withExpandButton=True,
        defaultExpanded=False,
        maxCollapsedHeight=260,
    )


def code_panel(tabs, **style):
    """Always-visible code panel (used inline, e.g. to the right of controls)."""
    panel = _code_blocks(tabs)
    panel.style = {"minWidth": 300, "flex": "1 1 360px",
                   "maxWidth": 600, "alignSelf": "stretch", **style}
    return panel


def view_code(tabs):
    """Collapsed-by-default 'View code' disclosure with the example's source."""
    return dmc.Accordion(
        chevronPosition="left", variant="separated", radius="md", mt="md",
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        "View code",
                        icon=DashIconify(icon="mdi:code-tags", width=18),
                    ),
                    dmc.AccordionPanel(_code_blocks(tabs)),
                ],
                value="code",
            ),
        ],
    )


# --- Faithful, condensed snippets for each example -------------------------- #
CODE = {}

CODE["colors_layout"] = '''from dash_mui_charts import TimeClock
import dash_mantine_components as dmc

# Face = ColorPicker with an alpha slider (rgba → opacity is adjustable);
# hand & numbers = compact ColorInputs.
dmc.ColorPicker(id="lab-color-face", format="rgba",
                value="rgba(231, 245, 255, 0.9)",
                swatches=SWATCHES, withPicker=True)
dmc.ColorInput(id="lab-color-hand", format="hex", value="#228be6")
dmc.ColorInput(id="lab-color-num",  format="hex", value="",
               placeholder="Theme default")

TimeClock(id="lab-color-clock", defaultValue="10:10:00",
          views=["hours", "minutes", "seconds"], showViewSwitcher=True)
'''

CODE["colors_callback"] = '''from dash import callback, Input, Output, ctx, no_update

@callback(
    Output("lab-color-clock", "sx"),
    Output("lab-color-face", "value"),
    Output("lab-color-hand", "value"),
    Output("lab-color-num", "value"),
    Input("lab-color-face", "value"),   # rgba string → opacity supported
    Input("lab-color-hand", "value"),
    Input("lab-color-num", "value"),
    Input("lab-color-reset", "n_clicks"),
)
def recolor_clock(face, hand, num, _reset):
    is_reset = ctx.triggered_id == "lab-color-reset"
    if is_reset:
        face, hand, num = "rgba(231, 245, 255, 0.9)", "#228be6", ""
    # Map each colour onto the MUI clock's internal classes via `sx`:
    sx = {
        "& .MuiClock-clock":        {"backgroundColor": face},
        "& .MuiClockPointer-root":  {"backgroundColor": hand},
        "& .MuiClockPointer-thumb": {"backgroundColor": hand,
                                     "borderColor": hand},
        "& .MuiClock-pin":          {"backgroundColor": hand},
    }
    if num:                              # tint digits only when chosen
        sx["& .MuiClockNumber-root"] = {"color": num}
    echo = (face, hand, num) if is_reset else (no_update,) * 3
    return (sx, *echo)
'''

CODE["glass_layout"] = '''# A normal TimeClock, themed entirely from CSS via a className.
html.Div(
    TimeClock(id="lab-glass-clock", className="liquid-glass-clock",
              value="10:09:00", ampm=False,
              views=["hours", "minutes", "seconds"], showViewSwitcher=True),
    className="liquid-glass-stage",   # gradient backdrop for the frosted glass
)
'''

CODE["glass_css"] = '''/* assets/liquid_glass_clock.css  (excerpt) */

/* Frosted-glass face + animated halo */
.liquid-glass-clock .MuiClock-clock {
    background: linear-gradient(135deg,
        rgba(255,255,255,.55), rgba(255,255,255,.20)) !important;
    backdrop-filter: blur(14px) saturate(180%);
    box-shadow: 0 10px 36px rgba(31,38,135,.18),
                inset 0 1px 0 rgba(255,255,255,.9);
}

/* Magnifying-lens thumb — recentred on the digit (x:50%, y:-3px) */
.liquid-glass-clock .MuiClockPointer-thumb {
    box-sizing: border-box !important;
    width: 40px !important; height: 40px !important;
    left: calc(50% - 20px) !important; top: -23px !important;
    border: 1.5px solid rgba(255,255,255,.92) !important;
}

/* Bold + enlarge the digit the hand lands on */
.liquid-glass-clock .MuiClockNumber-selected {
    font-size: 1.5rem !important; font-weight: 900 !important;
}

[data-mantine-color-scheme="dark"] .liquid-glass-clock .MuiClock-clock { /* … */ }
'''

CODE["stopwatch_layout"] = '''dcc.Interval(id="lab-sw-interval", interval=1000, disabled=True)
dcc.Store(id="lab-sw-store", data={"elapsed": 0, "running": False})

TimeClock(id="lab-sw-clock", value="00:00:00", view="seconds",
          views=["hours", "minutes", "seconds"], readOnly=True)

dmc.Button("Start",   id="lab-sw-start",   color="green")
dmc.Button("Stop",    id="lab-sw-stop",    color="red")
dmc.Button("Restart", id="lab-sw-restart", color="gray")
'''

CODE["stopwatch_callback"] = '''@callback(
    Output("lab-sw-store", "data"), Output("lab-sw-interval", "disabled"),
    Output("lab-sw-clock", "value"), Output("lab-sw-clock", "view"),
    Output("lab-sw-readout", "children"),
    Input("lab-sw-interval", "n_intervals"),
    Input("lab-sw-start", "n_clicks"), Input("lab-sw-stop", "n_clicks"),
    Input("lab-sw-restart", "n_clicks"),
    State("lab-sw-store", "data"), prevent_initial_call=True,
)
def run_stopwatch(_tick, _a, _b, _c, store):
    elapsed, running = store["elapsed"], store["running"]
    t = ctx.triggered_id
    if   t == "lab-sw-start":                 running = True
    elif t == "lab-sw-stop":                  running = False
    elif t == "lab-sw-restart":               elapsed, running = 0, True
    elif t == "lab-sw-interval" and running:  elapsed += 1

    h, m, s = elapsed // 3600, elapsed % 3600 // 60, elapsed % 60
    # the view climbs with magnitude: seconds → minutes → hours
    view = "seconds" if elapsed < 60 else "minutes" if elapsed < 3600 else "hours"
    return ({"elapsed": elapsed, "running": running}, not running,
            f"{h % 24:02d}:{m:02d}:{s:02d}", view, f"{h:02d}:{m:02d}:{s:02d}")
'''

CODE["sync_note"] = '''# Two-way sync pattern (used by every pairing below):
#   • ONE @callback, with both components as Input AND Output.
#   • Branch on ctx.triggered_id to find the source.
#   • Return no_update for the source side → no feedback loop.
#   • to_hms() normalises ISO / "HH:mm" / "HH:mm:ss" to "HH:MM:SS".
'''

CODE["timeinput_callback"] = '''dmc.TimeInput(id="lab-ti-input", withSeconds=True, value="08:30:00")

@callback(
    Output("lab-ti-clock", "value"), Output("lab-ti-input", "value"),
    Input("lab-ti-clock", "value"),  Input("lab-ti-input", "value"),
    Input("lab-ti-reset", "n_clicks"), Input("lab-ti-now", "n_clicks"),
    Input("lab-ti-0900", "n_clicks"), Input("lab-ti-1730", "n_clicks"),
    prevent_initial_call=True,
)
def sync_timeinput(clock_value, input_value, *_btns):
    t = ctx.triggered_id
    if t in PRESETS:                       # Reset / Now / 09:00 / 17:30
        return PRESETS[t], PRESETS[t]
    if t == "lab-ti-clock":                # clock → input
        return no_update, to_hms(clock_value)
    return to_hms(input_value), no_update  # input → clock
'''

CODE["timepicker_callback"] = '''dmc.TimePicker(id="lab-tp-input", withSeconds=True,
               withDropdown=True, clearable=True, value="14:45:00")

@callback(
    Output("lab-tp-clock", "value"), Output("lab-tp-input", "value"),
    Input("lab-tp-clock", "value"),  Input("lab-tp-input", "value"),
    prevent_initial_call=True,
)
def sync_timepicker(clock_value, input_value):
    if ctx.triggered_id == "lab-tp-clock":
        return no_update, to_hms(clock_value)   # clock → picker
    return to_hms(input_value), no_update       # picker → clock
'''

CODE["timegrid_callback"] = '''# Preset half-hour slots: ["06:00", "06:30", … "22:00"]
dmc.TimeGrid(id="lab-tg", data=TG_DATA, value="09:00", format="12h",
             allowDeselect=True, w="100%",
             simpleGridProps={"cols": {"base": 4, "sm": 6, "md": 8}})

@callback(
    Output("lab-tg-clock", "value"), Output("lab-tg", "value"),
    Input("lab-tg-clock", "value"),  Input("lab-tg", "value"),
    prevent_initial_call=True,
)
def sync_timegrid(clock_value, grid_value):
    if ctx.triggered_id == "lab-tg":            # slot → clock
        return to_hms(grid_value), no_update
    h, m, _ = (int(x) for x in to_hms(clock_value).split(":"))
    slot = f"{h:02d}:{m:02d}" if m in (0, 30) and 6 <= h <= 22 else ""
    return no_update, slot                      # clock → highlight slot (or clear)
'''

CODE["datetime_callback"] = '''dmc.DateTimePicker(id="lab-dtp", withSeconds=True,
                   value=f"{date.today()}T12:00:00")

@callback(
    Output("lab-dtp-clock", "value"), Output("lab-dtp", "value"),
    Input("lab-dtp-clock", "value"),  Input("lab-dtp", "value"),
    State("lab-dtp", "value"), prevent_initial_call=True,
)
def sync_datetime(clock_value, dtp_value, dtp_state):
    if ctx.triggered_id == "lab-dtp-clock":     # clock drives the TIME part
        day = (dtp_state or "")[:10] or str(date.today())
        return no_update, f"{day}T{to_hms(clock_value)}"
    return to_hms(dtp_value), no_update          # datetime → clock
'''


# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #
layout = dmc.Container(
    [
        dcc.Store(id="lab-sw-store", data={"elapsed": 0, "running": False}),
        dcc.Interval(id="lab-sw-interval", interval=1000, disabled=True,
                     n_intervals=0),

        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Title("TimeClock Lab", order=1),
                        dmc.Badge("TimeClock × DMC", color="grape", variant="light"),
                    ],
                    align="center",
                ),
                dmc.Text(
                    "Deep-dive examples pairing the MUI TimeClock with "
                    "dash-mantine-components — live theming, a stopwatch, and "
                    "fully two-way-synced time inputs.",
                    c="dimmed",
                ),
            ],
            gap=4, mb="lg",
        ),

        # --- 1. Dynamic colours ---------------------------------------------
        lab_section(
            "mdi:palette-outline",
            "1. Dynamic colours (dmc.ColorPicker + dmc.ColorInput)",
            "Recolor the face, the hand/pointer, and the digit text independently "
            "— fed straight into the TimeClock sx prop (.MuiClock-clock, "
            ".MuiClockPointer-root, .MuiClockNumber-root). The face uses a "
            "ColorPicker with an alpha slider, so you can make it translucent "
            "(rgba). Leave “Numbers” empty to keep the digits theme-coloured.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-color-clock",
                            defaultValue="10:10:00",
                            views=["hours", "minutes", "seconds"],
                            showViewSwitcher=True,
                        )
                    ),
                    dmc.Stack(
                        [
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            DashIconify(icon="mdi:circle-opacity",
                                                        width=16),
                                            dmc.Text("Clock face (with opacity)",
                                                     size="sm", fw=500),
                                        ],
                                        gap=6,
                                    ),
                                    dmc.ColorPicker(
                                        id="lab-color-face",
                                        value="rgba(231, 245, 255, 0.9)",
                                        format="rgba",
                                        swatches=SWATCHES,
                                        swatchesPerRow=7,
                                        withPicker=True,
                                        w=240,
                                    ),
                                ],
                                gap=4,
                            ),
                            dmc.ColorInput(
                                id="lab-color-hand", label="Hand & pointer",
                                value="#228be6", format="hex", swatches=SWATCHES,
                                w=240,
                                leftSection=DashIconify(icon="mdi:clock-time-three-outline"),
                            ),
                            dmc.ColorInput(
                                id="lab-color-num", label="Numbers / digits",
                                value="", format="hex", swatches=SWATCHES,
                                w=240,
                                placeholder="Theme default",
                                leftSection=DashIconify(icon="mdi:numeric"),
                            ),
                            dmc.Button(
                                "Reset colours", id="lab-color-reset",
                                variant="subtle", size="xs", w=140,
                                leftSection=DashIconify(icon="mdi:restart"),
                            ),
                        ],
                        gap="md",
                    ),
                    code_panel([
                        ("layout.py", CODE["colors_layout"], "python"),
                        ("callback.py", CODE["colors_callback"], "python"),
                    ]),
                ],
                align="flex-start", gap="xl",
            ),
        ),

        # --- 2. Liquid glass clock ------------------------------------------
        lab_section(
            "mdi:blur",
            "2. Liquid glass clock",
            "An elevated, glassmorphic clock: a frosted liquid-glass face with an "
            "animated halo, and a pointer thumb shaped like a magnifying lens that "
            "enlarges the digit it lands on. Drag the hand and watch the lens "
            "travel. Fully light/dark-mode aware — toggle the theme to see it shift.",
            dmc.Group(
                [
                    html.Div(
                        TimeClock(
                            id="lab-glass-clock",
                            className="liquid-glass-clock",
                            value="10:09:00",
                            views=["hours", "minutes", "seconds"],
                            ampm=False,
                            showViewSwitcher=True,
                        ),
                        className="liquid-glass-stage",
                        style={"width": "fit-content"},
                    ),
                    dmc.Stack(
                        [
                            dmc.Text("Selected time", size="sm", c="dimmed"),
                            dmc.Title(id="lab-glass-readout", children="10:09:00",
                                      order=2, ff="monospace"),
                            dmc.Text(
                                "Face → frosted gradient + animated halo. "
                                "Thumb → magnifying lens (recentred & enlarged). "
                                "Selected digit → scaled up via font-size.",
                                size="xs", c="dimmed", maw=260,
                            ),
                        ],
                        gap="sm", justify="center",
                    ),
                ],
                align="center", gap="xl",
            ),
            view_code([
                ("layout.py", CODE["glass_layout"], "python"),
                ("liquid_glass_clock.css", CODE["glass_css"], "css"),
            ]),
        ),

        # --- 2. Stopwatch ---------------------------------------------------
        lab_section(
            "mdi:timer-outline",
            "3. Stopwatch (dcc.Interval)",
            "Start, stop, and restart a stopwatch. The clock view climbs with "
            "magnitude — seconds until 0:60, then minutes until 60:00, then hours.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-sw-clock",
                            value="00:00:00",
                            view="seconds",
                            views=["hours", "minutes", "seconds"],
                            readOnly=True,
                        )
                    ),
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    dmc.Text("Elapsed", size="sm", c="dimmed"),
                                    dmc.Badge(id="lab-sw-unit", children="seconds",
                                              variant="dot", color="teal"),
                                ],
                                gap="xs",
                            ),
                            dmc.Title(id="lab-sw-readout", children="00:00:00",
                                      order=1, ff="monospace"),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        "Start", id="lab-sw-start", color="green",
                                        leftSection=DashIconify(icon="mdi:play"),
                                    ),
                                    dmc.Button(
                                        "Stop", id="lab-sw-stop", color="red",
                                        variant="light",
                                        leftSection=DashIconify(icon="mdi:pause"),
                                    ),
                                    dmc.Button(
                                        "Restart", id="lab-sw-restart", color="gray",
                                        variant="outline",
                                        leftSection=DashIconify(icon="mdi:restart"),
                                    ),
                                ],
                                gap="xs",
                            ),
                        ],
                        gap="sm",
                    ),
                ],
                align="center", gap="xl",
            ),
            view_code([
                ("layout.py", CODE["stopwatch_layout"], "python"),
                ("callback.py", CODE["stopwatch_callback"], "python"),
            ]),
        ),

        # --- 3. TimeClock + TimeInput ---------------------------------------
        lab_section(
            "mdi:form-textbox",
            "4. Paired with dmc.TimeInput + reset",
            "Drag the clock or type in the native time input — they stay in sync. "
            "The buttons reset or jump the selected time.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-ti-clock", value="08:30:00",
                            views=["hours", "minutes", "seconds"],
                            showViewSwitcher=True,
                        )
                    ),
                    dmc.Stack(
                        [
                            dmc.TimeInput(
                                id="lab-ti-input", label="TimeInput (HH:MM:SS)",
                                withSeconds=True, value="08:30:00", w=220,
                                leftSection=DashIconify(icon="mdi:clock-outline"),
                            ),
                            dmc.Group(
                                [
                                    dmc.Button("Reset", id="lab-ti-reset",
                                               size="xs", variant="light",
                                               color="red"),
                                    dmc.Button("Now", id="lab-ti-now",
                                               size="xs", variant="light"),
                                    dmc.Button("09:00", id="lab-ti-0900",
                                               size="xs", variant="default"),
                                    dmc.Button("17:30", id="lab-ti-1730",
                                               size="xs", variant="default"),
                                ],
                                gap="xs",
                            ),
                            dmc.Code(id="lab-ti-out", children="—"),
                        ],
                        gap="sm",
                    ),
                ],
                align="flex-start", gap="xl",
            ),
            view_code([
                ("pattern.py", CODE["sync_note"], "python"),
                ("timeinput.py", CODE["timeinput_callback"], "python"),
            ]),
        ),

        # --- 4. TimeClock + TimePicker --------------------------------------
        lab_section(
            "mdi:clock-time-four-outline",
            "5. Paired with dmc.TimePicker",
            "A richer DMC time picker with a dropdown and seconds, kept in sync "
            "with the clock both ways.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-tp-clock", value="14:45:00",
                            views=["hours", "minutes", "seconds"],
                            showViewSwitcher=True,
                        )
                    ),
                    dmc.Stack(
                        [
                            dmc.TimePicker(
                                id="lab-tp-input", label="TimePicker",
                                withSeconds=True, withDropdown=True,
                                clearable=True, value="14:45:00", w=220,
                                leftSection=DashIconify(icon="mdi:clock-edit-outline"),
                            ),
                            dmc.Code(id="lab-tp-out", children="—"),
                        ],
                        gap="sm",
                    ),
                ],
                align="flex-start", gap="xl",
            ),
            view_code([
                ("timepicker.py", CODE["timepicker_callback"], "python"),
            ]),
        ),

        # --- 5. TimeClock + TimeGrid ----------------------------------------
        lab_section(
            "mdi:view-grid-outline",
            "6. Paired with dmc.TimeGrid",
            "Pick a preset half-hour slot, or drag the clock — when it lands on a "
            "slot the grid highlights it, otherwise the grid clears.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-tg-clock", value="09:00:00",
                            views=["hours", "minutes"],
                            showViewSwitcher=True,
                        )
                    ),
                    dmc.Code(id="lab-tg-out", children="—"),
                ],
                align="center", gap="xl", mb="md",
            ),
            dmc.TimeGrid(
                id="lab-tg",
                data=TG_DATA,
                value="09:00",
                withSeconds=False,
                allowDeselect=True,
                format="12h",
                w="100%",
                simpleGridProps={
                    "cols": {"base": 4, "xs": 5, "sm": 6, "md": 8},
                    "spacing": "xs",
                    "verticalSpacing": "xs",
                },
            ),
            view_code([
                ("timegrid.py", CODE["timegrid_callback"], "python"),
            ]),
        ),

        # --- 6. TimeClock + DateTimePicker ----------------------------------
        lab_section(
            "mdi:calendar-clock",
            "7. Paired with dmc.DateTimePicker",
            "The clock controls the time portion of a full datetime — the date "
            "you pick is preserved while the clock sets the hours/minutes/seconds.",
            dmc.Group(
                [
                    clock_paper(
                        TimeClock(
                            id="lab-dtp-clock", value="12:00:00",
                            views=["hours", "minutes", "seconds"],
                            showViewSwitcher=True,
                        )
                    ),
                    dmc.Stack(
                        [
                            dmc.DateTimePicker(
                                id="lab-dtp", label="DateTimePicker",
                                withSeconds=True,
                                valueFormat="DD MMM YYYY  HH:mm:ss",
                                value=f"{_TODAY}T12:00:00", w=260, clearable=True,
                                leftSection=DashIconify(icon="mdi:calendar-clock"),
                            ),
                            dmc.Code(id="lab-dtp-out", children="—"),
                        ],
                        gap="sm",
                    ),
                ],
                align="flex-start", gap="xl",
            ),
            view_code([
                ("datetime.py", CODE["datetime_callback"], "python"),
            ]),
        ),
    ],
    size="lg", px=0, py="md", className="dmc",
)


# --------------------------------------------------------------------------- #
# 1. Dynamic colours
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-color-clock", "sx"),
    Output("lab-color-face", "value"),
    Output("lab-color-hand", "value"),
    Output("lab-color-num", "value"),
    Input("lab-color-face", "value"),
    Input("lab-color-hand", "value"),
    Input("lab-color-num", "value"),
    Input("lab-color-reset", "n_clicks"),
)
def recolor_clock(face, hand, num, _reset):
    is_reset = ctx.triggered_id == "lab-color-reset"
    if is_reset:
        face, hand, num = "rgba(231, 245, 255, 0.9)", "#228be6", ""
    sx = {
        "& .MuiClock-clock": {"backgroundColor": face},
        "& .MuiClockPointer-root": {"backgroundColor": hand},
        "& .MuiClockPointer-thumb": {"backgroundColor": hand, "borderColor": hand},
        "& .MuiClock-pin": {"backgroundColor": hand},
    }
    if num:  # only tint the digits when a colour is chosen (else theme default)
        sx["& .MuiClockNumber-root"] = {"color": num}
    if is_reset:
        return sx, face, hand, num
    return sx, no_update, no_update, no_update


@callback(
    Output("lab-glass-readout", "children"),
    Input("lab-glass-clock", "value"),
    prevent_initial_call=True,
)
def glass_readout(value):
    return to_hms(value) or "—"


# --------------------------------------------------------------------------- #
# 2. Stopwatch
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-sw-store", "data"),
    Output("lab-sw-interval", "disabled"),
    Output("lab-sw-clock", "value"),
    Output("lab-sw-clock", "view"),
    Output("lab-sw-readout", "children"),
    Output("lab-sw-unit", "children"),
    Output("lab-sw-unit", "color"),
    Input("lab-sw-interval", "n_intervals"),
    Input("lab-sw-start", "n_clicks"),
    Input("lab-sw-stop", "n_clicks"),
    Input("lab-sw-restart", "n_clicks"),
    State("lab-sw-store", "data"),
    prevent_initial_call=True,
)
def run_stopwatch(_tick, _start, _stop, _restart, store):
    store = store or {"elapsed": 0, "running": False}
    elapsed = store.get("elapsed", 0)
    running = store.get("running", False)

    trigger = ctx.triggered_id
    if trigger == "lab-sw-start":
        running = True
    elif trigger == "lab-sw-stop":
        running = False
    elif trigger == "lab-sw-restart":
        elapsed, running = 0, True
    elif trigger == "lab-sw-interval" and running:
        elapsed += 1

    h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    clock_value = f"{h % 24:02d}:{m:02d}:{s:02d}"
    if elapsed < 60:
        view, unit, color = "seconds", "seconds", "teal"
    elif elapsed < 3600:
        view, unit, color = "minutes", "minutes", "blue"
    else:
        view, unit, color = "hours", "hours", "grape"

    readout = f"{h:02d}:{m:02d}:{s:02d}"
    new_store = {"elapsed": elapsed, "running": running}
    return new_store, (not running), clock_value, view, readout, unit, color


# --------------------------------------------------------------------------- #
# 3. TimeClock <-> TimeInput (+ reset / presets)
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-ti-clock", "value"),
    Output("lab-ti-input", "value"),
    Output("lab-ti-out", "children"),
    Input("lab-ti-clock", "value"),
    Input("lab-ti-input", "value"),
    Input("lab-ti-reset", "n_clicks"),
    Input("lab-ti-now", "n_clicks"),
    Input("lab-ti-0900", "n_clicks"),
    Input("lab-ti-1730", "n_clicks"),
    prevent_initial_call=True,
)
def sync_timeinput(clock_value, input_value, _r, _n, _09, _17):
    trigger = ctx.triggered_id
    presets = {
        "lab-ti-reset": "00:00:00",
        "lab-ti-now": _dt.datetime.now().strftime("%H:%M:%S"),
        "lab-ti-0900": "09:00:00",
        "lab-ti-1730": "17:30:00",
    }
    if trigger in presets:
        hms = presets[trigger]
        return hms, hms, f"set → {hms}"
    if trigger == "lab-ti-clock":
        hms = to_hms(clock_value)
        return no_update, hms, f"clock → {hms}"
    if trigger == "lab-ti-input":
        hms = to_hms(input_value)
        if hms is None:
            return no_update, no_update, "input cleared"
        return hms, no_update, f"input → {hms}"
    return no_update, no_update, no_update


# --------------------------------------------------------------------------- #
# 4. TimeClock <-> TimePicker
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-tp-clock", "value"),
    Output("lab-tp-input", "value"),
    Output("lab-tp-out", "children"),
    Input("lab-tp-clock", "value"),
    Input("lab-tp-input", "value"),
    prevent_initial_call=True,
)
def sync_timepicker(clock_value, input_value):
    trigger = ctx.triggered_id
    if trigger == "lab-tp-clock":
        hms = to_hms(clock_value)
        return no_update, hms, f"clock → {hms}"
    hms = to_hms(input_value)
    if hms is None:
        return no_update, no_update, "picker cleared"
    return hms, no_update, f"picker → {hms}"


# --------------------------------------------------------------------------- #
# 5. TimeClock <-> TimeGrid (preset slots)
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-tg-clock", "value"),
    Output("lab-tg", "value"),
    Output("lab-tg-out", "children"),
    Input("lab-tg-clock", "value"),
    Input("lab-tg", "value"),
    prevent_initial_call=True,
)
def sync_timegrid(clock_value, grid_value):
    trigger = ctx.triggered_id
    if trigger == "lab-tg":
        hms = to_hms(grid_value)
        if hms is None:
            return no_update, no_update, "grid deselected"
        return hms, no_update, f"grid → {hms}"
    # clock changed: highlight a slot only when it lands on :00 / :30 in range
    hms = to_hms(clock_value)
    if hms is None:
        return no_update, no_update, no_update
    h, m, _s = (int(x) for x in hms.split(":"))
    if m in (0, 30) and 6 <= h <= 22:
        slot = f"{h:02d}:{m:02d}"
        return no_update, slot, f"clock → slot {slot}"
    return no_update, "", f"clock → {hms} (no slot)"


# --------------------------------------------------------------------------- #
# 6. TimeClock <-> DateTimePicker (clock drives the time portion)
# --------------------------------------------------------------------------- #
@callback(
    Output("lab-dtp-clock", "value"),
    Output("lab-dtp", "value"),
    Output("lab-dtp-out", "children"),
    Input("lab-dtp-clock", "value"),
    Input("lab-dtp", "value"),
    State("lab-dtp", "value"),
    prevent_initial_call=True,
)
def sync_datetime(clock_value, dtp_value, dtp_state):
    trigger = ctx.triggered_id
    if trigger == "lab-dtp-clock":
        hms = to_hms(clock_value)
        if hms is None:
            return no_update, no_update, no_update
        day = date_part(dtp_state)
        new_dt = f"{day}T{hms}"
        return no_update, new_dt, f"clock → {new_dt}"
    # DateTimePicker changed: pull its time onto the clock
    hms = to_hms(dtp_value)
    if hms is None:
        return no_update, no_update, "datetime cleared"
    return hms, no_update, f"datetime → {dtp_value}"
