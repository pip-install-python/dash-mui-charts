# DIVERGENCES — dash-mui-charts vs dash-documentation-boilerplate

What this file is: the record of every **deliberate** difference between
this fork and the template, with the reason. `.claude/CLAUDE.md` clause 5
is the rule it serves — a sync must never "restore" anything written
here, and an unrecorded difference is treated as drift.

Template baseline for this pass: **1.6.27** (`055363e`). The kit
surface is at those bytes; every item in the three sync specs
(1.6.10-16, 1.6.17-21, 1.6.22-27) has had its **detect** run against
this tree and its disposition reported. Only SYNC-1.6.17-1.6.21 item 1
was applied — what the detects found and did not fix is the drift list
at the foot of this file, not a decision recorded above it.

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

`.claude/CLAUDE.md` and the three skills are **byte-verbatim** from the
template and TRACK it — verified identical at 1.6.27 (`055363e`),
including the title, which names the template. That is the file's own
rule: identity derives from the repo (`BASE_URL`, `SATELLITE_APP_KEY`,
this file), never from `CLAUDE.md`. Those bytes are the template's to
update mechanically, which is why none of them appears in the
byte-owned fence below; `settings.json` is the exception, and the
fence's own prose says why it is still not listed.

One nuance the kit's host pin inherits from this fork: `tests/conftest.py`
hardcodes `APP_BASE_URL` (so a developer's `.env` cannot change what the
suite measures — a deliberate pin from the identity round), while
`tests/test_claude_kit.py` derives its expected host from
`lib.constants.BASE_URL`. Here that reads conftest's constant rather than
`DEFAULT_BASE_URL`. The pin still fires on the case it exists for — a fork
that leaves the template's host in `settings.json` — but a genuine host
move must update three files, not two. Upstream has no conftest pin and
does not have this.

---

## 8. The home lane states versions by import, not by substitution

SYNC-1.6.22-1.6.27 item 4's contract is "whatever the docs lane
substitutes, the home lane substitutes too", because upstream
`/llms.txt` serves `home.md`'s text and a `{{VERSION:...}}` token
there would ship raw.

There is no `home.md` here. `pages/home.py` is hand-written Dash — it
carries its own `LLMS_DOC` string and renders the version badge from
`from dash_mui_charts import __version__`, the live package the docs
image installs from this same tree (section 1). `pages/markdown.py`
does call `substitute_versions`, for the pages that are markdown.

So the item's failure mode cannot occur on this fork's home lane, and
its source pin (both modules call `substitute_versions`) would pin a
call that must not exist. The contract is met by construction: an
imported `__version__` cannot go stale the way a token can. Wire check
run 2026-08-26 — `/llms.txt` carries no `{{` token.

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
  here. The exec-form `CMD` hardcodes 8550. Correction to the earlier
  wording, which said it "works only because Render port-detects":
  Render never runs this image at all — `render.yaml` line 4 declares
  `runtime: python`. The Dockerfile's only consumer is CI's
  `docker image · boot · battery` job, which is also why the missing
  `HEALTHCHECK` costs a real check (see the CI verdict entry below).
- `.github/workflows/cd.yml`: template 1.6.13 widened the build-match
  wait to 100 × 15s with a 30-minute job timeout, sized for the
  cache-busted builds a floor bump forces, and made the hookless case a
  `::warning`. This repo is still at 60 × 15s / 25 / `::notice`.
Found by the 2026-08-26 detect sweep (all three specs run against this
tree; only SYNC-1.6.17-1.6.21 item 1 was applied):

- **The gate card promises an AI assistant this site does not ship**
  (SYNC-1.6.10-1.6.16 item 9). `lib/gate_layouts.py:75` — the
  demo-present intro string still ends "…the complete API reference,
  and the AI assistant." Nothing named "AI assistant" exists anywhere
  else in this tree, and that string renders live on `/pie`'s sign-in
  card, the one endpoint in `DEMOS`. The loudest of these findings:
  every other item here is machinery, this one is a promise to a
  visitor.
- **Three Pythons, and the one that serves production is the oldest**
  (SYNC-1.6.22-1.6.27 item 5). The image half landed on its own while
  this pass was running: PR #3 (dependabot, owner-merged as `d473482`)
  took `Dockerfile` to `python:3.14-slim`, which is byte-equivalent to
  the item's FROM line — minor tag, fleet minor — and CI proved it
  (`docker image · boot · battery` green, run 32671687289). Nothing
  else moved. `render.yaml` still declares `PYTHON_VERSION: "3.11.12"`
  and `ci.yml` still runs its singletons on `3.12`.
  The trap specific to this fork: `render.yaml` line 4 says
  `runtime: python`, NOT Docker. The image is a CI artifact here — it
  is not what serves traffic. So the bump widened the gap rather than
  closing it: CI now certifies the app on 3.14 while production runs
  3.11.12, and `/healthz` has no `python` field, so nothing on the
  wire can say so. Whoever takes item 5 here should start from that
  line, not from the Dockerfile.
