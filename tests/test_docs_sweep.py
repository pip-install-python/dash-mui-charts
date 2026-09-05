"""Every Python file under docs/ must actually compile — sync 1.6.44 item 7.

PORTED WITH A CORRECTION, measured on this repo 2026-09-05.

The item's stated premise does not hold here. It says `.flake8` excludes
`docs/*/`, so `flake8 docs/` exits 0 with ZERO output on a file containing
`def broken(:` while py_compile exits 1. This repo's `.flake8` carries no
docs exclusion, `docs` is already on CI's flake8 line, and that file is
reported `E902 TokenError` and fails the step.

What survives is narrower and was measured rather than assumed: flake8
catches MOST syntax errors and not all. These two are compile-time
SyntaxErrors that flake8 reports nothing whatsoever for —

    print(a=1, a=2)         duplicate keyword argument   flake8 0 / compile 1
    def f(): nonlocal q     no binding for nonlocal      flake8 0 / compile 1

— so a docs example carrying either would pass lint, ship, and raise at
render time inside `.. exec::` on a page nobody re-opened. That is the gap
the sweep closes here.
"""
from __future__ import annotations

import contextlib
import io
import py_compile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

# The shapes flake8 does NOT report, measured. If a future flake8 starts
# flagging one, this list is what should be revisited — not the sweep.
FLAKE8_BLIND_SPOTS = {
    "duplicate keyword argument": "print(a=1, a=2)\n",
    "nonlocal with no binding": "def f():\n    nonlocal q\n",
}


def test_the_corpus_is_not_empty():
    """Note 88, first: a sweep that swept nothing is not evidence."""
    files = list(DOCS.rglob("*.py"))
    assert len(files) > 50, f"only {len(files)} docs Python files — too few"


def test_every_docs_python_file_compiles():
    """The sweep itself, run in-process so it is not CI-only."""
    files = sorted(DOCS.rglob("*.py"))
    assert files, "empty corpus"

    bad = []
    for f in files:
        cfile = Path(str(f) + "c")
        try:
            py_compile.compile(str(f), doraise=True, cfile=str(cfile))
        except py_compile.PyCompileError as exc:
            bad.append(f"{f.relative_to(REPO_ROOT)}: {exc}")
        finally:
            cfile.unlink(missing_ok=True)
    assert bad == [], f"{len(bad)} of {len(files)} docs files do not compile: {bad}"


@pytest.mark.parametrize("label", sorted(FLAKE8_BLIND_SPOTS))
def test_py_compile_catches_what_flake8_does_not(label, tmp_path):
    """THE CORRECTION, pinned as a measurement.

    This is what justifies the sweep on a repo whose flake8 already reads
    docs/. If flake8 ever grows these checks the sweep becomes redundant
    here, and this test going red is how anyone would find that out.
    """
    src = FLAKE8_BLIND_SPOTS[label]
    probe = tmp_path / "probe.py"
    probe.write_text(src)

    # py_compile: red.
    with pytest.raises(py_compile.PyCompileError):
        py_compile.compile(str(probe), doraise=True,
                           cfile=str(tmp_path / "probe.pyc"))

    # flake8: green, and silent. Called IN-PROCESS, not as `python -m flake8`:
    # this repo's .venv has no flake8 of its own (it is borrowed from the
    # sibling boilerplate venv by appending to sys.path), so the subprocess
    # form SKIPPED on the first run and measured nothing at all — the same
    # empty-corpus failure this file's other tests guard against.
    try:
        from flake8.main.cli import main as flake8_main
    except ImportError:  # pragma: no cover
        pytest.skip(
            "flake8 unavailable here — CI runs it in the LINT job, not the "
            "test job, so the test job legitimately has no flake8 to call. "
            "The measurement this test records is a property of flake8, not "
            "of this repo; the py_compile half above is unconditional and is "
            "what actually guards docs/."
        )

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            flake8_main([str(probe)])
        code = 0
    except SystemExit as exc:
        code = int(exc.code or 0)

    assert code == 0, (
        f"flake8 now reports {label!r} ({buf.getvalue().strip()}) — the sweep "
        f"may be redundant on this repo; revisit rather than deleting blindly"
    )
    assert buf.getvalue().strip() == "", (
        f"flake8 said something about {label!r}: {buf.getvalue().strip()}"
    )


