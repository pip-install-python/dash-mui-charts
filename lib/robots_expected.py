"""What THIS APP would write as robots.txt — sync 1.6.44 item 19.

A PROXIED robots.txt IS NOT YOUR robots.txt. The file a crawler receives is
whatever the edge in front of this host chose to serve, and a CDN may inject
a managed block into it — a stanza the app never wrote, or a marker with
nothing under it. Both shapes leave the app's own posture intact in source
while the WIRE says something else, and a battery that only fetches the URL
and looks for expected lines cannot see either: the injected content is
additional, and the empty marker adds no rule at all.

So the check needs both sides. This module is the app's side.

GENERATED THROUGH THE PACKAGE'S OWN ``generate_robots_txt``, with the
config this app actually registers — never a reimplementation. A
hand-written expectation compares the edge against somebody's BELIEFS about
the config, so it agrees with the wire exactly when both are wrong in the
same way, which is the failure mode the whole item is about.

Importable without booting the app: ``run.py`` sets ``app._robots_config``
during boot, which a standalone battery cannot reach, so the config is
declared here and run.py reads it from here. One definition, two consumers.
"""
from __future__ import annotations

from dash_improve_my_llms import RobotsConfig

# THE ONE DECLARATION. run.py assigns `app._robots_config` from this, and the
# battery generates its expectation from it — so "what the app serves" and
# "what the battery expects" cannot drift apart, because they are the same
# object.
#
# Posture, deliberately, and recorded in DIVERGENCES.md's "Recorded
# conventions" section: training crawlers are ALLOWED. Since the ledger
# round every corpus read is a row (tier, vendor, verified, bytes) and the
# hub reconciles it against the wire, so a read is recorded and priceable
# and does not need a wall. The tool from here is per-vendor
# `vendor_policy={"<key>": "block"|"meter"}` for ONE vendor whose rows
# justify it, never the whole class.
ROBOTS_CONFIG = RobotsConfig(
    block_ai_training=False,   # training crawlers allowed; the ledger records every read
    allow_ai_search=True,      # Allow Claude-User/-SearchBot, ChatGPT-User, ...
    allow_traditional=True,    # Allow Googlebot, Bingbot, etc.
    crawl_delay=10,
    disallowed_paths=[],
)


def expected_robots_txt(base_url: str | None = None) -> str:
    """The robots.txt this app would generate, from the package itself.

    The signature is read from the package rather than assumed: dimll's
    ``generate_robots_txt(config, sitemap_url, base_url, mcp_enabled=False)``
    takes the sitemap URL separately, and calling it positionally with only
    a base URL raises. That is a floor-sensitive API — this fork pins a
    `>=` floor — so the call is built from the resolved signature and a
    changed parameter list fails loudly here instead of silently generating
    a different file.
    """
    import inspect

    from dash_improve_my_llms.robots_generator import generate_robots_txt

    if base_url is None:
        from lib.constants import BASE_URL

        base_url = BASE_URL
    base_url = base_url.rstrip("/")

    params = inspect.signature(generate_robots_txt).parameters
    kwargs = {"config": ROBOTS_CONFIG, "base_url": base_url}
    if "sitemap_url" in params:
        kwargs["sitemap_url"] = f"{base_url}/sitemap.xml"
    missing = [
        name for name, p in params.items()
        if p.default is inspect.Parameter.empty and name not in kwargs
    ]
    if missing:
        raise TypeError(
            f"dash-improve-my-llms' generate_robots_txt now requires "
            f"{missing} — lib/robots_expected must be taught about them "
            f"before the ai_bot_posture row means anything"
        )
    return generate_robots_txt(**kwargs)


def directive_lines(text: str) -> list[str]:
    """The RULE lines of a robots.txt, normalised — comments and blanks out.

    Comparison happens on directives, not on bytes: an edge may reflow
    whitespace or reorder comments without changing a single rule, and a
    byte comparison would call that a defect. What must not differ is the
    set of rules a crawler will obey.
    """
    out = []
    for raw in (text or "").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            # A line with no directive at all is not a rule; keep it visible
            # rather than dropping it, since it may be exactly the junk an
            # injection left behind.
            out.append(line.lower())
            continue
        field, _, value = line.partition(":")
        out.append(f"{field.strip().lower()}: {value.strip()}")
    return out
