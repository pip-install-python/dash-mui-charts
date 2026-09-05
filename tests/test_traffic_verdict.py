"""A read is not a serve, and /admin/traffic must say which.

SYNC 1.6.44 item 3. The acceptance is specific: a `mark_hidden` path fetched
with a crawler UA shows ONE ROW LABELLED BY ITS VERDICT, and is not counted
among serves. Both halves are asserted here, because a board that renders the
verdict column but still totals denied rows into "served" has ported the
column and missed the item.
"""
from __future__ import annotations

import json
from datetime import date, datetime

import pytest

from dash_improve_my_llms._ledger import EVENT_FIELDS, VERDICTS

DAY = date(2026, 9, 4)


def _read(verdict, vendor_key="claudebot", path="/llms.txt", status=200):
    ev = {k: None for k in EVENT_FIELDS}
    ev.update(
        ts=datetime(DAY.year, DAY.month, DAY.day, 12).timestamp(),
        path=path, method="GET", tier="index", lane="crawler",
        bot_type="training", vendor_key=vendor_key, vendor_class="ai",
        verified="n/a", verdict=verdict, status=status, bytes=500,
        ua="ua", kind="read",
    )
    ev.pop("client_ip")
    return ev


@pytest.fixture
def page(app_module, tmp_path, monkeypatch):
    """`app_module` first — `dash.register_page` raises before instantiation,
    so importing pages/traffic.py without the booted app is a PageError."""
    import importlib

    import pages.traffic as traffic

    p = tmp_path / "visitor_analytics.json"
    p.write_text(json.dumps({"visits": [], "reads": []}))
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(p))
    return importlib.reload(traffic)


def _rows(page, reads):
    from lib.traffic_rollup import load_reads
    import json as _json
    import tempfile
    import os

    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        _json.dump({"visits": [], "reads": reads}, f)
    try:
        return page.verdict_rows(load_reads(path))
    finally:
        os.unlink(path)


def test_a_denied_read_is_its_own_labelled_row(page):
    """The acceptance, exactly: one row, labelled `denied`."""
    reads = [_read("served")] * 4 + [_read("denied", path="/admin/traffic",
                                           status=404)] * 1
    rows = _rows(page, reads)

    denied = [r for r in rows if r["verdict"] == "denied"]
    assert len(denied) == 1, f"expected one denied row, got {rows}"
    assert denied[0]["hits"] == 1
    assert denied[0]["key"] == "claudebot"

    served = [r for r in rows if r["verdict"] == "served"]
    assert len(served) == 1 and served[0]["hits"] == 4


def test_denied_reads_are_not_counted_among_serves(page):
    """The half a verdict column alone does not deliver."""
    reads = [_read("served")] * 4 + [_read("denied")] * 6
    served_total = sum(
        r["hits"] for r in _rows(page, reads) if r["verdict"] == "served"
    )
    assert served_total == 4, "denied rows leaked into the serve count"


def test_headline_counts_serves_separately_from_reads(page):
    """`reads` and `served` diverge the moment anything is turned away."""
    from conftest import layout_text

    reads = [_read("served")] * 3 + [_read("blocked")] * 2
    block = page.headline_block(DAY, reads)
    text = layout_text(block)
    assert "served" in text
    # 3 serves out of 5 reads — the number that must appear, not 5.
    assert "3" in text


def test_every_verdict_the_package_defines_survives_the_fold(page):
    """No verdict silently collapses into another.

    Guards the normalisation: `verdict or "served"` must only catch an ABSENT
    verdict, never rewrite a real one.
    """
    reads = [_read(v) for v in VERDICTS]
    rows = _rows(page, reads)
    assert {r["verdict"] for r in rows} == set(VERDICTS)
    assert all(r["hits"] == 1 for r in rows)


def test_a_verdictless_row_reads_as_served_not_unknown(page):
    """Rows written before the field existed are serves, not a new bucket.

    `_ledger.verdict_for_status` returns "served" for any unlisted status, so
    this matches the package rather than inventing a local convention.
    """
    row = _read("served")
    row["verdict"] = None
    rows = _rows(page, [row])
    assert [r["verdict"] for r in rows] == ["served"]


def test_the_hub_payload_fold_is_untouched(page):
    """`vendor_rows` must NOT have gained the verdict key.

    The board is allowed to be finer-grained than the wire report; widening
    `vendor_rows` would change the v4 vendors[] block this host POSTs to
    2plot.ai for every consumer of it. Pins that the item stayed page-local.
    """
    from lib.traffic_rollup import load_reads, vendor_rows
    import json as _json
    import os
    import tempfile

    reads = [_read("served")] * 2 + [_read("denied")] * 3
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        _json.dump({"visits": [], "reads": reads}, f)
    try:
        rows = vendor_rows(load_reads(path))
    finally:
        os.unlink(path)

    assert len(rows) == 1, "vendor_rows split on verdict — the hub payload moved"
    assert rows[0]["hits"] == 5
    assert "verdict" not in rows[0]


def test_the_rendered_table_carries_a_verdict_column(page):
    """The column reaches the layout, not just the fold."""
    from conftest import layout_text
    from lib.traffic_rollup import load_reads
    import json as _json
    import os
    import tempfile

    reads = [_read("served")] * 2 + [_read("gated")] * 1
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        _json.dump({"visits": [], "reads": reads}, f)
    try:
        table = page.vendor_tier_table(load_reads(path))
    finally:
        os.unlink(path)

    text = layout_text(table)
    assert "verdict" in text, "no verdict header in the rendered table"
    assert "gated" in text, "the verdict itself never reached the layout"
