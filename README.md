<div align="center">

<!-- Absolute CDN URL, not a repo-relative path: this README is also the PyPI
     long_description, where a relative image 404s. -->
<a href="https://2plot.ai">
  <img src="https://cdn.2plot.ai/github_assets/light_mode_2plot.png" alt="2plot.ai" width="320">
</a>

# dash-mui-charts — MUI X charts for Dash

**Interactive [MUI X](https://mui.com/x/) charts, tree views and time pickers for [Plotly Dash](https://dash.plotly.com).**

13 components · full Python type hints · clicks, zoom, selection and edits as Dash callbacks · dark mode · Community and Pro tiers.

[![PyPI version](https://img.shields.io/pypi/v/dash-mui-charts?color=blue)](https://pypi.org/project/dash-mui-charts/)
[![Python](https://img.shields.io/pypi/pyversions/dash-mui-charts)](https://pypi.org/project/dash-mui-charts/)
[![Dash 3.3+](https://img.shields.io/badge/Dash-3.3%2B-1a1a2e?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![CI](https://github.com/pip-install-python/dash-mui-charts/actions/workflows/ci.yml/badge.svg)](https://github.com/pip-install-python/dash-mui-charts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/WEnZR35mrK)
[![YouTube](https://img.shields.io/badge/YouTube-%402plotai-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ)

**[Documentation](https://muicharts.2plot.dev)** · [Discord](https://discord.gg/WEnZR35mrK) · [YouTube](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) · [GitHub](https://github.com/pip-install-python/dash-mui-charts)

<br/>

_Maintained by **[Pip Install Python LLC](https://pip-install-python.com)**._

</div>

---

## Overview

**dash-mui-charts** wraps [MUI X Charts](https://mui.com/x/react-charts/), [MUI X Tree View](https://mui.com/x/react-tree-view/) and the MUI X Date & Time Pickers' TimeClock as first-class Dash components. Author charts in Python, and get every interaction back as a callback property.

- **13 components** — nine chart types, three tree views, and a clock-face time picker.
- **Callbacks-first** — `clickData`, `axisClickData`, `highlightedItem`, `hoverIndex`, `zoomData`, selection and edit events all arrive as Dash inputs; controlled props (`highlightedItem`, `expandedItems`, `value`, …) work in both directions for synchronized, cross-chart UIs.
- **Dark mode by construction** — components watch the Mantine color-scheme attribute and re-theme live.
- **Functions-as-props** — axis `valueFormatter` and alert formatters accept `{'function': 'name', 'options': {...}}` resolved from a JS registry, mirroring the dash-mantine-components pattern.
- **Community and Pro tiers** — Community features need no license; zoom/pan, sliders, toolbars, brush, Heatmap and TreeViewPro extras light up with a [MUI X Pro license key](#mui-x-pro-licensing).

## Installation

```bash
pip install dash-mui-charts
```

Requires `dash>=3.3`. See [Dash compatibility](#dash-compatibility) for the tested matrix.

## Quick Start

```python
from dash import Dash, html
from dash_mui_charts import LineChart, PieChart

app = Dash(__name__)

app.layout = html.Div([
    LineChart(
        series=[
            {'data': [2, 5, 3, 8, 1, 9], 'label': 'Sales'},
            {'data': [1, 3, 2, 5, 4, 6], 'label': 'Costs'},
        ],
        xAxis=[{'data': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'scaleType': 'band'}],
        height=300,
    ),
    PieChart(
        data=[
            {'id': 0, 'value': 35, 'label': 'Marketing'},
            {'id': 1, 'value': 25, 'label': 'Engineering'},
            {'id': 2, 'value': 20, 'label': 'Sales'},
            {'id': 3, 'value': 20, 'label': 'Support'},
        ],
        height=300,
    ),
])

if __name__ == '__main__':
    app.run(debug=True)
```

## Documentation

### 📚 **[muicharts.2plot.dev](https://muicharts.2plot.dev)**

41 pages of live, interactive examples — every chart family with working callbacks, two props playgrounds, and an [API reference](https://muicharts.2plot.dev/api) whose props tables are generated from the components' own metadata. Every docs page also serves an LLM-friendly version at `/<page>/llms.txt`.

Run it locally:

```bash
git clone https://github.com/pip-install-python/dash-mui-charts.git
cd dash-mui-charts
pip install -r requirements.txt
# markdown2dash pins gunicorn<22, against the CVE-driven gunicorn>=23 floor in
# requirements.txt. pip cannot resolve both, so it installs without its
# dependency graph — every one of them is in requirements.txt already.
pip install --no-deps markdown2dash==0.1.2
pip install -e .
python run.py    # http://127.0.0.1:7666
```

## Components

| Component          | Category | What it is                                                             | Tier            |
|--------------------|----------|------------------------------------------------------------------------|-----------------|
| `LineChart`        | Charts   | Line/area charts, biaxial axes, reference lines, zoom/pan, brush       | Community / Pro |
| `BarChart`         | Charts   | Vertical/horizontal bars, stacking, bar labels, dataset mode, zoom     | Community / Pro |
| `CandlestickChart` | Charts   | OHLC candlesticks with volume overlay and reference lines              | Community / Pro |
| `PieChart`         | Charts   | Pie, donut, and nested pies with controlled highlighting               | Community       |
| `ScatterChart`     | Charts   | Scatter plots, z-axis color mapping, voronoi interaction               | Community       |
| `CompositeChart`   | Charts   | Scatter + line series layered on one surface, multi-axis               | Community / Pro |
| `Heatmap`          | Charts   | Matrix visualization with continuous/piecewise color scales            | Pro             |
| `SparklineChart`   | Charts   | Compact inline charts for dashboards, KPI cards and tables             | Community       |
| `LiveTradingChart` | Charts   | Real-time streaming OHLCV simulation with forecast and alerts          | Community / Pro |
| `TreeView`         | Trees    | Data-driven RichTreeView: selection, expansion, inline label editing   | Community       |
| `SimpleTreeView`   | Trees    | JSX-driven tree for navigation sidebars and static hierarchies         | Community       |
| `TreeViewPro`      | Trees    | Drag-reorder, lazy loading, per-item slider and kebab controls         | Pro             |
| `TimeClock`        | Pickers  | Inline clock-face time picker                                          | Community       |

## MUI X Pro licensing

dash-mui-charts itself is MIT. **Pro-tier features run on MUI X Pro**, which requires [a commercial license from MUI](https://mui.com/x/introduction/licensing/) — pass your key to any component via the `licenseKey` prop:

```python
import os
from dash_mui_charts import BarChart

BarChart(
    licenseKey=os.environ['MUI_PRO_API_KEY'],
    series=[...],
    xAxis=[{'data': [...], 'scaleType': 'band', 'zoom': {'minSpan': 8}}],
    showSlider=True,   # Pro: zoom slider
)
```

Without a key, Pro features render with MUI's unlicensed watermark — components degrade, they never crash. Community features never need a key.

## API reference

The **[/api page](https://muicharts.2plot.dev/api)** lists every prop of all 13 components, generated from the components' own metadata so it always matches the installed version. The props you will meet everywhere:

| Prop                                  | Type | Description                                                       |
|---------------------------------------|------|-------------------------------------------------------------------|
| `id`                                  | str  | Dash callback identity — available on every component             |
| `licenseKey`                          | str  | MUI X Pro key — enables Pro features per component                |
| `clickData` / `axisClickData`         | dict | Callback **outputs**: what was clicked, with series/axis context  |
| `highlightedItem`                     | dict | Controlled highlight — works as callback input AND output         |
| `hoverIndex` / `hoverValue`           | —    | Sparkline hover stream for synchronized displays                  |
| `selectedItems` / `expandedItems`     | —    | Tree selection/expansion — controlled or uncontrolled             |
| `sx`                                  | dict | MUI system styling passed straight to the underlying component    |

## Dash compatibility

The **package** targets **Dash 3.3 and up**; the **documentation site** needs Dash 4.1+ (its llms.txt engine pins `dash>=4.1`). Both floors are verified, not assumed, in [GitHub Actions](.github/workflows/ci.yml) on every push and PR:

- the docs site boots and smoke-tests on **Dash 4.1.0 / 4.2.0 / 4.3.0 / 4.4.1** (Python 3.10–3.13), rebuilding the component bundle and Python wrappers from source in each cell;
- the wheel installs into a clean venv with **nothing but Dash present** on Python 3.9 → 3.13, plus a dedicated `dash==3.3.0` floor install;
- the production Docker image is built, booted secretless, and probed by the same network battery that checks the live site after every deploy.

```bash
python scripts/smoke_test.py     # the per-version harness, standalone
```

## Development

```bash
git clone https://github.com/pip-install-python/dash-mui-charts.git
cd dash-mui-charts

# JS toolchain (only needed when changing src/lib/components)
npm install
npm run build            # webpack bundle + regenerated Python wrappers
npm run validate-init    # all 13 components generated and importable

# Python
pip install -r requirements.txt
pip install --no-deps markdown2dash==0.1.2   # pins gunicorn<22; see above
pip install -e .
python run.py            # docs on :7666

# Test
pytest tests/                                # 80 checks, zero secrets by design
python scripts/smoke_test.py                 # routes, layouts, JS parse
python scripts/route_parity.py --charts-only # every live example, id and callback intact
python scripts/check_release.py              # version drift, stale bundle, packaging

# Build a distribution
python -m build
```

The React sources in `src/lib/components/*.react.js` are the source of truth — the Python classes in `dash_mui_charts/` are generated from their PropTypes by `dash-generate-components`. The built bundle and wrappers are committed so git-based deploys (Render) work without a node toolchain.

**After editing `src/lib/components/*.react.js` you must run `npm run build`** and commit the regenerated bundle and wrappers in the same commit — `check_release.py` compares git commit timestamps and flags a bundle older than its source. The version lives in two files: `package.json` (which `setup.py` reads) and `dash_mui_charts/package-info.json` (which `__version__` reads, regenerated by the build); `check_release.py` fails if they drift.

## Releasing

Tag-driven. `git tag -a vX.Y.Z && git push origin vX.Y.Z` runs [`release.yml`](.github/workflows/release.yml): it asserts the tag matches `package.json`, re-runs the consistency and smoke checks, builds, publishes to PyPI over **OIDC trusted publishing** (no API token stored anywhere), and opens a GitHub Release with that version's CHANGELOG section attached. A `workflow_dispatch` dry run publishes to TestPyPI instead.

## Deployment

The documentation site runs at **[muicharts.2plot.dev](https://muicharts.2plot.dev)** on Render. The repo ships a `render.yaml` blueprint and `Dockerfile` — create a Render Blueprint from the repo, fill the `sync: false` secrets in the dashboard, point the `muicharts.2plot.dev` CNAME at the service, and it auto-deploys on push to main with a `/healthz` health check.

The canonical origin lives in exactly one place — `DEFAULT_BASE_URL` in `lib/constants.py` (override per-environment with `APP_BASE_URL`). `templates/index.html` carries `__CANONICAL_ORIGIN__` tokens that `run.py` substitutes at startup, so the canonical link, `og:url`, the JSON-LD, `sitemap.xml`, `robots.txt` and the llms.txt links cannot drift apart.

## Requirements

- Python >= 3.9  (the documentation site itself needs >= 3.10 — see below)
- Dash >= 3.3  (the documentation site needs >= 4.1)
- Node.js >= 18 — only to rebuild the JS bundle
- A [MUI X Pro license](https://mui.com/x/introduction/licensing/) — only for Pro-tier features

The **package** needs only Python 3.9+ and Dash 3.3+; that range is verified in CI. Running the **documentation site** from source additionally needs Python 3.10+ (`python-frontmatter` imports `typing.TypeGuard`) and Dash 4.1+. Neither floor applies to `pip install dash-mui-charts`.

## Community & support

- 💬 [Discord](https://discord.gg/WEnZR35mrK) — questions and showcase
- ▶️ [YouTube @2plotai](https://www.youtube.com/channel/UC6Bmo0t0ZUpU_xKBYW0bJuQ) — tutorials
- 🐛 [GitHub Issues](https://github.com/pip-install-python/dash-mui-charts/issues) — bugs and feature requests

Come build with us.

## More from Pip Install Python LLC

dash-mui-charts is one of several tools built and maintained by **Pip Install Python LLC**:

| Project                                                          | What it is                                        |
|------------------------------------------------------------------|---------------------------------------------------|
| 📊 **[2plot.ai](https://2plot.ai)**                              | The network hub — data apps, analytics, sign-in   |
| 🎬 **[2plot.media](https://2plot.media)**                        | Videography application                           |
| 🧩 **[2plot.dev](https://2plot.dev)**                            | The full Dash component catalogue                 |
| 🤖 **[ai-agent.buzz](https://ai-agent.buzz)**                    | Infinite AI canvas                                |
| ⛵️ **[PiratesBargain](https://piratesbargain.com/shop)**         | E-commerce / digital commerce                     |

## License

MIT — see [LICENSE](LICENSE). dash-mui-charts is an independent Dash wrapper around [MUI X](https://mui.com/x/), which is its own project under its own licenses: the Community features wrap MIT-licensed MUI X packages, and Pro-tier features require your own commercial MUI X license. Built by [Pip Install Python](https://github.com/pip-install-python).
