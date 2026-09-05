"""`vendor_class` prefers the package and derives only when it is absent.

SYNC 1.6.44 item 8. Both directions are pinned, because the item's own note
warns that a one-sided test cannot fail: "prefer that never derives" and
"derive that never prefers" BOTH pass a test that only checks one of them.

The conflicting fixture is the load-bearing part of the prefer half. If the
event's class and the registry's class agree, a test asserting the result
equals the event's class passes just as well on an implementation that
ignored the event entirely.
"""
from __future__ import annotations

import lib.analytics_tracker as tracker_mod

CRAWLER_UA = "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)"


def _registry_class(key):
    from dash_improve_my_llms import vendors

    return getattr(vendors.get_vendor(key), "cls", None)


def test_the_fixture_vendor_is_actually_in_the_registry():
    """Non-vacuity for everything below: if `gptbot` were unknown, the derive
    half would trivially return None and look correct."""
    assert _registry_class("gptbot"), "gptbot has no class in the registry"


def test_a_package_provided_class_passes_through_untouched(monkeypatch):
    """PREFER. The fixture CONFLICTS with the registry on purpose."""
    real = _registry_class("gptbot")
    conflicting = f"not-{real}"
    assert conflicting != real

    monkeypatch.setattr(
        tracker_mod, "classify",
        lambda ua, ip=None: {
            "lane": "crawler", "bot_type": "training",
            "vendor_key": "gptbot", "vendor_class": conflicting,
            "verified": "unverified",
        },
    )
    out = tracker_mod._classify(CRAWLER_UA)
    assert out["vendor_class"] == conflicting, (
        "the derived class overwrote one the package actually emitted"
    )


def test_an_absent_class_is_derived_from_the_registry(monkeypatch):
    """DERIVE. The shape a wheel below dimll 2.9.4 produces."""
    monkeypatch.setattr(
        tracker_mod, "classify",
        lambda ua, ip=None: {
            "lane": "crawler", "bot_type": "training",
            "vendor_key": "gptbot", "vendor_class": None,
            "verified": "unverified",
        },
    )
    out = tracker_mod._classify(CRAWLER_UA)
    assert out["vendor_class"] == _registry_class("gptbot")


def test_an_absent_class_with_no_vendor_stays_absent(monkeypatch):
    """The unidentified crawler lane has no class, and must not gain one."""
    monkeypatch.setattr(
        tracker_mod, "classify",
        lambda ua, ip=None: {
            "lane": "crawler", "bot_type": None,
            "vendor_key": None, "vendor_class": None, "verified": "n/a",
        },
    )
    assert tracker_mod._classify("something/1.0")["vendor_class"] is None


def test_an_unknown_vendor_key_does_not_raise(monkeypatch):
    """The registry lookup must be total — a diagnostic never breaks a write."""
    monkeypatch.setattr(
        tracker_mod, "classify",
        lambda ua, ip=None: {
            "lane": "crawler", "bot_type": "training",
            "vendor_key": "a-vendor-that-does-not-exist", "vendor_class": None,
            "verified": "n/a",
        },
    )
    assert tracker_mod._classify("x")["vendor_class"] is None


def test_the_derivation_reads_the_registry_and_not_a_local_map():
    """The item's note: derive from `vendors.get_vendor().cls`, never a map.

    A second copy of the vendor→class mapping in this repo is the same defect
    as the UA list the tracker used to carry — it goes stale silently and the
    value becomes this app's opinion rather than the network's grouping.
    """
    import ast
    import inspect

    src = inspect.getsource(tracker_mod._vendor_class_from_registry)
    tree = ast.parse(src.lstrip())

    # No dict literal mapping vendor keys to classes.
    dicts = [n for n in ast.walk(tree)
             if isinstance(n, ast.Dict) and n.keys]
    assert dicts == [], "a local vendor→class map appeared in the tracker"
    assert "get_vendor" in src


def test_the_real_classifier_still_produces_a_class_end_to_end():
    """Unmonkeypatched, against the resolved wheel."""
    out = tracker_mod._classify(CRAWLER_UA)
    assert out["vendor_key"] == "gptbot"
    assert out["vendor_class"], "no vendor_class from either source"


def test_the_totalising_contract_is_unchanged():
    """Item 8 must not have moved anything else in the row.

    `_classify` is total: it never raises and always carries a `lane`. An
    EMPTY UA is crawler-lane at dimll >= 2.8 — no engine token means no
    browser — which is the documented behaviour and not a default kicking in;
    the `or "browser"` fallback exists for the case where classify() itself
    fails and returns nothing at all.
    """
    out = tracker_mod._classify("")
    assert out["lane"] == "crawler"
    assert out["verified"] == "n/a"
    assert set(out) == {"lane", "bot_type", "vendor_key", "vendor_class",
                        "verified"}


def test_the_browser_fallback_applies_when_classify_fails(monkeypatch):
    """The other half of total: a raising classifier must not break a write."""
    def boom(ua, ip=None):
        raise RuntimeError("classifier exploded")

    monkeypatch.setattr(tracker_mod, "classify", boom)
    out = tracker_mod._classify("anything")
    assert out["lane"] == "browser"
    assert out["vendor_class"] is None
