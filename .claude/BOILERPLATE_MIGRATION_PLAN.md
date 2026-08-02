# Boilerplate migration plan — dash-mui-charts onto the network's docs format

**Goal.** Rebuild this docs app on the dash-documentation-boilerplate
structure so muicharts.2plot.dev looks and works like every other satellite
(pannellum, email, leaflet, the boilerplate itself), while **retaining every
live example, callback and interaction** the 40 current pages ship. The model
repo is `~/PycharmProjects/dash_pannellum` — a component library with
boilerplate docs beside it, which is exactly what this repo is.

**What this supersedes.** The network-standard pass (Phases 0–4, branch
`network-standard-pass`) deliberately kept the Python pages and custom shell.
That constraint is now lifted by the owner: uniformity wins. Everything that
pass built at the *network* layer (identity constants, dimll wiring, card,
analytics chain, app id, bulletin, tests, CI/CD) **survives** — this
migration replaces the *presentation* layer and the page authoring format.

Surveyed 2026-08-02 against: dash-documentation-boilerplate,
dash_pannellum (primary model), dash-hook-my-ai (Python-pages hybrid
reference). Current inventory: 40 pages, 17,733 lines under pages/,
**112 H2 sections**, 194 chart mounts, 113 callbacks.

---

## 1. The target architecture (measured, not assumed)

- **`run.py`** (not app.py): pluggable backend (`DASH_BACKEND` = flask |
  fastapi | quart via `lib/backend.py`), dependency floors enforced at boot,
  optional Dash MCP, optional Clerk (`lib/auth.py`, dormant without keys),
  proxy scheme fix, dimll wiring, `app.layout =
  create_appshell(dash.page_registry.values())`.
- **`pages/markdown.py`**: globs `docs/**/*.md`; each file's frontmatter
  (`name, description, endpoint, package, category, icon, tier`) drives
  `dash.register_page(..., image_url=OG_IMAGE_URL)`; the parsed layout is
  wrapped in ONE keyed `html.Div` per page (React reconciliation fix — do
  not flatten); `inject_ad_into_aside()` appends the ad slot to the TOC
  aside; the **directive-expanded markdown body is registered as the page's
  `llms_doc`** — every md page gets real /llms.txt prose for free.
- **Directives**: `.. toc::` (aside TOC), `.. exec::docs.family.module`
  (imports the module, renders its module-level `component`, callbacks
  register at import; `:code: false` hides inline source),
  `.. source::docs/family/module.py` (collapsible source block, expanded
  into llms.txt), `.. kwargs::dash_mui_charts.LineChart` (**auto props
  table from component metadata** — 13 free API references),
  `.. admonition::`, `.. llms_copy::`, images, dividers.
- **Example module contract** (`docs/<family>/<name>_example.py`):
  module-level `component = <layout>` plus `@callback`s. Env reads (the MUI
  Pro key) at module import — the same degradation pattern the current
  pages use.
- **Shell** (`components/`): appshell.py (Mantine theme tokens, AppShell
  with 280px navbar + 280px aside, `dcc.Location(id="url",
  refresh="callback-nav")` — **the same id the analytics counting rule
  depends on**), header.py (brand, search Select, GitHub link, theme
  toggle, burger), navbar.py (nav from page_registry + `page_order`),
  navbar drawer for mobile.
- **Dependency reality**: `dash[flask]>=4.4`, `dmc>=2.7.0`,
  `markdown2dash==0.1.2` installed **`--no-deps`** everywhere (it pins
  `gunicorn<22` against the CVE-driven `>=23` floor — LESSONS §8) with
  `mistune>=3.0.0` listed explicitly; `python-frontmatter`;
  `dash-improve-my-llms[flask]>=2.3.4`; vendored
  `dash_clerk_auth-0.9.1.tar.gz`.

---

## 2. Decisions (locked unless the owner objects)

1. **Endpoints: keep all 40 exactly** (`/sparkline`, `/linechart-basic`,
   `/tree-pro`, …). Frontmatter `endpoint:` is free-form — nothing forces
   `/components/...` paths. Zero broken links, sitemap/analytics/llms
   continuity, and the route-set gate stays meaningful. (A later
   consolidation into fewer, longer pages is content work, out of scope.)
2. **Entry point becomes `run.py`** (network convention, `gunicorn
   run:server`). Dockerfile, render.yaml, CI, route_parity, tests update in
   the same phase. Default backend **flask**; FastAPI stays a config option
   we do not exercise yet (our analytics hooks are flask-first).
3. **Analytics: keep THIS repo's chain** (`lib/analytics.py` +
   `lib/traffic_report.py`, the SPA-aware doc/spa counting rule). It is the
   NEWER generation — the boilerplate's `analytics_tracker` /
   `traffic_rollup` / `satellite_reporter` chain is what it replaces, and
   the port to the other satellites is already pending. The new shell keeps
   `dcc.Location(id="url", refresh="callback-nav")`, so the before_request
   hook and the url→`analytics-sink` callback transplant unchanged.
   **Do NOT adopt** the boilerplate's tracker files.
