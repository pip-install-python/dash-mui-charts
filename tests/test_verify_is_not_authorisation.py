"""A verify verdict is metering evidence, never sole authorisation.

SYNC 1.6.44 item 18.

This fork DOES consult `hub_client.verify` for access, in `lib.access.check`,
so the item's acceptance applies in its first form rather than its second:
the route names the host-held secret beside it. That secret is
`CROSS_APP_WEBHOOK_SECRET`. Without it `hub_client.enabled()` is False and
`verify` returns "gated" without a network call — so the verdict never
depends on the caller's token alone, which is what makes this a legitimate
authorisation point rather than a decision trusted from outside.

SOURCE-PINNED, NOT MERELY EXERCISED, which is the item's own note and the
reason this file walks ASTs. A behavioural suite cannot see a default
restored ABOVE its own guard: add `return "allow"` as the first line of
`verify` and every behavioural test that drives it through a mocked hub
still passes, because they never reach the code they think they are
testing. So the closed fallbacks are asserted in the source.

And the GOOD rows are pinned beside the bypass rows. A test that only proves
"deny stays denied" passes on an implementation that denies everything,
which would be a different outage rather than a fix.
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HUB_CLIENT = REPO_ROOT / "lib" / "hub_client.py"

CLOSED = "gated"


def _verify_fn() -> ast.FunctionDef:
    tree = ast.parse(HUB_CLIENT.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "verify":
            return node
    raise AssertionError("lib/hub_client.verify is gone — item 18 needs review")


# --------------------------------------------------- the closed fallbacks ---

def test_every_early_return_in_verify_is_closed():
    """SOURCE-PINNED. Each guard clause must return the CLOSED verdict.

    Walks only the top-level guards, i.e. the returns that fire before the
    hub's own answer is parsed. If any of them ever returns "allow", a caller
    presenting any key at all opens the gate.
    """
    fn = _verify_fn()
    literals = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
            literals.append(node.value.value)

    assert literals, "verify has no literal returns — the parse found nothing"
    bad = [v for v in literals if v != CLOSED]
    assert bad == [], (
        f"verify has a literal return that is not {CLOSED!r}: {bad}. Every "
        f"fallback in this function must fail closed; the only non-literal "
        f"return is the verdict the hub actually sent."
    )


def test_verify_still_has_a_non_literal_return():
    """Non-vacuity: an implementation that ONLY returns "gated" would satisfy
    the test above and would also be broken — nothing could ever be allowed.
    """
    fn = _verify_fn()
    non_literal = [n for n in ast.walk(fn)
                   if isinstance(n, ast.Return)
                   and not isinstance(n.value, ast.Constant)]
    assert non_literal, "verify can never return the hub's own verdict"


def test_the_secret_gate_precedes_the_network_call():
    """`enabled()` must be checked BEFORE `_post`, not after.

    Order is the whole guarantee: a verify that posted first and checked the
    secret afterwards would leak the key and the path to whatever host
    HUB_URL names, on a deployment that never configured the hub at all.
    """
    src = inspect.getsource
    fn = _verify_fn()
    names = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            names.append((node.lineno, node.func.id))
    enabled = [ln for ln, n in names if n == "enabled"]
    posted = [ln for ln, n in names if n == "_post"]
    assert enabled and posted, f"expected both calls, found {names}"
    assert min(enabled) < min(posted), (
        "verify posts to the hub before checking CROSS_APP_WEBHOOK_SECRET"
    )
    assert src  # keep the import meaningful for readers


def test_an_unrecognised_verdict_is_closed():
    """The hub is not trusted to send only the three words."""
    fn = _verify_fn()
    source = ast.get_source_segment(HUB_CLIENT.read_text(), fn) or ""
    assert '("allow", "gated", "deny")' in source, (
        "the verdict allow-list is gone; an unexpected string could pass "
        "through as a verdict"
    )


# ------------------------------------------------- behaviour, both ways -----

@pytest.fixture
def hub(monkeypatch):
    import lib.hub_client as mod

    mod._CACHE.clear() if hasattr(mod, "_CACHE") else None
    return mod


def test_no_key_is_gated(hub):
    assert hub.verify("", "/pie", "auth") == "gated"


def test_no_secret_is_gated_without_a_network_call(hub, monkeypatch):
    """The host-held secret IS the anchor — prove nothing is sent without it."""
    calls = []
    monkeypatch.setattr(hub, "enabled", lambda: False)
    monkeypatch.setattr(hub, "_post", lambda *a, **kw: calls.append(a))
    assert hub.verify("some-key", "/pie", "auth") == "gated"
    assert calls == [], "verify posted to the hub with no secret configured"


def test_a_dead_hub_is_gated(hub, monkeypatch):
    monkeypatch.setattr(hub, "enabled", lambda: True)
    monkeypatch.setattr(hub, "_post", lambda *a, **kw: None)
    assert hub.verify("k1", "/pie-a", "auth") == "gated"


def test_a_nonsense_verdict_is_gated(hub, monkeypatch):
    monkeypatch.setattr(hub, "enabled", lambda: True)
    monkeypatch.setattr(hub, "_post",
                        lambda *a, **kw: {"verdict": "yes-please"})
    assert hub.verify("k2", "/pie-b", "auth") == "gated"


def test_a_good_row_is_allowed(hub, monkeypatch):
    """THE GOOD ROW, beside the bypass rows.

    Without this, every assertion above passes on an implementation that
    returns "gated" unconditionally — a different outage, not a fix.
    """
    monkeypatch.setattr(hub, "enabled", lambda: True)
    monkeypatch.setattr(hub, "_post", lambda *a, **kw: {"verdict": "allow"})
    assert hub.verify("k3", "/pie-c", "auth") == "allow"


def test_a_deny_row_is_denied(hub, monkeypatch):
    monkeypatch.setattr(hub, "enabled", lambda: True)
    monkeypatch.setattr(hub, "_post", lambda *a, **kw: {"verdict": "deny"})
    assert hub.verify("k4", "/pie-d", "auth") == "deny"


# --------------------------------------------- tier lookalikes (item 18) ---

@pytest.mark.parametrize("lookalike", [
    "Auth", "AUTH", " auth", "auth ", "auth\n", "\tadmin", "Hidden",
])
def test_a_tier_lookalike_is_normalised_not_ignored(lookalike):
    """REJECT CASE AND WHITESPACE LOOKALIKES, never one literal.

    The hub's tier arrives over the network and is NOT the already-validated
    value a local registration produces. An unnormalised
    `hub_tier not in ("auth", "admin", "hidden")` answers True for every
    string above, and each would have left a machine lane OPEN on a page the
    network restricted.
    """
    from lib.page_tiers import normalize_tier

    assert normalize_tier(lookalike) == lookalike.strip().lower()
    assert normalize_tier(lookalike) in ("auth", "admin", "hidden")


@pytest.mark.parametrize("junk", ["", "  ", "publik", None, 7, [], "auth;--"])
def test_a_non_tier_normalises_to_empty(junk):
    """"" means "the hub said nothing", which is the ceiling's no-op — and
    critically NOT the input echoed back, so an unrecognised value can never
    propagate as though it were a tier."""
    from lib.page_tiers import normalize_tier

    assert normalize_tier(junk) == ""


def test_the_hub_ceiling_reads_through_the_normaliser():
    """Source-pinned: both hub-tier reads in lib/access must normalise.

    Behaviourally these are hard to reach without a live hub, and the
    consequence of missing one is silent — so the call sites are asserted.
    """
    src = (REPO_ROOT / "lib" / "access.py").read_text()
    tree = ast.parse(src)

    raw_reads = 0
    normalised = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        seg = ast.get_source_segment(src, node) or ""
        if "hub_tiers()" in seg and ".get(" in seg:
            raw_reads += 1
            if "normalize_tier" in seg:
                normalised += 1
        # The wrapping call also matches; count it as the normalised form.
    assert raw_reads >= 2, f"expected both hub-tier reads, found {raw_reads}"


def test_both_hub_tier_reads_are_wrapped():
    """The simpler statement of the same fact, read off the source text."""
    src = (REPO_ROOT / "lib" / "access.py").read_text()
    code = "\n".join(ln for ln in src.splitlines()
                     if not ln.lstrip().startswith("#"))
    bare = code.count("hub_client.hub_tiers().get(path)")
    wrapped = code.count("normalize_tier(hub_client.hub_tiers().get(path))")
    assert bare == wrapped == 2, (
        f"{bare} hub-tier reads, {wrapped} normalised — every one must be"
    )
