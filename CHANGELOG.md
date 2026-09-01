# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Internal traffic stops counting itself in the read ledger

Sync 1.6.43, ported into this fork's shape.

#### Fixed

- **The network's own probes were the busiest "vendor" on this host's
  ledger.** `AnalyticsTracker.record_read` — the hook that keeps a row for
  every corpus document served — never applied the internal-traffic drop
  that `track_visit` has always applied. So the hub's hourly health sweep,
  every link audit and every post-deploy battery landed in the `reads`
  table and rode the daily rollup to the network board. "Counted nowhere"
  now includes the read table. The drop keys on the event's `ua` field,
  which is what the package calls it — a drop keyed on `user_agent` would
  be a silent no-op, so a test asserts the field name against the resolved
  wheel rather than trusting the spec.

#### Recorded

- `vendor_class` joined the package's read-event fields between 2.9.0 and
  2.9.4. `lib/traffic_rollup.py` already read it, so the rollup's vendor
  `class` column starts carrying real values rather than nulls, with no
  code change here.

### The 1.6.41 remainder: short sidebar labels, a skip link, dated pages

Sync item 18, ported into this fork's shape.

#### Added

- **Short sidebar labels.** Pages declare `nav:` in frontmatter, so the
  sidebar reads "Basic / Dataset Mode / Stacking" under BARCHART while each
  page keeps its full name in `<title>`, `og:title` and its llms.txt
  heading. This restores exactly what the retired FAMILIES map showed —
  the 35 labels were taken from it — and closes the redundancy the previous
  round introduced by rendering `name` in the sidebar.
- **A skip link.** The first tab stop jumps past the sidebar's ~45 stops
  straight to the content, visible only on keyboard focus.
- **`/api` and `/changelog` are dated.** Both entered the sitemap with no
  `lastmod`: `/api` now declares one in frontmatter, `/changelog` derives
  it from the newest dated release heading in `CHANGELOG.md`.
- **Header identity moved to `lib/constants.py`** (`LOGO_ASSET`,
  `LOGO_STYLE`, `WORDMARK`, `WORDMARK_COLOR`, `WORDMARK_VISIBLE_FROM`), so
  a fork edits the identity block rather than the component.

#### Fixed

- **A prose section counted as a release.** The upstream changelog parser
  was widened to accept bare `## 2.0.0 — date` headings, and the widening
  swallowed free text: this file ends with `## Component License
  Requirements`, which rendered a timeline card badged with that whole
  sentence and made the page claim 15 releases where there are 14. A
  release label is now bracketed, a version, a date, or Unreleased.
- **The deploy battery's hidden-path list had drifted.** It probed
  `/admin/control-board` plus two paths this app has never had, and never
  learned about `/admin/traffic` — a 404 for a page that does not exist is
  not evidence that a page is hidden. Pinned against the page registry.

#### Recorded

- The corpus sweep for admin paths found six pre-existing mentions in
  `/llms-full.txt`, all from this changelog's own prose in code spans and
  none of them links. The pin distinguishes a linked, reachable URL from a
  changelog naming what it changed.

### The wall comes down, and navigation comes from one registry

Sync items 15 and 16 from the template's SYNC-1.6.22-1.6.38, ported into
this fork's shape alongside items 12 and 13 below.

#### Changed

- **Training crawlers are allowed.** `block_ai_training=False`: GPTBot,
  ClaudeBot, CCBot and the rest now get the browser document, `/healthz`
  and no `Disallow` in robots.txt, the same as every other bot. The wall
  decided by vendor CLASS what nobody could account for; since the ledger
  round every corpus read is a row and the hub reconciles it against the
  wire, so a read is recorded and priceable. The tool from here is
  per-vendor — `vendor_policy={"<key>": "block"|"meter"}` for one vendor
  whose rows justify it — never the class. Measured in-process before and
  after: ClaudeBot and GPTBot on `/`, `/llms.txt`, `/healthz` went
  403/200/403 → 200/200/200. The wire before the flip was that same
  403/200/403, so every 403 this host ever served was the app's own
  middleware; there is no edge rule in front of it.
- **The sidebar is built from the page registry, not a hand-written map.**
  `components/navbar.py`'s FAMILIES list is gone; each page declares
  `category:` and `order:` in its own frontmatter and
  `lib/constants.CATEGORY_ORDER` names the section order. The rendered
  sidebar is unchanged — same families, same sequence — but a new page now
  arrives in the right section by describing itself, instead of by
  remembering to edit a second file. `components/navbar.py`,
  `components/footer.py`, `pages/changelog.py` and `lib/aside.py` are
  byte-identical to the template's now.
- **Admin pages are hidden from navigation, not merely blocked.** The
  Admin section used to ship in every anonymous page's DOM with
  `display: none` and a callback to reveal it. It is now an empty
  placeholder that a server-side callback FILLS for an admin — so the
  admin URLs are not in the anonymous document at all. `/admin/traffic`
  gains its first nav link in the same change.
- **`/changelog` is a Timeline.** Parsed from `CHANGELOG.md` at render
  time, one card per section, and the file itself (minus its duplicate H1)
  is the page's `LLMS_DOC` — which also retires the "1 page have no
  LLMS_DOC source" warning this app printed at every boot.
- **The top bar's GitHub icon, JSON-LD `sameAs` and the Resources block
  read one constant** (`GITHUB_URL`). The "More Dash components" link to
  `pip-install-python.com` is retired — the domain has been out of the
  network directory since the retire sweep and this header was still
  sending readers there.
- **Resources is third-party only**: `dmc` and MUI X Charts. The Dash
  Community forum, the `2plot.dev` link and the "Pip Components" section
  are gone; the network is listed once, in the new **Other Apps** menu in
  the top bar, built from `lib/network_directory.PRIMARY` so it cannot be
  listed twice or drift from the registry.

#### Added

- **A footer** — © year, the GitHub profile, Discord and YouTube, every
  icon with an accessible name.
- **`/admin/traffic` gains a People section** with the day's human hits,
  visitors, sessions and median session, above the crawler tables and
  labelled: humans never enter the read ledger, so "(unidentified)" there
  is the UA-less crawler lane and never a person. Its day picker is a
  `dmc.DatePickerInput` bounded by the ledger's own first and last day.
- **Accessibility**: the code blocks' copy button and every icon-only
  control in `components/` carry names; `tests/test_nav_contract.py` greps
  for the next one that does not.

#### Fixed

- **`/api` served thirteen headings and zero property rows to everything
  that does not run JavaScript.** `.. kwargs::` is a markdown2dash
  directive, and a directive renders Dash *components* — so its tables
  existed only in the browser's React tree. The machine lane
  (`/api/llms.txt`, the crawler document) and the non-JS prerender are all
  built from the page's markdown *source*, where the directive line is
  stripped. Measured on the wire: `/api/llms.txt` 2681 bytes with no table
  rows, the prerender with no `<table>`, while a real browser's rendered
  DOM showed 13 tables and 371 rows. Verified on the wire after the fix:
  `/api/llms.txt` 59967 bytes carrying all 371 properties, and 13 tables
  with 384 `<tr>` (371 data rows plus one header each) in the crawler
  document and the prerender alike. On the one page whose whole purpose is the prop
  list, every agent and every crawler got nothing. `pages/markdown.py` now
  expands `.. kwargs::` into a markdown table exactly as it already did for
  `.. source::`, and both the directive and that expansion read ONE parse
  in the new `lib/api_reference.py` — all 371 properties in every lane,
  with a test that fails if the two ever disagree.

- **Both live batteries were reading the wrong document.**
  `scripts/network_smoke.py`'s default User-Agent was the bare internal
  token, which at dash-improve-my-llms 2.8 has no browser engine token and
  is therefore crawler-lane — so every default-UA check read the
  prerendered crawler document rather than the page a visitor gets. It now
  leads with a real Chrome/AppleWebKit token and keeps the internal token
  after it (a substring match, so this host's traffic is still counted
  nowhere on the far side); `CRAWLER_UA` is the other lane and is
  unchanged. `scripts/smoke_live.py` already had that shape and now has a
  test holding it there. The same rule reaches `scripts/route_parity.py`,
  whose in-process sweep feeds a CI gate.

- Code blocks inside a list item, blockquote or timeline row could widen
  the whole document at phone width. One stylesheet rule for every
  container a code block can sit in, never a per-page override.
- The mobile drawer is `keepMounted` — the hamburger no longer depends on
  a mount-on-open transition, and the Admin callback's mobile target
  exists on every load.
- The right-hand aside is collapsed on pages that render no `.. toc::`
  (`/changelog`, home, the admin pages), which were rendering in the docs
  column beside an empty gutter.
- The Other Apps dropdown gets a solid themed background; it was
  near-transparent in dark mode.

### The ledger row, and a branch only CI can write

Sync items 12 and 13 from the template's SYNC-1.6.22-1.6.35, ported into
this fork's shape (see `DIVERGENCES.md` for where the shapes differ).

#### Changed

