"""Network bulletin — hub-published tips and announcements.

Adapted from the boilerplate's template copy (its ``app_id()`` reads
``lib.satellite_reporter``; this repo's reporter is ``lib.traffic_report``).

The hub (2plot.dev) serves one JSON document at ``/api/network/bulletin``
and every satellite renders it in the header of its llms.txt viewer: a
twenty-site network says "here is what changed" once, in one place.

The wiring is a function that returns whether it wired, and app.py prints
that at boot — the boilerplate shipped this commented out for weeks against
a hub endpoint that was already serving, and an announcement that never
appears is not a symptom anyone notices.

Env:
    NETWORK_BULLETIN_URL   the hub endpoint. Absent -> feature off, silently.
                           Must be set on the Render SERVICE, not only in
                           render.yaml — blueprint envVars apply on
                           Blueprint sync, not git-push autodeploys.
    NETWORK_BULLETIN_TTL_S seconds a cached bulletin stays fresh (default 900)
"""

from __future__ import annotations

import os
from typing import Optional

DEFAULT_TTL_S = 900.0

# The hub endpoint, for .env.example and the docs to copy from. Not a
# default — configure() requires the env var, because a satellite that
# silently starts calling a hub it was never pointed at is the kind of
# surprise a template must not ship.
HUB_BULLETIN_URL = "https://2plot.dev/api/network/bulletin"


def url() -> Optional[str]:
    return os.environ.get("NETWORK_BULLETIN_URL") or None


def _ttl() -> float:
    try:
        return max(60.0, float(os.environ.get("NETWORK_BULLETIN_TTL_S",
                                              DEFAULT_TTL_S)))
    except (TypeError, ValueError):
        return DEFAULT_TTL_S


def app_id() -> str:
    """This app's key in the hub's network directory.

    Reused from ``lib.traffic_report.APP_KEY`` rather than hard-coded, so
    the traffic rollups and the bulletin fetches identify this satellite
    the same way on every hub surface.
    """
    from lib.traffic_report import APP_KEY

    return APP_KEY


def configure() -> bool:
    """Point the package at the hub's bulletin. Returns whether it did.

    Fail-open in both directions: with no URL the feature is off and the
    llms viewer still renders on the package's built-in tips; with an
    unreachable URL the package's client degrades silently — a hub outage
    must not take the documentation down with it.
    """
    endpoint = url()
    if not endpoint:
        return False

    try:
        from dash_improve_my_llms import configure_bulletin
    except ImportError:  # pragma: no cover - older releases lack the feature
        return False

    configure_bulletin(url=endpoint, ttl=_ttl(), app_id=app_id())
    return True
