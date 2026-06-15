# dash-mantine-components — tips & tricks (project reference)

Index + project-actionable distillation of the DMC docs excerpts in this folder.
These are patterns that **recur** in SailsBoard work — reach for the relevant file
when the situation below comes up, and apply the "use it here" hook.

> **Version awareness.** The excerpts are from the **DMC v2.7.0** docs, built on
> **Mantine v8** — *"do not use Mantine v9 docs for API reference."* SailsBoard pins
> **`dash-mantine-components==2.4.0`** (`requirements.txt`). Function-props additions
> are versioned (v2.0 / v2.1 / v2.4 tables in `functions_as_props.md`); everything
> tagged **≤ v2.4.0 is available to us**, v2.7-only props are not until we bump DMC.
> When in doubt, check the prop exists on 2.4.0 before relying on it.

---

## Index

| file | covers | reach for it when… |
|---|---|---|
| `dash_4_components.md` | theming **Dash 4 core components** (`dcc.Dropdown`, `dcc.Slider`) to match the Mantine theme via CSS variables + dark mode | you mix a `dcc.*` component into a DMC form/grid and it looks off-theme or doesn't follow dark mode |
| `functions_as_props.md` | passing **JS function references** to DMC props (`{"function": "name"}` + `window.dashMantineFunctions`) — formatters, `renderOption`, chart `valueFormatter`, returning components | you need a chart `$`/unit formatter, a custom `Select` option, a slider label, or any prop Mantine expects as a function |
| `debounce_prop.md` | the **`debounce`** prop on DMC inputs (`True` / `False` / `<ms>`) + supported components | a search/filter input fires a callback on every keystroke, or you only want the final value on blur |
| `persistence_props.md` | DMC **persistence** (`persistence`, `persisted_props`, `persistence_type`) + the single-component-layout gotcha | you want an input value to survive reload/tab without a callback — **but mind the `storage_type` lesson (below)** |
| `dash_loading_states.md` | *(empty — 1 line, no content)* | — re-export from the DMC docs if loading-state guidance is wanted |

---

## 1. Theming Dash 4 core components (`dash_4_components.md`)

Dash 4 rewrote `dcc.*` with a new design system driven by `--Dash-*` CSS variables,
and **ships no built-in dark mode**. Map the `--Dash-*` vars to Mantine's scheme-aware
vars so `dcc.Dropdown`/`dcc.Slider` follow the harbor theme and flip on light/dark:

```css
.dmc {
  --Dash-Stroke-Strong: var(--mantine-color-default-border);
  --Dash-Fill-Interactive-Strong: var(--mantine-primary-color-filled);
  --Dash-Text-Primary: var(--mantine-color-text);
  /* …full block in the file… */
}
:root[data-mantine-color-scheme="dark"] .dmc { /* dark overrides */ }
```
Wrap the subtree in `className="dmc"`. **Use it here:** anywhere we keep a `dcc.Dropdown`
/`dcc.Slider` for a feature DMC's `Select`/`Slider` lacks — ensure the host carries the
`.dmc` class and `assets/` has the var mapping, or it renders off-theme (and dark-mode
broken). Quick single-prop accent override: `style={"--Dash-Fill-Interactive-Strong":
"var(--mantine-primary-color-filled)"}`. Ties to `theme-guardian` (no fixed shades; adapt
via Mantine vars).

## 2. Functions as props (`functions_as_props.md`) — **most useful for `/account`**

Functions can't serialize over the wire, so DMC takes a **named reference** to a JS
function you define in `assets/*.js`:

```python
dmc.LineChart(..., valueFormatter={"function": "formatUsd"})
```
```js
// assets/dmcfuncs.js
var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};
dmcfuncs.formatUsd = (v) => `$${new Intl.NumberFormat("en-US",{minimumFractionDigits:2}).format(v)}`;
```
Supported (≤ v2.4.0): `Slider.label/scale`, `Select/MultiSelect/TagsInput.renderOption/filter`,
`BarChart.getBarColor`, **all charts `.valueFormatter` / `.tooltipProps` / axis props**,
date pickers `disabledDates`/`renderDay`, `Tree.renderNode`. Can **return components** via
`React.createElement` (no JSX) using `window.dash_mantine_components`.