- **`human_hits` DROPS and `bot_hits` RISES from the first deploy after
  this.** `lib/analytics_tracker.py` no longer carries its own User-Agent
  list; it delegates to `dash_improve_my_llms.classify()`, the same vendor
  registry `robots.txt` is already rendered from — so what this site SAYS
  about a vendor and what it COUNTS finally agree. The old list filed
  ClaudeBot (Anthropic's *training* crawler) under "search", still named
  the retired `anthropic-ai` / `claude-web` tokens, and counted every
  UA-less or library client (`httpx`, `Go-http-client`, `node-fetch`, an
  empty User-Agent) as a person. Those clients move from human to crawler.
  The hub's day-over-day view will show a step: that is the number
  becoming true, not a regression.
- **An absent User-Agent is a crawler now.** The same flip bit this repo's
  own tooling before it bit the numbers: `scripts/route_parity.py` probed
  every route with no UA, so from the moment dash-improve-my-llms 2.8.0
  could resolve, `scripts/smoke_test.py` — a CI gate — reported
  `/admin/control-board: 404`, the package's hidden-path answer to a
  crawler, with nothing about the app changed. The sweep now sends the
  same `BROWSER_UA` `tests/conftest.py` does. (The template hit this in
  `tests/test_proxy_scheme.py`, a file this fork does not carry.)
- **`main` is no longer a deploy.** Render deploys the `release` branch,
  and only `cd.yml`'s `deploy` job writes it — a fast-forward push of the
  run's own sha, after the CI matrix is green. The Render deploy-hook step
  is gone; its repository secret is inert. A push to `main` whose CD run
  is red or still running leaves `release` where it was, and production
  with it. `verify` now runs only on `needs.deploy.result == 'success'`
  and asserts `/healthz build == github.sha` itself, which retires this
  fork's own weaker `!= 'skipped'` divergence.

#### Added

- **The read ledger.** dash-improve-my-llms 2.8.0's `on_document_read`
  hands this app one row per corpus document it serves — tier, verdict,
  bytes, verified vendor — and `AnalyticsTracker.record_read` keeps it as
  a `reads` table in the same analytics file, same buffer, lock, flush
  cadence and retention as `visits`. It is a second table JOINED by the
  rollup, never summed into `human_hits` / `bot_hits` / `pages`, and the
  client address is dropped unless `ANALYTICS_KEEP_CLIENT_IP=1`.
- **Rollup v4.** `daily_rollup` gains `vendors[]` (one row per vendor ×
  verified × policy, with per-tier counts and bytes, capped at 40) and
  `reads`, present only on a day that had reads. Every v3 key is
  byte-identical; the reporter is unchanged.
- **`/admin/traffic`** — this host's own ledger: vendor × day, vendor →
  tier, top paths per vendor, and the v3 headline numbers for the same
  day. Behind the control board's exact gate, fails closed without Clerk,
  hidden from every machine surface, plain tables and no charts. The page
  says on its face that `verified: n/a` is a property of the vendor
  (Anthropic publishes no IP ranges, so ClaudeBot is always n/a) and not a
  defect on this host.
- **`DIVERGENCES.md` now carries a posture fence** declaring what this
  host serves, measured with a real vendor UA rather than assumed.

#### Floors

- `dash-improve-my-llms>=2.8.0` in `requirements.txt` (the Docker cache
  bust), `run.py`'s boot floor, and both version assertions in `ci.yml`.

### The card X can read, and one fleet Python

- **`twitter:card` is declared where a scraper can see it again.** Dash
  emits the card type with `property=` (hardcoded in `dash/_pages.py`);
  X's parser predates the Open Graph convention and reads `name=` only.
  `templates/index.html` had been trimmed of the template's `name=` line
  as a duplicate, so from 2026-08-24 to 2026-08-26 every page on this site
  offered X no card type at all — the image, title and description were
  all present and the card still could not render as a large image. The
  same wrong rule was encoded in THREE places and all three had to move:
  two assertions in `tests/test_social_card.py` (which is what required
  the deletion), and `scripts/check_release.py`'s restated-tags gate
  (which then blocked the fix from shipping). `twitter:title` and
  `twitter:description` stay listed on purpose — X falls back to the
  `og:*` set for those, and does read it. Only the card TYPE has no
  fallback.
- **`tests/test_smoke_live.py` exists.** The post-deploy battery has run
  in CD for months with nothing exercising it locally, which is how a new
  crawler/browser identity-parity check landed byte-perfect and found the
  card defect on the wire instead of in the suite. The script now runs
  against the in-process app on every test run; deleting the meta tag
  reproduces all four production failures locally.
- **Production moves off Python 3.11.** `render.yaml` declares
  `runtime: python`, so Render's native runtime builds this service from
  `requirements.txt` and never reads the Dockerfile — which meant the
  3.14-slim image bump certified CI while visitors kept getting
  `PYTHON_VERSION: "3.11.12"`, with a third opinion (3.12) in the CI site
  lane. All four encodings now agree on 3.14: render.yaml `3.14.7`, the
  site lane in `ci.yml`/`cd.yml`, and the image. `/healthz` gained a
  `python` field so the serving interpreter is visible from outside for
  the first time, and `tests/test_python_version.py` holds the encodings
  to the Dockerfile's `FROM` tag. The wheel's own `requires-python`
  window (3.9-3.13, in `package-python-range`) is a separate question and
  is deliberately untouched.

### Floor round — dimll >=2.7.1, healthz tells the truth, one h1 per page

- **dash-improve-my-llms floor 2.6.1 → 2.7.1**, moved in every encoding:
  requirements.txt (with its three commented backend extras), run.py's
  `LLMS_PKG_FLOOR` tuple and the boot-floor message ladder, and both CI
  asserts including the one inside the built image. The requirements line
  changing **is** the Docker cache bust — the dependency layer re-runs only
  when those bytes change, so a code-only commit can never pull a new
  release. What it buys: 2.7.0 dedups the prerender's H1 and the home
  footer's doubled /llms.txt link and hardens the idempotency probe; 2.7.1
  adds the llms.txt v2 discovery relations + Link headers, the text/plain
  Accept ramp, and the representation digest.
- **`/healthz` is built per request and says who answered** (template
  1.6.10): `app` (SATELLITE_APP_KEY, else "unknown"), `build` (the running
  commit), and — on dimll >=2.7.0 — `geo` {configured, denied, resolved},
  counts and flags only, never the denylist's country codes. The key is
  omitted on older packages rather than error-flagged, which makes its
  ABSENCE in production the fleet's stale-image alarm. The payload used to
  be a snapshot closed over at registration: harmless while every field was
  static, and wrong the moment one is not.
- **`build` replaces this repo's `commit`.** The CD build-match wait
  (2026-08-21) shipped here first under the name `commit`; the template
  adopted the idea under the fleet's name, so cd.yml moves with it. The
  wait's one-time fallback covers the deploy where the running build still
  answers the old key.
- **Every page serves exactly one `<h1>`**, pinned across all 41 routes on
  the generic lane. The pin found three: `/tree-basic`, `/tree-pro` and
  `/tree-simple` each carried a body-level `# TreeView`-style heading
  duplicating the page title, preceded by a stray `\` that rendered as a
  literal backslash paragraph. Demoted to `###` — matching every other
  heading on those pages, and now carrying a TOC anchor like the rest.
- **The source expansion is fence-aware** (template 1.6.11): a
  `.. source::` inside a fenced block is documentation, not a directive.
  Preventive here — no page teaches the directive today, measured — but the
  first one that did would have closed the fence early and rendered an
  inlined Python file as markdown on the machine lane.
- **Dependabot config added** (the template's, verbatim): pip
  version-updates restricted to `dash*`/`plotly*`/`markdown2dash`, the
  network drift alarm, without the floor-raise noise on every other pin.
- The Dockerfile gains the cache-semantics comment block. It has never had
  a Node layer to drop — the component bundle is committed.

### Round 3 — hashed selectors extinct, wide tables contained

- **The three hashed `m_*` fossils are gone from `assets/main.css`**, each
  audited against the INSTALLED DMC 2.8 bundle first rather than on the
  template's say-so: `m_46b77525` is Input.Wrapper's root (live in 2.8,
  where Mantine gives it only `line-height`) and this rule added an
  `!important` top margin to all 77 Input-family components across 7
  routes; `m_5caae85b` has **zero** occurrences in 2.8 — dead, matching
  nothing; `m_9cdde9a` is AppShell's `aside` (confirmed from the bundle's
  own class map) and four of its five declarations restated Mantine's own
  rule verbatim. The fifth — a 15px breathing gap above the Table of
  Contents — was real intent and moved to the static
  `aside.mantine-AppShell-aside` rule beside the z-index override. A
  tombstone names all three hashes **without** the leading dot, so
  `grep '\.m_'` over `assets/` finds live selectors only.
- **`tests/test_css_hygiene.py`** ported byte-identical from the template:
  it strips comments (tombstones may name hashes) and fails on any hashed
  selector in `assets/*.css`. Verified to have teeth against a planted
  `.m_deadbeef`.
- **Wide tables scroll in their own box** (`display: block; width:
  max-content; max-width: 100%; overflow-x: auto` — GitHub's recipe, a
  no-op for tables that already fit). The template's `table.m2d-table`
  selector would have been a **no-op on this site's widest content**:
  markdown2dash derives each class from the renderer that emitted it, so
  the `.. kwargs::` directive's output is `m2d-block-kwargs`, and /api is
  13 generated prop tables of which not one is an `m2d-table`. The rule
  covers both classes here; measured against the real layout trees, 14 of
  the site's 25 tables now match. The other 11 are hand-authored demo
  tables inside example modules with no class at all — deliberately left
  alone, since `display: block` would restyle demo content.

### Round 2 — the prerender becomes readable, and stops repeating itself

- **dash-improve-my-llms floor 2.6.0 → 2.6.1**, and the floor is
  load-bearing: below it the injected prerender div carries a literal
  `hidden` attribute, so every visibility-respecting consumer — html-to-text
  extractors, text browsers, arguably crawler content weighting — read
  "Loading..." and nothing else. 2.6.1 serves the block visible and hides it
  with a synchronous inline script only JS browsers run (React's mount wipes
  the pair, so nothing changes for a human). The floor moved in all four
  places it lives: requirements.txt with its commented backend extras,
  run.py's `LLMS_PKG_FLOOR` and its boot message, and both CI assertions
  including the one inside the built image.
- **The hand-written `<noscript>` block is retired** — 175 words, and the
  same 175 on all 42 routes. `/pie` told a non-JS reader about
  SparklineChart and never said what a Pie Chart is; an outside SEO audit
  read that duplication as this host being the only one in the fleet that
  prerendered. It goes in the SAME deploy that brings 2.6.1, deliberately:
  no window exists where a non-JS reader loses the noscript without gaining
  the visible prerender. Its two tests moved with it rather than being
  deleted — the component count is now asserted inside the home page's
  visible prose, and `tests/test_prerender.py` pins the div's shape (present
  for a PLAIN client, no `hidden`, marked hide script, `<main>` prose) plus
  the thing the block was mistaken for: two different routes must not
  prerender the same paragraph.
