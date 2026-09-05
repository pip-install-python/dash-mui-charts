"""The ledger, from outside — sync 1.6.44 items 20, 21 and 22.

Three items in one file because they are one mechanism seen from three
places: `/healthz` reports the ledger continuously (20), the pruner decides
what stays in it (21), and the boot guard says once whether it will survive
a restart (22). Item 22's own note is that the guard and the block must
AGREE rather than either being pinned alone.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACKER = REPO_ROOT / "lib" / "analytics_tracker.py"


# ------------------------------------------------- item 20: the block -------

def test_the_block_has_exactly_the_four_keys():
    from lib.health import _ledger_block

    assert set(_ledger_block()) == {"path", "persistent", "visits", "reads"}


def test_the_block_reaches_the_payload():
    from lib.health import health_payload

    assert "ledger" in health_payload("flask")


def test_row_contents_never_appear():
    """Counts, a boolean and a path. Nothing about any visitor."""
    from lib.health import _ledger_block

    block = _ledger_block()
    assert isinstance(block["visits"], int)
    assert isinstance(block["reads"], int)
    assert isinstance(block["persistent"], bool)


def test_persistent_is_false_for_a_path_inside_the_tree(monkeypatch):
    """The container filesystem — measured, not declared."""
    import lib.analytics_tracker as tracker
    import lib.health as health

    monkeypatch.setattr(
        health, "_ledger_block", health._ledger_block  # keep the real one
    )
    monkeypatch.setenv(
        "TRAFFIC_ANALYTICS_FILE", str(REPO_ROOT / "visitor_analytics.json")
    )
    assert tracker.analytics_path()  # env is read at call time
    assert health._ledger_block()["persistent"] is False


# A path that is outside the repository BY CONSTRUCTION, not by assumption.
#
# The first version of this used pytest's `tmp_path`, and that is fragile in
# exactly the environment ops's verification standard prescribes: under
# `env -i` there is no TMPDIR, Python's tempdir fallback resolved to the
# REPOSITORY ROOT ITSELF, and `tmp_path` therefore landed INSIDE the tree —
# so `persistent` correctly reported False and the test failed while the
# code was right. Caught only by running from a clean clone with a stripped
# environment; every normal local run has a TMPDIR outside the repo and
# passed.
#
# The file need not exist: a missing ledger reports zero counts, and
# `persistent` is computed from the PATH, which is the whole point of it
# being a filesystem fact rather than a declaration.
DISK_PATH = "/var/data/visitor_analytics.json"


def test_persistent_is_true_for_a_path_outside_the_tree(monkeypatch):
    """A mounted disk. THE OTHER DIRECTION — the item requires both.

    A boolean pinned in only one direction is satisfied by a constant, and a
    constant `False` here would be indistinguishable from a host that
    genuinely has no disk.
    """
    import lib.health as health

    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", DISK_PATH)
    assert health._ledger_block()["persistent"] is True


def test_the_disk_path_really_is_outside_the_tree():
    """Non-vacuity for the fixture above, since the last one was not."""
    assert not str(DISK_PATH).startswith(str(REPO_ROOT))


def test_a_declared_disk_does_not_make_it_true(tmp_path, monkeypatch):
    """The failure the field exists for: leaflet ran for weeks with a
    DECLARED disk and no disk, and nothing on the wire could contradict the
    declaration. `persistent` must read the filesystem, never a config."""
    import lib.health as health

    monkeypatch.setenv("RENDER_DISK_MOUNT_PATH", "/var/data")  # a declaration
    monkeypatch.setenv(
        "TRAFFIC_ANALYTICS_FILE", str(REPO_ROOT / "visitor_analytics.json")
    )
    assert health._ledger_block()["persistent"] is False


def test_counts_are_read_from_the_real_file(tmp_path, monkeypatch):
    import lib.health as health

    ledger = tmp_path / "visitor_analytics.json"
    ledger.write_text(json.dumps({
        "visits": [{"a": 1}, {"a": 2}, {"a": 3}],
        "reads": [{"b": 1}],
    }))
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(ledger))
    block = health._ledger_block()
    assert block["visits"] == 3 and block["reads"] == 1


def test_a_missing_file_is_zeros_not_an_error(tmp_path, monkeypatch):
    import lib.health as health

    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(tmp_path / "nope.json"))
    block = health._ledger_block()
    assert block["visits"] == 0 and block["reads"] == 0
    assert block["path"], "the path is what a reader needs even when absent"


def test_an_unreadable_ledger_never_breaks_the_probe(tmp_path, monkeypatch):
    """A diagnostic that can take /healthz down with it is a liability."""
    import lib.health as health

    bad = tmp_path / "visitor_analytics.json"
    bad.write_text("{not json at all")
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(bad))
    payload = health.health_payload("flask")
    assert payload["ok"] is True
    assert payload["ledger"]["visits"] == 0


# ------------------------------------------ item 21: reads are not capped ---

def test_reads_are_pruned_by_time_but_never_by_count():
    """20,001 in-window reads plus one outside: 20,001 stay, the dated one goes."""
    from datetime import datetime, timedelta

    import lib.analytics_tracker as tracker

    now = datetime.now()
    fresh = now.timestamp()
    stale = (now - timedelta(days=tracker.RETENTION_DAYS + 5)).timestamp()

    rows = [{"ts": fresh, "kind": "read"} for _ in range(20001)]
    rows.append({"ts": stale, "kind": "read"})

    kept = tracker._prune(rows, stamp=tracker._read_stamp, cap=False)
    assert len(kept) == 20001, (
        f"{len(kept)} reads kept — the count cap is still culling billing-"
        f"grade rows oldest-first"
    )


def test_the_same_corpus_WITH_the_cap_loses_an_in_window_row():
    """PROVE THE TEST RED ON THE PRE-ITEM BEHAVIOUR, as the item demands.

    Without this, the test above passes on a corpus that never reached the
    cap — it would be asserting nothing at all.
    """
    from datetime import datetime, timedelta

    import lib.analytics_tracker as tracker

    now = datetime.now()
    fresh = now.timestamp()
    stale = (now - timedelta(days=tracker.RETENTION_DAYS + 5)).timestamp()
    rows = [{"ts": fresh, "kind": "read"} for _ in range(20001)]
    rows.append({"ts": stale, "kind": "read"})

    capped = tracker._prune(rows, stamp=tracker._read_stamp, cap=True)
    assert len(capped) == tracker.MAX_VISITS == 20000
    assert len(capped) < 20001, "the cap did not bite — the corpus is too small"


def test_visits_KEEP_the_count_cap():
    """The other table's rule is unchanged, and that is deliberate."""
    from datetime import datetime

    import lib.analytics_tracker as tracker

    stamp = datetime.now().isoformat()
    rows = [{"timestamp": stamp} for _ in range(tracker.MAX_VISITS + 500)]
    assert len(tracker._prune(rows)) == tracker.MAX_VISITS