**Use it here (Phase 2 `/account` dashboard):** the spend-over-time `LineChart` and the
by-model/by-kind `BarChart` need a **`$` `valueFormatter`** (raw AI cost) and a credits
formatter — this is the canonical use. Also handy for a `Select` that renders model/tool
options as `dmc.Badge` (harbor/brass/tidal/signal tokens). Note: `dash-mui-charts` (used on
`/admin/api-cost`) is a *different* lib with its own formatting — DMC charts + this pattern
are the lighter alternative when MUI Pro isn't needed.

## 3. `debounce` (`debounce_prop.md`)

`debounce=False` (default, every keystroke) · `True` (on blur) · `<ms>` (delay after last
keystroke). Supported on `TextInput`, `Textarea`, `NumberInput`, `Select`/`MultiSelect`/
`Autocomplete`, all date/time pickers, `RichTextEditor`, etc. (`Slider`/`RangeSlider` use
`updatemode` instead).

**Use it here:** any search/filter that triggers a server read — e.g. a `/account` ledger
**date-range / tool filter**, the userbase search, a shop search. Use `debounce=300`+ for
live-query inputs so we don't fire a callback per keystroke; `debounce=True` for "only the
final value matters" fields. Cheap win against callback storms.

## 4. Persistence (`persistence_props.md`) — **respect the project's `storage` lesson**

`persistence=True` + (optional) `persisted_props=[...]` + `persistence_type=` keeps an
input value across reload/tab without a callback. `id` is **required**. Gotcha: the layout
must be a **single component**, not a bare list (Dash issue #3147), or persistence silently
no-ops.

> ⚠️ **Cross-link to a paid-for lesson.** `persistence_type` defaults to **`"local"`**
> (`window.localStorage`). CLAUDE.md's load-bearing lesson is that `local`/`session`
> storage registers a window-level `storage` event listener that fires on **stale
> localStorage writes from earlier deployments** — the cause of the color-scheme cascade
> flicker. So: it's fine to use `persistence=True` for an *input value* on a form, but
> **prefer `persistence_type="memory"`** for anything near MantineProvider/theme, and
> **never** reach for `local`/`session` casually. Same rule as `dcc.Store` (`storage_type`).

**Use it here:** remembering a `/account` filter selection or a sprite-generator setting
*within a session* — use `persistence_type="memory"` (survives tab-switch, not reload) to
stay clear of the `storage`-event hazard.

> **To persist a `dcc.Store` (not an input) safely — the cart is the canonical example.**
> DMC `persistence` is for INPUT components, not a `dcc.Store`. When you need a Store to
> survive a reload (e.g. `cart-store`), do NOT give it `storage_type="local"/"session"`
> (the booby-trap). Instead keep it `"memory"` and bridge clientside: a `clientside_callback`
> on `Input(store, "data")` writes `localStorage.setItem(key, JSON.stringify(data))`, and a
> small `assets/*.js` script rehydrates on load via `window.dash_clientside.set_props(store,
> {data})`. Version the key (`-v1`) so a stale shape is ignored. Shipped for the cart in
> v0.20.0: `assets/cart_persist.js` + the persist callback in `callbacks/commerce.py`.

---

## How this maps to active work

- **Phase 2 `/account` dashboard** → `functions_as_props.md` (chart `$` `valueFormatter`,
  badge `renderOption`) + `debounce_prop.md` (ledger filters) are the direct hits.
- **Any `dcc.*` we keep** → `dash_4_components.md` (`.dmc` class + var mapping) so it
  themes + dark-modes correctly.
- **Persistence anywhere** → `persistence_props.md` **+** the `storage_type` lesson —
  default to `memory`.

*Index created 2026-06-02. Source: DMC v2.7.0 docs excerpts (Mantine v8) the maintainer
dropped in this folder. `dash_loading_states.md` is currently empty — re-export if needed.*
