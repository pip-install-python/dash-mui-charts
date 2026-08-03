"""Route-parity gate — proof that a migration phase changed no page.

Two modes, two eras of this repo's migrations:

EXACT mode (default) — the network-standard pass: identity, analytics, CI
and deploy plumbing may change, but every route must render exactly as
before. Fingerprints each route's fully-constructed layout tree plus the
app shell, and compares against a committed baseline.

    python scripts/route_parity.py --write-baseline   # record current truth
    python scripts/route_parity.py                    # gate: green or exit 1

CHARTS-ONLY mode — the boilerplate migration: the shell and page wrapping
change deliberately (markdown-driven pages, new appshell), but the LIVE
EXAMPLES must survive verbatim. The gate narrows to what re-wrapping cannot
touch: the route set, per-route dash_mui_charts.* component census, the
hand-prefixed chart component ids, and every callback that reads or writes
a chart id. A ported page passes iff its charts, their ids and their
callbacks all still exist.

    python scripts/route_parity.py --charts-only --write-baseline
    python scripts/route_parity.py --charts-only

What a fingerprint is (and deliberately is not):

- per route: component counts by "namespace.Type", the sorted set of
  component ids (all of them in exact mode, charts only in charts mode),
  and the count of dash_mui_charts.* instances. Prop VALUES stay out
  (pages may generate demo data), and page TITLES / descriptions stay out.
- app-wide: the route set, an HTTP status sweep of every route + /healthz;
  exact mode adds the app-shell fingerprint and total callback count,
  charts mode adds the chart-touching callback census instead.

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
CHART_BASELINE = Path(__file__).resolve().parent / "chart_parity_baseline.json"

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
    mui_ids: list[str] = []
    mui_mounts = 0
    for comp in component_iter(layout):
        key = f"{comp._namespace}.{comp._type}"
        counts[key] = counts.get(key, 0) + 1
        cid = getattr(comp, "id", None)
        if cid is not None:
            cid = (cid if isinstance(cid, str)
                   else json.dumps(cid, sort_keys=True))
            ids.append(cid)
        if comp._namespace == "dash_mui_charts":
            mui_mounts += 1
            if cid is not None:
                mui_ids.append(cid)
    return {
        "components": dict(sorted(counts.items())),
        "ids": sorted(ids),
        "mui_ids": sorted(mui_ids),
        "mui_mounts": mui_mounts,
    }


def _import_site():
    """The docs app, whichever entry point this era of the repo uses.

    The boilerplate migration renames app.py -> run.py; baselines recorded
    from one must stay comparable against the other.
    """
    if (REPO / "run.py").exists():
        import run as site
    else:
        import app as site
    return site


def _callback_ids(spec) -> set:
    """Every component id referenced by one callback_map entry."""
    ids = set()
    for dep_list in (spec.get("inputs") or [], spec.get("state") or []):
        for dep in dep_list:
            cid = dep.get("id")
            ids.add(cid if isinstance(cid, str)
                    else json.dumps(cid, sort_keys=True))
    return ids


def chart_callbacks(site, all_chart_ids: set) -> list[dict]:
    """Census of callbacks that read or write any chart id.

    The output key encodes the outputs ("id.prop" forms); inputs/state come
    from the spec. Shell callbacks come and go with a shell; these must not.
    """
    census = []
    for out_key, spec in site.app.callback_map.items():
        refs = {cid for cid in _callback_ids(spec)
                if cid in all_chart_ids}
        refs |= {cid for cid in all_chart_ids if f"{cid}." in out_key}
        if refs:
            census.append({"output": out_key, "chart_refs": sorted(refs)})
    return sorted(census, key=lambda c: c["output"])


def measure() -> dict:
    import dash

    site = _import_site()  # imports all pages, builds the shell

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

    all_chart_ids = {cid for r in routes.values() for cid in r["mui_ids"]}

    return {
        "routes": routes,
        "route_statuses": statuses,
        "plumbing": plumbing,
        "shell": fingerprint(site.app.layout),
        "callback_count": len(site.app.callback_map),
        "total_mui_mounts": sum(r["mui_mounts"] for r in routes.values()),
        "chart_callbacks": chart_callbacks(site, all_chart_ids),
    }


def charts_view(measurement: dict) -> dict:
    """The migration-proof projection of a measurement: only what page
    re-wrapping cannot legitimately change."""
    routes = {}
    for path, fp in measurement["routes"].items():
        routes[path] = {
            "mui_components": {k: v for k, v in fp["components"].items()
                               if k.startswith("dash_mui_charts.")},
            "mui_ids": fp["mui_ids"],
            "mui_mounts": fp["mui_mounts"],
        }
    return {
        "routes": routes,
        "route_statuses": measurement["route_statuses"],
        "healthz": measurement["plumbing"]["/healthz"],
        "total_mui_mounts": measurement["total_mui_mounts"],
        "chart_callbacks": measurement["chart_callbacks"],
    }


def diff_charts(baseline: dict, current: dict) -> list[str]:
    problems = []
    base_routes, cur_routes = baseline["routes"], current["routes"]
    for path in sorted(set(base_routes) - set(cur_routes)):
        problems.append(f"route GONE: {path}")
    for path in sorted(set(cur_routes) - set(base_routes)):
        problems.append(f"route ADDED (update baseline deliberately): {path}")
    for path in sorted(set(base_routes) & set(cur_routes)):
        b, c = base_routes[path], cur_routes[path]
        if b["mui_components"] != c["mui_components"]:
            problems.append(f"{path}: chart census changed "
                            f"(was {b['mui_components']} → "
                            f"now {c['mui_components']})")
        if b["mui_ids"] != c["mui_ids"]:
            problems.append(
                f"{path}: chart ids changed "
                f"(-{sorted(set(b['mui_ids']) - set(c['mui_ids']))} "
                f"+{sorted(set(c['mui_ids']) - set(b['mui_ids']))})")
    bad = {p: s for p, s in current["route_statuses"].items() if s != 200}
    if bad:
        problems.append(f"routes not serving 200: {bad}")
    if current["healthz"] != baseline["healthz"]:
        problems.append(f"healthz changed: {baseline['healthz']!r} → "
                        f"{current['healthz']!r}")
    if baseline["total_mui_mounts"] != current["total_mui_mounts"]:
        problems.append(f"total chart mounts {baseline['total_mui_mounts']} → "
                        f"{current['total_mui_mounts']}")
    base_cbs = {json.dumps(c, sort_keys=True)
                for c in baseline["chart_callbacks"]}
    cur_cbs = {json.dumps(c, sort_keys=True)
               for c in current["chart_callbacks"]}
    for gone in sorted(base_cbs - cur_cbs):
        problems.append(f"chart callback GONE: {gone}")
    for new in sorted(cur_cbs - base_cbs):
        problems.append(f"chart callback ADDED (update baseline "
                        f"deliberately): {new}")
    return problems


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
    ap.add_argument("--charts-only", action="store_true",
                    help="gate only the live examples (boilerplate migration "
                         "mode): chart census, chart ids, chart callbacks")
    args = ap.parse_args()

    current = measure()
    n = len(current["routes"])
    print(f"measured {n} routes, {current['total_mui_mounts']} "
          f"dash_mui_charts mounts, {current['callback_count']} callbacks, "
          f"{len(current['chart_callbacks'])} chart-touching callbacks")

    baseline_path = CHART_BASELINE if args.charts_only else BASELINE
    payload = charts_view(current) if args.charts_only else current

    if args.write_baseline:
        baseline_path.write_text(
            json.dumps(payload, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"baseline written → {baseline_path.relative_to(REPO)}")
        return 0

    if not baseline_path.exists():
        print("no baseline — run with --write-baseline first", file=sys.stderr)
        return 2
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if args.charts_only:
        problems = diff_charts(baseline, payload)
        label = "CHART PARITY"
    else:
        problems = diff(baseline, payload)
        label = "ROUTE PARITY"
    if problems:
        print(f"\n{label} BROKEN — {len(problems)} problem(s):",
              file=sys.stderr)
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        return 1
    print(f"{label.lower()} GREEN — all {n} routes identical to baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
