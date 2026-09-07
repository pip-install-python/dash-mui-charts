"""A proxied robots.txt is not your robots.txt — sync 1.6.44 item 19.

The file a crawler receives is whatever the edge in front of this host chose
to serve. A CDN may manage it, and the item names two shapes, both of which
are INVISIBLE to a battery that fetches the URL and looks for expected lines:

  * an INJECTED STANZA — rules the app never wrote. They are ADDITIONAL, so
    every expected line is still present and nothing looks wrong.
  * A MARKER WITH NOTHING UNDER IT — a managed block that adds no rule at
    all. Nothing is missing either.

Both are demonstrated below against the real comparison logic, which is why
this file exists rather than a single "robots.txt is served" assertion.
"""
from __future__ import annotations

import pytest

from lib.robots_expected import (
    ROBOTS_CONFIG,
    directive_lines,
    expected_robots_txt,
)

BASE = "https://muicharts.2plot.dev"


def _compare(served: str, base: str = BASE):
    """The battery's two-directional comparison, as a pair of sets."""
    want = set(directive_lines(expected_robots_txt(base)))
    got = set(directive_lines(served))
    return sorted(want - got), sorted(got - want)


# ------------------------------------------------------------ the generator --

def test_the_expectation_comes_from_the_package_not_a_reimplementation():
    """The item's note, pinned as a source fact.

    A hand-written expectation compares the edge against somebody's BELIEFS
    about the config, so it agrees with the wire exactly when both are wrong
    in the same way. The expectation must come from the package's own
    generator.
    """
    import inspect

    from lib import robots_expected

    src = inspect.getsource(robots_expected.expected_robots_txt)
    assert "generate_robots_txt" in src


def test_the_app_and_the_battery_share_one_config_object():
    """ONE DECLARATION, TWO CONSUMERS. run.py must not hold its own copy."""
    import run

    assert run.app._robots_config is ROBOTS_CONFIG


def test_the_generated_file_is_not_empty():
    """Note 88: an empty expectation makes every comparison below vacuous."""
    lines = directive_lines(expected_robots_txt(BASE))
    assert len(lines) > 3, f"only {len(lines)} directives generated: {lines}"


def test_the_app_agrees_with_itself():
    """The control run: unmodified output must compare clean both ways."""
    missing, injected = _compare(expected_robots_txt(BASE))
    assert missing == [] and injected == []


# -------------------------------------------------- shape 1: injected stanza --

def test_an_injected_stanza_is_caught():
    """Rules the app never wrote. ADDITIONAL, so nothing is missing."""
    served = expected_robots_txt(BASE) + (
        "\n\n# Managed by the edge\n"
        "User-agent: SomeVendorBot\n"
        "Disallow: /\n"
    )
    missing, injected = _compare(served)

    assert missing == [], (
        "sanity: an injection removes nothing, so a 'missing lines' check "
        "alone cannot see it — which is the point of the item"
    )
    assert injected, "the injected stanza was not detected"
    assert any("somevendorbot" in line.lower() for line in injected)


def test_a_one_sided_check_would_have_passed_the_injection():
    """THE NON-VACUITY THAT MATTERS.

    Proves the two-directional comparison is doing work: the direction a
    naive battery checks (are my lines present?) is green on the injected
    file. Without this, the test above could pass on a check that happened
    to be one-sided in the other direction.
    """
    served = expected_robots_txt(BASE) + "\nUser-agent: X\nDisallow: /\n"
    want = set(directive_lines(expected_robots_txt(BASE)))
    got = set(directive_lines(served))
    assert want <= got, "every expected directive is still present"


# --------------------------------------------- shape 2: empty managed marker --

def test_a_marker_with_nothing_under_it_is_caught():
    """A managed block that adds no rule. Nothing is missing OR added as a
    directive — so it must be caught as a non-directive line."""
    served = expected_robots_txt(BASE) + (
        "\n\n# BEGIN MANAGED BLOCK\n"
        "MANAGED-BLOCK-MARKER\n"
        "# END MANAGED BLOCK\n"
    )
    missing, injected = _compare(served)
    assert missing == []
    assert injected == ["managed-block-marker"], injected


def test_comments_alone_are_not_treated_as_injection():
    """The counter-case, so the check is usable.

    An edge or a maintainer may add a comment without changing a rule. If
    that read as an injection the row would cry wolf and get ignored, which
    is how a real one gets missed.
    """
    served = expected_robots_txt(BASE) + "\n# just a comment\n\n\n"
    missing, injected = _compare(served)
    assert missing == [] and injected == []