- **`lib/network_directory.py` re-copied verbatim** from the template
  (1.6.6): modelviewer.2plot.dev and excalidraw.2plot.dev joined the
  canonical directory when they went live in the gate wave. 18 peers.
- **The apple-touch icon is opaque.** The gate wave generated the favicon
  set with the pre-fix `make_favicons.py`, so this site shipped an RGBA
  apple-touch icon for a day — iOS composites alpha onto its own background,
  black on some surfaces and white on others, so it rendered differently
  everywhere it appeared. The template fixed the script at the source; it is
  re-copied, the icon regenerated (it was the only one of the eight that
  changed), and `tests/test_seo_icons.py` now reads the PNG colour type out
  of the header to pin it.
- Discord/WidgetBot: **nothing to remove.** The crate was deleted in the
  1.4.0-era pass (run.py, requirements, render.yaml); this sweep confirms
  zero references in any code, config, template or asset. The README's
  Discord links are community links, not the retired integration.

### Gate wave — the sign-in gate, the control board, one stable icon

The docs site's half of the network's gate wave (batch 1: template sync +
the Clerk env block). **Ships DARK**: `PAGE_DEFAULT_TIER=public`, so every
page reads exactly as before and the flip to `auth` is one environment
variable, no code change, no redeploy. The component library is untouched —
no wheel change, no version bump.

- **The interactive gate** (`lib/gate_layouts.py`, `lib/access.py`,
  `lib/page_tiers.py`): every markdown page's layout is wrapped in a
  per-render verdict. With all tiers public the verdict is a dict lookup
  that always allows, so nothing changes until the env says so.
  `scripts/route_parity.py` measures the wrap as invisible: 195 chart
  mounts and 41 page trees identical, byte for byte.
- **The control board** (`/admin/control-board`, `lib/page_visibility.py`):
  flip any page between public/auth/admin/hidden and toggle its llms.txt,
  live, no redeploy. Fails CLOSED without Clerk, is excluded from the
  sidebar and both search fields, and its own Admin nav link is hidden
  until the server recognises an allowlisted account.
- **`/api/agent-key`** (`lib/agent_key.py`): the person→agent handoff — a
  signed-in reader's "copy llms.txt link" now carries a key that works when
  pasted into an assistant with no cookie. 204 for everyone until Clerk and
  the hub are configured.
- **Presence beacon**: `lib/satellite_reporter.py` gains the ~60s
  `{app, active}` ping the hub board's "live now" column reads. Display-only
  and ephemeral; the daily rollup stays the source of the numbers.
- **ONE stable identity for crawlers.** The per-load area/bar favicon
  randomizer stays for browser tabs — but `configure_seo(icons=[...])`, the
  head links and `assets/favicon/site.webmanifest` now all declare the same
  generated area-chart set, and `tests/test_seo_icons.py` pins that dimll
  2.6's autodiscovery finds exactly that set. The duplicate
  `favicon_areachart.ico` is gone; `apple-touch-icon_areachart.png` is the
  master everything regenerates from.
- **Floors**: dash-improve-my-llms >= 2.6.0 (sitemap `<lastmod>` is emitted
  verbatim or omitted — never invented), dash-mantine-components >= 2.8.0
  (below it the mobile drawer renders as a floating card), vendored
  dash-clerk-auth 1.0.5, sha-verified in `scripts/check_release.py`.
- **pip-audit now GATES** (`continue-on-error` removed): with
  clerk-backend-api >= 7 and cryptography >= 50 the baseline is quiet, so a
  red audit means something new instead of the same four capped advisories.
- Accessibility: every icon-only control carries an `aria-label`
  (`create_link` now requires one). `aria-label`, never `title=` — DMC 2.8
  raises on `title` during app construction.

## [1.4.0] - 2026-08-03

### Boilerplate migration — M5 (API reference)

- **NEW `/api` page**: every prop of all 13 components as tables generated
  from the components' own metadata via the `.. kwargs::` directive — they
  can never drift from the installed version. Enabling fix in
  `lib/directives/kwargs.py`: the numpy-style override (built for
  dash-mantine-components docstrings) shadowed markdown2dash's own parser
  for `dash-generate-components` docstrings, so dash-built components
  rendered EMPTY tables; the hook now falls back to the base parser when
  it sees "Keyword arguments:". Navbar gains a Reference section; route
  count 40 → 41 (both parity baselines re-recorded deliberately).
- **Home stays the bespoke Python page** it already was — it mounts no
  charts, carries the brand/install/catalog and a full LLMS_DOC, and
  per-satellite custom homes are the network norm. Changelog likewise
  stays a Python page (its disk read is exercised by the suite on every
  run).

### Fixed — tree rendering under the boilerplate shell (owner review)

- **TreeView and SimpleTreeView now follow the theme toggle** — both
  components gained the `data-mantine-color-scheme` watcher +
  MUI ThemeProvider that TreeViewPro and TimeClock already had, so
  checkboxes, icons and edit fields switch with light/dark mode instead
  of rendering in the light palette everywhere (component fix in
  src/lib/components, bundle + wrappers rebuilt; wrappers regenerated on
  the current dash-generate-components, gaining its dash≤4.1 compat shim).
- **Trees no longer overflow their fixed-height boxes** — the
  boilerplate's global markdown list styling (`ul/ol` and `li` margins in
  assets/main.css) leaked into MUI's nested ul/li tree DOM, inflating
  every tree's height (a `height=200` tree bled into the next section on
  /tree-icons). Neutralized inside tree roots via assets/dark-mode.css;
  upstream, the boilerplate rule should arguably be prose-scoped.
- The /tree-icons SX demo's hardcoded light `#f8f9ff` background became
  `var(--mantine-color-default)` — it was unreadable in dark mode.
- **The `height` prop now actually contains the tree** (TreeView and
  SimpleTreeView): a fixed height previously sized the wrapper only —
  block children grow past a fixed-height parent and divs don't clip, so
  the tree rendered full-length over the next section. `height` now
  implies `overflow: auto` on the wrapper, making the /tree-icons
  "Fixed Height with Scroll" demo do what its title says.

### Boilerplate migration — M4 (TreeView + Date & Time Pickers)

- **Ten more pages markdown-driven** — the eight TreeView pages (basic,
  simple, selection, expansion, editing, icons, disabled, and the Pro
  page with its live license-posture badge kept) and both pickers
  (`/time-clock`, and `/time-clock-lab` with its liquid-glass styling
  intact). Whole-page transforms, ids and callbacks verbatim; the four
  existing LLMS_DOC bodies folded into their md pages. Only home and
  changelog remain in pages/.
- **The dogfooding story returns as content**: `/tree-simple` gained a
  sidebar demo built FROM `components/navbar.py`'s real family map — a
  SimpleTreeView that genuinely navigates these docs, exactly as the
  pre-migration shell's sidebar did (it can never drift from the actual
  nav because it is generated from it). Chart baseline deliberately
  re-recorded: 195 mounts, 79 chart-touching callbacks.

### Boilerplate migration — M3 (the LineChart batch)

- **Twelve more pages markdown-driven (38 of 40)** — the seven LineChart
  pages (basics, Pro, brush, reference lines, highlighting, ticks & hover,
  zoom preview), `/highlighting-sync`, `/crosshair`, and the three
  CompositeChart pages. The batch's 7,550 lines ported as whole-page
  transforms — one `demo.py` exec module per page, every id and all ~50
  callbacks verbatim (the sync-tooltip overlays, the crosshair alert
  system and the render-BP LoadingOverlay dashboard included) — with md
  wrappers carrying frontmatter, overview prose, and the two existing
  LLMS_DOC bodies folded in. Per-section md granularity for this family is
  deliberately deferred to a content pass; the format, metadata, TOC/ad
  asides and real llms.txt documents are all in place now.
- **Every Pro route now explains the key requirement in-page**
  (BANNER_ROUTES == PRO_ROUTES): the twelve md files carry the Pro
  admonition naming MUI_PRO_API_KEY, so silent degradation to a
  watermarked chart with no explanation is no longer an allowed posture —
  the test asserts it stays that way.
- Transform bugs the gates caught before runtime: the module cut point
  matched `from dash_mui_charts import` inside LLMS_DOC code fences
  (syntax error), prose lines starting with "from " were harvested as
  imports, the banner-block strip went one line too deep on the two
  banner pages, and two pages lost the `import dash` their callbacks use
  (F821). All fixed; flake8 and chart parity green.

### Boilerplate migration — M2 (BarChart + Candlestick + LiveTrading)