def test_the_call_sites_choose_the_rule_and_are_source_pinned():
    """SOURCE-PINNED BY AST, because the choice lives at the CALL.

    A behavioural test cannot see `cap=True` restored above it — the pruner
    would still behave correctly when called directly, while the writer
    silently capped reads again.
    """
    tree = ast.parse(TRACKER.read_text())
    calls = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_prune"):
            kwargs = {kw.arg: kw for kw in node.keywords}
            # Which table is this call assigned to?
            calls[node.lineno] = kwargs

    assert len(calls) == 2, f"expected two _prune call sites, found {len(calls)}"

    src = TRACKER.read_text().splitlines()
    for lineno, kwargs in calls.items():
        line = src[lineno - 1]
        if '"reads"' in line:
            assert "cap" in kwargs, "the reads call does not pass cap"
            assert kwargs["cap"].value.value is False, (
                "the reads table is capped by count again"
            )
        elif '"visits"' in line:
            assert "cap" not in kwargs or kwargs["cap"].value.value is True


# ------------------------------------------------ item 22: the boot guard ---

def _boot(env_extra):
    """Boot a FRESH interpreter and capture what it printed at import.

    A subprocess, not a re-import: the drop suggested `caplog`, but a `print`
    at import time is not a logging record and caplog never sees it. This
    also exercises the real boot path rather than a re-import inside an
    already-warm interpreter, where the module is cached and prints nothing.
    """
    env = {**os.environ, **env_extra}
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r); import lib.analytics_tracker"
         % str(REPO_ROOT)],
        capture_output=True, text=True, env=env, cwd=str(REPO_ROOT),
    )


def test_an_unset_ledger_path_warns_once_at_boot():
    env = {k: v for k, v in os.environ.items()}
    env.pop("TRAFFIC_ANALYTICS_FILE", None)
    r = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r); import lib.analytics_tracker"
         % str(REPO_ROOT)],
        capture_output=True, text=True,
        env={k: v for k, v in env.items() if k != "TRAFFIC_ANALYTICS_FILE"},
        cwd=str(REPO_ROOT),
    )
    assert "TRAFFIC_ANALYTICS_FILE is unset" in r.stdout, r.stdout
    assert r.stdout.count("TRAFFIC_ANALYTICS_FILE is unset") == 1, "said twice"


def test_a_set_ledger_path_is_SILENT(tmp_path):
    r = _boot({"TRAFFIC_ANALYTICS_FILE": str(tmp_path / "v.json")})
    assert "TRAFFIC_ANALYTICS_FILE is unset" not in r.stdout, r.stdout


def test_the_guard_mirrors_the_existing_boot_line_prefix():
    """An operator greps ONE deploy log — the prefix must match the others."""
    src = TRACKER.read_text()
    assert "[muicharts] WARNING: TRAFFIC_ANALYTICS_FILE" in src


def test_the_guard_and_the_block_AGREE(monkeypatch):
    """Item 22's own note: assert they agree rather than pinning either value.

    The guard fires exactly when the block would report persistent=False for
    the default path, and stays silent exactly when it would not.
    """
    import lib.health as health

    # Unset: guard fires, and the default path is inside the tree.
    monkeypatch.delenv("TRAFFIC_ANALYTICS_FILE", raising=False)
    assert health._ledger_block()["persistent"] is False

    # Set to a disk: guard silent, block says persistent. DISK_PATH rather
    # than tmp_path, for the reason recorded above it.
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", DISK_PATH)
    assert health._ledger_block()["persistent"] is True

    r = _boot({"TRAFFIC_ANALYTICS_FILE": DISK_PATH})
    assert "is unset" not in r.stdout
