"""THE COUNTING RULE — the invariant any navigation change invalidates.

This app is a single-page app: every sidebar click is a `dcc.Location`
navigation, so document requests alone would report one hit per visitor with
`/` as the only page. The recorder therefore writes two kinds of row
(lib/analytics.py) and the rollup (lib/traffic_report.build_rollup) counts
them asymmetrically:

    human_hits  =  rows with source="spa" and bot=False   (rendered views)
    bot_hits    =  rows with source="doc" and bot=True    (crawlers run no JS)

A human's hard load produces BOTH a doc row and a spa row — counting rule
means it lands in human_hits exactly once. A JS-executing crawler's spa rows
count nowhere. These tests pin that arithmetic with synthetic rows through
the real `build_rollup` (geo=False keeps the suite offline), because the rule
is documented prose in traffic_report.py and prose does not fail CI.

If a navigation refactor moves page views off the url callback, the spa rows
stop and `human_hits` silently collapses to zero while the site looks fine —
kickoff preservation invariant #5.
"""
from __future__ import annotations

from lib.traffic_report import APP_KEY, SESSION_GAP_S, build_rollup

BROWSER = "Mozilla/5.0 (Macintosh) Chrome/120.0"
GOOGLEBOT = "Mozilla/5.0 (compatible; Googlebot/2.1)"


def _row(source, *, bot, path="/sparkline", ip="203.0.113.7", ua=BROWSER,
         ts="2026-08-01T10:00:00"):
    return {"ts": ts, "path": path, "ua": ua, "ip": ip, "bot": bot,
            "source": source}


def _rollup(rows):
    return build_rollup("2026-08-01", rows=rows, geo=False)


def test_the_app_key_is_the_short_directory_id():
    """STANDARD §5: one short app id on every hub surface."""
    assert APP_KEY == "muicharts"
    assert build_rollup("2026-08-01", rows=[], geo=False)["app"] == "muicharts"


def test_a_hard_load_counts_exactly_once():
    """One person, one hard load: a doc row (the HTTP GET) plus a spa row
    (the url callback). human_hits must be 1, not 2."""
    rows = [_row("doc", bot=False), _row("spa", bot=False)]
    rollup = _rollup(rows)
    assert rollup["human_hits"] == 1
    assert rollup["bot_hits"] == 0


def test_spa_navigation_is_the_page_view_stream():
    """Three sidebar clicks after a hard load = four page views."""
    rows = [_row("doc", bot=False)] + [
        _row("spa", bot=False, path=p, ts=f"2026-08-01T10:0{i}:00")
        for i, p in enumerate(["/", "/sparkline", "/pie", "/heatmap"])
    ]
    rollup = _rollup(rows)
    assert rollup["human_hits"] == 4
    assert {p["path"] for p in rollup["pages"]} == {"/", "/sparkline", "/pie",
                                                    "/heatmap"}


def test_crawlers_only_ever_count_as_doc_bots():
    """A crawler runs no JS, so it appears only as doc rows → bot_hits. A
    JS-executing crawler that DOES reach the spa callback still counts
    nowhere — the bot flag keeps it out of human_hits."""
    rows = [
        _row("doc", bot=True, ua=GOOGLEBOT),
        _row("doc", bot=True, ua=GOOGLEBOT, path="/pie"),
        _row("spa", bot=True, ua="HeadlessChrome bot"),
    ]
    rollup = _rollup(rows)
    assert rollup["bot_hits"] == 2
    assert rollup["human_hits"] == 0
    assert rollup["visitors"] == 0


def test_a_humans_doc_rows_never_reach_bot_hits():
    rows = [_row("doc", bot=False), _row("doc", bot=False, path="/pie")]
    rollup = _rollup(rows)
    assert rollup["bot_hits"] == 0
    assert rollup["human_hits"] == 0  # no JS ran — no rendered page view


def test_visitors_are_ip_browser_pairs_from_human_spa_rows():
    rows = [
        _row("spa", bot=False, ip="203.0.113.7"),
        _row("spa", bot=False, ip="203.0.113.7", ts="2026-08-01T10:01:00"),
        _row("spa", bot=False, ip="198.51.100.2"),
        _row("doc", bot=True, ua=GOOGLEBOT, ip="66.249.66.1"),
    ]
    assert _rollup(rows)["visitors"] == 2


def test_sessions_split_on_the_thirty_minute_gap():
    """SESSION_GAP_S mirrors the hub's session rule — the numbers only
    compare across the network if both sides split identically."""
    assert SESSION_GAP_S == 30 * 60
    base = "2026-08-01T{:02d}:{:02d}:00"
    rows = [
        _row("spa", bot=False, ts=base.format(10, 0)),
        _row("spa", bot=False, ts=base.format(10, 10)),
        # 50 minutes later — a new session
        _row("spa", bot=False, ts=base.format(11, 0)),
    ]
    rollup = _rollup(rows)
    assert rollup["sessions"] == 2
    # median_session_s comes from multi-hit sessions only: the 10-minute one.
    assert rollup["median_session_s"] == 600.0


def test_the_shell_wires_the_spa_recorder(app):
    """The url→analytics-sink callback is the spa stream's only source. Its
    registration disappearing is exactly the silent collapse this file
    exists to catch."""
    wired = any(
        "analytics-sink" in key for key in app.callback_map
    )
    assert wired, "no callback outputs to analytics-sink — spa rows have no writer"
