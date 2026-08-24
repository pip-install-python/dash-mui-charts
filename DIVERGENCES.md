# DIVERGENCES — dash-mui-charts vs dash-documentation-boilerplate

What this file is: the record of every **deliberate** difference between
this fork and the template, with the reason. `.claude/CLAUDE.md` clause 5
is the rule it serves — a sync must never "restore" anything written
here, and an unrecorded difference is treated as drift.

Template baseline for this pass: **1.6.15** (`1638528`, the .claude kit).
Anything the template changed after that is unreviewed here.

How to use it in a sync: read this file before the work list. If a
template change collides with an entry below, port the change's
*contract* into this fork's shape rather than copying the file, and say
so in the report.

---

## 1. This repo is two projects in one tree

The template is a documentation site. This repo is a documentation site
**and** the `dash-mui-charts` component library it documents — React
sources, generated Dash wrappers, the npm build, the PyPI package. Every
item below follows from that and is deliberate:

- **Library tree**: `src/lib/components/*.react.js`, `dash_mui_charts/`
  (generated wrappers + committed `.min.js` bundles), `package.json`,
  `webpack.*.config.js`, `setup.py`, `usage.py`, `_validate_init.py`.
- **A third workflow**: `.github/workflows/release.yml` — tag-driven PyPI
  publish over OIDC trusted publishing (no stored token). The template
  has CI and CD only.
- **Library jobs inside `ci.yml`** with no template analogue: `smoke`
  (Dash-version × Python matrix that rebuilds the wrappers from source),
  `package` (wheel build, metadata check, clean-venv import, dash-floor
  measurement), `package-python-range`.
- **`Dockerfile` runs `pip install .`** — the docs image installs the
  library from this same tree, so a demo page and the published wheel
  can never disagree about what a component does. And **no Node layer**:
  the bundle and wrappers are committed, so the image needs no npm. Same
  end state as the template's node-layer removal, different reason —
  here the trade-off is that changes under `src/lib` require a local
  `npm run build` and committing the regenerated artifacts.
- **`.flake8` per-file ignores** the template has no need for:
  `dash_mui_charts` (dash-generate-components owns generated style),
  `src`, `build`, `dist`, and the budgeted `pages/*.py` debt from the
  first CI run (~75 findings; the route-parity gate pins those layout
  trees, so a style sweep belongs in its own verified change).
- **`tests/test_version_parity.py` + `scripts/check_release.py`** — the
  five-way version-drift gate (package.json, package-info.json,
  setup.py, the header badge, the JSON-LD). The 2026-08-01 survey found
  this repo advertising five different versions at once; nothing
  upstream needs this because nothing upstream ships a package.
- **`scripts/route_parity.py`** + `route_parity_baseline.json` +
  `chart_parity_baseline.json` — the migration gate (exact mode for
  network passes, `--charts-only` for the boilerplate migration). It is
  how a pass proves it changed no page; the gate wave caught the control
  board leaking into the public navbar with it.
- **`scripts/smoke_test.py`** — the battery for the library matrix. Its
  `EXPECTED_ROUTES = 42` counts every registered route; the suite's
  `tests/test_pages_smoke.py` counts 41 crawlable pages (the control
  board is registered, not crawlable). Two independent gates on purpose:
  **adding a page moves both numbers.**

## 2. CD refuses to verify a deploy that never ran

The `verify` job's condition here is
`always() && needs.deploy.result != 'cancelled' && needs.deploy.result != 'skipped'`;
the template stops at `!= 'cancelled'`.

Why: CI red → `deploy` skipped → `verify` still ran and graded the
**previous** release against the **new** checkout's battery. The gate
wave produced two red jobs from one cause, and the loud one was the
wrong one. Template-class — worth paying upstream.

Lineage note, not a divergence: this repo's build-match wait is the
origin of the fleet's. It shipped here as `commit` and the template
adopted the idea under the name `build`; the 2.7.1 floor round renamed
it here to match. `cd.yml`'s comment block tells that story — a sync
should not read it as drift.

## 3. pip-audit gates here, advises upstream

The template runs pip-audit with `continue-on-error: true`. Here it is a
hard gate, since the 2026-08-18 triage: dash-clerk-auth 1.0.5 allowed
clerk-backend-api ≥7, which pulled cryptography ≥50 and actually closed
the four open CVEs. With the baseline quiet, a red pip-audit here means
something new landed — which is the whole value.

## 4. Flask only

`run.py` raises on any `DASH_BACKEND` other than `flask` (this site's
visitor-tracking hook is Flask-specific). Consequences:

- `lib/asgi_routes.py` and `lib/asgi_middleware.py` are deliberately
  absent.
