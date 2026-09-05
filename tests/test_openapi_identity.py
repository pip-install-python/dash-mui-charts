"""The API surface's identity, and the signature guard that ships it safely.

SYNC 1.6.44 item 1, with the ops seat's measured correction (2026-09-05).

The item as originally worded pinned `dash-improve-my-llms == 2.9.4` and
passed the three `openapi_*` knobs unconditionally. This fork's requirements
line stays a `>=2.8.0` FLOOR until the fleet pin lands at 1.6.45, and on a
2.8.0-shaped `LLMSConfig` those parameters DO NOT EXIST — passing one is a
`TypeError` at import, i.e. a boot crash, not a degraded feature. So the
knobs ship behind an `inspect.signature` guard.

Both directions are pinned here because a one-sided test cannot fail in the
way that matters: a guard that never passes the knobs and a guard that always
passes them BOTH satisfy "the app boots on 2.10.0". The negative direction
therefore uses a synthetic 2.8.0-shaped config rather than the installed
wheel, which is 2.9.4-or-newer on every leg this repo runs.
"""
from __future__ import annotations

import inspect

import pytest

import run
from lib.constants import SITE_DESCRIPTION, SITE_SHORT_NAME
from lib.health import health_payload

KNOBS = ("openapi_title", "openapi_description", "openapi_version")


class _PreOpenapiConfig:
    """A 2.8.0-shaped ``LLMSConfig``: no ``openapi_*`` parameters at all."""

    def __init__(self, warn_missing_llms_doc: bool = False):
        self.warn_missing_llms_doc = warn_missing_llms_doc


class _OpenapiConfig:
    """A 2.9.4-shaped ``LLMSConfig``: the three knobs present."""

    def __init__(
        self,
        warn_missing_llms_doc: bool = False,
        openapi_title: str | None = None,
        openapi_description: str | None = None,
        openapi_version: str | None = None,
    ):
        self.openapi_title = openapi_title


def test_guard_omits_knobs_on_a_pre_2_9_4_config():
    """The direction that would otherwise be a boot crash."""
    assert run._openapi_kwargs(_PreOpenapiConfig) == {}

    # And the crash is real, not asserted: passing them UNGUARDED to the
    # same shape raises. Without this line the test above would pass just as
    # well if the knobs were harmless on 2.8.0, which is the claim under test.
    with pytest.raises(TypeError):
        _PreOpenapiConfig(warn_missing_llms_doc=True, openapi_title="x")


def test_guard_passes_knobs_on_a_2_9_4_shaped_config():
    """The direction that would otherwise be a silently unnamed API."""
    kwargs = run._openapi_kwargs(_OpenapiConfig)
    assert set(kwargs) == set(KNOBS)
    assert kwargs["openapi_title"] == f"{SITE_SHORT_NAME} API"
    assert kwargs["openapi_description"] == SITE_DESCRIPTION
    assert kwargs["openapi_version"] == "1.0"


def test_the_synthetic_fixtures_are_not_the_same_shape():
    """Non-vacuity: the two fixtures must actually differ, or both tests pass
    for free. This is the control run for the pair above."""
    pre = inspect.signature(_PreOpenapiConfig).parameters
    post = inspect.signature(_OpenapiConfig).parameters
    assert not any(k in pre for k in KNOBS)
    assert all(k in post for k in KNOBS)


def test_the_knobs_would_actually_construct_the_real_config():
    """The guard's answer is only useful if it matches the INSTALLED package.

    Where the resolved wheel carries the knobs, constructing the real
    `LLMSConfig` with what the guard returns must not raise — that is the
    thing the guard exists to promise.
    """
    from dash_improve_my_llms import LLMSConfig

    kwargs = run._openapi_kwargs(LLMSConfig)
    params = inspect.signature(LLMSConfig).parameters
    if not all(k in params for k in KNOBS):
        pytest.skip(
            "installed dash-improve-my-llms predates the openapi_* knobs; "
            "the guard's negative direction is pinned above"
        )
    assert set(kwargs) == set(KNOBS)
    LLMSConfig(warn_missing_llms_doc=True, **kwargs)  # must not raise


def test_boot_floor_is_not_raised_above_the_requirements_floor():
    """A boot floor above what requirements.txt guarantees is a brick.

    `LLMS_PKG_FLOOR` must never exceed the floor the requirements line
    actually declares — otherwise the app refuses to start on a dependency
    set the repo itself calls legal. Pins the ops seat's correction.
    """
    import re
    from pathlib import Path

    text = Path(run.__file__).parent.joinpath("requirements.txt").read_text()
    declared = re.search(
        r"^dash-improve-my-llms(?:\[[a-z,]+\])?>=(\d+)\.(\d+)\.(\d+)",
        text,
        re.M,
    )
    assert declared, "no dash-improve-my-llms floor line in requirements.txt"
    assert run.LLMS_PKG_FLOOR <= tuple(int(g) for g in declared.groups())


def test_healthz_reports_the_resolved_llms_version():
    """Item 1's other half: the resolved package version reaches the wire."""
    import dash_improve_my_llms as pkg

    payload = health_payload("flask")
    assert payload["llms_version"] == pkg.__version__


def test_llms_version_is_omitted_rather_than_invented(monkeypatch):
    """An unreadable package drops the key; it never reports "unknown"."""
    import lib.health as health

    monkeypatch.setattr(
        health, "_llms_version", lambda: {}, raising=True
    )
    assert "llms_version" not in health.health_payload("flask")
