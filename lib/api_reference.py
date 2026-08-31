"""One parse of a component's props, for BOTH lanes.

`.. kwargs::dash_mui_charts.LineChart` renders a `dmc.Table` into the page's
component tree. A markdown2dash directive produces Dash COMPONENTS, never
markdown — so everything it renders exists only in the browser's React tree
and reaches no other reader. The machine lane (`/<page>/llms.txt`, the
crawler document) and the non-JS prerender are all built from the page's
markdown SOURCE, where the directive is a line that gets stripped.

That is how `/api` came to serve 13 component headings and zero property
rows to every agent, every crawler and every reader without JavaScript,
while a JS browser saw 371 rows and looked perfectly healthy. Measured
2026-08-30 on the wire: `/api/llms.txt` 2681 bytes, zero table rows; the
prerender block 9259 bytes, zero `<table>`; a real Chrome, 13 tables and
371 rows.

`pages/markdown.py` already had the shape of the answer — it expands
`.. source::` into a fenced block for exactly this reason. This module is
the same treatment for `.. kwargs::`, and it is deliberately the SINGLE
source both lanes read: `lib/directives/kwargs.py` calls `props_for` to
build the table, `pages/markdown.py` calls `props_markdown` to build the
prose, and neither can drift from the other because there is only one
parse. Two implementations of "what are this component's props" is how the
lanes disagreed in the first place.

Sync item 16 contract 7 asked for this in one line — "LLMS_DOC is the same
tables as Markdown". This fork kept its markdown `/api` page and reported
the contract met on the strength of the browser lane alone; the machine
half was never checked, and the test that should have caught it asserted
component NAMES appeared in the llms doc. They did — from the page's own
`### LineChart` headings, with no table under them.
"""
from __future__ import annotations

import importlib
import inspect

# `dmc.Button` / `html.Div` shorthands, as the directive has always accepted.
PACKAGE_MAP = {
    "dmc": "dash_mantine_components",
    "html": "dash.html",
    "dcc": "dash.dcc",
    "dash": "dash",
}

# The column order the rendered table uses (markdown2dash title-cases the
# dict keys), so the markdown table below carries the same three headers a
# browser sees. Not "Prop / Type / Default / Description": the generated
# docstrings fold the default into the type ("string; optional"), and a
# column that is always empty is worse than no column.
COLUMNS = ("Name", "Type", "Description")


def _numpy_props(docstring: str) -> list[dict]:
    """numpy-style parameter block — dash-mantine-components' hand-written docs."""
    lines = docstring.split("----------\n")[-1].split("\n")
    params: list[dict] = []
    current = None
    for line in lines:
        if not line.startswith("    "):
            if current is not None:
                params.append(current)
            if ": " not in line:
                current = None
                continue
            name, type_ = line.split(": ", 1)
            current = {"name": name, "type": type_, "description": ""}
        elif current is not None:
            current["description"] += " " + line.strip()
    if current is not None:
        params.append(current)
    return params


def resolve(spec: str, default_package: str = "dash_mantine_components"):
    """`"dash_mui_charts.LineChart"` / `"dmc.Button"` / `"Button"` -> the class."""
    if "." in spec:
        package_abbr, component_name = spec.rsplit(".", 1)
        package = PACKAGE_MAP.get(package_abbr, package_abbr)
    else:
        package, component_name = default_package, spec
    return getattr(importlib.import_module(package), component_name)


def props_for(spec: str, default_package: str = "dash_mantine_components") -> list[dict]:
    """Every documented prop as ``{name, type, description}``, or ``[]``.

    Reads the DOCSTRING, not ``_prop_names``: Dash 4's generated component
    classes do not carry that attribute at all (measured on this package —
    ``hasattr(SparklineChart, "_prop_names")`` is False), which is the trap
    sync item 16 note (b) names. The docstring is what exists, in two
    shapes — dash-generate-components' "Keyword arguments:" block for every
    wrapper in this library, and the numpy block DMC hand-writes.

    Returns ``[]`` rather than raising: a missing props table must not take
    a documentation page down. The caller is responsible for making the
    emptiness VISIBLE — see `props_markdown`, and note that the rendered
    table's `else` branch emits `None`, i.e. silence.
    """
    try:
        component = resolve(spec, default_package)
        docstring = inspect.getdoc(component)
    except Exception:
        return []
    if not docstring:
        return []
    if "----------" in docstring:
        return _numpy_props(docstring)
    if "Keyword arguments:" in docstring:
        # dash-generate-components' own format; the base package ships the
        # parser for it and this module must not grow a second one.
        from markdown2dash.src.utils import convert_docstring_to_dict

        try:
            return convert_docstring_to_dict(docstring.split("Keyword arguments:")[-1])
        except Exception:
            return []
    return []


def _cell(text) -> str:
    """A markdown table cell: no pipes, no newlines, both of which end a row."""
    return " ".join(str(text or "").split()).replace("|", "\\|")


def props_markdown(spec: str, default_package: str = "dash_mantine_components") -> str:
    """The same props as a markdown table, for the machine lane.

    An HTML comment rather than silence when there is nothing to say: a
    component whose props cannot be read is a defect worth seeing in the
    source of the document, and this is the lane where nobody would notice
    a table that simply is not there.
    """
    rows = props_for(spec, default_package)
    if not rows:
        return f"\n<!-- No documented props found for {spec} -->\n"
    out = [
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "| " + " | ".join("---" for _ in COLUMNS) + " |",
    ]
    for row in rows:
        out.append(
            "| " + " | ".join(
                _cell(row.get(key.lower())) for key in COLUMNS
            ) + " |"
        )
    out.append("")
    return "\n".join(out)