- The template's FastAPI/Quart healthz tests are **not** ported — they
  would exercise unreachable code here.
- `requirements.txt` pins `dash-improve-my-llms[flask]`; the other
  extras stay as commented lines.

A sync of anything in `lib/health.py` or the route-registration seam
lands Flask-lane only.

## 5. Excluded links hide through a different seam

Template: `components/navbar.excluded_links` plus a navbar-time
`mark_hidden` loop, pinned by `tests/test_excluded_links_hidden.py`.

Here: `EXCLUDED_LINKS` (one entry, `/admin/control-board`) filters the
sidebar, and the path hides itself from the machine surfaces at its own
import (`pages/control_board.py` → `mark_hidden`). This fork also has a
hidden Admin nav section revealed by a server-side callback
(`ADMIN_NAV_ID`), which the template does not have at all.

Same contract, different seam — so it is pinned over the **set** rather
than the one path:
`tests/test_control_board.py::test_every_excluded_link_is_machine_hidden`.
That is the llms-2plot-dev footgun (hidden from the sidebar, still
published to every crawler), closed on this fork's shape.

## 6. Table scroll containment needs two selectors

`table.m2d-table` alone is inert here. markdown2dash derives the class
from the renderer method, so the `.. kwargs::` directive's output is
`m2d-block-kwargs` — which is all 13 of `/api`'s prop tables, this
site's widest content. `assets/main.css` carries both selectors. The
kwargs directive is the boilerplate's, so this is an upstream gap, not a
fork preference.

## 7. The .claude kit ships two extra domains

`.claude/settings.json` is the template's file with the host swapped to
`muicharts.2plot.dev`, plus `mui.com` and
`www.dash-mantine-components.com` in `sandbox.network.allowedDomains`
and `permissions.allow`. The library half wraps MUI X Charts; its API
documentation is the reference a session here actually needs, and
`settings.local.json` (which held them) is per-seat and never ships.

`.claude/CLAUDE.md` and the three skills are **byte-verbatim** from
template 1.6.15 — including the title, which names the template. That is
the file's own rule: identity derives from the repo (`BASE_URL`,
`SATELLITE_APP_KEY`, this file), never from `CLAUDE.md`.

---

## Checked, and NOT divergent

Recorded because a reader has reason to wonder:

- **Robots posture**: `block_ai_training=True`, `allow_ai_search=True` —
  the template default, deliberately unchanged. Training crawlers
  (GPTBot, ClaudeBot, CCBot) are disallowed; AI *search* agents are
  allowed. The sibling fork that opens AI training is the divergent one;
  this host does not share that position.
- **`/healthz` payload**: template 1.6.10 verbatim apart from the
  `[muicharts]` log prefix — `app`, `build`, `geo` and nothing extra. A
  missing `geo` block here means the Docker cache trap fired, with no
  local exemption to explain it away.
- **The gate wave surface**: vendored dash-clerk-auth with the sha
  check, the security floors, `lib/gate_layouts` / `page_visibility` /
  `agent_key`, the control board, ship-dark via `PAGE_DEFAULT_TIER` —
  all template shape.

## Known drift — NOT divergence. Take these on the next sync.

Listed here because this is where a syncing session looks; none of it is
a decision this fork made.

- `lib/health.py`: template 1.6.13 passes `headers=request.headers`
  explicitly (pannellum's FastAPI finding). Identical behaviour on the
  Flask lane, so it is cosmetic here — sync it rather than diverge.
- `Dockerfile`: template 1.6.14's shell-form
  `CMD gunicorn ... ${PORT:-8550}` and the curl `HEALTHCHECK` are not
  here. The exec-form `CMD` hardcodes 8550 and works only because Render
  port-detects.
- `.github/workflows/cd.yml`: template 1.6.13 widened the build-match
  wait to 100 × 15s with a 30-minute job timeout, sized for the
  cache-busted builds a floor bump forces, and made the hookless case a
  `::warning`. This repo is still at 60 × 15s / 25 / `::notice`.
- Template test modules with no counterpart here:
  `test_network_directory`, `test_bulletin`, `test_proxy_scheme`,
  `test_runtime_imports`, `test_auth_wiring`, `test_llms_routes`,
  `test_config`, `test_docs_content`, `test_pages`,
  `test_network_smoke`, `test_smoke_live`, `test_excluded_links_hidden`.
  Some subject matter is covered under this repo's own names
  (`test_pages_smoke`, `test_site_identity`, `test_access`,
  `test_prerender`); `network_directory`, `bulletin` and the proxy-scheme
  handling look genuinely unpinned. Each needs a keep / port /
  not-applicable call — the M0 migration ported a subset and never
  recorded which.
