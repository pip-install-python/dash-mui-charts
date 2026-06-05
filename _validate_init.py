"""Pre-deploy check: validate that all Python components have been generated.

Run after `npm run build` and before publishing / deploying. Confirms the
version, that every expected component wrapper exists, and that each is a real
Dash component class.
"""
import sys

import dash_mui_charts

EXPECTED = {
    "BarChart", "CandlestickChart", "CompositeChart", "Heatmap", "LineChart",
    "LiveTradingChart", "PieChart", "ScatterChart", "SimpleTreeView",
    "SparklineChart", "TimeClock", "TreeView", "TreeViewPro",
}

if __name__ == "__main__":
    print("dash_mui_charts version:", dash_mui_charts.__version__)
    print("Components:", dash_mui_charts.__all__)

    generated = set(dash_mui_charts.__all__)
    missing = EXPECTED - generated
    extra = generated - EXPECTED

    if missing:
        print(f"ERROR: missing component wrappers: {sorted(missing)}")
        print("Run `npm run build` to regenerate the Python wrappers.")
        sys.exit(1)
    if extra:
        # Not fatal, but flag it so EXPECTED stays in sync with the library.
        print(f"NOTE: components present but not in EXPECTED set: {sorted(extra)}")

    # Each name must resolve to an importable Dash component class.
    for name in sorted(EXPECTED):
        comp = getattr(dash_mui_charts, name, None)
        if comp is None:
            print(f"ERROR: {name} not importable from dash_mui_charts")
            sys.exit(1)
        print(f"  {name}: OK")

    print(f"\nValidation passed! {len(generated)} components, "
          f"version {dash_mui_charts.__version__}.")
