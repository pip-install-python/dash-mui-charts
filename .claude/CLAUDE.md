# Dash Documentation Boilerplate

## Project Overview

This project is a modern documentation boilerplate for Dash applications,
providing a markdown-driven documentation system with interactive examples,
comprehensive theming, and AI/LLM integration. It is the template that the
`*.2plot.dev` component documentation sites are forked from.

Versions, dependencies and history are deliberately not restated here — they go
stale. Read `requirements.txt` for the stack and `CHANGELOG.md` for what
changed and when.

---

## Custom Directives

| Directive | Syntax | Purpose |
|-----------|--------|---------|
| `toc` | `.. toc::` | Generate table of contents |
| `exec` | `.. exec::module.path` | Render Python component |
| `source` | `.. source::file/path.py` | Display source code |
| `kwargs` | `.. kwargs::ComponentName` | Show component props |

Options are documented in `docs/directives/directives.md`.

---

## Configuration

### Customization Points

| File | Purpose |
|------|---------|
| `lib/constants.py` | App-wide constants (colors, titles) |
| `assets/main.css` | Custom CSS styles |
| `templates/index.html` | HTML template (analytics, meta tags, SEO) |
| `components/appshell.py` | Theme configuration, MantineProvider settings |
| `components/navbar.py` | Navigation ordering and organization (incl. the full-height mobile drawer — the network-standard mobile nav) |
| `pages/control_board.py` | `/admin/control-board` — live per-page tier + llms.txt toggles (owner/admin-gated, fails closed) |
| `lib/page_visibility.py` | The board's override store (persists to `PAGE_VISIBILITY_FILE`; overrides beat frontmatter in `lib/access.py`) |
| `lib/auth_demos.py` | Live-demo teasers rendered inside the sign-in gate cards |

---

## Development Notes

### Adding New Documentation Pages
1. Create folder in `docs/` (e.g., `docs/my-component/`)
2. Create markdown file with frontmatter:
```markdown
---
name: My Component
description: Description of my component
endpoint: /components/my-component
icon: mdi:code-tags
---

.. toc::

## Overview
...
```
3. Add Python examples as needed
4. Reference with `.. exec::docs.my-component.example`
5. Page will auto-register and appear in navigation

### Creating Theme-Aware Charts
1. Import `dmc.add_figure_templates()`
2. Register templates at module level
3. Create callback with `Input("color-scheme-storage", "data")`
4. Use ternary to select template: `"mantine_dark" if theme == "dark" else "mantine_light"`
5. Recreate figure with template parameter

---

## Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Dash Mantine Components](https://www.dash-mantine-components.com/)
- [Mantine](https://mantine.dev/)
- [dash-improve-my-llms](https://pypi.org/project/dash-improve-my-llms/)
- [Project Repository](https://github.com/pip-install-python/Dash-Documentation-Boilerplate)
- [dmc-docs Inspiration](https://github.com/snehilvj/dmc-docs)
- [Plotly Community Forum](https://community.plotly.com/)

---

## Network role & the behavioral contract

This repo is a member of the 2plot network — either the template
itself (dash-documentation-boilerplate) or a fork of it serving one
component's documentation. **Identity derives from the repo, never
from this file**: the app key comes from `SATELLITE_APP_KEY` and
run.py's fork point, the host from `lib/constants.py`'s `BASE_URL`,
the deliberate differences from the template from `DIVERGENCES.md`
at the repo root. If those disagree with anything written here,
they win.

### The contract — every session, every prompt

1. **Check the prompt against this tree before executing.** Prompts
   are written from the template's perspective and your fork may
   legitimately differ — floors, backends, payload shapes, page
   sets. A prompt step that doesn't fit this repo is a finding to
   return, not an instruction to force.
2. **Corrections are your job, not scope creep.** If a prompt's
   reference list doesn't match its steps, if its assumed state is
   wrong, or if executing it as written would produce a
   green-but-vacuous result, say so and propose the corrected
   version before running it.
3. **Verify your own deploy on the wire before reporting.** A push
   is not a result. Run `/wire-verify` (or its manual equivalent)
   against production and paste what came back. If your sandbox
   cannot reach your own domain, say exactly that — an unverified
   claim marked as unverified is honest; the same claim unmarked is
   not.
4. **Report observed versus expected, with evidence.** Paste the
   JSON, the status code, the test count. "Should work" and summary
   claims without artifacts are not reports.
5. **Divergence is legitimate when written down.** Before syncing
   template changes, read `DIVERGENCES.md`; never let a sync
   "restore" a recorded deliberate difference. When you deliberately
   diverge, record it there in the same commit — an unrecorded
   divergence is indistinguishable from drift and will be treated
   as drift.
6. **Never touch**: environment variable VALUES, hosting dashboards,
   secrets, other repos' trees, or anything the prompt didn't put in
   scope. Enumerate what you cannot do (closing PRs, dashboard
   steps) for the owner instead of claiming it done.

### Verification traps (fleet-learned, keep them)

- A `>=` floor can never pull a new release through a Docker cache
  hit — the requirements line changing IS the cache bust, and floors
  live in several encodings (requirements, run.py's boot floor,
  tests, CI): grep the number, move every one.
- `/healthz` build == HEAD is the deploy proof; a missing geo block
  on dimll ≥2.7 means the cache trap fired (unless DIVERGENCES.md
  says this host's healthz is deliberately minimal).
- Always GET, never HEAD — and the mechanism, measured 2026-08-27
  after two rounds of wrong diagnoses: on the ASGI backends HEAD is
  answered by NOTHING AT ALL. Werkzeug derives a HEAD rule from
  every GET rule; FastAPI's `APIRoute` does not, so a route declared
  `@router.get(...)` returns 405, and every ASGI host in the network
  was 405ing HEAD on every route — `/healthz`, `/robots.txt`,
  `/sitemap.xml` included. Get the LAYER right (corrected 1.6.33,
  after this text and two seats' drops all said "Starlette", and
  three probes went looking in the wrong package):
  `starlette.routing.Route` DOES add HEAD wherever GET is present —
  `self.methods.add("HEAD")`, the same courtesy Werkzeug does — and
  FastAPI's `APIRoute` is the one that takes `methods` literally.
  A HEAD probe therefore tells you about
  the router's method table and never about the document. GET is
  never wrong, which is the whole reason to have one rule.
  Do NOT "verify" the trap on one host and conclude HEAD is fine:
  excalidraw measured twice and was right about its own Flask host
  and wrong about the fleet. Do not verify it on `HEAD /` either —
  a crawler-UA `HEAD /` is answered by the prerender middleware
  before routing, so it returns 200 on a host that 405s everything
  else, and that one case is how this repo's 1.6.31 in-process
  probe cleared the app code. Earlier text here said the ASGI hosts
  DROP the `Link` headers on HEAD: a 405 carries no `Link`, so the
  observation was true and the diagnosis was not. Fixed in the
  template at 1.6.32 (a HEAD→GET ASGI middleware, because the
  package's own adapter declares its routes GET-only); the fleet's
  two ASGI forks consume it as spec item 11, and the hub plus four
  second-ring hosts had the same defect — if you serve a non-Flask
  backend, assume you have it until you have probed a route that is
  NOT `/`. The middleware stays after dimll 2.7.2 fixes the
  package's own routes: `/` is Dash's page catch-all and every Dash
  route is an `APIRoute` too.
- Any throwaway Python probe a session writes against a production
  host needs the certifi SSL context AND a retry guard. Fixing the
  shipped tools does not cover the next ad-hoc script: the template
  seat hit `CERTIFICATE_VERIFY_FAILED` in a hand-written CD watcher
  one hour after shipping that exact fix inside both live tools,
  and the ops seat hit it plus an `IncompleteRead` on a chunked
  response in the same session. It is a seat habit, not a repo
  contract, which is what this file is for.
- Run-watchers keyed on a commit sha can match Dependabot's runs on
  the same sha — key on the workflow path (cd.yml) instead.
- The browser lane and the machine lane are different documents;
  a fix proven on one is unproven on the other.
- SUPERSESSION: cd.yml's build-match wait cannot tell "not deployed
  yet" from "already replaced" — both look like a live build that
  is not the sha it wants. A bot-merged PR (any GITHUB_TOKEN merge)
  is one road in: it lands with ZERO workflow runs on the merge sha
  (anti-recursion) yet still reaches production, because the deploy
  hook builds branch HEAD — so an in-flight CD run ships the merge
  while its own wait holds out for the superseded release sha
  (observed live on 4a1d430, 2026-08-25). It is NOT the only road,
  and taking the bot actor off main does not close the class: two
  human pushes inside one deploy window, or hook dispatch lag,
  produce exactly the same state. Since 1.6.25 the wait fails FAST
  when the live build is a DESCENDANT of the wanted sha (compare
  API) instead of going red at timeout — that is the diagnosis, and
  it works whoever merged. The policy — actions PRs: human merge
  when green, never a bot actor on main — removes the most common
  road, not the trap.
- Anonymous api.github.com is 60 requests/hour. With no `gh` and no
  token, read a run ONCE after CI's own jobs report complete — a
  blind 20 s poll loop spends the whole budget reading rate-limit
  bodies as "not done yet" (modelviewer, 2026-08-26).
- A GitHub API JSON body WITHOUT the field you asked for
  (`workflow_runs` absent, not empty) is a rate-limit error body,
  never an empty result — check the field exists before trusting
  the answer.
- `git fetch` before any audit: the fan-out pushes to these repos
  now, and a checkout current yesterday is 2–3 merges behind
  origin/main today (three pilot sessions, same day, 2026-08-26).
- A failed STEP is not a failed RUN. A job with
  `continue-on-error: true` (pip-audit here) reports its step red
  and the RUN still concludes `success`; the reverse also bites —
  a green-looking job list under a run whose conclusion is
  `failure`. Read the run's `conclusion`, then the annotations;
  never infer either one from the other.
- Never round-trip JSON through zsh `echo` — it interprets the
  `\n` inside a multi-line commit message and hands the parser
  real control characters (a broken API read on the template, then
  the same hour on the ops seat). Pipe curl straight into
  `python3`, or use `printf '%s'`.
- Repeated HTTP headers survive only if you keep them: both
  `dict(resp.headers)` and `{k: v for k, v in resp.headers.items()}`
  keep the LAST value per name, and dimll emits several `Link`
  headers (muicharts, 2026-08-26). Iterate the items, or ask for
  `resp.headers.get_all(name)`; in curl, `-D -` and read the raw
  block.
- Name the crawler UA when you probe the machine lane. Which
  document a host serves is decided by the package's UA
  classification, not by the absence of a UA: on the template
  today, curl's default `curl/8.x` receives the SAME crawler
  document as Googlebot (18,779 bytes, byte-identical) while a
  Chrome UA gets the 148 KB app shell. One host (muicharts) reported
  a UA-less probe classified the other way; treat that as
  UNCONFIRMED — muischeduler filed the same observation and then
  RETRACTED it (its report had the two documents swapped), leaving
  one unreproduced sighting, and a trap carrying an unreproducible
  fact spends somebody's afternoon. The advice does not depend on
  it: either lane can be the one you did not mean to test, so send
  `-A "<a real crawler UA>"` and confirm from the body which
  document came back.
- There is ONE classifier: `dash_improve_my_llms.classify()`. Never
  add a User-Agent list to this app — the tracker had one for a year
  (`lib/analytics_tracker.py`, until 1.6.34), it filed ClaudeBot as
  *search* (it is Anthropic's training crawler; the package's registry
  and this repo's own `run.py` comment both said so six lines from
  where the list ignored them), it still named the retired
  `anthropic-ai` / `claude-web` tokens, and it counted every UA-less or
  library client as a human. Every host in the fleet reported those
  numbers. A token the registry lacks is a pushback to the package
  seat, not a list here; `tests/test_analytics_classifier.py` greps the
  module for the old tokens and goes red if one comes back.
- `build == HEAD` on `/healthz` means HEAD of **`release`**, not main
  (1.6.35). Render deploys `release`; only cd.yml's `deploy` job writes
  it, fast-forward, after the CI matrix is green. `main` ahead of
  `release` is an uncertified push pending — its CD run is red or still
  running — never "drift" and never a reason to deploy by hand or to
  write `release` yourself (a non-fast-forward push fails the next run
  on purpose). Compare the wire against `git rev-parse origin/release`;
  the one measurement behind this: 2026-08-29 14:12Z, de0bcff pushed
  to main, built by Render inside the minute, red in CD at 14:13Z,
  served for ~6 minutes. A host whose DIVERGENCES.md posture fence has
  no `deploy:` key still watches main — there the trap is the old one.
- Headless browsers are CRAWLER-lane from dash-improve-my-llms 2.9.0
  (measured on the wheel, 2026-08-29: `HeadlessChrome/…` and a
  Playwright UA classify `lane: crawler, bot_type: monitor,
  vendor_key: headless`; 2.8.0 said browser). A host that screenshots
  ITSELF for social cards — Playwright, Puppeteer, a headless Chrome
  in a job — now receives the crawler document, not the app shell,
  unless the screenshot service sends its own non-headless UA. If a
  card went blank or textual after a floor bump, look here before
  the template. Same class as the two lane traps above: name the UA,
  confirm from the body which document answered.
- Which branch Render actually builds can be measured on a GREEN push,
  by TIMING, without waiting for a red one (leaflet, 2026-08-31 — the
  method, not just its answer). `main == release == wire` at every step
  of a promote tells you nothing: both refs hold the same sha, so the
  wire cannot separate them, and four promotes across three hosts said
  nothing at all. Sample `/healthz` every ~45 s from the moment of the
  push and note when the swap lands relative to the PROMOTE, not the
  push. leaflet measured build+swap at 2m03s from the promote; had
  Render reacted to the push instead, the same 2m03s would have put the
  build live ~1m52s earlier than it appeared, and the wire was still
  serving the old sha well past that point. That is STRONG EVIDENCE
  that Render is building `release` — not proof, since a queued or slow
  build could in principle produce the same shape. The canonical
  discriminator is unchanged and still owed: the first push that goes
  RED on main must leave `release` unmoved and the wire unchanged.
  Worth taking on every SECOND promote — it costs one background
  sampler and converts "asserted" into "strongly evidenced".
  THE CONCRETE FORM IS NOW A SCRIPT (1.6.44 item 17):
  `python3 scripts/promote_sampler.py --sha <the run's sha>`, which
  takes eight samples at 45 s on ONE loop and does three things a
  hand-written watcher gets wrong. (a) ONE LOOP, ONE TIMELINE — the
  wire and the run state are read in the same iteration, because two
  separate reconstructions invite exactly the arithmetic error the
  measurement exists to avoid. (b) It times against the PROMOTE STEP's
  `completed_at`, NEVER the deploy JOB's: the job CONTAINS the
  build-match wait, so it completes when the wait SEES the swap — it
  tracks the swap and never the promote, and landed at -13 s and 0 s
  on the template's two measured pairs, useless for timing either way.
  (c) It retries each sample three times and records `unreadable` as a
  state DISTINCT from `old`, because the container restart lands
  exactly where the bracket needs its sample — twice out of two on the
  template — so an un-retried loop is systematically blind at the only
  moment that matters, and collapsing unreadable into old INVENTS a
  bracket nobody observed. The sampler REFUSES to report a bracket it
  did not observe: a single "new" sample cannot say what it followed.
- Verify the artifact the claim is about, and say which one you
  measured. Three hosts got this wrong in one round while holding the
  rule: a skip link checked in the received HTML lives in the RENDERED
  DOM (muicharts, twice inside an hour, having written the rule
  itself); a props table absent from the crawler document is a defect
  of the site, not of the harness — pannellum moved that assertion onto
  the rendered layout and the pin passed for a fortnight over a corpus
  serving zero props. WHEN A LANE DISAGREES, THAT IS THE FINDING; never
  relocate the assertion to the lane that passes. And an owner-gated
  section needs BOTH cookie states to be a measurement at all
  (modelviewer: `credentials: 'include'` → 2,962 B with admin hrefs,
  `'omit'` → 108 B with none — hidden, not merely styled away).
  The error runs BOTH ways and the second one is worse, because it
  sends someone hunting a bug that does not exist: `curl https://…/ |
  grep -c skip-link` returns **0** on a host where the skip link is
  shipped and working (excalidraw, 2026-08-31) — it is a Dash
  component in `app.layout`, so React renders it and the served HTML
  never contains it. A fork "verifying the skip link on the wire" with
  curl reports a missing feature that is present. Anything built by
  the layout rather than written into the template is invisible to the
  two artifacts curl can reach; assert it through the layout or a real
  browser, and say which you used.
- Assert the corpus is NON-EMPTY before trusting any negative, and print
  the count beside the result (note 88). A sweep that found nothing and a
  sweep that swept nothing produce the same green, and only one of them
  is evidence. **CORRECTED 2026-09-05, re-measured on this tree**: the
  example this note used to give is WRONG for this repo today. It said
  `.flake8` excludes `docs/*/` so `flake8 docs/` exits 0 on a file
  containing `def broken(:`. There is no docs exclusion in this repo's
  `.flake8`, `docs` is on CI's flake8 line, and that file is reported
  `E902 TokenError` and fails the step. The RULE stands; the example was
  stale, and a trap carrying an unreproducible fact spends somebody's
  afternoon. What is still true here, and is now what item 7's sweep
  exists for: flake8 catches most syntax errors and NOT all —
  `print(a=1, a=2)` (duplicate keyword argument) is a compile-time
  SyntaxError that flake8 reports NOTHING for, exit 0, while `py_compile`
  exits 1. **AND PIN THE TOOL VERSION WHEN YOU PIN A TOOL'S BLIND SPOT.**
  This seat first recorded `def f(): nonlocal q` as a second blind spot;
  it is one on the flake8 available here — **3.9.2 / pyflakes 2.3.1**,
  borrowed from a sibling venv and years behind — and NOT on a current
  one, where pyflakes >= 3.2 reports `F824`. Caught by the ops seat
  re-measuring on 7.3.0 before it reached a spec. A blind-spot pin taken
  on an old toolchain asserts something false and goes red the day the
  venv upgrades, so record the version beside the measurement — the same
  rule as printing the resolved package version, applied to the linter.
  Same family, same day: a naive
  substring count read fenced documentation as defects (this seat), a
  file-scoped grep matched prose ABOUT the defect it was hunting
  (muicharts, clerkhook), a `git show … && diff` printed "(empty = same)"
  on a comparison that never ran (llms), and `pytest … | tail -2 && git
  commit` committed over a red suite because a pipeline's exit status is
  the LAST command's (this seat, one hour after writing the note above).
  Capture the exit code; count what you swept; say both.
- And the same family one turn later, MEASURED TWICE — this seat and
  clerkhook hit it independently within the hour, so it is a property
  of the technique and not one seat's slip — and worth keeping because
  it nearly shipped a wrong fact into a spec: extracting a package
  constant with
  `re.search(r"EVENT_FIELDS = \((.*?)\)", src, re.S)` truncated at a `)`
  inside a COMMENT in the middle of the tuple, printed eight of sixteen
  fields, and reported `'ua' present: False` — confidently, with a
  number beside it. Caught only because eight looked too few. When you
  parse a language construct out of source with a regex, check the count
  against something independent (the file, `python -c "from … import X;
  print(len(X))"`, the CHANGELOG) before you believe a negative.
- ACCEPTANCE IS QUOTED AT THE RESOLVED VERSION, not at the declared one
  (1.6.44 item 10). Every acceptance line in a report prints the version
  the run actually imported, and prints it by IMPORTING and reading
  `__file__` — never by reading `requirements.txt`, which states a floor
  and not a fact. On this fork the difference is routine rather than
  theoretical: the line is `dash-improve-my-llms[flask]>=2.8.0` and the
  local venv resolves **2.10.0 from a dev checkout at
  `/Users/pip/PycharmProjects/dash-hook-my-ai/`**, so a report that
  quoted the requirements line would name a version no test ran against.
  Print both the version and the path.
- AND NAME THE TOOLS WHOSE LOCAL INVOCATION IS NOT CI'S. A local run is
  not the CI run, and the gap is silent in both directions. Measured on
  this seat 2026-09-05: `actionlint` and `shellcheck` are NOT installed
  here, so every workflow lint this session could claim was in fact not
  run — CI's `lint` job downloads actionlint 1.7.7 and runs it, and that
  is the only place it happens. The template's own note adds the subtler
  half: `actionlint` WITHOUT shellcheck on PATH silently skips every
  run-block's shell analysis, so "actionlint clean" from a machine
  lacking shellcheck is a weaker claim than the same words from CI. This
  repo's `.venv` likewise has no pytest and no flake8 — both are
  borrowed from the sibling boilerplate venv by APPENDING to
  `sys.path` — so say which interpreter and which site-packages produced
  a count before quoting it.
- WHEN A DETECT HUNTS A STRING, PARSE — do not grep (1.6.44 item 13,
  whose file target `sync/README.md` this fork does not have: it
  consumes specs and authors none). The rule is worth carrying anyway
  because it recurs for a structural reason: **a good comment explains
  the ABSENCE of the thing a detect hunts**, so the better-documented
  the code, the more reliably a raw grep reports the very defect the
  comment documents the fixing of. Strip comments AND STRINGS, or use
  `ast.parse` — a comment strip alone still matches a live DOCSTRING
  saying the same words. Flatten whitespace before matching prose: a
  fragment that WRAPS across a line, or sits under a blockquote's `> `
  markers, is otherwise invisible. And read case-insensitively.
  FOUR instances in ONE session on this seat, 2026-09-05, each caught
  only because the sweep went red on its own fix:
    * `"HeadAsGet" in py.read_text()` over the whole tree matched the
      test file's own prose about the shim it was proving absent;
    * a workflow curl sweep matched the workflow's COMMENT about curl
      and the `PROBE_UA:` value containing the string `curl/8`;
    * `'trigger="hover"' not in text` matched the comment explaining
      that `trigger="hover"` had been the defect — fixed with an AST
      walk for the keyword argument;
    * `"pointer: coarse" in css` found the CSS COMMENT above the rule
      rather than the rule — fixed by stripping `/* */` first.
  A fifth, from the same session and the same family: a whole-file
  regex that matched NOTHING and would have reported a clean sweep, if
  the non-empty-corpus assertion had not been there to catch it.
- A SHELL'S CWD CAN SHADOW AN INSTALLED PACKAGE, and it produces the
  most convincing wrong answer of the family: measuring `EVENT_FIELDS`
  across two dimll versions, a seat ran the comparison with the cwd
  inside an unpacked 2.9.4 wheel, so `import dash_improve_my_llms`
  resolved from the CURRENT DIRECTORY rather than site-packages — and
  two readings of ONE wheel were reported as two versions agreeing, in
  a CHANGELOG and a shipped spec (2026-09-01, corrected the same day).
  The load-bearing half was true and the supporting detail was
  invented. When comparing versions, `print(mod.__file__)` and assert
  it is the path you meant, or set PYTHONPATH explicitly and import in
  a fresh process per version. Live here: this repo's
  `dash_improve_my_llms` resolves to a DEV CHECKOUT at
  `/Users/pip/PycharmProjects/dash-hook-my-ai/`, not site-packages and
  not the requirements floor — which is exactly why item 10's rule
  says print the path beside the version.
- NAME THE CHECK THAT ACTUALLY RAN, not the one you meant to run
  (1.6.44 item 7). The general form: a report says which invocation
  produced the number, over how many files, and with what exit code,
  because "lint passed" is a claim about a COMMAND and everyone reads
  it as a claim about the CODE. The template's worked example does not
  reproduce on this fork — see the note-88 entry above, where the
  `docs/*/` exclusion claim is corrected — but the rule is the same,
  and here CI runs `py_compile sweep of docs/` as its own named step
  that FAILS on an empty corpus and prints the file count (100 today).
- A CD LANE THAT CALLS ci.yml MUST NOT ALSO LET ci.yml RUN ITSELF on a
  push to main (1.6.44 item 12). Both runs resolve to the concurrency
  group `ci-${{ github.ref }}` with `cancel-in-progress: true`, so one
  is killed at random; when the standalone run wins, CD's `test` job is
  CANCELLED, `deploy` skips, `release` never moves — and `main` ahead
  of `release` then reads as an ordinary pending push instead of as the
  accident it is. Detect: `ci.yml` declares `push: branches: [main]`
  AND `cd.yml` has `uses: ./.github/workflows/ci.yml`. THIS FORK HAS
  THE CORRECT SHAPE ALREADY (pull_request + workflow_dispatch +
  workflow_call) and the pin now lives in
  `tests/test_cd_promotes_release.py`. Writing that pin has its own
  trap: PyYAML parses an unquoted `on:` as the BOOLEAN True, so
  `workflow["on"]` raises KeyError on every workflow file, and a test
  that catches that and moves on asserts nothing at all.
- A FORK'S TRAPS SECTION DRIFTS BEHIND THE TEMPLATE'S SILENTLY (1.6.44
  item 14). The kit is contract-class, so a sync never copies it and
  nothing prints the gap: emojimart carried 7 entries against the
  template's 22, and its HEAD trap still held the diagnosis 1.6.32 had
  corrected — a fork can be reading, and acting on, a fact the fleet
  retired months ago. Detect, printed as a PAIR:
  `python3 scripts/kit_traps.py <template>/.claude/CLAUDE.md` reports
  `fork N / template M` and names what is missing. This fork's copy is
  ORIENTED THE OTHER WAY from the template's — the fork under test is
  this repo and the template is the argument, because on a fork the
  useful question is "how far behind am I?". Matching is by token
  overlap of the opening sentence, never exact text: a fork is EXPECTED
  to merge a trap into its own wording, so a strict check would report
  an adaptation as absence and train forks to paste over their
  adaptations. MERGED, NEVER INSTALLED OVER. And read the output with
  that looseness in mind — measured here 2026-09-05, `fork 24 /
  template 28` listed nine missing of which TWO were false positives
  this fork carries in its own words (the `release` build-proof trap
  and the resolved-version rule).
- A VERIFY VERDICT IS METERING EVIDENCE, NEVER SOLE AUTHORISATION (1.6.44
  item 18). A hub verdict says a key was presented and what the hub thought
  of it; on its own it is a claim from OUTSIDE this host. A route may act
  on it only where a HOST-HELD SECRET anchors the answer — here
  `CROSS_APP_WEBHOOK_SECRET`, without which `hub_client.enabled()` is False
  and `verify` returns "gated" before any network call, so a forged `?key=`
  opens nothing. Name that secret beside any route consulting `verify` for
  access, or document the route as metering-only. `lib/access.check` is
  this fork's one such call site and now names it.
  Three sub-rules, each learned from a way the pin can be present and
  useless:
  * SOURCE-PIN THE CLOSED FALLBACKS, do not merely exercise them. A
    behavioural suite cannot see a default restored ABOVE its own guard —
    put `return "allow"` as the first line of `verify` and every mocked-hub
    test still passes, because none of them reaches the code it believes it
    is testing. Walk the AST and assert every literal return is the closed
    verdict, plus one non-literal return so "gated always" cannot pass.
  * PIN THE GOOD ROWS BESIDE THE BYPASS ROWS. "deny stays denied" passes on
    an implementation that denies everything, which is a different outage
    rather than a fix.
  * REJECT CASE AND WHITESPACE LOOKALIKES OF A TIER, not one literal. A
    tier from the hub arrives over the network and is NOT the validated
    value a local registration produces: `hub_tier not in ("auth", "admin",
    "hidden")` answers True for "Auth", " auth " and "auth\n" alike, and
    every one of those leaves a machine lane OPEN on a page the network
    restricted. Found live here 2026-09-05, both hub-tier reads in
    `lib/access.py`; `page_tiers.normalize_tier` returns "" for a non-tier
    so an unrecognised value can never propagate as though it were one.
- A PROXIED robots.txt IS NOT YOUR robots.txt (1.6.44 item 19). The file a
  crawler receives is whatever the EDGE chose to serve, and a CDN may
  manage it. Two shapes, both invisible to a battery that fetches the URL
  and looks for its expected lines: an INJECTED STANZA (rules the app never
  wrote — additional, so nothing is missing) and a MARKER WITH NOTHING
  UNDER IT (a managed block adding no rule — so nothing is missing
  either). The check must therefore be TWO-DIRECTIONAL: every directive
  the app writes is served, AND every directive served is one the app
  writes. Generate the app's side through the PACKAGE'S OWN
  `generate_robots_txt` with the registered config — a reimplementation
  compares the edge against your BELIEFS about the config and agrees with
  the wire exactly when both are wrong the same way. `ai_bot_posture` in
  `scripts/network_smoke.py`; the config is declared once in
  `lib/robots_expected.py` and run.py reads it from there.
  TWO TRAPS INSIDE THE TRAP, both hit here on the first live run:
  * THE ROW NEEDS THE APP'S DEPENDENCIES INSTALLED BESIDE IT. CD's verify
    job did checkout + setup-python and no install, so the generator was
    unimportable and the row would have SKIPPED FOREVER — green, having
    compared nothing. cd.yml now installs requirements before the battery.
  * COMPARE ONLY AT THE SAME PACKAGE VERSION. The expectation is generated
    by the dimll resolved where the battery RUNS; the served file by
    whatever the deployed image resolved, and a `>=` floor lets those
    differ legitimately. Measured 2026-09-05 against production: the row
    reported `content-signal: search=yes, ai-input=yes, ai-train=yes` as
    MISSING — a directive 2.10.0 emits and the deployed build's older
    version does not. Version skew, not a proxy, and reporting it as one
    sends somebody hunting a CDN that is doing nothing. `llms_version` on
    `/healthz` (item 1) is the discriminator: absent or different -> SKIP
    and say which versions; equal -> a difference can only be the edge.