- **healthz has no CF-IPCountry pin, and the resolver still reads the
  Flask context** (SYNC-1.6.10-1.6.16 item 1). Extends the
  `lib/health.py` entry above: `_resolved_country()` takes no
  arguments, so the item's context-free
  `_resolved_country({"CF-IPCountry": "DE"})` pin — the only one that
  can fail from inside a Flask suite — cannot be written until the
  signature moves. The wire half passes (geo block present, resolved
  `US (via cf-ipcountry)`), and `tests/test_pages_smoke.py:327` pins
  the block's shape, but no test spoofs a country.
- **The smoke-live SSL source pin is absent** (SYNC-1.6.10-1.6.16
  item 7). The BEHAVIOR is here — `scripts/smoke_live.py:140` is the
  file's only `urlopen` and it carries `context=SSL_CONTEXT`, and
  there is no `post()` to fix. Only the pin that holds it is missing,
  and CI on Linux is blind to the defect it guards.
- **CI checks that the container RUNS, not that Docker calls it
  healthy** (SYNC-1.6.17-1.6.21 item 2). `ci.yml:231` inspects
  `{{.State.Running}}`; the item wants `{{.State.Health.Status}}`
  polled to `healthy` and failing on `none`. Paired with the
  `Dockerfile` entry above — with no `HEALTHCHECK` instruction the
  verdict here would be `none`, which is the point of failing on it.
- **`tests/test_auth_demos.py` is absent** (SYNC-1.6.22-1.6.27 item
  3). The CONTRACT is already satisfied and deliberately so — `DEMOS`
  holds one entry, `/pie`, chosen for being license-free (see the
  comment in `lib/auth_demos.py`), and it resolves: `/pie` is a
  registered page and `docs.pie.interactive_example` imports with a
  module-level `component`. Only the byte-verbatim test that would
  hold it is missing; it rides SYNC-1.6.22-1.6.27's block.
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

## Byte-owned paths

Paths this fork owns byte-for-byte. The F3b fan-out never overwrites
a path listed here; everything else in the spec's `sync-verbatim`
block is the template's to update mechanically. Prose above explains
divergences; this block is the machine answer.

Repo-relative paths, one per line, `#` comments, no `..`; exactly one
block. An EMPTY block means "the template owns every sync-verbatim
path here" — present so the absence is a statement. When the block
exists it is authoritative; a fork without it gets the conservative
mention heuristic (over-flags, never restores).

Empty here, and audited to be: the union of the `sync-verbatim`
blocks in SYNC-1.6.10-1.6.16, SYNC-1.6.17-1.6.21 and
SYNC-1.6.22-1.6.27 is the three skills, `tests/test_claude_kit.py`,
`.github/dependabot.yml` and `tests/test_auth_demos.py`. Section 7's
host-pin nuance NAMES `tests/test_claude_kit.py` while describing how
the pin READS — that is the mention the fence exists to retire, and
its bytes are the template's (verified identical at 1.6.27). This
fork's `.github/dependabot.yml` differs from the template's only by
being BEHIND 1.6.24 — drift, not a decision, so the machine should
overwrite it. `tests/test_auth_demos.py` is not here to own yet.

The heuristic this fence replaces cost a real delivery here, which is
worth recording while the evidence is fresh. The F3b fan-out ran
against this repo as PR #6 (`f4812a8`, spec @ `16d61ce`) and shipped
ONE of the two block files whose bytes differed: it copied
`.claude/skills/sync-template/SKILL.md` and withheld
`tests/test_claude_kit.py` — the path section 7 mentions. Conservative
and correct by its own rules, and still the wrong answer: those bytes
were the template's, and the file it withheld was the one carrying the
pin for this very fence. With the block below present, that path is
mechanical again.

`.claude/settings.json` is the one real byte-level divergence on the
kit surface (section 7's two extra domains) and is deliberately NOT
listed: no shipped spec carries it as a `- path` entry — it appears
only as a `# requires:` adoption gate, which the fan-out reads and
never copies. Should a release ever intend a fleet-wide settings
change, this fork's entry belongs here on that day, not before.

```yaml byte-owned
# Empty by audit, 2026-08-26 (template 1.6.27, 055363e). See above.
```