def test_reflowed_whitespace_does_not_read_as_a_difference():
    """Directives are compared as rules, not as bytes.

    WHITESPACE ONLY, and the first draft of this test got that wrong by
    upper-casing whole lines. Field NAMES are case-insensitive and are
    normalised; VALUES are not, and must not be — a `Disallow` path and a
    `Sitemap` URL are case-sensitive, so folding their case would blind the
    check to exactly the kind of substitution an edge might make. The test
    was over-aggressive, not the comparison.
    """
    served = "\n".join(
        f"   {line}   " for line in expected_robots_txt(BASE).splitlines()
    )
    missing, injected = _compare(served)
    assert missing == [] and injected == [], (
        f"reflowed whitespace read as a rule change: "
        f"missing={missing} injected={injected}"
    )


def test_a_field_name_in_another_case_is_the_same_rule():
    """Field names ARE case-insensitive per the robots.txt convention."""
    served = expected_robots_txt(BASE).replace("User-agent:", "USER-AGENT:")
    missing, injected = _compare(served)
    assert missing == [] and injected == []


def test_a_changed_value_is_NOT_forgiven():
    """The complement, and the reason values keep their case: an edge that
    repoints the sitemap at another host must be caught."""
    served = expected_robots_txt(BASE).replace(
        "muicharts.2plot.dev", "someone-elses-host.example"
    )
    missing, injected = _compare(served)
    assert missing and injected, "a repointed sitemap URL was not detected"


# ----------------------------------------------------- a REMOVED rule too ---

def test_a_stripped_directive_is_caught():
    """The other direction: an edge that DROPS one of this app's rules."""
    lines = expected_robots_txt(BASE).splitlines()
    kept = [ln for ln in lines if not ln.lower().startswith("crawl-delay")]
    missing, injected = _compare("\n".join(kept))
    assert any("crawl-delay" in m for m in missing), missing


# ------------------------------------------------------- the battery wiring --

def test_the_row_is_registered_by_name():
    import importlib.util
    from pathlib import Path

    repo = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        "_battery19", repo / "scripts" / "network_smoke.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    seen = []
    import types

    original = mod.check
    mod.check = lambda name, fn: seen.append(name)
    mod.fetch = lambda *a, **kw: (200, mod.Headers([]), "")
    try:
        mod.satellite_checks("http://example.invalid")
    finally:
        mod.check = original
    assert "ai_bot_posture" in seen
    assert isinstance(types, object)  # keep the import meaningful


def test_cd_installs_the_app_before_running_the_battery():
    """The rider: without the install the row SKIPS FOREVER, reading green
    while comparing nothing. CD's verify job used to do checkout +
    setup-python and no install at all."""
    from pathlib import Path

    cd = (Path(__file__).resolve().parent.parent
          / ".github" / "workflows" / "cd.yml").read_text()
    verify = cd.split("  verify:", 1)[1]
    assert "pip install -r requirements.txt" in verify, (
        "cd.yml's verify job does not install the app, so ai_bot_posture "
        "cannot import the generator and will skip on every run"
    )
    # And the install must come BEFORE the battery runs.
    assert verify.index("pip install -r requirements.txt") < verify.index(
        "scripts/network_smoke.py"
    )


@pytest.mark.parametrize("field", ["block_ai_training", "allow_ai_search",
                                   "allow_traditional"])
def test_the_recorded_posture_is_what_is_configured(field):
    """DIVERGENCES records this posture; the config must still match it."""
    expected = {"block_ai_training": False, "allow_ai_search": True,
                "allow_traditional": True}[field]
    assert getattr(ROBOTS_CONFIG, field) is expected


# ------------------------------------------- the version-skew guard (live) --

def _battery():
    import importlib.util
    from pathlib import Path

    repo = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        "_battery19b", repo / "scripts" / "network_smoke.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_posture(mod, *, health_body, robots):
    """Drive just the ai_bot_posture row with a scripted host."""
    def fake_fetch(url, **kw):
        body = health_body if url.endswith("/healthz") else robots
        return (200, mod.Headers([]), body)

    mod.fetch = fake_fetch
    mod._RESULTS.clear()
    captured = {}

    real_check = mod.check

    def capture(name, fn):
        if name == "ai_bot_posture":
            real_check(name, fn)
            captured["verdict"] = mod._RESULTS[-1][1]
            captured["detail"] = mod._RESULTS[-1][2]

    mod.check = capture
    try:
        mod.satellite_checks("https://muicharts.2plot.dev")
    finally:
        mod.check = real_check
    return captured


def test_a_host_with_no_llms_version_skips_rather_than_failing():
    """MEASURED LIVE, 2026-09-05: this is production's state today.

    Item 1 has not deployed, so /healthz reports no llms_version and the
    comparison cannot be shown to be same-version. It must SKIP — a FAIL
    here would send somebody hunting a CDN that is doing nothing.
    """
    mod = _battery()
    out = _run_posture(mod, health_body='{"ok": true}',
                       robots=expected_robots_txt(BASE))
    assert out["verdict"] == mod.SKIP, out
    assert "llms_version" in out["detail"]


