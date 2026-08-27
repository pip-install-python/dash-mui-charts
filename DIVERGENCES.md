# DIVERGENCES — dash-mui-charts vs dash-documentation-boilerplate

What this file is: the record of every **deliberate** difference between
this fork and the template, with the reason. `.claude/CLAUDE.md` clause 5
is the rule it serves — a sync must never "restore" anything written
here, and an unrecorded difference is treated as drift.

Template baseline for this pass: **1.6.29** (`5589318`). The kit
surface and every path in the three specs' `sync-verbatim` blocks are
at those bytes — verified by md5, 2026-08-26. Every item in the three
sync specs (1.6.10-16, 1.6.17-21, 1.6.22-29) has had its **detect**
run against this tree and its disposition reported. What the detects
found and did not fix is the drift list at the foot of this file, not
a decision recorded above it.

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
- **TWO PYTHONS in one `ci.yml`**, which is why
  `tests/test_python_version.py` here is job-scoped where the template's
  reference implementation greps the whole file. The SITE lane (`lint`,
  `docs-tests`, `docker`, `smoke`, `pip-audit`, `lint-js`) is held to the
  fleet Python; the PACKAGE lane (`package`, `package-python-range`)
  exercises the wheel's own `requires-python` window, 3.9-3.13, and
  pinning it to a container base would break it the moment the image
  moved. SYNC-1.6.22-1.6.29 item 5 names this split and tells a fork to
  scope its greps; `_JOB_LANES` in that test is where this fork states
  it, and `test_every_ci_job_is_assigned_a_lane` is what stops a new job
  from escaping both lanes unnoticed.

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
tree):

**RESOLVED the same day — the drift that reached production.** From
`c746876` (2026-08-24) until the fix on 2026-08-26 this site declared
no Twitter card type any scraper could read. `templates/index.html` had
been trimmed of the template's
`<meta name="twitter:card" content="summary_large_image">` on the
reasoning that Dash already emits the tag — it does, but with
`property=` (hardcoded in `dash/_pages.py`), and X's parser predates
the OG convention and reads `name=` only. Two things then made the
loss invisible:

- `tests/test_social_card.py` asserted `twitter:card` appears exactly
  ONCE and listed it among the tags Dash emits that must never be
  restated. Those two assertions did not merely fail to catch the
  deletion — they are the rule that *required* it. The template had
  already carved out the exception (both tests there compare the SET
  of values and pin `name="twitter:card"` separately); this fork was
  running the pre-2.5.x version. Ported as contract, not copied: the
  surrounding file is a fork rewrite and stays one.
- Nothing here ran `scripts/smoke_live.py`. The 1.6.28 block copied in
  a script with a new crawler/browser identity-parity check, the suite
  went green because no test exercised it, and the check found the
  defect on the WIRE instead — CD run `33002187234`, red at
  "Smoke-test the deployment", four failures all reading
  `crawler=['summary_large_image'] browser=[]`. `tests/test_smoke_live.py`
  now exists (SYNC-1.6.22-1.6.29 item 6, fork-owned by class) and
  reproduces those four lines exactly when the tag is removed —
  verified by deleting it and watching the suite refuse.

The general lesson, worth more than the tag: a fork-owned test that
encodes a rule the template has since qualified will defend the bug,
and a copied script with no fork-owned test is certified by nothing.

- **The gate card promises an AI assistant this site does not ship**
  (SYNC-1.6.10-1.6.16 item 9). `lib/gate_layouts.py:75` — the
  demo-present intro string still ends "…the complete API reference,
  and the AI assistant." Nothing named "AI assistant" exists anywhere
  else in this tree, and that string renders live on `/pie`'s sign-in
  card, the one endpoint in `DEMOS`. The loudest of these findings:
  every other item here is machinery, this one is a promise to a
  visitor.
