"""The battery's machinery, and the mutation checks the invariants rest on.

SYNC 1.6.44 item 5. The four invariants themselves run against a deployed
host and cannot be asserted from a unit test; what CAN and MUST be asserted
here is the machinery they depend on, because both pieces fail SILENTLY:

  * `skip` must be a verdict. Before this item `check()` had two outcomes, so
    a check whose precondition was absent could only go green — `SKIP` was a
    word the summary could count and nothing could raise.
  * the header mapping must keep REPEATED names, and `get_all()` alone is not
    enough: over HTTP/2 an origin may fold repeated headers into one
    comma-separated value, so a check that COUNTS headers reads 1 where it
    expected 3 and reports the relations missing on a healthy host.

And the acceptance the item names explicitly: the `/api rows > 0` line is
mutation-checked — an empty corpus must SKIP, not pass.
"""
from __future__ import annotations

import importlib.util

import pytest

from conftest import REPO_ROOT


def _battery():
    spec = importlib.util.spec_from_file_location(
        "_battery", REPO_ROOT / "scripts" / "network_smoke.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def battery():
    return _battery()


# ------------------------------------------------------- skip is a verdict --

def test_skip_is_a_verdict_not_a_pass(battery):
    """The whole point: an absent precondition must not read as evidence."""
    battery._RESULTS.clear()

    def precondition_absent():
        battery.skip_unless(False, "nothing to measure")

    battery.check("a_check_that_cannot_run", precondition_absent)
    assert battery._RESULTS == [
        ("a_check_that_cannot_run", battery.SKIP, "nothing to measure")
    ]


def test_a_met_precondition_does_not_skip(battery):
    """Non-vacuity: skip_unless must not swallow checks that CAN run."""
    battery._RESULTS.clear()
    battery.check("a_check_that_runs", lambda: battery.skip_unless(True, "n/a"))
    assert battery._RESULTS[0][1] == battery.PASS


def test_a_failure_is_still_a_failure(battery):
    """The skip path must not have widened into a catch-all."""
    battery._RESULTS.clear()
    battery.check("a_failing_check", lambda: battery.expect(False, "boom"))
    assert battery._RESULTS[0][1] == battery.FAIL


def test_skip_and_fail_are_different_verdicts(battery):
    """A skip that scored as a fail would be just as wrong, in reverse."""
    assert battery.SKIP != battery.FAIL != battery.PASS


# ------------------------------------------------ repeated headers survive --

def test_headers_keep_every_repeat(battery):
    h = battery.Headers([
        ("Link", "<https://x/llms.txt>; rel=llms"),
        ("Link", "<https://x/a.txt>; rel=alternate"),
        ("Content-Type", "text/html"),
    ])
    assert len(h.get_all("link")) == 2
    assert h.get("content-type") == "text/html"


def test_a_plain_dict_comprehension_would_have_lost_one(battery):
    """The control run: prove the bug this class exists to fix is real.

    Without this, `test_headers_keep_every_repeat` would pass just as well on
    a host that never sends a repeated header.
    """
    raw = [("Link", "<a>; rel=llms"), ("Link", "<b>; rel=alternate")]
    naive = {k.lower(): v for k, v in raw}
    assert len(naive) == 1, "the fixture does not actually repeat a header"
    assert len(battery.Headers(raw).get_all("link")) == 2


def test_link_relations_parses_separate_headers(battery):
    h = battery.Headers([
        ("Link", '<https://x/llms.txt>; rel="llms"'),
        ("Link", "<https://x/a.txt>; rel=alternate"),
    ])
    assert battery.link_relations(h) == {"llms", "alternate"}


def test_link_relations_parses_the_comma_folded_form(battery):
    """The HTTP/2 shape `get_all()` alone does not solve."""
    h = battery.Headers([
        ("Link", '<https://x/llms.txt>; rel="llms", <https://x/a.txt>; rel=alternate'),
    ])
    assert len(h.get_all("link")) == 1, "fixture is not the folded shape"
    assert battery.link_relations(h) == {"llms", "alternate"}


def test_link_relations_handles_a_multi_token_rel(battery):
    h = battery.Headers([("Link", '<https://x/>; rel="alternate llms"')])
    assert battery.link_relations(h) == {"alternate", "llms"}


def test_link_relations_is_empty_without_a_link_header(battery):
    assert battery.link_relations(battery.Headers([("X", "y")])) == set()


# ------------------------------------------- the /api mutation requirement --

def test_api_rows_check_skips_on_an_empty_corpus(battery, monkeypatch, tmp_path):
    """THE ACCEPTANCE: empty API_PACKAGES must SKIP, not pass.

    Driven by pointing the check's corpus lookup at a tree with no
    `docs/api/api.md`, which is the state a fork with no props page is in.
    The check must then decline to report anything rather than going green
    against a document it never established should carry rows.
    """
    battery._RESULTS.clear()

    # Nothing declared, whatever the file on disk says — the state a fork
    # with no props page is in.
    monkeypatch.setattr(battery.re, "findall", lambda *a, **kw: [])
    monkeypatch.setattr(
        battery, "fetch", lambda *a, **kw: (200, battery.Headers([]), "")
    )

    battery.satellite_checks("http://example.invalid")
    verdicts = dict((n, v) for n, v, _ in battery._RESULTS)
    assert verdicts.get("api_llms_rows_present") == battery.SKIP, (
        f"empty corpus did not skip: {battery._RESULTS}"
    )


def test_the_four_invariants_are_registered_by_name(battery, monkeypatch):
    """The item's detect: registered BY NAME, so a failure reads the same
    on every host in the fleet."""
    seen = []
    monkeypatch.setattr(battery, "check", lambda name, fn: seen.append(name))
    monkeypatch.setattr(
        battery, "fetch",
        lambda *a, **kw: (200, battery.Headers([]), ""),
    )
    battery.satellite_checks("http://example.invalid")

    for name in ("head_get_parity_three_uas", "api_llms_rows_present",
                 "discovery_link_headers_per_lane",
                 "directory_counts_are_derived"):
        assert name in seen, f"{name} is not registered"