def test_a_version_skew_skips_rather_than_failing():
    """THE FALSE POSITIVE THIS GUARD EXISTS FOR, reproduced.

    The first live run of this row reported
        missing: content-signal: search=yes, ai-input=yes, ai-train=yes
    against production — a directive dimll 2.10.0 emits and the deployed
    build's older version does not. Version skew, not a proxy.
    """
    mod = _battery()
    out = _run_posture(
        mod,
        health_body='{"ok": true, "llms_version": "2.8.0"}',
        robots=expected_robots_txt(BASE),
    )
    assert out["verdict"] == mod.SKIP, out
    assert "skew" in out["detail"].lower()


def test_a_matching_version_actually_compares():
    """Non-vacuity: the guard must not skip everything forever."""
    import dash_improve_my_llms as pkg

    mod = _battery()
    out = _run_posture(
        mod,
        health_body='{"ok": true, "llms_version": "%s"}' % pkg.__version__,
        robots=expected_robots_txt(BASE),
    )
    assert out["verdict"] == mod.PASS, out


def test_a_matching_version_with_an_injection_FAILS():
    """And the row does its job once the versions agree."""
    import dash_improve_my_llms as pkg

    mod = _battery()
    out = _run_posture(
        mod,
        health_body='{"ok": true, "llms_version": "%s"}' % pkg.__version__,
        robots=expected_robots_txt(BASE) + "\nUser-agent: EdgeBot\nDisallow: /\n",
    )
    assert out["verdict"] == mod.FAIL, out
    assert "never wrote" in out["detail"]


# ----------------------------- the CI failure this row shipped with ---------

def test_the_expectation_uses_the_APPS_base_not_the_probe_url():
    """CD run 34073327071, `ci / Docs site · pytest (zero secrets)`, FAILED.

    The row generated its expectation from the URL the battery was DIALLING
    (`http://127.0.0.1:8550` in CI) instead of the app's own BASE_URL, so it
    compared "the file the app would serve if it lived at 127.0.0.1" against
    "the file the app actually serves":

        missing : sitemap: http://127.0.0.1:8550/sitemap.xml
        injected: sitemap: https://muicharts.2plot.dev/sitemap.xml

    It passed against production, where the probe URL and BASE_URL coincide,
    and failed the moment it ran against the CI container — which is exactly
    the class of bug a production-only check cannot show you.

    The base is the app's IDENTITY, not the prober's address.
    """
    from lib.constants import BASE_URL

    at_app = directive_lines(expected_robots_txt())
    at_probe = directive_lines(expected_robots_txt("http://127.0.0.1:8550"))
    assert at_app != at_probe, "the fixture does not distinguish the two bases"
    assert any(BASE_URL in line for line in at_app)
    assert not any("127.0.0.1" in line for line in at_app)


def test_a_container_probe_still_compares(monkeypatch):
    """Probing the app at localhost must NOT skip — that is where CI runs."""
    mod = _battery()
    import dash_improve_my_llms as pkg

    out = _run_posture_at(
        mod, "http://127.0.0.1:8550",
        health_body='{"ok": true, "llms_version": "%s"}' % pkg.__version__,
        robots=expected_robots_txt(),
    )
    assert out["verdict"] == mod.PASS, out


def test_a_cross_host_probe_declines_instead_of_answering_wrongly():
    """A workflow_dispatch against another host is a different question.

    This checkout's robots config describes THIS app, so it cannot say what
    someone else's host ought to serve. Declining is the honest answer; the
    alternative is a confident diff about a config we do not have.
    """
    mod = _battery()
    import dash_improve_my_llms as pkg

    out = _run_posture_at(
        mod, "https://some-other-host.2plot.dev",
        health_body='{"ok": true, "llms_version": "%s"}' % pkg.__version__,
        robots=expected_robots_txt(),
    )
    assert out["verdict"] == mod.SKIP, out
    assert "another host" in out["detail"]


def _run_posture_at(mod, base, *, health_body, robots):
    def fake_fetch(url, **kw):
        body = health_body if url.endswith("/healthz") else robots
        return (200, mod.Headers([]), body)

    mod.fetch = fake_fetch
    mod._RESULTS.clear()
    captured = {}
    real_check = mod.check

    def capture(name, fn):
        if name == "ai_bot_posture":
            real_check(name, fn)
            captured["verdict"] = mod._RESULTS[-1][1]
            captured["detail"] = mod._RESULTS[-1][2]

    mod.check = capture
    try:
        mod.satellite_checks(base)
    finally:
        mod.check = real_check
    return captured