- ~~**Three Pythons, and the one that serves production is the
  oldest**~~ (SYNC-1.6.22-1.6.29 item 5) — **APPLIED 2026-08-26.** The
  image half had landed on its own via PR #3 (dependabot, owner-merged
  as `d473482`), which took `Dockerfile` to `python:3.14-slim` and
  widened the gap rather than closing it: `render.yaml` line 4 says
  `runtime: python`, so Render's NATIVE runtime builds this service and
  never reads that image. CI certified 3.14 while visitors ran
  `PYTHON_VERSION: "3.11.12"`, and `/healthz` had no `python` field, so
  nothing on the wire could say so. Closed in every encoding at once:
  `render.yaml` -> `3.14.7`, the site lane in `ci.yml` and `cd.yml` ->
  `3.14` with the window legs moved to the adjacent minors,
  `lib/health.py` gains `python` from `platform.python_version()`, and
  `tests/test_python_version.py` holds them to the Dockerfile's FROM
  tag. The Dockerfile's own header said "Render docker runtime" until
  this pass — a false line that is how two contradictory declarations
  sat in the tree unread; it now says what the file actually is.
  **This is the change that moved PRODUCTION off 3.11**, and it moved
  it without a dashboard edit: `/healthz` on build `460d201` answers
  `"python": "3.14.3"` where the previous build had no `python` key at
  all, so Render's blueprint sync did carry `PYTHON_VERSION`. Note the
  PATCH: the file asked for 3.14.7 and the platform resolved to 3.14.3,
  its latest available 3.14. `render.yaml` was corrected to 3.14.3 —
  declaring a patch nothing runs is the same defect class in miniature.
  The pins compare the MINOR on purpose, so a future platform bump
  inside 3.14 stays green.
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
  item 7; re-detected as SYNC-1.6.22-1.6.29 item 6, 2026-08-26).
  The BEHAVIOR is complete: the 1.6.28 copy brought a `post()` for
  the auth-wiring probe, so the file now has TWO `urlopen` calls and
  both carry `context=SSL_CONTEXT` — the earlier wording here ("there
  is no `post()` to fix") was true when written and is not any more.
  Still missing is the SOURCE pin that holds it, which upstream lives
  in `tests/test_auth_wiring.py` — a module this fork does not carry.
  CI on Linux is blind to the defect it guards, so nothing here would
  notice the context argument going away again.
- **`scripts/network_smoke.py` had no SSL context — a
  TEMPLATE-CLASS finding, fixed here 2026-08-26.** Running the fleet
  battery by hand against production from a Mac reported ALL TWELVE
  checks failed with `CERTIFICATE_VERIFY_FAILED` — indistinguishable
  from "the site is down", on a host that was perfectly healthy. macOS
  Python ships without OS trust-store integration; CI runs on Linux and
  can never see it; nothing in `tests/` exercises the transport. Fixed
  with the same certifi-backed `_ssl_context()` `smoke_live.py` already
  carries. **The template's own copy has no context either** (checked at
  `5589318`), so this belongs upstream: SYNC-1.6.10-1.6.16 item 7 and
  SYNC-1.6.22-1.6.29 item 6 both name `smoke_live.py` in their file
  lists, while item 6's contract sentence says "whatever live tool a CD
  run certifies with" — and CD certifies with BOTH scripts. The file
  list is narrower than the contract it states.
- **The gate's CONFIGURED branch is certified by nothing**
  (SYNC-1.6.22-1.6.29 item 7). `tests/conftest.py` blanks every
  `CLERK_*` var before any import, so every gate card this suite renders
  is the zero-secret branch; no test has ever rendered the ClerkJS
  bootstrap branch with a fake publishable key. The detect fires here —
  and it fires on the template too, which records its own adoption as
  `open` and queues it for a runtime pass. Left open here for the same
  reason: the reference implementation does not exist yet, and inventing
  one fork-side is how two shapes end up in the fleet.
- **CI checks that the container RUNS, not that Docker calls it
  healthy** (SYNC-1.6.17-1.6.21 item 2). `ci.yml:231` inspects
  `{{.State.Running}}`; the item wants `{{.State.Health.Status}}`
  polled to `healthy` and failing on `none`. Paired with the
  `Dockerfile` entry above — with no `HEALTHCHECK` instruction the
  verdict here would be `none`, which is the point of failing on it.
- ~~**`tests/test_auth_demos.py` is absent**~~ (SYNC-1.6.22-1.6.29
  item 3) — **CLOSED 2026-08-26**: the F3b fan-out landed it byte-
  verbatim in `ad0fc06` (PR #7) and it is green. The contract it
  holds was already satisfied and deliberately so — `DEMOS` holds one
  entry, `/pie`, chosen for being license-free (see the comment in
  `lib/auth_demos.py`), and it resolves.
- Template test modules with no counterpart here:
  `test_network_directory`, `test_bulletin`, `test_proxy_scheme`,
  `test_runtime_imports`, `test_auth_wiring`, `test_llms_routes`,
  `test_config`, `test_docs_content`, `test_pages`,
  `test_network_smoke`, `test_excluded_links_hidden`.
  (`test_smoke_live` came off this list on 2026-08-26 — see the
  RESOLVED entry above. It is the proof the list is worth working
  through rather than admiring: that one absence cost a red CD.)
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

Empty here, and re-audited at 1.6.29 to still be: the union of the
`sync-verbatim` blocks in SYNC-1.6.10-1.6.16, SYNC-1.6.17-1.6.21 and
SYNC-1.6.22-1.6.29 is the three skills, `tests/test_claude_kit.py`,
`.github/dependabot.yml` and `tests/test_auth_demos.py`. All six are
byte-identical to template `5589318` (md5, 2026-08-26), so the fork
owns none of them. Section 7's host-pin nuance NAMES
`tests/test_claude_kit.py` while describing how the pin READS — that
is the mention the fence exists to retire. `.github/dependabot.yml`
and `tests/test_auth_demos.py`, both open questions in the 1.6.27
audit, were settled mechanically by the fan-out in `ad0fc06`: the
first is no longer behind 1.6.24, the second is here and green.

**What an empty fence does and does not say — the 1.6.28 lesson.** It
says the template owns these BYTES. It does not say a copy is safe.
`scripts/smoke_live.py` rode the 1.6.28 block into this repo on that
authority, byte-perfect and correct, and took production red the same
day (see the RESOLVED entry above) — not because the bytes were
wrong, but because nothing here exercised them and a check the file
newly carried was right about this host. Template 1.6.29 drew the
same conclusion and pulled the file back out of the block, reclassing
it contract. The fence is the machine's half; the fork-owned test is
the half that decides whether a copy can be trusted, and this repo
had none. Nothing to add to the block for it: the file is not in the
1.6.29 block at all, and its bytes here ARE the template's.

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
# Empty by audit, 2026-08-26; re-audited by md5 at template 1.6.29
# (5589318) the same day, still empty. See above.
```