4. **Ad client: return to the canonical boilerplate `lib/ad_client.py`**
   (aside injection per page from markdown.py). The floating-slot fork
   existed because the old shell had ONE static slot — the double-impression
   bug does not exist for per-page aside slots, so the fork's reason
   retires with the shell. `AD_APP_ID=muicharts` stays. Home/changelog
   stay ad-free (no `.. toc::` on home; changelog is a Python page and gets
   no aside injected).
5. **Navbar: grouped sections per component family** (SparklineChart, Pie,
   Bar, Heatmap, Scatter, Line, Candlestick, LiveTrading, Composite,
   TreeView, Pickers + Changelog/API) — a fork of `create_content()` using
   frontmatter `category`, styled exactly like the boilerplate's sections.
   A flat 40-link list (pannellum has 11 pages) does not scale to 40; the
   grouped fork is the same one-file customization every satellite makes.
   The header search Select covers all 40 pages — a feature the current
   site lacks.
6. **The SimpleTreeView sidebar is retired** — accepted cost of
   uniformity, explicitly reversing the earlier dogfooding invariant. The
   component remains fully demonstrated on the 8 TreeView pages; add a
   sidebar-shaped demo to `/tree-simple` so the dogfooding story survives
   as content.
7. **Theme system: the boilerplate's** (`color-scheme-storage` +
   clientside init). `assets/00-loading-theme.js` and `01-nav-restore.js`
   retire with the old shell (nav-restore's localStorage key dies with the
   tree). `dark-mode.css`, `liquid_glass*.css`, `muiChartsFunctions.js`
   **stay** — the functions-as-props registry is a runtime contract for the
   dateFormat examples regardless of shell. Verify charts follow the new
   toggle on the pilot family before mass-porting.
8. **Home** = boilerplate-style `pages/home.py` + `pages/home.md` hero
   (brand, install, component gallery cards). **Changelog stays a Python
   page** (`pages/changelog.py`, reads CHANGELOG.md — pannellum's
   `pages/analytics.py` is the precedent for Python pages beside markdown).
9. **Clerk**: vendor `dash_clerk_auth-0.9.1.tar.gz` + `lib/auth.py`,
   dormant without CLERK_* keys — uniformity now, satellite auth ready for
   Phase-4 cutover without another pass.
10. **Site Dash floor moves to 4.4** (`dash[flask]>=4.4.0` in
    requirements.txt) — the boilerplate stack's floor. The PACKAGE floor
    stays `dash>=3.3.0` (unchanged, still measured by CI). The CI smoke
    matrix narrows to the new site floor (4.4.x); the package jobs keep the
    3.3→latest range. Local dev venv must be rebuilt (it runs dash 3.3.0
    with a `.pth`-linked dimll today).
11. **What survives verbatim**: `lib/constants.py` (identity/OG/
    INTERNAL_UA; gains `NAME_CONTENT_MAP`, `PRIMARY_COLOR`,
    `HEADER_HEIGHT`, `APP_TITLE`), `templates/index.html` (GA4, favicon
    swapper, JSON-LD, noscript — already network-standard),
    `lib/bulletin.py`, `lib/network_directory.py`, healthz, the social
    card, `scripts/network_smoke.py` + `smoke_live.py` + `check_release.py`
    + `make_social_card.py`, MUI_PRO degradation posture, hand-prefixed
    callback ids, GA4, port 8550.

---

## 3. The acceptance gate: chart parity (route parity, redefined)

Exact-tree parity is deliberately broken by this migration (the wrapping
changes on every page). What must NOT change is the charts themselves. The
gate becomes, per route, measured against the CURRENT committed baseline:

- the **route set**: all 40 endpoints, byte-identical paths;
- the **dash_mui_charts.\* component census**: per-route counts by
  `namespace.Type` (e.g. `/sparkline` mounts N SparklineChart) — these
  survive re-wrapping and prove no example was dropped;
- the **chart component ids** (hand-prefixed, unique) — proves examples
  ported, not rewritten;
- **callback coverage**: every callback whose Inputs/Outputs touch a
  dash_mui_charts id exists in the new app (shell callbacks legitimately
  differ);
- `/healthz` ok:true, all routes 200, llms.txt H1, card tags — the
  existing suites.

Mechanics: extend `scripts/route_parity.py` with a `--charts-only` mode
that filters the existing baseline to the dash_mui_charts census + chart
ids + chart-touching callbacks. Record it from the CURRENT app BEFORE any
migration commit; every family phase must keep migrated routes green in
charts-only mode. Browser-level spot checks per family (port 7666 flow,
interactions: click events, zoom, tree editing, time clock) close the gap
fingerprints cannot see.

---

## 4. Phases

