<!--
  Scheduler + TimeClock port plan for dash_mui_charts.
  Generated 2026-06-04 from a fan-out research pass over the official MUI X
  Scheduler + date-pickers docs (17/18 doc/API pages extracted), grounded in
  this repo's verified conventions and live npm compatibility checks.
  TimeClock (Section 2) is already SHIPPED. Sections 3-8 are the forward plan.
-->

# Implementation Plan: Porting MUI X Scheduler + TimeClock into `dash_mui_charts`

Build-ready plan grounded in the repo's verified conventions (functional React components with `setProps`, auto-generated `.py` wrappers via `dash-generate-components`, `LicenseInfo`-gated Pro components, Mantine-color-scheme `MutationObserver` dark mode, demo pages + `NAV_ITEMS`). TimeClock already exists (`src/lib/components/TimeClock.react.js`, registered in `index.js`, demo at `pages/time_clock.py`); it is the working template for the string↔dayjs boundary.

---

## 1. Compatibility & the gating decision

### The dependency reality

| Family | Current library (X v8 / Material v6) | Scheduler requires |
|---|---|---|
| `@mui/material` | `^6.5.0` | `^7.3.0` |
| `@mui/icons-material` | `^6.5.0` | `^7.3.0` |
| `@mui/system` | `7.3.7` (already v7) | `^7.3.0` ✅ |
| MUI X core | `@mui/x-charts@8.24`, `x-tree-view@8.27`, `x-date-pickers@8.24` (v8) | `@mui/x-internals@^9.1`, `x-tree-view@^9.4`, `@mui/utils@9.0.1` (v9) |
| Base UI | none | `@base-ui/react@^1.5.0` (NEW) |
| License | `@mui/x-license@^7.24` | `@mui/x-license@^9.4` (Premium) |
| Status | stable | `@mui/x-scheduler@9.0.0-beta.0` (Preview, API may shift) |

### The unifying move

X v8 (charts, tree-view, date-pickers) **all declare peer support for `@mui/material@^7.0.0`**. `@mui/system` is already 7.3.7. So **bumping `@mui/material` 6→7 + `@mui/icons-material` 6→7 is non-breaking for the existing 12 components** and is the single uplift that unblocks the scheduler family. MUI X v8 (charts) and X v9 (scheduler) coexist as nested deps — webpack will resolve two copies, which is functionally fine but has two costs:

1. **Dual `@mui/x-license` singletons.** Charts/tree-view/date-pickers use `@mui/x-license@7`; the scheduler-premium uses `@mui/x-license@9`. `LicenseInfo.setLicenseKey()` must be called against **both** singletons. The React component must import from the matching version (`import { LicenseInfo } from '@mui/x-license'` resolves per-package via node_modules nesting). Concretely: the scheduler React file calls the v9 `LicenseInfo`; existing Pro charts/tree keep calling the v7 `LicenseInfo`. The same license string is set on both.
2. **Bundle size.** Two MUI X cores + Base UI + scheduler internals. Webpack `externals` already excludes react/react-dom/plotly/prop-types only — MUI is bundled. Estimate **+450–700 KB minified** (scheduler + x-internals v9 + base-ui + virtualizer for premium). Mitigate with import-path tree-shaking (`@mui/x-scheduler/event-calendar`, not barrel) and shipping premium as a separate registered component so community users don't pull `@mui/x-scheduler-premium` + `x-virtualizer`.

### Options

| Option | What | Pros | Cons | Recommendation |
|---|---|---|---|---|
| **A — Full uplift** | Bump material/icons 6→7 globally, add `@mui/x-scheduler@9` (+ premium), add `@base-ui/react`. All 13 existing components + new scheduler share material v7. | One material version, cleanest long-term, no duplicate `@mui/material`. | Regression surface across all 12 chart/tree components (material v6→v7 visual + API deltas: Grid v2 default, removed deprecated APIs, sx/styled changes). Beta scheduler in production tree. | **Chosen.** Material v6→v7 is low-risk here (components use `createTheme`+`ThemeProvider`+`sx`, the stable surface). Do it behind a feature branch with the full demo-page smoke test. |
| **B — Isolate scheduler** | Keep material v6 for charts; load scheduler in an isolated bundle pinning a nested `@mui/material@7`. | Existing components untouched. | Two `@mui/material` copies → two emotion caches, doubled theme context, ThemeProvider mismatch across the page, ~1MB+ bundle, brittle. Emotion style insertion order bugs. | Reject — emotion/material duplication is a known footgun. |
| **C — Defer scheduler, ship TimeClock now** | Ship TimeClock (already built, zero new deps) this release; gate scheduler until `@mui/x-scheduler` exits beta and (ideally) declares material v8 peer compat. | Zero risk now; scheduler API stabilizes. | No calendar until GA. | **Adopt as the phasing for the scheduler portion** — ship TimeClock in the current release; do the material v7 uplift + EventCalendar in the next minor, flagged "Preview". |

