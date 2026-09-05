#!/usr/bin/env python3
"""Count the fleet-class traps in a `.claude/CLAUDE.md` traps section.

Sync 1.6.44 item 14, ported with the ORIENTATION REVERSED. The template's
copy hardcodes its own kit as the reference and takes the fork as an
argument, which is the right shape for the seat doing a fan-out. On a fork
the useful question is the other way round — "how far behind is MY kit?" —
so here the fork under test is this repo by default and the TEMPLATE is what
you point at:

    python3 scripts/kit_traps.py                              # this repo's count
    python3 scripts/kit_traps.py ../dash-documentation-boilerplate/.claude/CLAUDE.md

Why it exists: a fork's traps section can sit fifteen entries behind the
template's — 7 against 22 on emojimart, whose HEAD trap still carried the
diagnosis 1.6.32 had corrected. The kit is contract-class, so a sync never
copies it, and nothing printed the gap.

Matching is by TOKEN OVERLAP of each entry's first sentence, not exact text.
That is deliberately generous, and the reason is the item's own note: a fork
is EXPECTED to have merged a trap into its own wording and to have added
host-specific clauses, so a strict check would report a fork's adaptation as
absence and train it to paste over its adaptations — the opposite of what
the item asks for. The check exists to find a trap a fork NEVER RECEIVED.

Exit code: 1 if the fork is missing any template trap, else 0.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING = "### Verification traps"
REPO_ROOT = Path(__file__).resolve().parent.parent
FORK_KIT = REPO_ROOT / ".claude" / "CLAUDE.md"


def traps_section(text: str) -> str:
    """The traps section, or "" when the file has none."""
    if HEADING not in text:
        return ""
    after = text.split(HEADING, 1)[1]
    # The section runs to the next `## ` heading, or to end of file.
    return re.split(r"^## ", after, maxsplit=1, flags=re.M)[0]


def trap_entries(text: str) -> list[str]:
    """One entry per top-level `- ` bullet, continuation lines folded in."""
    section = traps_section(text)
    entries, current = [], None
    for line in section.splitlines():
        if line.startswith("- "):
            if current is not None:
                entries.append(" ".join(current))
            current = [line[2:].strip()]
        elif current is not None and line.startswith("  "):
            current.append(line.strip())
        elif current is not None and not line.strip():
            continue
    if current is not None:
        entries.append(" ".join(current))
    return entries


def key(entry: str) -> str:
    """A readable identity for printing: the first sentence, normalised."""
    first = re.split(r"(?<=[.:])\s", entry, maxsplit=1)[0]
    first = re.sub(r"[`*_\"']", "", first)
    return re.sub(r"\s+", " ", first).strip().lower()[:60]


def _tokens(entry: str) -> set:
    """Content words of the first sentence, for overlap matching."""
    first = re.split(r"(?<=[.:])\s", entry, maxsplit=1)[0]
    words = re.findall(r"[a-z0-9_./>=-]+", first.lower())
    return {w for w in words if len(w) > 2}


# How much of a template trap's opening sentence a fork entry must share to
# count as the same trap. See the module docstring — loose on purpose.
OVERLAP = 0.6


def _present(template_entry: str, fork_entries: list) -> bool:
    wanted = _tokens(template_entry)
    if not wanted:
        return True
    for candidate in fork_entries:
        shared = wanted & _tokens(candidate)
        if len(shared) / len(wanted) >= OVERLAP:
            return True
    return False


def compare(fork_text: str, template_text: str):
    """(fork count, template count, template entries the fork is missing)."""
    fork = trap_entries(fork_text)
    template = trap_entries(template_text)
    missing = [e for e in template if not _present(e, fork)]
    return len(fork), len(template), missing


def main(argv: list[str]) -> int:
    fork_text = FORK_KIT.read_text()
    if len(argv) < 2:
        count = len(trap_entries(fork_text))
        print(f"fork {FORK_KIT}: {count} trap entries")
        return 0 if count else 1

    template_path = Path(argv[1])
    if not template_path.is_file():
        # A fork's sandbox often cannot see the template checkout at all.
        # SKIP-shaped, not pass-shaped: say so and exit non-zero rather than
        # printing a comparison that never happened.
        print(f"cannot read template kit at {template_path} — "
              f"no comparison was made")
        return 2

    fork_n, template_n, missing = compare(fork_text, template_path.read_text())
    print(f"{FORK_KIT}: fork {fork_n} / template {template_n}")
    for entry in missing:
        print(f"  MISSING: {key(entry)}…")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
