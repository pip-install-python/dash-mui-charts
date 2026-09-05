"""The fleet probe convention — measured on the resolved wheel, not asserted.

SYNC 1.6.44 item 4. A PROBE is machinery fetching a network host to CHECK it
(a workflow's `curl /healthz`, a smoke battery, a link audit); `internal_ua()`
is this app calling a peer server-to-server. Same token, different spelling,
so the far side's log can tell them apart.

The claim that earns a test rather than a comment: appending the suffix moves
NEITHER lane, bot_type NOR vendor_key on any engine. That is a property of
`dash_improve_my_llms.classify()`, which is a dependency with a `>=` floor —
so it is exactly the kind of fact a version bump can move underneath the
comment that states it. This file re-measures the table.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from dash_improve_my_llms import classify

from lib.constants import (
    INTERNAL_UA_TOKEN,
    PROBE_UA_SUFFIX,
    probe_ua,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

ENGINES = {
    "chrome": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "googlebot": (
        "Mozilla/5.0 (compatible; Googlebot/2.1; "
        "+http://www.google.com/bot.html)"
    ),
    "curl": "curl/8.7.1",
}


def test_the_suffix_carries_the_suppression_token():
    """Suppression is the tracker's job, and it keys on this substring."""
    assert INTERNAL_UA_TOKEN in PROBE_UA_SUFFIX
    assert PROBE_UA_SUFFIX == f"{INTERNAL_UA_TOKEN}/probe"


def test_probe_ua_refuses_an_engineless_probe():
    """The failure this refusal prevents is a SILENT one.

    A UA carrying only the internal suffix classifies crawler-lane, so an
    engineless probe is answered with the crawler document — and a
    browser-lane assertion written against it measures the wrong artifact
    while passing. Better to raise at construction.
    """
    for empty in ("", "   ", None):
        with pytest.raises(ValueError):
            probe_ua(empty)


def test_an_engineless_probe_really_would_be_crawler_lane():
    """Non-vacuity for the refusal above: prove the hazard is real.

    Without this, `test_probe_ua_refuses_an_engineless_probe` would pass just
    as well if the suffix alone classified browser-lane and the refusal were
    pointless ceremony.
    """
    assert classify(PROBE_UA_SUFFIX, None)["lane"] == "crawler"


@pytest.mark.parametrize("engine", sorted(ENGINES))
def test_the_suffix_moves_neither_lane_nor_vendor_nor_bot_type(engine):
    """THE MEASUREMENT. Re-run against whatever wheel resolved."""
    bare = classify(ENGINES[engine], None)
    probed = classify(probe_ua(ENGINES[engine], "network-smoke"), None)
    for field in ("lane", "bot_type", "vendor_key"):
        assert probed.get(field) == bare.get(field), (
            f"{engine}: appending {PROBE_UA_SUFFIX!r} moved {field} "
            f"{bare.get(field)!r} -> {probed.get(field)!r}"
        )


def test_a_generic_caller_word_would_change_the_classification():
    """Why the caller tag must never be a generic word.

    `2plot-monitoring/1` classifies off the word "monitoring" alone. Pinned
    because it is the mistake the convention exists to prevent, and a reader
    who does not believe it will otherwise reintroduce it.
    """
    assert classify("2plot-monitoring/1", None).get("bot_type") == "monitor"


# ---------------------------------------------------------------- the files --

# Every curl in these workflows fetches a live host (the deployed site, or the
# app booted inside the runner). The actionlint DOWNLOAD is excluded: it
# fetches a release script from raw.githubusercontent.com, which is not a
# network host and has no ledger to pollute.
WORKFLOWS = ("cd.yml", "ci.yml")


# `curl` in COMMAND POSITION — start of line, or after a pipe, `&&`, `;`,
# `$(`, or an `if`. Not merely "the line contains the word curl".
_CURL_CMD = re.compile(r"(?:^|[|;&]|\$\(|\bif\s+|=\"?\$\()\s*curl\s")


def _curl_lines(text: str) -> list[str]:
    """Every line INVOKING curl, with comments and assignments excluded.

    Three revisions, and the last two are item 13's failure mode arriving on
    schedule. A whole-file regex matched nothing (caught by the non-empty
    guard). A plain `\\bcurl\\b` line scan then matched this workflow's own
    COMMENT about curl and the `PROBE_UA:` value containing the string
    `curl/8` — reporting as defects the two lines that document and implement
    the fix. Comments are stripped and curl must appear in command position.
    """
    out = []
    for ln in text.splitlines():
        stripped = ln.strip()
        if stripped.startswith("#"):
            continue
        if _CURL_CMD.search(ln):
            out.append(ln)
    return out


@pytest.mark.parametrize("name", WORKFLOWS)
def test_every_workflow_curl_at_a_host_names_itself(name):
    """The gap item 4 predicts: the scripts had the token, the workflows did not."""
    text = (REPO_ROOT / ".github" / "workflows" / name).read_text()
    lines = _curl_lines(text)
    assert lines, f"{name}: no curl invocations found — the sweep swept nothing"

    checked, bare = 0, []
    for line in lines:
        if "raw.githubusercontent.com" in line:
            continue  # a release-script download, not a network host
        checked += 1
        if "-A " not in line:
            bare.append(line.strip())
    assert checked, f"{name}: every curl was excluded — nothing was measured"
    assert bare == [], f"{name}: curls with no User-Agent: {bare}"


@pytest.mark.parametrize("name", WORKFLOWS)
def test_the_workflow_probe_ua_obeys_the_convention(name):
    """It must lead with an engine token and carry the suppression token."""
    text = (REPO_ROOT / ".github" / "workflows" / name).read_text()
    m = re.search(r'PROBE_UA:\s*"([^"]+)"', text)
    assert m, f"{name}: curls reference $PROBE_UA but no PROBE_UA is defined"
    ua = m.group(1)

    assert INTERNAL_UA_TOKEN in ua, f"{name}: PROBE_UA is not suppressed"
    assert PROBE_UA_SUFFIX in ua, f"{name}: PROBE_UA is not the /probe spelling"
    # And it classifies as the engine it names, not off the suffix.
    assert classify(ua, None)["lane"] == classify("curl/8.7.1", None)["lane"]


@pytest.mark.parametrize("script", ["smoke_live", "network_smoke"])
def test_the_batteries_use_the_probe_spelling(script):
    """The `/probe` half of the item — the token alone was already there."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        f"_probe_{script}", REPO_ROOT / "scripts" / f"{script}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    agents = [
        value
        for name, value in vars(module).items()
        if (name == "UA" or name.endswith("_UA")) and isinstance(value, str)
    ]
    assert agents, f"scripts/{script}.py declares no User-Agent constant"
    missing = [ua for ua in agents if PROBE_UA_SUFFIX not in ua]
    assert missing == [], f"scripts/{script}.py still on the old spelling: {missing}"


@pytest.mark.parametrize("script", ["smoke_live", "network_smoke"])
def test_the_standalone_fallback_matches_the_real_probe_ua(script):
    """CD may copy a battery without an importable checkout.

    Both scripts carry a fallback definition for that case. A drifted
    fallback silently re-enters the far side's ledger, so it is pinned to
    produce the same string as `lib.constants.probe_ua`.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        f"_fb_{script}", REPO_ROOT / "scripts" / f"{script}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    fallback = module._probe_ua
    for engine in ENGINES.values():
        for caller in ("", "network-smoke"):
            assert fallback(engine, caller) == probe_ua(engine, caller)
    with pytest.raises(ValueError):
        fallback("")