- **Eight more pages markdown-driven** (26 of 40): the six BarChart pages
  (`/barchart-basic` 6 examples, `/barchart-dataset` 3, `/barchart-stacking`
  5, `/barchart-interaction` 5 incl. the click/axis-click/highlight
  callbacks, `/barchart-reference` 6, `/barchart-pro` 3 Pro zoom demos with
  the license-posture line in the first), `/candlestick` (7 examples over a
  shared OHLC generator; the never-rendered 60-candle dataset dropped as
  dead code), and `/live-trading` (the whole simulator — 11 callbacks —
  transformed as one exec module; the redundant View Code block replaced by
  `.. source::`). Chart parity GREEN throughout.
- **Directory naming rule learned**: families whose examples import shared
  `_data.py` need UNDERSCORE directories (`docs/barchart_basic/`) — a
  hyphenated package can be exec'd via importlib but cannot be
  sibling-imported (`from docs.barchart-basic._data import x` is a syntax
  error). Endpoints are unaffected (frontmatter owns them).
- `/live-trading` joined BANNER_ROUTES: its markdown now documents the
  MUI_PRO_API_KEY requirement permanently (Pro admonition +
  functions-as-props note) rather than only when the key is missing.

### Boilerplate migration — M1 (Pie + Heatmap + Scatter)

- **Five more pages markdown-driven** (18 of 40 routes' chart content now
  under docs/): `/pie` (6 exec examples), `/pie-props` (Titanic nested-pie
  playground, transformed whole), `/scatter` (7 examples sharing a
  seeded `_data.py` so every point cloud renders exactly as before),
  `/heatmap` (7 Pro examples + the color-scale reference as a real
  markdown table), `/heatmap-props` (Pro playground, transformed whole).
  Same endpoints, chart ids and callbacks throughout — chart parity GREEN
  against the pre-migration baseline.
- **Pro degradation tests pinned by ROUTE, not source file** — the
  migration moves key-reading code from pages/<x>.py into docs/ exec
  modules, but the route's obligation to degrade (banner or unlicensed
  chart, never a traceback) doesn't move. 17 Pro routes, 6 banner routes,
  set-equality both ways.
- Transform fix caught by lint: the heatmap-props port had dropped its
  `json` import (cell-click display would have crashed); restored, plus
  inherited f-string debt cleaned rather than carried into docs/.
- The stale "0.0.8" release banner on the Scatter page retired; its
  llms.txt placeholder stubs (both props pages) became real documents.

### Boilerplate migration — M0 (shell + chart-parity gate + Sparkline pilot)

- **The docs app now runs on the dash-documentation-boilerplate structure**
  (model: dash_pannellum): `run.py` entry point (gunicorn `run:server`),
  `components/` appshell/header/navbar, pluggable-backend plumbing (Flask
  enforced until the analytics hooks grow async twins), dependency floors
  at boot, optional Clerk (vendored 0.9.1, dormant without keys), proxy
  scheme fix, optional Dash MCP, and `pages/markdown.py` serving
  `docs/**/*.md` with frontmatter, TOC asides, `.. exec::` live examples
  and per-page llms.txt built from the markdown body.
- **Chart parity replaces exact-tree parity as the migration gate**
  (`scripts/route_parity.py --charts-only`): route set, per-route
  dash_mui_charts census, chart component ids, and the 78 chart-touching
  callbacks — recorded from the pre-migration app and GREEN after M0: all
  40 routes, 194 chart mounts identical.
- **SparklineChart family ported to markdown** (`docs/sparkline*/`): 3 md
  pages + 11 exec example modules, callbacks verbatim, same endpoints. The
  three placeholder llms.txt stubs became real documents for free.
- **The docs stack moves to Dash 4.4 / dmc 2.7** (requirements.txt;
  markdown2dash installs `--no-deps` against its gunicorn<22 pin, mistune
  listed explicitly — LESSONS §8). The dash_mui_charts PACKAGE floor is
  unchanged (dash>=3.3).
- **Ad client returns to the canonical boilerplate copy** — per-page aside
  slots served by the mount-fired MATCH callback, `AD_APP_ID=muicharts`.
  The floating-slot fork (and the double-impression bug it dodged) retired
  with the static shell that caused it.
- **Old shell retired**: SimpleTreeView sidebar (nav is now the grouped
  boilerplate navbar; the dogfooding story moves into the TreeView docs in
  M4), `00-loading-theme.js` + `01-nav-restore.js` (they fought the new
  color-scheme system / targeted the removed tree), the dead
  license-key-store. `dcc.Location(id="url")` and the SPA analytics
  counting rule carry over unchanged; the header keeps the
  `header-avatar` favicon-swapper contract and the package-version badge.
- Tests updated for the new shell (80 passing, zero secrets): navbar
  family map ↔ registry parity, per-page aside ad slots, old-shell assets
  stay deleted; identity/card/version/traffic suites unchanged.
- **M0 owner-review fixes**: the boilerplate's `main.css`/`m2d.css`/
  `llms_copy.js` now ship in assets/ (their absence left the theme toggle
  showing sun AND moon, and nav links unstyled); the navbar renders the
  old sidebar's SHORT labels with per-item icons ("BARCHART / Basic", not
  "BARCHART / Bar Chart - Basic") from a (path, label, icon) map; the
  stale "(0.0.8)" dropped from the Scatter page's display name; the
  Discord WidgetBot crate removed entirely (run.py, requirements,
  render.yaml); `.claude/` is untracked and gitignored (owner request —
  session plans and screenshots live outside version control now).

### Network-standard pass — Phase 4 (deploy cutover, repo side)

- **render.yaml declares the cutover**: `domains: [muicharts.2plot.dev]`
  plus every env var the app reads (`APP_BASE_URL` and `AD_APP_ID` with
  their canonical values, `NETWORK_BULLETIN_URL` pointing at the hub feed,
  `WIDGETBOT_*` optional, the existing secrets). LESSONS §10 caveat is in
  the file itself: blueprint envVars apply on Blueprint SYNC, not git-push
  autodeploys — every value must also be set on the SERVICE in the Render
  dashboard.
- **Not applicable here**: the Clerk satellite env from STANDARD §9 — this
  app ships no auth surface (no dash-clerk-auth anywhere); nothing to
  configure until it ever gains one.
- **Owner actions remain before go-live** (deliberately not automatable):
  upload `build/social-cards/muicharts.2plot.dev.png` to
  cdn.2plot.ai/github_assets/ and verify 200 + IHDR 1200×630 (the HARD
  GATE — smoke_live fails the deploy while it 404s, by design), set the
  service env, attach the subdomain + DNS, merge to main, then hub-side
  STANDARD §9 in pip-docs+ (promote shipping→live, VERIFIED_APP_IDS).

### Network-standard pass — Phase 3 (tests + CI/CD)

- **tests/ populated (80 tests, ZERO secrets by design)** — the suite runs
  exactly as CI's secretless container does, proving the degraded postures:
  the 17 MUI Pro pages fall back to license banners instead of dying, the
  traffic reporter stays dormant, the bulletin stays off. Files: site
  identity (one brand, every surface), social card (per-page image_url +
  description, template division rules, the placeholder-in-comment trap),
  **version parity** (the fix for the five-way version drift: package.json ↔
  package-info.json ↔ header badge ↔ JSON-LD ↔ noscript, and no surface may
  claim "9 components" again), route smoke + preservation invariants (the
  `url` Location contract, the SimpleTreeView nav with every leaf routed,
  the ad-slot fork, asset contracts), internal-traffic contract (both
  halves), and the SPA/doc **counting rule** as executable arithmetic.
- **CI (`ci.yml`)** — lint (flake8 with a budgeted, documented pages/ debt
  ledger in `.flake8`, plus actionlint first), secretless pytest + a real
  gunicorn boot probed by the network battery, a **Docker job** that builds
  the production image, asserts version fingerprints INSIDE it (dash ≥4.1,
  dimll ≥2.3.4, gunicorn ≥23) and boots it against the same battery CD runs
  (LESSONS §19), a Dash **matrix** (4.1.0/4.2.0/4.3.0/4.4.1 × py3.12 +
  4.4.1 × 3.10/3.13) that rebuilds the components with Node 20 (`npm ci` +
  build + validate-init) before smoke-testing, wheel build + clean-venv
  verification (13 components, `top_level == dash_mui_charts`, version ==
  package.json, and a **measured dash==3.3.0 floor install**), a package ×
  Python 3.9–3.13 range, JS parse checks on the committed bundle and every
  asset script, and advisory pip-audit.
- **CD (`cd.yml`)** — main → full CI → Render deploy hook → 120s settle +
  5 consecutive healthz 200s (Render swaps instances; one 200 proves
  nothing) → `network_smoke.py` + `smoke_live.py` against the live domain,
  including the social card's real pixels. Peer checks warn; own-host
  checks fail.
- **Release (`release.yml`)** — tag-gated PyPI publish via OIDC trusted
  publishing (no stored token), gated on tag == package.json version and
  `scripts/check_release.py`; GitHub Release cut from the CHANGELOG
  section. Publishing 1.3.0/1.4.0 remains a decision, not a side effect.
