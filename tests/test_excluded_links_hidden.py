"""Admin pages hide from BOTH audiences — the llms-2plot-dev footgun, kept.

Before 1.6.8, a path hidden from the sidebar (then `excluded_links`) stayed
in sitemap.xml, /llms.txt, the tier corpora, MCP and the prerender; a fork
"hid" the template's tutorials and kept publishing them to every crawler
as its own documentation. 1.6.38 deleted `excluded_links` (the sidebar is
built from frontmatter now) — what remains hidden-by-rule is `/admin/*`,
and this suite pins the parity from both ends: the mechanism (every admin
path is in dimll's hidden state) and the surfaces (none appears in the
sitemap or /llms.txt, none in the sidebar tree, while a control page does
— so an empty sitemap can never pass this vacuously).
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _admin_paths():
    import dash

    return [p["path"] for p in dash.page_registry.values() if p["path"].startswith("/admin/")]


def test_every_admin_path_is_machine_hidden(app):
    from dash_improve_my_llms import is_hidden

    paths = _admin_paths()
    assert paths, "no admin pages registered — the pin would be vacuous"
    not_hidden = [p for p in paths if not is_hidden(p)]
    assert not_hidden == [], (
        f"in the app but NOT hidden from the machine surfaces: {not_hidden} — "
        "the page's mark_hidden wiring is broken or was removed"
    )


def test_admin_paths_absent_from_sitemap_llms_and_sidebar(client, app):
    import dash

    from components.navbar import create_content

    sitemap = client.get("/sitemap.xml").text
    llms = client.get("/llms.txt").text
    tree = str(create_content(dash.page_registry.values()))

    leaked = []
    for path in _admin_paths():
        if f"{path}</loc>" in sitemap:
            leaked.append(f"{path} in sitemap.xml")
        if f"{path})" in llms or f"{path}/llms.txt" in llms:
            leaked.append(f"{path} in /llms.txt")
        if path in tree:
            leaked.append(f"{path} in the startup sidebar tree")
    assert leaked == [], f"admin pages published: {leaked}"

    # Positive control: a real page IS listed, so an empty sitemap or a
    # broken llms.txt cannot make the assertions above pass vacuously.
    # Derived from the sidebar's own first page, never named, so this file
    # stays fork-invariant.
    from components.navbar import sections_for

    sections = sections_for(dash.page_registry.values())
    assert sections, "the sidebar has no docs section"
    control = sections[0][1][0]["path"]
    assert f"{control}</loc>" in sitemap
    assert control in llms
    assert control in tree


def test_admin_paths_absent_from_the_WHOLE_corpus(client, app):
    """The corpus half (sync item 18, llms's note 75): PROSE can leak what
    STRUCTURE hides. Hyperlinking /admin/control-board from five docs pages
    put the path into that host's /llms.txt while every navbar, sitemap and
    mark_hidden pin passed — the page was hidden and its URL was published
    anyway, in the body text.

    So sweep the corpus documents themselves, not just the index: the tier
    docs are where a fork's prose actually lands.
    """
    docs = {
        "/llms.txt": client.get("/llms.txt").text,
        "/llms-small.txt": client.get("/llms-small.txt").text,
        "/llms-full.txt": client.get("/llms-full.txt").text,
    }
    served = {k: v for k, v in docs.items() if v and len(v) > 200}
    assert served, "no corpus document came back — the sweep would be vacuous"

    # TWO strictnesses, because the defect is a REACHABLE url and not the
    # mere appearance of a string.
    #
    # 1. A LINK to an admin path, anywhere in the corpus. This is note 75's
    #    actual failure — `](/admin/control-board)` in five docs pages —
    #    and it is what the template's sitemap/llms pin already keys on.
    linked = []
    for path in _admin_paths():
        for name, body in served.items():
            if f"]({path})" in body or f'href="{path}"' in body or f"{path}/llms.txt" in body:
                linked.append(f"{path} linked in {name}")
    assert linked == [], (
        f"admin paths LINKED from the corpus: {linked} — structure hid the "
        "page and prose published a reachable URL anyway. Fix the PROSE "
        "(drop the link), not the pin."
    )

    # 2. A bare MENTION, from anywhere except the changelog. A docs page has
    #    no reason to name an admin path even without linking it; the
    #    changelog does, because its whole subject is what changed, and a
    #    changelog that cannot name the page it added is not a changelog.
    #    Measured 2026-08-31: this host's /llms-full.txt carries six such
    #    mentions, ALL from CHANGELOG.md prose (code spans, no links), and
    #    they predate this pin — verified byte-identical at f0b469c before
    #    the sweep existed. That is disclosure of a path whose page fails
    #    closed and 404s to crawlers, not access.
    changelog_body = (REPO / "CHANGELOG.md").read_text() if (REPO / "CHANGELOG.md").exists() else ""
    stray = []
    for path in _admin_paths():
        for name, body in served.items():
            for line in body.split("\n"):
                if path in line and line.strip() not in changelog_body:
                    stray.append(f"{path} in {name}: {line.strip()[:70]}")
    assert stray == [], (
        f"admin paths named in the corpus by something other than the "
        f"changelog: {stray}"
    )
