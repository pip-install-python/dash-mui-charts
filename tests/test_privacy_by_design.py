"""The tracker stores no address and looks nothing up — sync 1.6.44 item 16.

What was removed, and why it mattered: `_geolocate` POSTed every non-bot
visitor's IP address to `http://ip-api.com` — a third party, over PLAINTEXT
HTTP — to turn it into a city, on a background thread, and the visit row
stored the raw address beside the result. Three problems on one path: a
third-party disclosure nothing on the site disclosed, in cleartext, and an
identifier that made every row personally identifying for the whole 45-day
retention window.

THE DETECT IS PARSED, NOT GREPPED, and the item says so explicitly. A
substring check for "ip-api" cannot pass on a tree that DOCUMENTS the
removal — which this one does, at length, immediately above the replacement
— so it would fail its own detect. The check walks the AST for imports and
function definitions instead.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACKER = REPO_ROOT / "lib" / "analytics_tracker.py"

# Any of these in the tracker means an address can leave this process.
NETWORK_MODULES = {"requests", "urllib", "urllib.request", "http.client",
                   "socket", "httpx", "aiohttp"}

# The callables the item names. None may be DEFINED here any more.
REMOVED_CALLABLES = {"_geolocate", "geo_for", "get_geolocation",
                     "_backfill_geo"}


@pytest.fixture(scope="module")
def tree():
    return ast.parse(TRACKER.read_text())


def test_the_tracker_imports_nothing_that_can_reach_the_network(tree):
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    offending = {m for m in imported
                 if m in NETWORK_MODULES or m.split(".")[0] in NETWORK_MODULES}
    assert offending == set(), (
        f"the tracker can reach the network again: {sorted(offending)}"
    )


def test_none_of_the_removed_callables_is_defined(tree):
    defined = {n.name for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert not (defined & REMOVED_CALLABLES), (
        f"geolocation machinery is back: {sorted(defined & REMOVED_CALLABLES)}"
    )


def test_the_parse_actually_saw_the_module(tree):
    """Note 88 applied to the detect itself.

    An empty or unparsed tree would satisfy both tests above trivially.
    """
    defined = {n.name for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert "track_visit" in defined and len(defined) > 10


def test_a_substring_grep_would_have_failed_here(tree):
    """The item's CORRECTION, pinned so nobody reinstates the weaker detect.

    The drop's original detect was `no "ip-api" string in lib/`. This module
    documents the removal in prose, so that detect reports a defect on the
    very tree that fixed it — the item corrected it to a parsed check for
    exactly this reason.
    """
    assert "ip-api" in TRACKER.read_text(), (
        "the explanatory comment was deleted; if that was deliberate, this "
        "test should go too, but the parsed detects above are what matter"
    )


# ------------------------------------------------------------ acceptance ----

def _visit(tracker, headers, ua="Mozilla/5.0 (Macintosh) Chrome/128 Safari/537"):
    tracker._buffer.clear()
    tracker.track_visit("/sparkline", ua, "203.0.113.9", headers=headers)
    assert tracker._buffer, "nothing was tracked"
    return tracker._buffer[-1]


@pytest.fixture
def tracker(tmp_path, monkeypatch):
    import lib.analytics_tracker as mod

    monkeypatch.setattr(mod, "VISITOR_SALT_FILE", tmp_path / ".visitor_salt")
    mod._salt_cache.clear()
    monkeypatch.setattr(mod, "KEEP_CLIENT_IP", False)
    return mod.tracker


def test_no_ip_address_in_a_default_config_visit_row(tracker):
    row = _visit(tracker, {"CF-IPCountry": "GB"})
    assert "ip_address" not in row, "the raw address is still being stored"
    assert row["visitor_key"], "no visitor_key to replace it"


def test_a_visit_with_cf_ipcity_carries_city(tracker):
    row = _visit(tracker, {"CF-IPCountry": "GB", "CF-IPCity": "Manchester"})
    assert row["location"]["city"] == "Manchester"
    assert row["location"]["country"] == "GB"


def test_a_visit_without_city_carries_country_only(tracker):
    row = _visit(tracker, {"CF-IPCountry": "GB"})
    assert row["location"] == {"country": "GB", "country_code": "GB"}
    assert "city" not in row["location"]


def test_a_visit_with_no_headers_carries_no_location_at_all(tracker):
    row = _visit(tracker, {})
    assert "location" not in row, (
        "a location appeared for a request the CDN told us nothing about"
    )


def test_the_opt_in_still_works(tracker, monkeypatch):
    """The switch exists; it is just off by default."""
    import lib.analytics_tracker as mod

    monkeypatch.setattr(mod, "KEEP_CLIENT_IP", True)
    row = _visit(tracker, {"CF-IPCountry": "GB"})
    assert row["ip_address"] == "203.0.113.9"


# -------------------------------------------------------- the visitor key ---

def test_the_key_is_stable_for_one_visitor(tracker):
    a = _visit(tracker, {"CF-IPCountry": "GB"})
    b = _visit(tracker, {"CF-IPCountry": "GB"})
    assert a["visitor_key"] == b["visitor_key"]


def test_two_uas_behind_one_address_are_two_visitors(tracker):
    a = _visit(tracker, {"CF-IPCountry": "GB"}, ua="Chrome/128 Safari/537")
    b = _visit(tracker, {"CF-IPCountry": "GB"}, ua="Firefox/131 Gecko/2010")
    assert a["visitor_key"] != b["visitor_key"], (
        "two readers behind one NAT collapsed into one visitor"
    )


def test_the_key_is_not_the_address_in_disguise(tmp_path, monkeypatch):
    """A DIFFERENT SALT must produce a different key for the same address.

    This is what makes the hash non-reversible in practice: without the salt
    an attacker holding the ledger could hash the whole IPv4 space and undo
    it in an afternoon.
    """
    import lib.analytics_tracker as mod

    monkeypatch.setattr(mod, "VISITOR_SALT_FILE", tmp_path / "a")
    mod._salt_cache.clear()
    first = mod.visitor_key_for("203.0.113.9", "Chrome/128")

    monkeypatch.setattr(mod, "VISITOR_SALT_FILE", tmp_path / "b")
    mod._salt_cache.clear()
    second = mod.visitor_key_for("203.0.113.9", "Chrome/128")

    assert first != second
    assert "203.0.113.9" not in first


def test_the_salt_is_gitignored():
    """IN THE SAME COMMIT that introduced it — a committed salt makes every
    visitor_key in every fork recomputable and undoes the item entirely."""
    import subprocess

    r = subprocess.run(
        ["git", "check-ignore", "-q", ".visitor_salt"],
        cwd=REPO_ROOT, capture_output=True,
    )
    assert r.returncode == 0, ".visitor_salt is NOT gitignored"


def test_the_salt_is_not_tracked():
    """Belt and braces: ignored is not the same as absent from the index."""
    import subprocess

    r = subprocess.run(
        ["git", "ls-files", "--error-unmatch", ".visitor_salt"],
        cwd=REPO_ROOT, capture_output=True,
    )
    assert r.returncode != 0, ".visitor_salt is committed"


# ------------------------------------------------- the rollup's fallback ----

def test_the_rollup_prefers_a_stored_visitor_key():
    from lib.traffic_rollup import visitor_key

    row = {"visitor_key": "abc123", "ip_address": "203.0.113.9",
           "user_agent": "Chrome/128"}
    assert visitor_key(row) == "abc123"


def test_the_rollup_falls_back_for_a_pre_item_row():
    """THE HALF THAT SAVES THE HISTORY.

    Rows written before this item have no visitor_key and do have an
    address. Without the fallback every one of them inside the 45-day
    retention window collapses to its User-Agent, and a month of history
    reports a handful of visitors — a schema change that looks exactly like
    a traffic cliff.
    """
    from lib.traffic_rollup import visitor_key

    old = {"ip_address": "203.0.113.9", "user_agent": "Chrome/128"}
    other = {"ip_address": "198.51.100.4", "user_agent": "Chrome/128"}
    assert visitor_key(old) != visitor_key(other), (
        "two pre-item rows from different addresses collapsed into one visitor"
    )
    assert visitor_key(old).startswith("203.0.113.9|")


def test_a_row_with_neither_still_resolves():
    from lib.traffic_rollup import visitor_key

    assert visitor_key({"user_agent": "Chrome/128"}).startswith("?|")


def test_the_conditional_grep_finds_nothing():
    """pip-docs+ only, but cheap and unambiguous: no sample locations."""
    import re

    src = TRACKER.read_text()
    assert not re.search(r"sample_locations|Mumbai", src)
