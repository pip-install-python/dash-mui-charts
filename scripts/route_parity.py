"""Route-parity gate — proof that a migration phase changed no page.

The network-standard pass (kickoff: pip-docs+/kickoff/KICKOFF-muicharts.md)
is allowed to touch identity, analytics, CI and deploy plumbing, but every
one of the 40 doc routes must render exactly as before. This script is that
proof: it fingerprints each route's fully-constructed layout tree plus the
app shell, and compares against a committed baseline.

    python scripts/route_parity.py --write-baseline   # record current truth
    python scripts/route_parity.py                    # gate: green or exit 1

What a fingerprint is (and deliberately is not):

- per route: component counts by "namespace.Type", the sorted set of
  component ids, and the count of dash_mui_charts.* instances — the
  component-mount marker proving the charts actually sit in the tree.
  Prop VALUES stay out (pages may generate demo data), and page TITLES /
  descriptions stay out (Phase 1 changes register_page metadata on
  purpose; the layout must not change with it).
- app-wide: the route set, the app-shell fingerprint (nav tree, url store,
  ad slot), the registered-callback count, and an HTTP status sweep of
  every route + /healthz through the Flask test client.

Needs MUI_PRO_API_KEY in the environment or .env (17 pages hard-require it
at import); analytics writes are redirected to a temp dir so a gate run
never lands in the real hit log.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "route_parity_baseline.json"

sys.path.insert(0, str(REPO))

# Keep gate runs out of the real analytics log, and the reporter asleep.
os.environ["ANALYTICS_DIR"] = tempfile.mkdtemp(prefix="route-parity-")
os.environ.pop("CROSS_APP_WEBHOOK_SECRET", None)


def component_iter(node):
    """Depth-first over every Dash component reachable from ``node`` —
    through children AND through any component-valued prop (dmc uses
    label=/leftSection=/etc. freely)."""
    from dash.development.base_component import Component

    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, Component):
            yield cur
            for name in cur._prop_names:
                val = getattr(cur, name, None)
                if val is not None and name != "id":
                    stack.append(val)
        elif isinstance(cur, (list, tuple)):
            stack.extend(cur)
        elif isinstance(cur, dict):
            stack.extend(cur.values())


def fingerprint(layout) -> dict:
    counts: dict[str, int] = {}
    ids: list[str] = []
    mui_mounts = 0
    for comp in component_iter(layout):
        key = f"{comp._namespace}.{comp._type}"
        counts[key] = counts.get(key, 0) + 1
        if comp._namespace == "dash_mui_charts":
            mui_mounts += 1
        cid = getattr(comp, "id", None)
        if cid is not None:
            ids.append(cid if isinstance(cid, str)
                       else json.dumps(cid, sort_keys=True))
    return {
        "components": dict(sorted(counts.items())),
        "ids": sorted(ids),
        "mui_mounts": mui_mounts,
    }


def measure() -> dict:
    import dash

    import app as site  # noqa: F401 — imports all pages, builds the shell

    routes = {}
    for entry in dash.page_registry.values():
        layout = entry.get("layout")
        if layout is None:
            layout = getattr(sys.modules[entry["module"]], "layout", None)
        if callable(layout):
            layout = layout()
        routes[entry["path"]] = fingerprint(layout)

    client = site.server.test_client()
    statuses = {}
    for path in routes:
        statuses[path] = client.get(path).status_code
    hz = client.get("/healthz")
    plumbing = {
        "/healthz": [hz.status_code, bool((hz.get_json() or {}).get("ok"))],
        "/_dash-layout": client.get("/_dash-layout").status_code,
        "/_dash-dependencies": client.get("/_dash-dependencies").status_code,
    }

    return {
        "routes": routes,
        "route_statuses": statuses,
        "plumbing": plumbing,
        "shell": fingerprint(site.app.layout),
        "callback_count": len(site.app.callback_map),
        "total_mui_mounts": sum(r["mui_mounts"] for r in routes.values()),
    }


def diff(baseline: dict, current: dict) -> list[str]:
    problems = []
    base_routes, cur_routes = baseline["routes"], current["routes"]
    for path in sorted(set(base_routes) - set(cur_routes)):
        problems.append(f"route GONE: {path}")
    for path in sorted(set(cur_routes) - set(base_routes)):
        problems.append(f"route ADDED (update baseline deliberately): {path}")
    for path in sorted(set(base_routes) & set(cur_routes)):
        b, c = base_routes[path], cur_routes[path]
        if b["components"] != c["components"]:
            gone = {k: v for k, v in b["components"].items()
                    if c["components"].get(k) != v}
            new = {k: v for k, v in c["components"].items()
                   if b["components"].get(k) != v}
            problems.append(f"{path}: component tree changed "
                            f"(was {gone} → now {new})")
        if b["ids"] != c["ids"]:
            problems.append(
                f"{path}: ids changed "
                f"(-{sorted(set(b['ids']) - set(c['ids']))} "
                f"+{sorted(set(c['ids']) - set(b['ids']))})")
        if b["mui_mounts"] != c["mui_mounts"]:
            problems.append(f"{path}: mui mounts {b['mui_mounts']} → "
                            f"{c['mui_mounts']}")
    for surface in ("route_statuses", "plumbing", "shell", "callback_count",
                    "total_mui_mounts"):
        if baseline[surface] != current[surface]:
            problems.append(f"{surface} changed: {baseline[surface]!r} → "
                            f"{current[surface]!r}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write-baseline", action="store_true",
                    help="record the current state as the committed truth")
    args = ap.parse_args()

    current = measure()
    n = len(current["routes"])
    print(f"measured {n} routes, {current['total_mui_mounts']} "
          f"dash_mui_charts mounts, {current['callback_count']} callbacks")

    if args.write_baseline:
        BASELINE.write_text(json.dumps(current, indent=1, sort_keys=True)
                            + "\n", encoding="utf-8")
        print(f"baseline written → {BASELINE.relative_to(REPO)}")
        return 0

    if not BASELINE.exists():
        print("no baseline — run with --write-baseline first", file=sys.stderr)
        return 2
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    problems = diff(baseline, current)
    if problems:
        print(f"\nROUTE PARITY BROKEN — {len(problems)} problem(s):",
              file=sys.stderr)
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        return 1
    print(f"route parity GREEN — all {n} routes identical to baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