**M0 — scaffold + pilot family (SparklineChart, 3 pages).**
Branch `boilerplate-migration` off `network-standard-pass`. Rebuild the
venv (dash 4.4 stack). Record the charts-only baseline from the current
app. Bring in: `components/` (header brand: area-chart icon +
"Dash MUI Charts" + version badge from the package — keep the version-
parity contract), forked navbar with family groups, `lib/` additions
(backend, auth, proxy, health, access, page_tiers, directives/, canonical
ad_client), `pages/markdown.py`, `run.py` (flask default, floors, THIS
repo's analytics wired in), requirements.txt (markdown2dash --no-deps
pair, mistune, dmc 2.7, dash[flask]>=4.4), vendor/. **All 37 unported
Python pages stay registered and working under the new shell** (they are
plain Dash pages; only their old ad/nav assumptions are gone) — the site
never breaks mid-migration. Port sparkline: `docs/sparkline/…` (3 md + ~11
exec modules, shared `_data.py`), delete the 3 old pages. Gate: charts-only
parity green for /sparkline*, all 40 routes 200, theme toggle drives the
charts, browser check.

**M1 — Pie + Heatmap + Scatter (5 pages, ~21 sections).** Includes the two
props-explorer pages (heavy interactivity — each becomes one md page whose
single exec module carries the explorer). Gate as M0.

**M2 — BarChart (6 pages) + Candlestick + LiveTrading (2 pages, ~20
sections).** live_trading's dcc.Interval streaming ports inside its exec
module. Pro pages keep the env-read + banner pattern inside exec modules.

**M3 — LineChart + Composite + Crosshair + Highlighting-sync (12 pages,
~40 sections).** The biggest and most intricate batch: synchronized-tooltip
overlays, zoom preview, brush. The `dateFormat` examples must find
`muiChartsFunctions.js` untouched.

**M4 — TreeView family (8 pages) + Pickers (2 pages).** TimeClock Lab
keeps `liquid_glass*.css`; add the sidebar-shaped SimpleTreeView demo
(decision 6). tree-pro drag/kebab interactions browser-checked.

**M5 — Home + Changelog + API reference.** home.md hero; changelog.py
restyled minimally for the new shell; NEW `/api` page with
`.. kwargs::` tables for all 13 components (net-new content the format
gives us nearly free).

**M6 — tests, CI, deploy config, cleanup.** Update the Phase-3 suites:
shell invariants (navbar/search/drawer replace nav-tree; aside ad slots
replace the floating slot; url Location test unchanged), pro-degradation
census (now over docs/**/ exec modules), STUB checks, version parity
(badge source moves to components/header.py). CI: markdown2dash --no-deps
in docs-tests/smoke/docker/release + in-image `import markdown2dash`
fingerprint (copy dash-email's), site matrix → dash 4.4.x, package jobs
unchanged. Dockerfile: `COPY vendor`, the --no-deps pair, `run:server`.
render.yaml startCommand → run:server. check_release: markdown2dash/
mistune checks, run.py presence. Delete: old pages/*.py (37 files),
components of the old shell in app.py, 00-loading-theme.js,
01-nav-restore.js, the ad_client fork. Update .claude/CLAUDE.md +
SKILLS.md (View-Code pattern section → exec/source directives; nav
section), memory files. Full battery + charts-only parity across all 40 +
browser sweep. CHANGELOG. PR.

---

## 5. Sizing and risks

**Size.** ~40 md files + ~110–150 exec modules distilled from 17.7k lines
of pages (112 sections). M3 is the long pole. Realistic effort: each family
phase is a focused session; the port is mechanical (layout section → exec
module `component`, prose → markdown, code-tab strings → `.. source::`)
but every section needs its callbacks carried and its demo re-verified.

**Risks / mitigations.**
- *Chart dark-mode under the new theme system* — verified in M0 pilot
  before anything else ports.
- *dmc 2.6 → 2.7 and dash 3.3 → 4.4 behavior shifts in demos* — the 4.4.1
  route-parity run already proved the trees identical; dmc 2.7 is the
  network's proven pairing (pannellum/boilerplate).
- *markdown2dash renderer quirks* (headings with inline code crash it) —
  the boilerplate's `patch_renderer()` ships with markdown.py; keep
  headings plain.
- *Two pages with module-name collisions in exec imports* — exec modules
  live under `docs.family.name` namespaces; keep names unique per family.
- *Analytics continuity through the shell swap* — the counting rule's two
  write paths (before_request + url callback) are shell-independent as
  long as `id="url"` survives; `verify_traffic.py` re-run per phase.
- *SEO* — endpoints unchanged, canonicals/dimll unchanged, and llms.txt
  page docs IMPROVE (26 pages currently serve placeholder stubs; the md
  bodies close that).

**Open questions for the owner** (defaults chosen, flag to change):
1. Endpoints stay as-is (default) vs. restructure to `/components/...`
   with redirects?
2. Grouped navbar sections (default) vs. pannellum-style flat list?
3. Vendor Clerk now, dormant (default), vs. leave it out entirely?
4. Is FastAPI-in-production a goal? (Default: flask now; the analytics
   hooks gain async twins only if/when the backend flips.)