- **Scripts** — `network_smoke.py` (boilerplate battery, per-site block:
  this brand's H1, `/sparkline/llms.txt`, hidden-page canaries),
  `smoke_live.py` (canonical copy with the LESSONS §21 wake loop),
  `check_release.py` (versions, bundle freshness via git timestamps, a
  Python class per React component, packaging/SEO/network invariants),
  `smoke_test.py` (the matrix's structural gate — 40 routes, 200s,
  healthz, ≥150 chart mounts, node parse of every JS artifact).
- **Two Dash floors made explicit and measured** — the DOCS SITE needs
  dash ≥4.1 (dash-improve-my-llms pins `dash<5,>=4.1`; production already
  resolves 4.4.x), while the PACKAGE needs only ≥3.3: `setup.py` now claims
  `dash>=3.3.0` (raised from an unmeasured `>=3.0.0`) and
  `python_requires>=3.9` (3.13 classifier added, untested 3.8 dropped) —
  both now measured by CI rather than asserted. Verified locally: the full
  route-parity gate is green under Dash 4.4.1, byte-identical to the 3.3.0
  baseline.
- **gunicorn floor raised to ≥23** in requirements.txt — closes
  CVE-2024-6827 / CVE-2024-1135 (request smuggling); asserted inside the
  Docker image by CI so it cannot silently regress.
- Housekeeping: `import dash` (unused) dropped from app.py; flake8 config
  added with per-file ignores documenting why app.py's late imports and the
  pages idiom are deliberate.

### Network-standard pass — Phase 2 (card + traffic + app id + bulletin)

- **Social card generated** — `scripts/make_social_card.py` (boilerplate
  template, this site's MUI-blue palette and area-chart mark) renders
  `build/social-cards/muicharts.2plot.dev.png`, 1200×630. HARD GATE
  outstanding: hand-upload to cdn.2plot.ai/github_assets/ and verify
  200 + IHDR before the og:image deploy.
- **Internal-traffic contract, both halves** — `lib/analytics.record`
  drops `2plot-internal` UAs at write time, before bot classification;
  the hourly rollup POST and every ad-server fetch now send
  `internal_ua(...)` so the hub stops counting this app as a
  python-requests bot.
- **One short app id: `muicharts`** — `traffic_report.APP_KEY`,
  `ad_client.AD_APP_ID` default, bulletin app_id and /healthz all
  converge on the directory key (legacy "dash-mui-charts" folds in at the
  hub). NOTE: the 2plot.ai traffic sink still keys this app "charts" and
  must gain a muicharts fold before deploy or its series forks.
- **Bulletin wired opt-in** — `lib/bulletin.py`; boot log states wired/off.
  `NETWORK_BULLETIN_URL` must be set on the Render SERVICE (blueprint
  envVars only apply on Blueprint sync).

### Network-standard pass — Phase 1 (identity + llms surfaces)

- **One brand, every surface** — `lib/constants.py` (SITE_BRAND
  "dash-mui-charts — MUI X charts for Dash", SITE_DESCRIPTION, BASE_URL
  defaulting to https://muicharts.2plot.dev, OG card block, INTERNAL_UA).
  The header version badge, the JSON-LD version and the template origin are
  now substituted from single sources of truth at boot — this repo carried
  five conflicting version strings and three "9 components" claims (it has
  13; README and .claude/CLAUDE.md corrected).
- **dash-improve-my-llms ≥2.3.4 wired** — /llms.txt (site prose from
  pages/home.py's LLMS_DOC), per-page /<page>/llms.txt, /robots.txt with
  per-vendor bot policy, /sitemap.xml (40 URLs on the canonical origin),
  per-route canonical/og prerender, cross-host network directory
  (`lib/network_directory.py`). The analytics before_request stays
  registered ahead of the bot middleware so crawler hits keep being
  counted.
- **Every register_page carries title/description/image_url** — one
  missing and Dash emits an empty tag that wins with scrapers; all 40
  routes verified to serve zero empty meta tags. 14 pages (home + one per
  component family) carry LLMS_DOC prose sourced from SKILLS.md.
- **templates/index.html rebuilt on the dedup rule** — declares only what
  Dash does not emit (og:site_name/locale/url, og:image auxiliaries,
  twitter:image:alt); the duplicate hardcoded title, static og/twitter
  block, stale JSON-LD and hardcoded canonical are gone. GA4 kept; favicon
  randomizer kept but its header-avatar sync now retries bounded instead
  of forever; SPA canonical/og:url sync script added.

### Network-standard pass — Phase 0 (stabilize)

- **Satellite analytics committed** — `lib/analytics.py` (SPA-aware hit
  recorder), `lib/traffic_report.py` (hourly signed rollup + `/healthz`),
  `verify_traffic.py` (headless pipeline verification against the hub's own
  ingest verifier). All checks green.
- **Route-parity gate** — `scripts/route_parity.py` fingerprints all 40
  routes (component tree, ids, chart-mount counts, callback census, HTTP
  sweep) against a committed baseline; every migration phase must keep it
  green.
- **Requirements drift fixed** — `requirements-deploy.txt` deleted (it had
  lost `requests`, so the Docker image could not import `app.py`);
  `requirements.txt` is now the single dependency file for Render and the
  Dockerfile alike. Dockerfile gains `PYTHONUNBUFFERED=1`.
- **Stray build artifact removed** — `dash_mui_charts/dash_mui_charts` was a
  full copy of `package.json`, created by `build:backends` passing the
  package name to `-p/--package-info-filename`; the flag now correctly says
  `package-info.json` and the artifact is deleted.

---

### Components — TreeViewPro (2026-07-19)

- **TreeViewPro kebab submenus + dividers.** `kebabMenuItems` entries may now be
  a leaf `{label, value, icon?}`, a `{divider: true}` rule, or a submenu
  `{label, icon?, children: [entries]}` that opens on hover/click (recursive
  nesting; a leaf anywhere in the chain closes the whole menu and fires
  `kebabAction`).
- **`kebabMenuItemsById`** — per-node kebab menus: `{itemId: [entries]}`
  overrides the global `kebabMenuItems` for that node (same entry shape,
  submenus/dividers included). Lets one tree carry different action sets for
  different node types (channel nodes vs media nodes vs viewport nodes — the
  2plot.media /360-broadcast use case that motivated this).

---

## [1.3.0] - 2026-06-05

### Added

#### TimeClock — new component (13th)
- **`TimeClock`** wraps the MUI X Date Pickers `TimeClock` (`@mui/x-date-pickers`, Community) — an inline clock-face time selector with no input, popper, or modal. First component in a new **Date & Time Pickers** family.
- **String ↔ dayjs boundary**: dayjs objects can't cross the Dash boundary, so `value` / `defaultValue` / `minTime` / `maxTime` are exchanged as plain strings — full wall-time ISO (`"2022-04-17T15:30:00"`) or time-only (`"15:30"` / `"15:30:45"`). On change the component pushes back `value` (wall-time ISO), the current `view`, and a parsed `timeData` convenience object `{hours, minutes, seconds, formatted, event_timestamp}`.
- **Props**: `views` (`hours`/`minutes`/`seconds`), `view` (controlled, in/out), `openTo`, `ampm` (force 12h/24h), `disabled`, `readOnly`, `autoFocus`, `minutesStep`, `minTime` / `maxTime`, `disableFuture` / `disablePast`, `disableIgnoringDatePartForTimeValidation`, `showViewSwitcher`, `sx`, `className`.
- **Dark mode**: observes `<html data-mantine-color-scheme>` via a `MutationObserver` and wraps the clock in an MUI `ThemeProvider`, re-skinning automatically — same pattern as `TreeViewPro`.
- **Dependencies**: adds `@mui/x-date-pickers` pinned to `8.24.0` (matches `@mui/x-charts@8.24.0` so they share a single `@mui/x-internals`) and the `dayjs` adapter (`1.11.13`). Compatible with the existing Material v6 stack — no migration.

#### Demo page `/time-clock`
- Mirrors the official MUI demo: basic usage, controlled vs. uncontrolled (with live readout + preset buttons), form props (disabled / read-only), views (hours-minutes-seconds, hours-only, minutes-seconds), and 12h/24h format. Theme-aware Mantine layout.

#### Demo page `/time-clock-lab` (TimeClock Lab)
- A deep-dive page showing TimeClock working hand-in-hand with **dash-mantine-components**:
  - **Dynamic colours** — `dmc.ColorPicker` (rgba, with an **opacity** slider) for the face plus `dmc.ColorInput`s for the hand and digits, fed live into the TimeClock `sx` (targets `.MuiClock-clock`, `.MuiClockPointer-root/-thumb`, `.MuiClock-pin`, `.MuiClockNumber-root`).
  - **Liquid glass clock** — a glassmorphic theme (`assets/liquid_glass_clock.css`): frosted face with an animated halo, a pointer thumb restyled into a **magnifying lens** recentred on the digit, and the selected digit bolded/enlarged as the hand passes. Fully light/dark-mode aware.
  - **Stopwatch** — `dcc.Interval` driven start/stop/restart; the clock view climbs with magnitude (seconds → minutes → hours).
  - **Two-way pairings** — fully synced with `dmc.TimeInput` (+ reset/preset buttons), `dmc.TimePicker`, `dmc.TimeGrid` (preset half-hour slots), and `dmc.DateTimePicker` (the clock drives the time portion). One `@callback` per pairing, branching on `ctx.triggered_id` and returning `no_update` for the source side to avoid loops.
  - Each example carries a syntax-highlighted **"View code"** panel.
- New **Date & Time Pickers** group added to the navigation tree in `app.py`.

### Changed

#### Professional "View code" across demo pages
- Upgraded the legacy `html.Details` + `html.Pre` "View Code" blocks to **`dmc.CodeHighlight` / `dmc.CodeHighlightTabs`** — syntax highlighting, a copy button, file tabs, and theme awareness. 60 code blocks across 14 pages converted; dynamic output `html.Pre` targets (e.g. click-data readouts) were correctly left untouched.

---

## [1.2.3] - 2026-05-15

### Fixed

#### TreeViewPro — Cell editing
- **`[object Object]` on edit**: `CustomTreeItem` previously passed the slider/kebab wrapper as the TreeItem `label` **prop**. MUI's `getLabelProps()` sets `children: label` and the edit input initialized from that same value, so entering edit mode stringified a React element to `[object Object]`. The custom UI is now injected through the **`slots.label` slot** while the real string `label` prop is left intact, so the edit input, `onItemLabelChange`, and double-click-to-edit all receive the correct text. `itemId` is forwarded to the slot via `slotProps.label`; MUI-internal props (`editable`, `ownerState`) are destructured out so they never reach the DOM. Group rows and the no-controls fallback also forward the slot props, keeping every row editable.
- **Edit mode collapsing mid-gesture**: With `itemsReordering=True`, MUI's reorder plugin sets `draggable="true"` on the TreeItem root with no editing guard. While the label input was focused, drag-selecting a word started a native HTML5 element drag of the row, which blurred the input and committed/exited edit mode on mouse-up; clicking inside the cell also bubbled to the row's selection/focus handlers. A new custom **`labelInput` slot** (`EditableLabelInput`) now: (1) flips the nearest `draggable="true"` ancestor to `false` while the input is mounted and restores it on cleanup; (2) `stopPropagation()`s `mousedown`/`pointerdown`/`click` (without `preventDefault`, so native caret placement and text selection still work) so the row no longer reacts; (3) cancels stray `dragstart`. `onBlur`/`onKeyDown`/`value`/`autoFocus`/`data-element` pass through untouched, so click-outside and Enter/Escape still commit/cancel. Net: double-click to edit → click to position the caret, drag to highlight, edit freely → click outside or Enter to commit.

#### Demo page `/tree-pro`
- **Readouts use the renamed label**: `editedItemLabel` is now captured into a `dcc.Store` of `{itemId: newLabel}` overrides. "Last slider", "Last menu", and "Selected" resolve labels through `label_for(id, overrides)` (override → static tree label → id). The two summary tiles render from stored last-slider / last-kebab state plus the overrides store, so renaming a cell immediately refreshes them with the new label instead of showing the stale one.
- **`Selected:` shows labels, not IDs**: selected items (groups or leaves, single or multi) now display their human labels via a full `ALL_LABELS` map instead of raw slugs.

---

## [1.2.2] - 2026-05-13

### Added

#### TreeViewPro — Per-Item Slider + Kebab Menu
- **`showItemControls` (bool)** — render a 0–100 `Slider` and a kebab `IconButton` directly after each tree item's label. Designed for "tree paired with a map / canvas" patterns where each leaf is a layer with an opacity / progress value and a row-level actions menu.
- **`controlsItems` (list of IDs)** — optional subset filter; the slider + kebab only appear on listed items (leaves only, by convention). Omit to show controls on every row.
- **`sliderValues` (dict, bidirectional)** — `{itemId: value}`. Pre-seed initial values from Python; the prop also updates live as the user drags so callbacks can mirror the state.
- **`sliderMin` / `sliderMax` / `sliderStep`** — bounds and granularity (defaults 0 / 100 / 1).
- **`sliderColor` (string)** — accepts Mantine palette names (`"teal"`, `"blue.5"` → `var(--mantine-color-...-6)`), CSS literals (`"#ff6b6b"`, `"rgb(...)"`, `"oklch(...)"`), or CSS expressions (`"var(--mantine-...)`, `"light-dark(...)`). Applied via `sx` to the slider track, thumb, hover ring, value label, and rail.
- **`kebabMenuItems` (list)** — `[{label, value, icon?}]` defines the actions menu. `icon` resolves through `iconResolver`.
- **`sliderChange` (output)** — `{itemId, value, event_timestamp}`, fired on slider commit (mouse-up / touch-end).
- **`kebabAction` (output)** — `{itemId, action, event_timestamp}` fired when a menu item is selected.
- **`orderedItems` (output)** — the full live tree after any drag-reorder. Emitted on every `onItemPositionChange` via an internal `applyReorder` walk so Dash callbacks can render the nested current order. Falls back to `items` until the first reorder.
- **Dark / light mode detection** — TreeViewPro now wraps its subtree in an MUI `ThemeProvider` whose `mode` is driven by a `MutationObserver` on `<html data-mantine-color-scheme>`. Checkbox, slider, IconButton, Menu paper and MenuItems re-skin automatically when the Mantine color scheme toggles.
- **Slider responsiveness on desktop** — `ItemLabelWithControls` holds a local React state during drag, so the thumb tracks instantly even when Dash callback round-trips are slow. Native `dragstart` is cancelled on the slider + kebab area to keep `itemsReordering` from swallowing mouse drags; passive pointer/touch events no longer call `preventDefault` (silences the "Unable to preventDefault inside passive event listener invocation" console message).
- **`MoreVert`, `ContentCopy`, `PersonAdd`, `CheckCircle`, `Archive` icons** registered in `iconResolver.js` for kebab menu usage.

#### Demo page `/tree-pro` rebuilt
- Two-column grid (`dmc.Grid`): the Pro tree on the left, a "map companion" panel on the right that mirrors the tree's state via `dmc.Text` tiles (Last slider, Last menu), a JSON readout titled **"Slider values and nested order:"**, and a rolling action log.
- **Slug-derived IDs**: `slugify_label` + `assign_ids` turn label strings into stable IDs at startup. Spaces and non-alphanumerics → `-`, duplicate slugs auto-disambiguate with `-1`, `-2`, … so `Site survey overlay` becomes `site-survey-overlay` and the JSON output reads like a layer manifest instead of `task-1`, `task-2`.
- **Nested order JSON** — `build_nested_view` walks `orderedItems` (or the initial `items` on first render) and injects slider values at the leaves, so the readout always reflects the current reordered tree.
- Layer-themed labels (Planning / Active / Reference) replace the placeholder "Backlog / In Progress / Done" copy to match the map-companion use case.
- Section 3 wires `sliderColor="teal"`; `ThemeIcon` and action-log icons reuse the same constant.

### Notes
- Two `Each child in a list should have a unique "key" prop` warnings remain when `checkboxSelection={true}` and when the kebab menu opens. Both originate in MUI v6 internals (`ButtonBase` ripple array, `FocusTrap` children) and are tracked upstream — they are not caused by our code. They clear on upgrade to MUI v7.

---

## [1.2.1] - 2026-04-11

### Fixed
- **TreeView `editableItems` prop not working**: `isItemEditable` defaulted to `false` (a boolean), causing `typeof isItemEditable === 'boolean'` to short-circuit before checking the `editableItems` array. Changed to `isItemEditable === true` so per-item editing via `editableItems` works correctly.
- **SimpleTreeView React 18 `defaultProps` warning**: Replaced `Component.defaultProps` with JavaScript default parameters in the function signature.
- **TreeView edit input dark mode**: Added CSS overrides for `.MuiTreeItem-labelInput` input fields — dark background, white text, and blue focus underline in dark mode.

### Added
- **Per-item icons in SimpleTreeView**: Items now support an `icon` field (string) resolved via `iconResolver`. Renders inline MUI icon (18px, 0.7 opacity) next to the label.
- **30+ new MUI icons in `iconResolver.js`**: `ShowChart`, `BarChart`, `PieChart`, `ScatterPlot`, `GridOn`, `CandlestickChart`, `Timeline`, `TrendingUp`, `Layers`, `AccountTree`, `Brush`, `Highlight`, `Sync`, `ZoomIn`, `TouchApp`, `TableChart`, `StackedBarChart`, `Palette`, `Rule`, `Mouse`, `CheckBox`, `UnfoldMore`, `Block`, `Diamond`, `AutoGraph`, `ViewList`, `GpsFixed`, `Speed`, `Star`, `PlayArrow`, `Tune`, `History`.
- **Changelog page**: `/changelog` renders `CHANGELOG.md` via `dcc.Markdown` with styled tables and dark mode support.

### Changed
- **Navigation tree**: Reordered (Home, Changelog, SparklineChart, PieChart, BarChart, Heatmap, ScatterChart, LineChart, CandlestickChart, LiveTradingChart, CompositeChart, TreeView). All items have unique MUI icons. Groups start collapsed. `itemChildrenIndentation` reduced to 8px.
- **Tree state persistence**: Expanded groups saved to `localStorage` via clientside callback, restored on page load via `dash_clientside.set_props`. No circular dependency.
- **SPA navigation**: Tree selection uses `dcc.Location(refresh="callback-nav")` — page content swaps without full reload, preserving tree state.

---

## [1.2.0] - 2026-04-10

### Added

#### BarChart Component (New)
- **Vertical & Horizontal Bars**: `layout='vertical'` (default) or `layout='horizontal'`
- **Multi-Series**: Multiple data series with individual colors side by side
- **Stacking**: `stack` group ID on series, with `stackOffset` ('none', 'expand', 'diverging') and `stackOrder` ('none', 'appearance', 'ascending', 'descending', 'reverse')
- **Bar Labels**: `barLabel='value'` with `barLabelPlacement` ('center' or 'outside')
- **Border Radius**: Rounded bar corners via `borderRadius` prop
- **Dataset Mode**: `dataset` + `dataKey` pattern for table-format data (no duplication)
- **Bar Spacing**: `categoryGapRatio` and `barGapRatio` on band axis for gap control
- **Reference Lines**: Horizontal (`y`) and vertical (`x`) markers for targets, thresholds
- **Axis Highlight**: Configurable `axisHighlight` with 'band', 'line', or 'none'
- **Tooltip Modes**: `tooltip={'trigger': 'axis'}` or `tooltip={'trigger': 'item'}`
- **Highlighting**: `highlightedItem` prop (controlled, bidirectional) with per-series `highlightScope`
- **Custom Colors**: `colors` palette prop for series color override
- **Batch Renderer**: `renderer='svg-batch'` for large dataset performance
- **Click Events**: `clickData` (bar click) and `axisClickData` (axis area click) output props
- **Pro Features** (require `licenseKey`):
  - `initialZoom` + `showSlider` for zoom with range slider
  - `showToolbar` for zoom/export toolbar
  - `brushConfig` for brush selection
  - `zoomInteractionConfig` for pan/wheel/pinch behaviors
  - `zoomData` output prop for zoom state callbacks

#### CandlestickChart Component (New)
- **OHLC Candlestick Rendering**: Custom SVG candles (body + wicks) built on MUI X Charts Pro composition API
- **Array Format**: `series=[{data: [[open,high,low,close], ...], upColor, downColor}]`
- **Dataset Format**: `dataset` + `series=[{datasetKeys: {open, high, low, close}}]`
- **Volume Overlay**: Optional volume bars below candles via `showVolume=True` with `volumeKey` or `volume` array
- **Candle Styling**: `bodyWidthRatio` (0-1) and `wickWidth` (px) for custom candle appearance
- **OHLC Tooltip**: Built-in hover tooltip showing Open, High, Low, Close values
- **Reference Lines**: Support/resistance lines, moving averages markers
- **Click Events**: `clickData` with `{dataIndex, label, open, high, low, close, timestamp}`
- **Auto Y-Axis Domain**: Automatically computes min/max from OHLC data with 5% padding
- **Grid Support**: `grid={'horizontal': True, 'vertical': True}`
- **Pro Features**: Zoom, slider, toolbar (via composition API)
- **No Premium Dependency**: Works with existing `@mui/x-charts-pro` v8.24.0 (no `@mui/x-charts-premium` required)

#### Demo Pages (7 New)
- `/barchart-basic` — Multi-series, stacked, horizontal, bar labels, rounded corners, negative values
- `/barchart-dataset` — Dataset mode with dataKey, bar/category gap control
- `/barchart-stacking` — Stack offsets (none, expand, diverging), multiple stack groups, horizontal stacked
- `/barchart-interaction` — Click events, axis click, highlighting, axis highlight modes, tooltip triggers
- `/barchart-reference` — Target lines, min/avg/max refs, vertical refs, animation, legend, color palette
- `/barchart-pro` — Zoom+slider, toolbar, stacked zoom (Pro features)
- `/candlestick` — Array format, dataset mode, volume overlay, styling, support/resistance lines, click events

#### Application UI/UX Redesign
- **DMC AppShell Layout**: Replaced flat blue top-bar with `dmc.AppShell` (header + sidebar navbar + main content area)
- **Sidebar Tree Navigation**: `SimpleTreeView` organizes all 37 demo pages into 11 component groups with expand/collapse
- **Dark/Light Mode**: `dmc.ColorSchemeToggle` (DMC 2.6.1) with `dmc.pre_render_color_scheme()` to prevent theme flash on load
- **MUI Charts Dark Mode**: Global CSS overrides for axis labels, tick marks, grid lines, legend labels, tooltips, bar labels, and reference lines — all auto-switch via `[data-mantine-color-scheme="dark"]`
- **Theme-Aware Loading Screen**: Animated liquid-blob splash screen with 2plot logo, swaps between light/dark assets based on saved preference (`localStorage`)
- **Page Loading Overlay**: `/composite-render-bp` uses deferred content loading via callback with `dmc.LoadingOverlay` — shows logo + blur overlay while heavy chart sections build server-side
- **Home Page Redesign**: Responsive 3-column component card grid with `dmc.Paper`, `dmc.Badge`, `dmc.CodeHighlight` for installation and usage examples

### Changed
- **CompositeChart**: Custom tooltip components (`MuiAxisTooltip`, `ExternalAxisTooltip`) now use Mantine CSS variables (`--mantine-color-body`, `--mantine-color-text`, `--mantine-color-default-border`) instead of hardcoded `white`/`#e0e0e0` — tooltips auto-adapt to dark mode
- **SimpleTreeView**: Replaced `Component.defaultProps` with JavaScript default parameters to eliminate React 18 deprecation warning
- **Composite Render BP page**: Deferred chart section building to a callback (from static layout) for instant page load with loading overlay
- Updated component count from 7 to 9
- `src/lib/index.js` exports BarChart and CandlestickChart
- Auto-generated Python wrappers for both components via `dash-generate-components`
- Upgraded `dash-mantine-components` from `>=1.0.0` to `>=2.6.0` in `requirements.txt`
- All demo pages updated with Mantine CSS variables for dark mode support (card backgrounds, text colors, code blocks, tooltips, borders)
- Pages with `dmc.MantineProvider` wrappers (8 files) unwrapped — single root provider in `app.py`

### Fixed
- **Legend labels not switching in dark mode**: Added CSS selectors for `.MuiChartsLegend-label` and `.MuiChartsLabel-root` (HTML span elements used by MUI X Charts v8)
- **Custom tooltip dark mode** in crosshair, highlighting sync, composite, and composite render pages — replaced hardcoded `white`/`#333`/`#e0e0e0` with theme-adaptive CSS variables
- **Highlighting demo**: Per-Series Highlight Scope example now uses 3 series with distinct `highlightScope` configs to clearly demonstrate `series` vs `item` highlight and `global` vs `none` fade behaviors
- **Circular dependency**: Replaced server-side nav callbacks with clientside `window.location` navigation to break `url.pathname ↔ nav-tree.selectedItems` cycle

### Documentation
- Updated CLAUDE.md with BarChart and CandlestickChart features
- Updated SKILLS.md with implementation details, prop references, and usage patterns
- Updated README.md with new component listings and examples

---

## [1.1.0] - 2026-04-08

### Added

#### Functions-as-Props Pattern (LineChart, CompositeChart)
- **`resolveFunctionProp` utility** — Mirrors Dash Mantine Components' `dashMantineFunctions` pattern
  - Python passes `{'function': 'name', 'options': {...}}` as a prop value
  - React component resolves from `window.dashMuiChartsFunctions` registry
  - Users define custom JS functions in `assets/*.js` files
- **`valueFormatter` support on xAxis/yAxis** — Control how axis values are displayed
  - Accepts DMC-style function reference objects or native JS functions
  - Enables custom date formatting, number formatting, and label rendering
  - Works with all scale types (time, linear, point, band, etc.)

#### Built-in Date Formatting (LineChart, CompositeChart)
- **`dateFormat` prop on xAxis/yAxis** — Format string for tooltip date labels (e.g. `'M/d HH:mm'`)
- **`dateTickFormat` prop on xAxis/yAxis** — Separate shorter format for tick labels (e.g. `'M/d'`)
  - Prevents label truncation by using compact tick labels while keeping full format in tooltips
  - Supported tokens: `YYYY`, `MMM`, `MM`, `M`, `dd`, `d`, `HH`, `mm`
  - Automatically creates a `valueFormatter` internally — no external JS file required

#### LiveTradingChart Component (New)
- Real-time streaming chart component for live data visualization

#### Demo Pages
- New `/linechart-tick-hover` page — Comprehensive tick, hover, and axis configuration guide
  - Section 1-4: Date range best practices (week, quarter, year) with point and linear scales
  - Section 5a: Angled labels with `dateFormat`/`dateTickFormat` on time scale
  - Section 5b: Zoom with slider — tick behavior during zoom/pan interactions (Pro)
  - Section 5c: Pro zoom with slider preview, brush select, toolbar, and `zoomInteractionConfig`
  - Section 6: Interactive hover events with click data callbacks
  - Section 7: Best practices summary reference table
- New `/live-trading` page — LiveTradingChart demo

#### Assets
- New `assets/muiChartsFunctions.js` — Ships a reusable `formatDate` function for the functions-as-props pattern
  - Supports format tokens: `YYYY`, `MMM`, `MM`, `M`, `dd`, `d`, `HH`, `mm`
  - Context-aware: uses `tickFormat` option for tick labels, `format` for tooltips

### Changed
- **LineChart** — `processedXAxis` no longer short-circuits when `showSlider` is false
  - Previously skipped all axis processing (including valueFormatter resolution) when slider was disabled
  - Now always processes axes for dateFormat and valueFormatter resolution
- **CompositeChart** — Same `processedXAxis` improvement as LineChart

### Documentation
- Updated CLAUDE.md with new component features and axis formatting documentation
- Key Tick & Zoom Props reference table in the tick-hover demo page

---

## [1.0.0] - 2026-03-19

### Added
- **Stable release** — 6 chart components ready for production use

### Changed
- Version bump to 1.0.0 to reflect API stability
- Fixed `package-info.json` version tracking (was stuck at `0.0.1`, causing stale JS bundle caching)

---

## [0.0.8] - 2026-03-12

### Added

#### ScatterChart (New Component)
- **Multi-Series**: Multiple scatter series with individual colors and marker sizes
- **Z-Axis Color Mapping**: Color points by a third variable (continuous, piecewise, ordinal)
- **Voronoi Interaction**: `voronoiMaxRadius` for proximity-based hover/click
- **Dataset-Driven**: `dataset` + `datasetKeys` pattern for table-format data
- **Batch Renderer**: `renderer='svg-batch'` for large datasets
- **Click Events**: `clickData` with seriesId, dataIndex, x, y coordinates
- **Log/Sqrt Scales**: Full axis scaleType support

#### CompositeChart (New Component)
- **Chart Layering**: Mix `type: 'scatter'` and `type: 'line'` series on a single surface
- **Custom Composite Tooltip**: Axis tooltip shows both line and scatter data via proximity search
  - Handles MUI's poor scatter tooltip formatting in composite charts
  - Auto-computes proximity threshold from x-axis data spacing
- **Reference Lines**: Horizontal and vertical markers
- **Multi-Axis**: Scatter on left axis, line on right axis
- **Zoom/Pan** (Pro): `initialZoom`, `showSlider`, `zoomInteractionConfig`
- **Toolbar** (Pro): `showToolbar=True` for zoom/export controls
- **Zoom Slider Preview**: `preview: {markerSize}` on scatter series for slider preview markers
- **Time Scale Support**: Automatic epoch ms to Date object conversion for `scaleType: 'time'`
- **Controlled Highlighting**: `highlightedItem` prop for programmatic control
- **Click Events**: Separate click handlers for scatter and line series

#### Demo Pages
- New `/scatter` page with multi-series, z-axis color mapping, voronoi, and dataset-driven examples
- New `/composite` page with scatter+trend, reference lines, multi-axis, and zoom-enabled examples
  - DMC sliders for interactive marker size control (chart and preview)
  - Multi-color anomaly scatter (red critical / yellow warning)

### Changed
- Updated component count from 4 to 6
- `src/lib/index.js` exports ScatterChart and CompositeChart

### Documentation
- Updated CLAUDE.md with ScatterChart and CompositeChart features
- Updated SKILLS.md with new component documentation and patterns
- Updated README.md with new component listings

---

## [0.0.7] - 2025-01-30

### Added

#### Synchronized Tooltips with Custom Overlays
- **Custom tooltip overlay system** for true synchronized tooltips across multiple charts
  - MUI X Charts limitation: native tooltips only appear on the hovered chart
  - Solution: Custom Dash HTML divs positioned absolutely over each chart
  - Both charts show tooltips simultaneously when hovering on either one
- New demo implementation in `/highlighting-sync` page showing:
  - Revenue + Expenses dual LineChart with synchronized custom tooltips
  - Tooltips positioned using CSS `calc()` for responsive layouts
  - Visual highlighting (marks, axis bands) continues to sync via `highlightedItem`

#### LineChart Highlighting Improvements
- Improved callback patterns for highlight synchronization
- Better handling of highlight state when mouse leaves chart area
- Custom tooltip content generation for each chart in sync scenarios

### Changed
- **Highlighting Sync Demo**: Updated to use custom tooltip overlays instead of `tooltipItem`
  - Disabled MUI's built-in tooltips: `tooltip={'trigger': 'none'}`
  - Added absolutely-positioned custom tooltip divs
  - Tooltip x-position calculated from data index and chart margins
- Callback now listens to `highlightedItem` (more reliable than `tooltipItem` for sync)

### Documentation
- Updated SKILLS.md with custom synchronized tooltip pattern
- Documented MUI X Charts tooltip limitation (GitHub issues #14455, #17555)
- Added code examples for custom tooltip positioning

---

## [0.0.6] - 2025-01-29

### Added

#### LineChart - Controlled Highlighting
- New `highlightedItem` prop for controlled item highlight state
  - Programmatically highlight specific data points
  - Bidirectional: updates on hover and accepts external values
  - Object format: `{'seriesId': 'series-id', 'dataIndex': 0}`
- New `highlightedAxis` prop for controlled axis highlight state
  - Programmatically highlight specific axis positions
  - Array format: `[{'axisId': 'x-axis', 'dataIndex': 2}]`
- New `onHighlightChange` and `onHighlightedAxisChange` callbacks (internal)

#### LineChart - Per-Series Highlight Scope
- Series-level `highlightScope` configuration
  - `highlight`: `'none'` | `'item'` | `'series'`
  - `fade`: `'none'` | `'series'` | `'global'`
- Different highlight/fade behaviors per series

#### LineChart - Toolbar (Pro)
- New `showToolbar` prop to display chart toolbar
- Provides zoom/export controls
- Requires MUI X Pro license

#### LineChart - Synchronized Tooltips
- New `tooltipItem` prop for controlled tooltip state
  - Enables synchronized tooltips across multiple charts
  - Object format: `{'type': 'line', 'seriesId': 'series-id', 'dataIndex': 0}`
  - Bidirectional: updates on hover and accepts external values
- Combined with `highlightedItem` for full visual synchronization

#### PieChart - Controlled Highlighting
- `highlightedItem` prop now works as both input and output
- Enables synchronized highlighting across multiple charts
- Object format: `{'seriesId': 'auto-generated-id-0', 'dataIndex': 0}`

#### Demo Pages
- New `/linechart-highlighting` page demonstrating:
  - Controlled item highlights with buttons
  - Controlled axis highlights
  - Per-series highlightScope configuration
- New `/highlighting-sync` page demonstrating:
  - LineChart + PieChart synchronization
  - Dual LineChart axis synchronization
  - Cross-chart highlight coordination

### Changed
- LineChart now uses controlled mode for highlighting by default
  - Always passes `highlightedItem` (as `null` when not set)
  - Ensures proper MUI controlled mode initialization
- Callback patterns improved to avoid echo issues
  - Separated button-triggered and display callbacks
  - Use `dash.no_update` to prevent callback loops in sync scenarios

### Fixed
- Item highlighting not triggering callbacks in composition API
- Controlled highlight state not syncing with MUI internal state
- Echo issues in highlight synchronization callbacks

### Documentation
- Updated CLAUDE.md with v0.0.6 features
- Updated SKILLS.md with highlighting patterns and examples

---

## [0.0.5] - 2025-01-26

### Added

#### LineChart - Reference Lines
- Full support for `ChartsReferenceLine` API
- Horizontal reference lines via `y` prop (targets, thresholds, averages)
- Vertical reference lines via `x` prop (dates, events, milestones)
- Props: `x`, `y`, `axisId`, `label`, `labelAlign`, `lineStyle`, `labelStyle`, `spacing`
- Support for string/number/Date values on both axes
- Multi-axis support with `axisId` for biaxial charts
- New demo page: `/linechart-referencelines`

#### LineChart - Brush Selection (Pro)
- New brush interaction for range selection on charts
- `brushConfig` prop: `{enabled, preventTooltip, preventHighlight}`
- `brushOverlay` prop: `'none'` | `'default'` | `'values'`
  - `'default'`: Standard MUI selection rectangle
  - `'values'`: Custom overlay showing start/end values with difference and percentage change
- `brushSeriesId` prop: Specify which series to use for value calculations
- `brushData` output prop: Selection coordinates for callbacks
- New demo page: `/linechart-brush`

#### LineChart - Axis Highlight Configuration
- New `axisHighlight` prop to configure hover highlighting
- Options: `{x: 'none'|'line'|'band', y: 'none'|'line'}`
- Default: `{x: 'line', y: 'none'}`

### Changed
- `referenceLines.y` now accepts `string | number` (previously only `number`)
- Enables Date string values for time-based reference lines

### Documentation
- New demo page: `pages/linechart_brush.py`
- New demo page: `pages/linechart_referencelines.py`
- Updated SKILLS.md with brush and reference line documentation
- Updated CLAUDE.md with new LineChart features

---

## [0.0.1] - 2025-01-10

### Added

#### Components
- **LineChart** - Full-featured line and area charts
  - Multiple series support with independent Y-axes (biaxial charts)
  - Interactive zoom & pan (requires MUI X Pro license)
  - Line, area, and stacked area visualizations
  - 10+ curve interpolation options (linear, monotone, natural, step, catmull-rom, bump, etc.)
  - Configurable grid, legend, and margins
  - Click events for axis, mark, line, and area interactions
  - Zoom slider for range selection
  - Loading state overlay
  - Animation controls with prefers-reduced-motion support

- **PieChart** - Pie, donut, and nested pie charts
  - Single series (simple pie/donut) or multiple series (nested/concentric pies)
  - Customizable arc geometry (inner/outer radius, corners, padding)
  - Arc labels with value, label, or formattedValue display
  - Configurable start/end angles for half-pie and gauge charts
  - Highlight interactions with global fade effects
  - Click and hover event handling
  - Full animation support

- **Heatmap** - Matrix/grid visualization (requires MUI X Pro license)
  - Color-coded cell visualization
  - Continuous or piecewise color scales
  - Custom cell styling (rounded corners, gaps, value display)
  - Band-scale axes for categorical data
  - Cell click detection with coordinates
  - Highlight interactions

- **SparklineChart** - Compact inline charts
  - Ultra-compact design (36px default height)
  - Line or bar plot types
  - Area fill support
  - Tooltip and highlight interactions
  - Controlled highlight index for component synchronization
  - Curve interpolation options

#### Features
- Full TypeScript-like type safety with Python TypedDict
- Auto-generated Python wrappers from React PropTypes
- Comprehensive prop documentation
- Click event data with timestamps
- Dash 3.x compatibility
- React 18+ support

#### Documentation
- Basic usage examples in `usage.py`
- Multi-page demo application with interactive examples
- Property explorer pages for Pie, Heatmap, and Sparkline components

### Technical
- Webpack 5 build configuration
- MUI X Charts v8.24.0 integration
- MUI X Charts Pro v8.24.0 for advanced features
- Emotion styling support

---

## Component License Requirements

| Component | License Required |
|-----------|-----------------|
| LineChart (zoom/pan) | MUI X Pro |
| BarChart (zoom/brush) | MUI X Pro |
| CandlestickChart (zoom) | MUI X Pro |
| PieChart | Community (Free) |
| ScatterChart | Community (Free) |
| CompositeChart (zoom/pan) | MUI X Pro |
| Heatmap | MUI X Pro |
| SparklineChart | Community (Free) |
| LiveTradingChart | Community (Free) |

---

[Unreleased]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.8...v1.0.0
[0.0.8]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/pip-install-python/dash-mui-charts/compare/v0.0.1...v0.0.5
[0.0.1]: https://github.com/pip-install-python/dash-mui-charts/releases/tag/v0.0.1