**Net decision:** Option A's dependency posture, executed on Option C's timeline. Ship TimeClock now. Land the material v7 + scheduler work on a `feat/scheduler` branch, validated against every demo page, released as a clearly-labeled **Preview** minor.

---

## 2. TimeClock — confirmed unblocked

Already built on `@mui/x-date-pickers@8.24.0` + `dayjs` (`AdapterDayjs`), peer-compatible with material v6 **and** v7 (no change needed at uplift). Existing file: `src/lib/components/TimeClock.react.js`, registered in `index.js`, demo `pages/time_clock.py` (`/time-clock`). **No work required beyond a NAV entry** (see §7). For completeness, the shipped Dash prop surface:

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (ISO `"2022-04-17T15:30:00"` or time-only `"15:30"`/`"15:30:45"`) | — | Controlled value; **also OUTPUT** (full wall-time ISO on change). |
| `defaultValue` | `string` | — | Uncontrolled initial value, same formats. |
| `views` | `['hours','minutes','seconds']` subset | `['hours','minutes']` | Views to render, in order. |
| `view` | `'hours'\|'minutes'\|'seconds'` | — | Controlled visible view; **also OUTPUT**. |
| `openTo` | same enum | — | View to open first (uncontrolled). |
| `ampm` | `bool` | (locale) | Force 12h/24h. |
| `disabled` | `bool` | `false` | Disable clock. |
| `readOnly` | `bool` | `false` | Read-only. |
| `autoFocus` | `bool` | `false` | Focus on mount. |
| `minutesStep` | `number` | — | Step between selectable minutes. |
| `minTime` / `maxTime` | `string` | — | Bounds (ISO or time-only). |
| `disableFuture` / `disablePast` | `bool` | `false` | Disable future/past relative to now. |
| `disableIgnoringDatePartForTimeValidation` | `bool` | `false` | Include date part in min/max comparison. |
| `skipDisabled` | `bool` | `false` | Skip disabled times when picking default. |
| `showViewSwitcher` | `bool` | `false` | Show view-switch arrows. |
| `className` | `string` | — | Class on wrapping div. |
| `sx` | `object` | — | MUI sx (object form only). |
| **`timeData`** (OUTPUT) | `exact({hours,minutes,seconds,formatted,event_timestamp})` | — | Parsed convenience output on every change. |

**Serialization boundary:** `parseToDayjs()` maps strings → dayjs in; `newVal.format('YYYY-MM-DDTHH:mm:ss')` maps dayjs → string out. `minTime`/`maxTime` parse the same way.

