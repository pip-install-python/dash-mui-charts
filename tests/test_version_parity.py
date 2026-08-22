"""Version and component-count parity — THE fix for the five-way drift.

The 2026-08-01 survey found this repo advertising FIVE different versions at
once: package.json said 1.4.0, PyPI served 1.2.3, the header badge said
v1.3.0, the JSON-LD said 1.2.1, and README/CLAUDE.md said "9 components" (it
has 13). Phase 1 rewired every surface to substitute from single sources of
truth at boot; these tests are what keeps that true. Every assertion here is
against a surface a READER meets, traced back to the one source it must now
derive from.

The two sources that remain (root package.json for setup.py, and
dash_mui_charts/package-info.json for __version__) are regenerated together
by `npm run build` — their equality is the "did you rebuild after bumping"
check. scripts/check_release.py makes the same checks at release time with
git-history context; this copy runs on every CI push.
"""
from __future__ import annotations

import json
import re

from conftest import REPO_ROOT, layout_text

COMPONENT_COUNT = 13
COMPONENTS = {
    "BarChart", "CandlestickChart", "CompositeChart", "Heatmap", "LineChart",
    "LiveTradingChart", "PieChart", "ScatterChart", "SimpleTreeView",
    "SparklineChart", "TimeClock", "TreeView", "TreeViewPro",
}


def _root_version() -> str:
    return json.loads((REPO_ROOT / "package.json").read_text())["version"]


def _package_version() -> str:
    import dash_mui_charts

    return dash_mui_charts.__version__


# ------------------------------------------------------------- the versions --


def test_the_two_version_sources_agree():
    """package.json is what PyPI serves (setup.py reads it);
    dash_mui_charts/package-info.json is what __version__ reports. They are
    different files, synchronized only by `npm run build` — bump the root
    and skip the rebuild and you ship a wheel whose label and __version__
    disagree."""
    assert _root_version() == _package_version()


def test_the_header_badge_derives_from_the_package(app):
    """The badge shipped as a hardcoded "v1.3.0" for a full release cycle."""
    assert f"v{_package_version()}" in layout_text(app.layout)


def test_the_served_html_carries_the_real_version(client):
    """The JSON-LD version, substituted from __APP_VERSION__ at boot. It
    carried a hardcoded 1.2.1 two releases after it stopped being true.

    This used to assert a second copy, `v{version}`, from the hand-written
    <noscript> block. That block was retired with the dash-improve-my-llms
    2.6.1 pickup (2026-08-22) — the package's own per-page prerender is
    visible now, and it carries each page's prose rather than one
    duplicated site-level paragraph. The version is a SITE fact, not page
    prose, so it did not move into the prerender: its surfaces are this
    JSON-LD and the header badge, and the badge has its own test above
    (which reads the layout, not the served HTML).
    """
    html = client.get("/").text
    version = _package_version()
    assert f'"version": "{version}"' in html, "JSON-LD version drifted"
    assert "__APP_VERSION__" not in html, "the substitution did not run"


def test_the_changelog_knows_this_version():
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text()
    assert _root_version() in changelog, (
        f"CHANGELOG.md has no section for {_root_version()}"
    )


# ------------------------------------------------------- the component count --


def test_the_package_exports_exactly_the_thirteen_components():
    import dash_mui_charts

    assert set(dash_mui_charts.__all__) == COMPONENTS, (
        sorted(set(dash_mui_charts.__all__) ^ COMPONENTS)
    )
    assert len(COMPONENTS) == COMPONENT_COUNT


def test_the_validate_init_gate_agrees():
    """_validate_init.py is the post-build gate; its EXPECTED set drifting
    from the real export list would let a build drop a component silently."""
    text = (REPO_ROOT / "_validate_init.py").read_text()
    listed = set(re.findall(r'"([A-Z]\w+)"', text))
    assert COMPONENTS <= listed, sorted(COMPONENTS - listed)


def test_the_site_description_counts_thirteen():
    from lib.constants import SITE_DESCRIPTION

    assert f"{COMPONENT_COUNT} " in SITE_DESCRIPTION
    for name in COMPONENTS:
        assert name in SITE_DESCRIPTION, f"{name} missing from SITE_DESCRIPTION"


def test_the_non_js_surface_counts_thirteen(client):
    """The component count as a NON-JS reader sees it.

    Was `test_the_noscript_surface_counts_thirteen`: the count lived in the
    hand-written <noscript> block, which shipped the same catalogue on all
    42 routes. That block is retired (dimll 2.6.1); the count now reaches a
    non-JS reader through the home page's own prose inside the visible
    prerender — which is where a claim about this library belongs, and
    which is why /pie no longer tells anyone about SparklineChart.

    Asserted INSIDE the prerender block, case-insensitively: the prose says
    "13 components" in a sentence, and pinning the exact casing of a
    sentence is how a test starts failing on a copy-edit that broke
    nothing.
    """
    html = client.get("/").text
    assert 'id="dimll-prerender"' in html, "no prerender block on the home page"
    block = html.split('id="dimll-prerender"', 1)[1]
    assert re.search(rf"\b{COMPONENT_COUNT}\s+components?\b", block, re.I), (
        f"the home page's visible prose no longer says {COMPONENT_COUNT} "
        "components — the one place a non-JS reader learns the size of this "
        "library"
    )


def test_no_surface_still_claims_nine_components():
    """The stale count survived in three places at once. The sweep is scoped
    to reader-facing files IN the repo — git history legitimately remembers,
    and .claude/ is untracked local state a CI checkout does not have."""
    offenders = []
    for path in ("README.md", "templates/index.html", "lib/constants.py"):
        text = (REPO_ROOT / path).read_text()
        if re.search(r"\b9 components\b|\bnine components\b", text, re.I):
            offenders.append(path)
    assert offenders == [], f"the stale component count survives in {offenders}"


def test_the_readme_names_every_component():
    readme = (REPO_ROOT / "README.md").read_text()
    missing = sorted(name for name in COMPONENTS if name not in readme)
    assert missing == [], f"README.md does not mention {missing}"
