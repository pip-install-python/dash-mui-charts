#!/usr/bin/env python3
"""Compatibility smoke — does this docs site actually work on THIS Dash?

ci.yml runs it across the supported Dash range (the matrix installs
`dash==X` first, then requirements). It answers the question the version
matrix exists for: with this exact Dash resolved, do all 41 pages
register, do their layouts construct, does every route serve 200, and is the
component bundle the browser will load syntactically whole?

This is deliberately NOT scripts/route_parity.py: the parity gate compares
exact layout trees against a baseline recorded WITH a MUI Pro key, and CI is
secretless by design — the 17 Pro pages render their license banners here,
which is a different (and correct) tree. What must hold on every Dash
version is the structure this script asserts, not the exact tree.

    python scripts/smoke_test.py                    # exit 1 on any failure
    python scripts/smoke_test.py --json out.json    # also write a report

Needs the site requirements installed; uses node for the JS checks when
available and reports them skipped when not (CI always installs node — a
skip there means the setup step broke).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

EXPECTED_ROUTES = 41  # 40 originals + /api
# dash_mui_charts component instances across all pages: 194 on 2026-08-02,
# with and without a Pro key (Pro pages mount their charts unlicensed and add
# a banner). The floor has slack for demo edits but fails on "a whole
# component family stopped mounting".
MIN_MUI_MOUNTS = 150
MIN_CALLBACKS = 90

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(f"{name}: {detail}")


def js_checks() -> dict:
    """`node --check` over the committed bundle and every asset script.

    The bundle is a build artifact nobody reviews line by line; parsing it is
    the cheapest guard against committing a truncated build. The assets are
    load-bearing at runtime (muiChartsFunctions.js is the functions-as-props
    registry) and only ever fail in the browser console.
    """
    node = shutil.which("node")
    targets = sorted((REPO / "dash_mui_charts").glob("*.js")) + \
        sorted((REPO / "assets").glob("*.js"))
    if node is None:
        print("  skip  JS syntax checks — node not on PATH")
        return {"ran": False, "files": len(targets)}
    for path in targets:
        proc = subprocess.run([node, "--check", str(path)],
                              capture_output=True, text=True)
        check(f"node --check {path.relative_to(REPO)}", proc.returncode == 0,
              proc.stderr.strip().splitlines()[0] if proc.returncode else "")
    return {"ran": True, "files": len(targets)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", help="write the measurement report to this path")
    args = ap.parse_args()

    # Keep a smoke run out of the real visitor ledger wherever it runs.
    os.environ.setdefault(
        "TRAFFIC_ANALYTICS_FILE",
        os.path.join(tempfile.mkdtemp(prefix="smoke-test-"),
                     "visitor_analytics.json"))
    os.environ.pop("CROSS_APP_WEBHOOK_SECRET", None)

    import dash

    print(f"smoke test — dash {dash.__version__}, "
          f"python {sys.version.split()[0]}\n")

    # route_parity.py owns the measurement (fingerprints, status sweep,
    # healthz); this script reuses it and asserts structure instead of
    # diffing against the Pro-key baseline.
    spec = importlib.util.spec_from_file_location(
        "route_parity", REPO / "scripts" / "route_parity.py")
    route_parity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(route_parity)

    try:
        current = route_parity.measure()
    except Exception as exc:  # noqa: BLE001 — the failure IS the finding
        check("app imports and measures", False, f"{type(exc).__name__}: {exc}")
        raise SystemExit(1)

    routes = current["routes"]
    statuses = current["route_statuses"]
    check(f"{EXPECTED_ROUTES} routes registered", len(routes) == EXPECTED_ROUTES,
          f"got {len(routes)}")
    bad = {p: s for p, s in statuses.items() if s != 200}
    check("every route serves 200", not bad, str(bad) if bad else "")
    hz_status, hz_ok = current["plumbing"]["/healthz"]
    check("/healthz returns ok:true", hz_status == 200 and hz_ok,
          f"status={hz_status} ok={hz_ok}")
    check("dash plumbing answers",
          current["plumbing"]["/_dash-layout"] == 200
          and current["plumbing"]["/_dash-dependencies"] == 200)
    check(f"charts mount (>= {MIN_MUI_MOUNTS} dash_mui_charts instances)",
          current["total_mui_mounts"] >= MIN_MUI_MOUNTS,
          f"got {current['total_mui_mounts']}")
    check(f"callbacks registered (>= {MIN_CALLBACKS})",
          current["callback_count"] >= MIN_CALLBACKS,
          f"got {current['callback_count']}")

    print()
    js = js_checks()

    if args.json:
        report = {
            "dash": dash.__version__,
            "python": sys.version.split()[0],
            "routes": len(routes),
            "mui_mounts": current["total_mui_mounts"],
            "callbacks": current["callback_count"],
            "js_checks": js,
            "failures": failures,
        }
        Path(args.json).write_text(json.dumps(report, indent=1) + "\n")

    print(f"\n{'PASS' if not failures else 'FAIL'} — "
          f"{len(failures)} failure(s)")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