**Function-only MUI props omitted:** `shouldDisableTime`, `shouldDisableClock`, `referenceDate` (function/Date), `slots`/`slotProps`, `onError`. These take JS functions/Date objects and are not serializable — omit (or, if demanded later, expose via a `window.dashMuiChartsFunctions` registry like the charts' `valueFormatter`).

---

## 3. EventCalendar (community) — `MuiEventCalendar` Dash component

New file `src/lib/components/MuiEventCalendar.react.js`. Imports: `import { EventCalendar } from '@mui/x-scheduler/event-calendar'`. Same dark-mode `useMantineColorScheme` hook + `ThemeProvider` as TimeClock/TreeViewPro. Wrap in a sized `<div id={id} className={className} style={{height, width:'100%'}}>` (MUI fills the container; demos use `height:600`).

> **Date boundary:** the scheduler accepts **ISO 8601 strings** for `start`/`end`/`visibleDate` (verified from live demos — the React layer converts to its internal adapter, Luxon `DateTime`, on the JS side). So Dash passes ISO strings throughout; the wrapper converts `visibleDate` string → adapter DateTime before passing, and serializes the change event's DateTime → ISO string before `setProps`. Event objects are passed through verbatim (already ISO-string dates).

### 3a. Events

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `events` | `array<SchedulerEvent>` | `[]` | Events to render; **INPUT + OUTPUT** (round-trips on create/edit/move/resize/delete via internal `onEventsChange`). |
| `eventColor` | `oneOf(9 palette names)` | `'teal'` | Component-level fallback color (lowest priority in resolution). |
| `eventCreation` | `oneOfType([bool, exact({duration:number, interaction:oneOf(['click','double-click'])})])` | `true` | `false` disables creation; object configures default duration (minutes) + click/double-click. |

### 3b. Resources

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `resources` | `array<SchedulerResource>` | — | Resources events can link to (supports nested `children`). |
| `visibleResources` | `object` (Record<id,bool>) | — | Controlled visibility; **INPUT + OUTPUT**. Visible if absent or `true`. |
| `defaultVisibleResources` | `object` | `{}` | Uncontrolled initial visibility. |
| `shouldEventRequireResource` | `bool` | `false` | Require a resource on each event (hides "No resource"). |

### 3c. Views

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `views` | `arrayOf(oneOf(['day','week','month','agenda']))` | `['day','week','month','agenda']` | Which view buttons are offered. |
| `view` | `oneOf(['day','week','month','agenda'])` | — | Controlled active view; **INPUT + OUTPUT**. |
| `defaultView` | same enum | `'week'` | Uncontrolled initial view. |

### 3d. Navigation / visible date

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `visibleDate` | `string` (ISO) | — | Controlled visible date; **INPUT + OUTPUT**. Wrapper converts string↔DateTime. |
| `defaultVisibleDate` | `string` (ISO) | today | Uncontrolled initial visible date. |
| `goToDate` | `string` (ISO) | — | **Imperative replacement for `apiRef.setVisibleDate`** — a write-only trigger: when set, the wrapper navigates and clears it. (`apiRef` is non-serializable; we expose navigation via the controlled `visibleDate` + this trigger prop.) |

### 3e. Drag / resize

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `areEventsDraggable` | `bool` | `true` | Allow drag-to-reschedule (per-event/per-resource overrides win). |
| `areEventsResizable` | `oneOfType([bool, oneOf(['start','end'])])` | `true` | Resize behavior. |
| `canDragEventsFromTheOutside` | `bool` | `false` | Allow external `StandaloneEvent` drops in. |
| `canDropEventsToTheOutside` | `bool` | `false` | Allow dragging events out. |

### 3f. Editing

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `readOnly` | `bool` | `false` | Global read-only (disables create/drag/resize/dialog editing). Per-event `readOnly` and per-resource `areEventsReadOnly` override. |

### 3g. Preferences

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `preferences` | `exact({ampm, isSidePanelOpen, showEmptyDaysInAgenda, showWeekends, showWeekNumber, weekStartsOn})` (all optional) | — | Controlled prefs; **INPUT + OUTPUT**. |
| `defaultPreferences` | same shape | `{showWeekends:true, showWeekNumber:false, isSidePanelOpen:true, showEmptyDaysInAgenda:true, ampm:true}` | Uncontrolled initial prefs. `weekStartsOn` 0=Sun..6=Sat. |
| `preferencesMenuConfig` | `oneOfType([oneOf([false]), exact({toggleAmpm, toggleWeekStartsOn, toggleWeekendVisibility, toggleWeekNumberVisibility, toggleEmptyDaysInAgenda})])` | — | `false` hides menu; object toggles items. |

### 3h. Localization / timezone

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `displayTimezone` | `string` | `'default'` | IANA name, or `'default'`/`'locale'`/`'UTC'`. Render-only. |
| `localeText` | `object` (string→string) | — | UI label overrides. **Only string-valued keys accepted** (the ~10 function keys, e.g. `hiddenEvents`, `recurrenceMonthlyPresetLabel`, are recurrence/plural formatters — dropped or resolved from a JS registry; see flags below). |
| `dateLocale` | `string` (locale code, e.g. `'fr'`) | `'enUS'` | Wrapper maps a string code → the date-fns/Luxon locale object on the JS side via a small `{code: localeObj}` lookup. |
| `showCurrentTimeIndicator` | `bool` | `true` | Current-time line in time views. |

### 3i. Theming

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Class on wrapping div. |
| `sx` | `object` | — | MUI sx (object form only). |
| `height` | `number\|string` | `600` | Height of the wrapping container (component fills it). |

### Callback → Dash output mapping (controlled-prop write-back pattern)

| MUI callback | Signature | Dash realization |
|---|---|---|
| `onEventsChange(newEvents)` | `(SchedulerEvent[]) => void` | `setProps({events: newEvents, lastAction: {...}})` — `events` is in+out. |
| `onViewChange(view)` | `(string) => void` | `setProps({view})`. |
| `onVisibleDateChange(dt)` | `(DateTime, ev?) => void` | `setProps({visibleDate: dt.toISO()})`. |
| `onVisibleResourcesChange(map)` | `(Record<string,bool>) => void` | `setProps({visibleResources: map})`. |
| `onPreferencesChange(prefs)` | `(Partial<Prefs>) => void` | `setProps({preferences: prefs})`. |

### Function-only MUI props — flagged + Dash alternative

| MUI prop | Why unserializable | Dash-friendly alternative |
|---|---|---|
| `apiRef` (`useEventCalendarApiRef`) | React ref / imperative methods | Controlled `visibleDate` + write-only `goToDate` trigger prop. |
| `dataSource` `{getEvents, persistEvents}` | JS functions (lazy loading) | Use `events` + `onEventsChange` round-trip (Phase 1). Lazy loading is a Premium concern (§4). |
| `eventModelStructure` `{field:{getter,setter}}` | JS getter/setter | **Drop.** Require canonical field names. Optionally accept a simple `{canonicalField: 'customKey'}` **string→string** remap dict and build getters client-side. |
| `resourceModelStructure` `{field:{getter}}` | JS getter | Same: drop, or accept string→string remap and synthesize getters in the wrapper. |
| `dateLocale` (date-fns/Luxon object) | non-serializable object | `dateLocale` string code → object lookup on JS side. |
| `localeText` function keys | JS `(arg)=>string` formatters | Accept only string keys; ignore/strip function keys (or resolve from `window.dashMuiChartsFunctions`). |
| `sx` function form | JS function | Object form only. |
| `classes` | (serializable, but 200+ rules) | Pass through `sx` + `className` instead; defer `classes`. |

### Dash-friendly data models

**SchedulerEvent (dict):**
```python
{
  "id": "1",                      # str|int, required
  "title": "Team Meeting",        # str, required
  "start": "2024-01-15T10:00:00", # ISO string, required
  "end":   "2024-01-15T11:00:00", # ISO string, required
  "resource": "team-a",           # str|int, optional (resource.id)
  "allDay": False,                # bool, optional
  "timezone": "America/New_York", # IANA str, optional
  "color": "blue",                # oneOf 9 palette, optional (highest priority)
  "className": "highlighted",     # str, optional
  "draggable": True,              # bool, optional per-event override
  "resizable": "end",             # bool|'start'|'end', optional
  "readOnly": False,              # bool, optional (highest priority)
  # "rrule": "FREQ=WEEKLY;..."    # PREMIUM only (§4)
  # "description": "..."          # str, dialog General tab
}
```

**SchedulerResource (dict):**
```python
{
  "id": "team-a",                 # str|int, required
  "title": "Team A",              # str, required (canonical; map 'name'->title in Python)
  "eventColor": "pink",           # oneOf 9, optional
  "children": [ {...} ],          # nested resources, optional
  "areEventsDraggable": False,    # bool, optional
  "areEventsResizable": "start",  # bool|'start'|'end', optional
  "areEventsReadOnly": True,      # bool, optional (inherited by descendants)
}
```
Palette enum (9, default `teal`): `purple, teal, lime, orange, green, pink, indigo, amber, blue` *(the API-page list of 11 includes `grey`+`red`; the events/resources guide pages enumerate 9 — declare PropTypes against the 9 guide-confirmed names plus `grey`,`red` to be safe).*

---

## 4. EventCalendarPremium additions

New file `src/lib/components/MuiEventCalendarPremium.react.js` (or a `premium` boolean branch inside the community file selecting `EventCalendarPremium` from `@mui/x-scheduler/event-calendar-premium`). All community props/models apply. Adds:

| Feature | Dash surface |
|---|---|
| **Recurrence** | `event.rrule` accepted as **RRULE string** (`"FREQ=WEEKLY;INTERVAL=2;BYDAY=TH"`) or object form `{freq, interval, byDay, byMonthDay, count, until}`. Both are plain-serializable — pass through verbatim. Recurrence tab appears in the dialog. |
| **Exception dates** | Per-event exception list (RRULE `EXDATE`-style); pass through as part of the event dict per the premium event model. |
| **DST-aware recurrence** | Automatic in the premium engine; no Dash prop. |
| **Lazy loading / `dataSource`** | Function-valued (`getEvents`/`persistEvents`) — **not portable directly**. Dash alternative: keep `events`+`onEventsChange`, or expose `loadRange` output `{start, end}` (window the user scrolled to) + `events` input so Python can fetch and feed back. Defer to Phase 3+. |
| **`licenseKey`** | `licenseKey: PropTypes.string`. Module-level `let licenseKeySet = false;` gate; on render: `if (licenseKey && !licenseKeySet) { LicenseInfo.setLicenseKey(licenseKey); licenseKeySet = true; }` — using the **v9** `@mui/x-license` (`@mui/x-scheduler-premium` peer). Mirrors `TreeViewPro.react.js` lines 498–500, but against the v9 singleton. |

---

## 5. EventTimelinePremium Dash component

New file `src/lib/components/MuiEventTimeline.react.js`. Import: `import { EventTimelinePremium } from '@mui/x-scheduler-premium/event-timeline-premium'` (note the **distinct package** `@mui/x-scheduler-premium`). Premium-only; `licenseKey` gated like §4. Resource-row Gantt-style timeline (events placed on `resource` rows; demos use `height:400`).

| Dash prop | Type | Default | Description |
|---|---|---|---|
| `events` | `array<SchedulerEvent>` | `[]` | Allocation bars; each needs `resource`. **IN + OUT** via `onEventsChange`. |
| `resources` | `array<SchedulerResource>` | — | Resource rows. |
| `defaultVisibleDate` / `visibleDate` | `string` (ISO) | today | Timeline window center; `visibleDate` IN+OUT. |
| `units` / `zoom` | `string` enum (e.g. `'day'`, `'week'`, `'monthAndYear'`) | — | Timeline granularity/zoom (confirm exact enum against `/x/api/scheduler/event-timeline-premium/` during build — page was beyond the captured extraction). |
| `areEventsDraggable` / `areEventsResizable` | `bool` / union | `true` | Reschedule/resize allocations on the timeline. |
| `readOnly` | `bool` | `false` | Read-only timeline. |
| `licenseKey` | `string` | `''` | Premium license (v9 `LicenseInfo`). |
| `height` | `number\|string` | `400` | Container height. |
| `className` / `sx` | `string` / `object` | — | Styling. |

Callback mapping identical to §3: `onEventsChange → events`, `onVisibleDateChange → visibleDate`. **Build note:** the timeline API table was not in the captured docs — fetch `/x/api/scheduler/event-timeline-premium/` at build time to finalize the `units`/`zoom` enum and any timeline-specific props before locking PropTypes.

---

## 6. Serialization & callbacks design

**Contract (all scheduler components):**

1. **Events round-trip.** `events` is both Input and Output. Internal handler:
   ```js
   const handleEventsChange = useCallback((newEvents) => {
     if (!setProps) return;
     const prev = eventsRef.current;          // ref tracking last events
     const action = diffEvents(prev, newEvents); // classify the change
     setProps({ events: newEvents, lastAction: { ...action, event_timestamp: Date.now() }});
   }, [setProps]);
   ```
2. **`event_timestamp` pattern.** Every output object carries `event_timestamp: Date.now()` (matches the existing `TimeClock.timeData.event_timestamp` convention) so Dash callbacks can dedupe and order, and use it as the `Input` that fires.
3. **`lastAction` output** (OUTPUT-only convenience):
   ```python
   {
     "type": "create" | "update" | "delete" | "move" | "resize",
     "event": { ...the affected SchedulerEvent... },  # null for ambiguous bulk
     "event_timestamp": 1718000000000
   }
   ```
   Derived in the wrapper by diffing previous vs. new `events` (added → `create`; removed → `delete`; same id, changed start/end with equal duration → `move`; changed duration → `resize`; other field change → `update`). This gives Python a precise signal without diffing the full array server-side.
4. **Controlled write-backs** for `view`, `visibleDate` (ISO string), `visibleResources`, `preferences` — each its own `setProps` key, each usable as a Dash `Input`.
5. **Date conversion** lives entirely in the React layer: ISO string in → adapter DateTime; DateTime out → `.toISO()`. Python never sees a non-string date.

PropTypes for outputs use `PropTypes.exact({...})` (as TimeClock does for `timeData`) so the auto-generated wrapper documents them.

---

## 7. File-by-file work plan

### New React files
- `src/lib/components/MuiEventCalendar.react.js` — community calendar (§3).
- `src/lib/components/MuiEventCalendarPremium.react.js` — premium calendar (§4) *(or a `premium` branch in the above; separate file keeps community bundle lean and is the safer split for tree-shaking)*.
- `src/lib/components/MuiEventTimeline.react.js` — premium timeline (§5).
- *(Optional Phase 3)* `src/lib/components/SchedulerStandaloneEvent.react.js` — for external drag-and-drop (`StandaloneEvent`).

Each follows the TimeClock template: `useMantineColorScheme` MutationObserver hook, `light/darkTheme = createTheme({palette:{mode}})`, `ThemeProvider` wrap, `defaultProps`, JSDoc-annotated `PropTypes`, `export default`.

### `src/lib/index.js` edits
Add imports + exports for `MuiEventCalendar`, `MuiEventCalendarPremium`, `MuiEventTimeline` (and `TimeClock` is already present).

### `package.json` dependency changes
```jsonc
"@mui/material": "^7.3.0",            // 6.5.0 -> 7
"@mui/icons-material": "^7.3.0",     // 6.5.0 -> 7
"@mui/system": "^7.3.7",             // pin (already present transitively)
"@base-ui/react": "^1.5.0",          // NEW (scheduler peer)
"@mui/x-scheduler": "9.0.0-beta.0",  // community calendar (pin exact — beta)
"@mui/x-scheduler-premium": "9.0.0-beta.0", // premium calendar + timeline (pin exact)
"@mui/x-license": "^9.4.0"           // bump 7 -> 9 for scheduler-premium; v7 still resolves nested for charts
```
Keep `@mui/x-charts@^8.24`, `@mui/x-charts-pro@^8.24`, `@mui/x-tree-view@^8.27`, `@mui/x-tree-view-pro@^8.27`, `@mui/x-date-pickers@8.24.0`, `dayjs@1.11.13` unchanged. Run `npm install`, confirm webpack resolves both x-license copies (charts→v7, scheduler→v9).

### Demo pages (`pages/`) — `dash.register_page` + `layout` + `@callback`
- `pages/time_clock.py` — exists (`/time-clock`); just add NAV entry.
- `pages/scheduler_calendar.py` (`/scheduler`) — sections: Basic events; Views (`day/week/month/agenda`); Controlled view + visibleDate (Dash `dcc.Store`/buttons driving `view`/`goToDate`); Resources + visibility toggles; Drag/resize toggles; Editing/read-only; Preferences + `preferencesMenuConfig`; Timezone (`displayTimezone`); `lastAction` live readout. Use `dmc` helpers like `pages/time_clock.py`'s `demo_item`/`section`.
- `pages/scheduler_premium.py` (`/scheduler-premium`) — recurrence (`rrule` string + object), exception dates, `licenseKey` from env.
- `pages/scheduler_timeline.py` (`/scheduler-timeline`) — resource rows, allocation bars, `units`/`zoom`.

### `app.py` `NAV_ITEMS` additions
Add after the TreeView group:
```python
{"itemId": "group-scheduler", "label": "Scheduler", "icon": "CalendarMonth", "children": [
    {"itemId": "/scheduler", "label": "Event Calendar", "icon": "PlayArrow"},
    {"itemId": "/scheduler-premium", "label": "Recurrence (Pro)", "icon": "Diamond"},
    {"itemId": "/scheduler-timeline", "label": "Timeline (Pro)", "icon": "ViewTimeline"},
]},
{"itemId": "group-timeclock", "label": "TimeClock", "icon": "Schedule", "children": [
    {"itemId": "/time-clock", "label": "Examples", "icon": "PlayArrow"},
]},
```
(`ALL_GROUP_IDS` derives automatically from the `group-` prefix.)

### Build / validation steps
1. `npm install` (after package.json edits).
2. `npm run build` (= `webpack --mode production` + `dash-generate-components ./src/lib/components dash_mui_charts`). Confirm `dash_mui_charts/MuiEventCalendar.py` etc. auto-generate — **do not hand-write**.
3. `python _validate_init.py` (the repo's `validate-init` script).
4. `python app.py` — smoke-test **every** demo page (charts + tree + new scheduler) for material v6→v7 regressions.
5. Verify dark mode (toggle Mantine color scheme) re-skins calendar.
6. Verify events round-trip + `lastAction` via a console-printing callback.

### Phased rollout
- **Phase 1 (release now):** TimeClock NAV entry only — zero new deps, ships immediately.
- **Phase 2 (`feat/scheduler` branch, next minor, "Preview"):** material/icons 6→7 uplift + `@base-ui/react` + `@mui/x-scheduler` → `MuiEventCalendar` community + `/scheduler` demo. Full demo-page regression pass is the gate.
- **Phase 3:** `@mui/x-scheduler-premium` → `MuiEventCalendarPremium` (recurrence) + `licenseKey` wiring + `/scheduler-premium`.
- **Phase 4:** `MuiEventTimeline` (`EventTimelinePremium`) + `/scheduler-timeline`; optional `StandaloneEvent` for external DnD + lazy-loading `loadRange` pattern.

---

## 8. Risks & open questions

1. **Beta API churn.** `@mui/x-scheduler@9.0.0-beta.0` is Preview; prop names/event signatures may change pre-GA. **Mitigation:** pin exact `9.0.0-beta.0` (no `^`), label the demo pages "Preview," and isolate the scheduler React files so a breaking bump is a contained edit. The Quickstart "API" section is literally a `TODO` placeholder — the only authoritative prop table is `/x/api/scheduler/event-calendar/` (captured here); re-verify before each dependency bump.
2. **Material v6→v7 regression surface across 12 existing components.** v7 changes: Grid v2 becomes default, removal of deprecated APIs, `styled`/`sx` internals, possible visual deltas. **Mitigation:** components here use the stable `createTheme`+`ThemeProvider`+`sx` surface (low blast radius), but a full manual smoke test of every `pages/*.py` is mandatory before merge. Watch for `@mui/x-charts@8` runtime warnings under material v7 (peer-declared, but verify zoom/brush Pro paths).
3. **Dual `@mui/x-license` singletons.** Charts/tree (v7) and scheduler-premium (v9) are separate singletons — the same key must be set on both. **Risk:** a user setting only the chart license sees a scheduler watermark (and vice-versa). **Mitigation:** document that `licenseKey` must be passed to each Pro component; each component sets its own version's `LicenseInfo`.
4. **Base UI vs Mantine/MUI theming interop.** `@mui/x-scheduler@9` introduces `@base-ui/react` (a new, non-emotion styling primitive). Its theming may not respond to the MUI `ThemeProvider` dark mode the way charts/tree do — **dark mode for the calendar may need Base UI-specific CSS-variable theming, not just `createTheme({palette:{mode}})`**. Open question: does `EventCalendar` honor the MUI theme `mode`, or does it need `data-` attribute / CSS-var theming? Verify during Phase 2; may require targeting `.MuiEventCalendar-*` CSS vars via `sx`.
5. **Bundle size.** Two MUI X cores (v8 + v9) + Base UI + scheduler internals + (premium) `x-virtualizer`. Estimate **+450–700 KB min**. **Mitigation:** subpath imports (`@mui/x-scheduler/event-calendar`), keep premium in a separate registered component, consider webpack analysis post-build. If unacceptable, fall back to Option C (defer scheduler) until GA reduces the footprint.
6. **EventTimeline API gap.** The `/x/api/scheduler/event-timeline-premium/` prop table was not in the captured extraction — `units`/`zoom` enum (`monthAndYear`, etc.) and timeline-specific props must be fetched and confirmed before locking §5 PropTypes.
7. **`localeText` function keys + `dateLocale` object.** ~10 `localeText` keys are formatter functions and the `dateLocale` is a non-serializable object; the string-only / locale-code-lookup approach covers most needs but loses recurrence/plural label customization unless a `window.dashMuiChartsFunctions` registry is added later.

**Key files referenced:** `src/lib/components/TimeClock.react.js` (boundary template), `src/lib/components/TreeViewPro.react.js` (license + dark-mode template, lines 35, 444, 498–500), `src/lib/index.js` (registration), `app.py` (`NAV_ITEMS`, lines 60–119), `pages/time_clock.py` (demo template), `package.json` (deps/scripts).