def test_the_ci_step_is_registered_by_name():
    """The item's detect: the step `py_compile sweep of docs/` by name."""
    ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text()
    assert "name: py_compile sweep of docs/" in ci


def test_the_ci_step_fails_on_an_empty_corpus():
    """The item's note: the step must FAIL on an empty corpus."""
    ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text()
    block = ci.split("name: py_compile sweep of docs/", 1)[1]
    block = block.split("- name:", 1)[0]
    assert "if not files:" in block and "sys.exit(1)" in block


# ------------------------------------------------------------------ rider --

def test_no_docs_page_emits_its_own_order_1_title(pages):
    """The rider: a page emitting `Title(order=1)` under markdown.py's
    `order=2` renders a DOUBLE heading.

    Asserted STRUCTURALLY, on the rendered layout, because a page that does
    not render through markdown.py is entitled to its own order=1 — a
    text-level grep for "order=1" cannot tell those apart.
    """
    import dash_mantine_components as dmc

    from conftest import component_iter, page_layout

    offenders, checked = [], 0
    for path, entry in pages:
        layout = page_layout(entry)
        if layout is None:
            continue
        titles = [c for c in component_iter(layout)
                  if isinstance(c, dmc.Title)]
        # THE DISCRIMINATOR IS markdown.py's EXACT CONSTRUCTION, and getting
        # here took three attempts, each instructive:
        #
        #   1. "has both an order 1 and an order 2" — that is simply what a
        #      correct document looks like. Flagged `/`.
        #   2. "has an order=2 Title classed m2d-heading" — looked precise,
        #      is not: markdown2dash marks EVERY `##` heading m2d-heading,
        #      so /terms and /privacy were flagged for having an h1 and an
        #      h2 like every other document on earth.
        #   3. `entry["module"] == "pages.markdown"` — the registry stores
        #      the page NAME there for these pages, not a module path, so
        #      NOTHING matched and the corpus guard caught it.
        #
        # markdown.py builds the page title as
        # `dmc.Title(metadata.name, order=2, className="m2d-heading")`, so
        # the page's own registered NAME appearing as that heading's text is
        # what identifies it. A page not rendered that way is entitled to
        # its own order=1, which is exactly what the rider says.
        name = entry.get("name")
        rendered_by_markdown_py = any(
            getattr(t, "order", None) == 2
            and "m2d-heading" in (getattr(t, "className", "") or "")
            and getattr(t, "children", None) == name
            for t in titles
        )
        if not rendered_by_markdown_py:
            continue
        checked += 1
        if any(getattr(t, "order", None) == 1 for t in titles):
            offenders.append(path)

    # QUANTITATIVE, not merely non-zero. Discriminator #3 above satisfied a
    # bare `assert checked` with a count of zero only because the guard
    # existed at all; a discriminator matching ONE page would have satisfied
    # a non-zero check while measuring almost nothing. Most of this site's
    # pages render through markdown.py, so the count should be large.
    assert checked > 25, (
        f"only {checked} pages identified as markdown.py-rendered — the "
        f"discriminator is probably wrong again"
    )
    assert offenders == [], (
        f"pages emitting their own order=1 under markdown.py's order=2 "
        f"(a double heading): {offenders}"
    )


# ------------------------------------------------------------ item 9 --------

def test_divergences_has_a_recorded_conventions_section():
    """SYNC 1.6.44 item 9. A guard entry needs a home in THIS file.

    The reason it is not enough to leave guards in test docstrings: the
    fan-out and the sync authors read DIVERGENCES.md and nothing else, so a
    deliberate match recorded only in `tests/` is, to them, indistinguishable
    from an accident — and the next sync restores it.
    """
    text = (REPO_ROOT / "DIVERGENCES.md").read_text()
    assert "## Recorded conventions (not divergences)" in text


def test_the_guard_entries_actually_live_under_it():
    """Non-vacuity: the header alone is not the item.

    An empty section would satisfy a header check while leaving every guard
    where it was.
    """
    text = (REPO_ROOT / "DIVERGENCES.md").read_text()
    section = text.split("## Recorded conventions (not divergences)", 1)[1]
    section = section.split("\n## ", 1)[0]
    bullets = [ln for ln in section.splitlines() if ln.startswith("- **")]
    assert len(bullets) >= 3, f"only {len(bullets)} guard entries recorded"
    # And the a11y outcomes were moved under it rather than left as a peer.
    assert "### The a11y block's per-host outcomes" in section
