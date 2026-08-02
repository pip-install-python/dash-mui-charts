"""The network's internal-traffic contract — the analytics point of truth.

The rule (https://2plot.ai/docs/satellite-analytics, "Internal traffic"): a
request whose User-Agent contains `2plot-internal` is 2plot machinery talking
to itself — the hub's hourly health sweep, CI smoke batteries, this app's own
server-to-server calls — and is counted NOWHERE. Dropped at WRITE time,
before bot classification. `/healthz` is never a visit either.

Both halves are tested, because a contract kept on only one side is not kept
at all:

*inbound*   token-carrying requests never reach the hit log, and therefore
            never reach human_hits/bot_hits in the hourly rollup;
*outbound*  every call this host makes to another network host sends
            INTERNAL_UA, so the far side can apply the same rule. That half
            was the Phase 2 fix: the ad client fetched a campaign from
            2plot.dev on every page view, arriving as `python-requests/2.x`,
            and the hub counted this satellite's readers as its own bots.
"""
from __future__ import annotations

import urllib.request

import pytest

from conftest import BROWSER_UA, CRAWLER_UA, REPO_ROOT
from lib import analytics
from lib.constants import INTERNAL_UA, INTERNAL_UA_TOKEN, internal_ua

# A real doc page: analytics.trackable_path drops infrastructure paths
# (/healthz, /llms.txt, ...), so an assertion against one of those would
# pass no matter what the recorder did.
PAGE = "/sparkline"


def _ledger():
    return analytics.load_day()


# --------------------------------------------------------------- the token --


def test_token_is_the_network_wide_string():
    """The contract only works if every host agrees on the byte sequence."""
    assert INTERNAL_UA_TOKEN == "2plot-internal"
    assert INTERNAL_UA.startswith(INTERNAL_UA_TOKEN)


def test_caller_suffix_never_breaks_the_token():
    ua = internal_ua("traffic-report")
    assert INTERNAL_UA_TOKEN in ua
    assert ua.endswith("traffic-report")
    assert internal_ua() == INTERNAL_UA
    assert internal_ua("  ") == INTERNAL_UA


# ------------------------------------------------------------------ inbound --


def test_the_tests_can_see_the_ledger_at_all(client, tmp_state_dir):
    """Guard for every delta assertion below: if the ledger path were wrong
    (or the suite were writing into the repo's own analytics/), every
    "count did not change" test would pass vacuously."""
    assert str(analytics.analytics_dir()) == tmp_state_dir
    before = len(_ledger())
    client.get(PAGE, user_agent=BROWSER_UA)
    assert len(_ledger()) == before + 1


def test_internal_ua_is_counted_nowhere(client):
    before = len(_ledger())
    client.get(PAGE, user_agent=internal_ua("network-smoke"))
    client.get("/", user_agent=INTERNAL_UA)
    assert len(_ledger()) == before


def test_a_crawler_shaped_probe_carrying_the_token_stays_internal(client):
    """The battery's crawler probe exercises the bot path deliberately. It
    must still not be counted — which is precisely why the drop happens
    BEFORE bot classification; after it, the probe files under bot_hits."""
    before = len(_ledger())
    client.get(PAGE, user_agent=f"{CRAWLER_UA} {INTERNAL_UA}")
    assert len(_ledger()) == before


def test_the_token_is_matched_case_insensitively(client):
    before = len(_ledger())
    client.get(PAGE, user_agent="2PLOT-INTERNAL/1.0 Health-Sweep")
    assert len(_ledger()) == before


def test_healthz_is_never_a_visit(client):
    before = len(_ledger())
    client.get("/healthz", user_agent="Render/1.0 health-check")
    client.get("/healthz", user_agent=BROWSER_UA)
    assert len(_ledger()) == before


def test_real_traffic_is_still_counted(client):
    """The exclusions must not have lobotomised the recorder: a rule that
    drops everything also satisfies every assertion above."""
    before = len(_ledger())
    client.get(PAGE, user_agent=BROWSER_UA)
    client.get(PAGE, user_agent=CRAWLER_UA)
    rows = _ledger()
    assert len(rows) == before + 2
    assert rows[-2]["bot"] is False
    assert rows[-1]["bot"] is True
    assert all(r["source"] == "doc" for r in rows[-2:])


# ----------------------------------------------------------------- outbound --


class _Captured(Exception):
    """Abort the request once the headers have been seen."""


def test_the_traffic_rollup_post_sends_the_token(monkeypatch):
    from lib import traffic_report

    seen = {}

    def fake_urlopen(req, timeout=None):
        seen["ua"] = req.get_header("User-agent") or ""
        raise _Captured

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(_Captured):
        traffic_report.report_traffic(
            {"app": "muicharts", "date": "2026-08-01"}, secret="test-secret"
        )
    assert INTERNAL_UA_TOKEN in seen["ua"]


def test_the_ad_client_session_carries_the_token():
    """One fetch per docs page view — the loudest outbound call this app
    makes. The UA is set on the session at import, so asserting the header
    covers every request the session will ever send."""
    from lib import ad_client

    assert INTERNAL_UA_TOKEN in ad_client._session.headers.get("User-Agent", "")


@pytest.mark.parametrize("script", ["network_smoke", "smoke_live"])
def test_every_battery_script_sends_the_token(script):
    """A post-deploy battery sweeps every peer; it must not register
    anywhere as a visitor or a crawler."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        f"_ua_{script}", REPO_ROOT / "scripts" / f"{script}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    agents = [
        value
        for name, value in vars(module).items()
        if (name == "UA" or name.endswith("_UA")) and isinstance(value, str)
    ]
    assert agents, f"scripts/{script}.py declares no User-Agent constant"
    missing = [ua for ua in agents if INTERNAL_UA_TOKEN not in ua]
    assert missing == [], f"scripts/{script}.py sends untokened UAs: {missing}"
