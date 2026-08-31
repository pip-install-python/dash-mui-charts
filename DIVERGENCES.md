# DIVERGENCES — dash-mui-charts vs dash-documentation-boilerplate

What this file is: the record of every **deliberate** difference between
this fork and the template, with the reason. `.claude/CLAUDE.md` clause 5
is the rule it serves — a sync must never "restore" anything written
here, and an unrecorded difference is treated as drift.

Template baseline for this pass: **1.6.35** (`4c63992`) for sync items
12 and 13; the kit surface (`.claude/CLAUDE.md`, the three skills,
`tests/test_claude_kit.py`) is at those bytes as of 2026-08-29. The
1.6.22-1.6.33 verbatim block landed by fan-out in `79be8c3` (PR #8).
The 1.6.29 baseline this line used to state (`5589318`, md5-verified
2026-08-26) held for items 1-11. Every item in the three
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
- **THE DOCKERFILE IS A CI ARTIFACT. IT DOES NOT SERVE PRODUCTION.**
  `render.yaml` line 4 declares `runtime: python`, so Render's NATIVE
  runtime builds this service from `requirements.txt` + `pip install .`
  and never reads the image at all. The Dockerfile's only consumer is
  CI's `docker image · boot · battery` job. Stated as its own line
  (2026-08-30, at the ops seat's request) because it was buried in a
  drift entry and it decides who is right in whole classes of finding:
  the fleet's `python:3.14-slim` bump certified an interpreter nothing
  ran until `PYTHON_VERSION` moved too (see the RESOLVED entry below),
  and pannellum's "CHANGELOG.md missing from the image" defect cannot
  occur here for two independent reasons — this Dockerfile is `COPY . .`
  rather than an explicit-file COPY, AND Render never opens it. A finding
  that reasons from the image to production is wrong on this host before
  it is examined.
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

## 2. CD refuses to verify a deploy that never ran — RETIRED 2026-08-29

**Subsumed by sync item 13 (a2), which is strictly stronger.** `verify`'s
condition here is now `needs.deploy.result == 'success'` — the template's
own shape since 1.6.35 — so this fork and the template agree again and
there is nothing left to pay upstream. The record stays because reports
written before today describe the divergence as live, and because the
reasoning is what made the stronger form legible: the fork had already
found that a SKIPPED deploy must not be verified; the ops seat then found
on the template's run 33262495272 that a FAILED one must not be either
(`!= 'cancelled' && != 'skipped'` still admits `failure`, and that run
went GREEN against the previous build). Same defect class, one more branch.
The historical text follows.

The `verify` job's condition here was
`always() && needs.deploy.result != 'cancelled' && needs.deploy.result != 'skipped'`;
the template stopped at `!= 'cancelled'`.

Why: CI red → `deploy` skipped → `verify` still ran and graded the
**previous** release against the **new** checkout's battery. The gate
wave produced two red jobs from one cause, and the loud one was the
wrong one. Template-class — worth paying upstream.

**Measured on the road's two runs, 2026-08-30, both conclusion
success.** Timestamps from the runs themselves, not from wall-clock
guesses:

*Before the dashboard Branch click* — CD run 33334818928, head `9928ba0`,
created 20:51:47Z, concluded 20:54:20Z (153 s):

    20:53:35Z  wire serves 9928ba0            108 s into the run
    20:53:55Z  origin/release still EMPTY     128 s into the run
    20:54:20Z  run concludes

Render built `main`: the wire had the build 45 s before the run that
judges it concluded, and `release` did not exist at all when the wire had
already moved, so `release` cannot have been the source. Item 13's note
says a first promoted run cannot discriminate because both refs hold the
same sha — true only once `release` EXISTS. When the wire moves before the
promote step runs, absence of the ref is the proof, and this run had it.

*After the click* — CD run 33335418597, head `0224479`, created 21:04:59Z,
concluded 21:08:33Z (214 s):

    21:06:42Z  origin/release 9928ba0 -> 0224479   103 s into the run
    21:08:08Z  wire serves 0224479                 189 s into the run

**The ref moved 86 seconds BEFORE the wire.** That is the road working:
Render is watching `release`, and `release` only moves when a green matrix
lets the promote step write it. Same host, same cache-busting build class,
opposite ordering — the click is what changed between them.

This is also the fleet's first fork-side confirmation of the
`fetch-depth: 0` fix (template `bf1fde2`). The FIRST promote proves
nothing about it, because creating a ref works from a shallow clone; this
one fast-forwarded an EXISTING `release` from `9928ba0`, which is exactly
what failed in one second on the template's run 33262495272.

CORRECTION, recorded because the earlier text of this entry asserted it:
"95 seconds is far less than this CI matrix takes" was an ASSUMPTION, not
a measurement, and the margin is much narrower than it implied — CI here
reaches the promote step in roughly 100 s (103 s on the run above), so the
wire beat it by seconds, not minutes. The conclusion survives and is now
measured rather than reasoned; the reasoning that reached it did not.

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

## 5. Excluded links hide through a different seam — RETIRED 2026-08-30

**Both seams are gone, on both sides.** Sync item 16 deleted the
template's `excluded_links` AND this fork's `EXCLUDED_LINKS`: the sidebar
and the header search now both ask `components.navbar.is_nav_page`, which
excludes `/admin/*` and hidden-tier pages structurally, so the two halves
that used to be kept in step by hand are one rule. This fork's hidden
`ADMIN_NAV_ID` section (rendered with `display: none` and revealed by a
callback on `url.pathname`) converged on the template's pip-docs+ shape in
the same change — a placeholder `Box` the callback FILLS, which is
strictly better: the anonymous DOM no longer carries the admin URLs at
all, where `display: none` still did. `components/navbar.py` is now
byte-identical to the template's.

What survives, because it is still this fork's shape: each admin page
calls `mark_hidden` at its OWN import (`pages/control_board.py`,
`pages/traffic.py`) rather than the navbar doing it in a loop. The pin
moved with the seam — `tests/test_control_board.py::
test_every_admin_path_is_machine_hidden` now reads the registry's
`/admin/*` instead of a hand-kept set, and `tests/test_excluded_links_hidden.py`
(new here, ported) holds the other end: the surfaces. That is the
llms-2plot-dev footgun — hidden from the sidebar, still published to every
crawler — closed on a rule instead of a list. The historical text follows.

Template was: `components/navbar.excluded_links` plus a navbar-time
`mark_hidden` loop. Here: `EXCLUDED_LINKS` filtered the sidebar and the
path hid itself at its own import.

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

---

## 9. This host's posture — measured, not assumed

The fence below is SYNC-1.6.22-1.6.35 item 9's contract (1.6.30), ported
here on 2026-08-29 because item 13 (c) needs the `deploy:` key and a key
cannot be added to a fence that does not exist. Until today
`tests/test_claude_kit.py` SKIPPED its posture pin on this repo with
"DIVERGENCES.md has no posture fence" — that skip is what an unported
contract item looks like, and it is now gone.

### The wall is retired (sync item 15) — MEASURED ON THE WIRE 2026-08-30

`ai_bots` below is a WIRE measurement, taken at 20:54:20Z on build
`9928ba0`, GET not HEAD, with real vendor UAs:

    ClaudeBot GET /          -> 200 (14065b)
    ClaudeBot GET /llms.txt  -> 200 (20693b)
    ClaudeBot GET /healthz   -> 200 (213b)
    GPTBot    GET /          -> 200 (14065b)
    GPTBot    GET /llms.txt  -> 200 (20719b)
    GPTBot    GET /healthz   -> 200 (213b)
    robots.txt: NO stanza for GPTBot, ClaudeBot or CCBot — all three fall
    under `User-agent: *`.

The ops seat's independent probe agrees on all six. `/` is 14065 bytes on
the wire and 14065 in-process — the same crawler document byte for byte,
which is the confirmation that nothing sits in front of this host
rewriting anything.

The three readings that produced it, kept because the SHAPE of the
evidence is the point — the wire minus in-process is what an edge rule
would show up in, and here it is zero:

**Wire, 2026-08-29** (build `79be8c3`, ClaudeBot UA, GET not HEAD):

    ClaudeBot GET /          -> 403
    ClaudeBot GET /llms.txt  -> 200
    ClaudeBot GET /healthz   -> 403

**In-process, 2026-08-30, BEFORE the flip** (`run.py` at
`block_ai_training=True`; the app's own answer, no proxy in front):

    ClaudeBot / 403 (318b) · /llms.txt 200 · /healthz 403 (318b)
    GPTBot    / 403 (318b) · /llms.txt 200 · /healthz 403 (318b)

**In-process, 2026-08-30, AFTER the flip** (`block_ai_training=False`):

    ClaudeBot / 200 (14065b) · /llms.txt 200 · /healthz 200
    GPTBot    / 200 (14065b) · /llms.txt 200 · /healthz 200
    robots.txt: NO training stanza at all — GPTBot, ClaudeBot and CCBot
    fall under `User-agent: *`. The fingerprints in scripts/smoke_live.py
    and scripts/network_smoke.py assert "not Disallow", never "Allow: /",
    for exactly that reason.

**The wire minus in-process is ZERO on this host, before and after.**
Before the flip the wire and the app agreed on 403/200/403; after it they
agree on 200/200/200. Every 403 muicharts.2plot.dev ever served was
dash-improve-my-llms' own middleware, and there is no edge wall in front
of this host — matching the owner's finding of 2026-08-30 that the
Cloudflare AI-bot rule is Enterprise-only on this plan and no zone rule
exists. Item 15's acceptance is CLOSED on both halves.

`healthz: full` — the live payload carries `app`, `backend`, `build`,
`dash_version`, `geo`, `ok`, `python` (read on the wire at build
`79be8c3`). `runtime: python` — `render.yaml` line 4, the one value the
kit test validates against the repo itself. `deploy: release-branch` —
sync item 13, and CONFIRMED on the platform 2026-08-30: the owner set the
Render service's Branch to `release`, and the run after that click moved
`origin/release` 86 s before the wire moved (§2). The key is a statement
about what deploys this host, and it is now a measured one.

Nothing but a probe can validate a status: re-measure and paste the probe
whenever what this host serves changes.

```yaml posture
ai_bots: {"/": 200, "/llms.txt": 200, "/healthz": 200}
healthz: full
runtime: python
deploy: release-branch
```

---

## 10. The navigation contract, ported where the tree differs (item 16)

`components/navbar.py`, `components/footer.py`, `pages/changelog.py` and
`lib/aside.py` are byte-identical to the template at 1.6.39 — this fork
holds NO content in them, which is the evidence sync item 16 asks for
before it reclasses them as cargo. Four places the tree required a port
rather than a copy, each deliberate:

- **`/api` is a markdown page here, not a generated one — and the half of
  contract 7 that is about the MACHINE LANE was missed on the first pass.**
  The template adds `pages/api.py` + a generator whose `as_markdown()`
  exists precisely so the llms doc carries the same tables. This fork has
  `/api` as a markdown doc whose `.. kwargs::` directive builds one table
  per component from the installed package's own docstrings, wrapped in the
  site's prose and carrying its own `.. toc::`. Keeping that page is still
  right — the generator would replace a richer page with a thinner one and
  orphan §6's `m2d-block-kwargs` selector — but the report that said
  "contract 7 is met by behaviour" was **true of the browser lane only**.
  A markdown2dash directive renders Dash COMPONENTS; the machine lane and
  the non-JS prerender are built from the markdown SOURCE, where the
  directive line is stripped. Measured on the wire 2026-08-30 at build
  `0224479`: `/api/llms.txt` 2681 bytes with ZERO table rows, the crawler
  document zero `<table>`, the prerender block 9259 bytes with zero
  `<table>` — while a real Chrome's RENDERED DOM showed 13 tables and 371
  rows. Name which of the two you measured, always: the HTML Chrome
  RECEIVES has zero tables as well (curl with a Chrome UA runs no
  JavaScript and gets the same app shell), so "zero tables in the browser
  lane" and "13 tables in the browser lane" are both true statements about
  different artifacts, and a report that does not say which is unreadable.
  The defect was never in the DOM. Thirteen
  headings and nothing under them, for every agent and every reader
  without JavaScript, on the one page whose entire purpose is the prop
  list.
  Closed by giving `.. kwargs::` the same treatment `pages/markdown.py`
  already gave `.. source::` — expansion into the prose — over a single
  shared parse in `lib/api_reference.py` that both the directive and the
  expansion call. One parse, two renderings: 384 rows in every lane, and
  `test_the_two_lanes_report_the_same_number_of_props` fails the moment a
  second implementation appears.
  `API_PACKAGES = ["dash_mui_charts"]` IS set — it drives the header's
  version badge and the sidebar's API section. Consequence:
  `has_aside("/api")` is True here and False on the template.
  **The lesson, and it is about the test rather than the page**: the pin
  that should have caught this asserted each component NAME appeared in
  the layout and in `/api/llms.txt`. Both were true with zero rows — the
  names come from the page's own `### LineChart` headings. A test that
  checks a table's headers and not its body certifies an empty table.
- **`SAME_AS` keeps the PyPI project.** The template ships
  `SAME_AS = [GITHUB_URL]` because it publishes no package. This host
  documents one, so the sameAs loop names GitHub *and*
  `pypi.org/project/dash-mui-charts/` — three properties pointing at each
  other is the strongest statement of which URL is this package's
  canonical docs home. The contract's pin (`GITHUB_URL in SAME_AS`) holds.
- **`pages/home.py` stays hand-written Dash.** The template's home is 56
  lines of markdown2dash over `pages/home.md`; this fork's is a 371-line
  Dash layout with a component-card grid, and §8 above records why (it
  renders the version badge from an import rather than a substituted
  token). Contract 9 applied to it as written — `dcc.Link` became
  `dmc.Anchor` — and `lib/directives/headings.py`'s new inline-image
  renderer is `not-applicable`: it exists so the template's home can carry
  `![alt](src)` through markdown2dash, and no page here goes through that
  path.
- **`components/header.py` keeps this fork's identity**: the
  `header-avatar` id (a contract with the random favicon swapper in
  `templates/index.html` — rename both or neither), the "Dash MUI Charts"
  wordmark in `#1976d2`, and the version badge fed by
  `dash_mui_charts.__version__` that `tests/test_version_parity.py` pins
  five ways. What the contract changed: the search reads
  `navbar.search_data`, the Other Apps menu arrived, the GitHub icon reads
  `GITHUB_URL`, and the "More Dash components" link to
  `pip-install-python.com` is RETIRED — the domain has been out of
  `lib/network_directory.py` since the retire sweep and the header was
  still sending readers there.

Also retired in this pass, without replacement: the sidebar's "Pip
Components" section (`2plot.dev/pip`) and its `2plot.dev` and Dash
Community (`community.plotly.com`) Resources links. The network is listed
once now, in the top bar's Other Apps menu; the forum was the owner's
explicit removal.

---

## Checked, and NOT divergent

Recorded because a reader has reason to wonder:

- **Robots posture**: `block_ai_training=False`, `allow_ai_search=True`,
  `allow_traditional=True` — the template default, deliberately
  unchanged, and the default INVERTED fleet-wide on 2026-08-30 (sync item
  15). Training crawlers are allowed now. The reasoning is the ledger:
  since sync item 12 every corpus read is a row (tier, vendor, verified,
  bytes) and the hub reconciles it against the wire, so a read is recorded
  and priceable and does not need a wall — the tool from here on is
  per-vendor `vendor_policy={"<key>": "block"|"meter"}` for ONE vendor
  whose rows justify it, never the whole class. This entry read "training
  crawlers are disallowed … the sibling fork that opens AI training is the
  divergent one" until that day; it is kept, corrected, rather than
  deleted, because reports written before it describe the old posture as
  this host's position.
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
- ~~`.github/workflows/cd.yml`: template 1.6.13 widened the build-match
  wait to 100 × 15s with a 30-minute job timeout~~ — **TAKEN 2026-08-29**
  with sync item 13, because the ledger round's floor bump (item 12) is
  exactly the cache-busted build class the widening was sized for: the
  requirements line changing IS the cache bust, and dash-email's wait
  timed out on that class (2026-08-23) inside the old 60 × 15s window.
  The `::notice` / `::warning` half of that entry went with the hook step
  itself. NOT taken: the template's compare-API fast-fail on supersession
  (its wait reads `gh api .../compare` and exits 1 when the live build is
  a DESCENDANT of the wanted sha). This fork's wait is still the plain
  loop — a superseded run here goes red at timeout instead of red in one
  second, with a worse message. Next sync.

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
