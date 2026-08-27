"""One fleet Python — image, render.yaml, CI and CD must agree.

Adapted from the template's reference implementation at 1.6.29 (`5589318`)
per SYNC-1.6.22-1.6.29 item 5. What this fork had on 2026-08-26, before
these pins existed: the Dockerfile said `python:3.14-slim`, ci.yml ran the
site lane on 3.12, and `render.yaml` declared `PYTHON_VERSION: "3.11.12"` —
three declared Pythons, and the one that actually served visitors was the
oldest of them, because `render.yaml` line 4 says `runtime: python` and
Render's NATIVE runtime never reads the Dockerfile at all. Nothing on the
wire could contradict any of the three until `/healthz` gained its `python`
field.

The single source is the Dockerfile's `FROM` tag, even here where the image
is only a CI artifact: it is the one declaration the whole fleet shares, so
holding the others to it is what makes "the fleet Python" a real number
rather than three local opinions.

TWO PYTHONS LIVE IN THIS ci.yml, and this file pins exactly one of them.
The SITE lane — the jobs that install `requirements.txt` and boot or serve
the docs app — is held to the image's minor. The PACKAGE lane
(`package`, `package-python-range`) tests the `dash-mui-charts` wheel's own
`requires-python` window, currently 3.9-3.13; that is the package's
business and pinning it to a container base would break the moment the
image moved. The split is the 1.6.28 amendment, filed independently by
flows and clerkhook. `_JOB_LANES` below is where a fork states it, and
`test_every_ci_job_is_assigned_a_lane` is what stops a new job from
quietly escaping both.

`.github/workflows/release.yml` is deliberately OUT of scope, and the
omission is stated rather than silent: its `build` job installs the
site's `requirements.txt` and runs `scripts/smoke_test.py` — site-lane
work by the item's own definition — but it is also the job that builds
the artifact published to PyPI, and the interpreter that builds a
released wheel is a package decision this file has no business making.
Item 5 names `ci.yml` and `cd.yml`. So one site-lane certification does
still run on 3.12, in the release path only, and that is a call for the
owner rather than a drift for a session to close.

What is deliberately NOT here: any comparison against the RUNNING
interpreter. The suite legitimately runs on the window legs, where that
assertion would be false by design. Serving-host-versus-declaration is
`scripts/network_smoke.py`'s `python_matches_declared`, against a host.
"""
from __future__ import annotations

import re

from conftest import REPO_ROOT

CI = ".github/workflows/ci.yml"
CD = ".github/workflows/cd.yml"

# Which lane each ci.yml job belongs to. SITE jobs install the docs site's
# requirements and are held to the fleet Python; PACKAGE jobs exercise the
# wheel across its own supported range and are out of this file's scope.
_JOB_LANES = {
    "lint": "site",
    "docs-tests": "site",
    "docker": "site",
    "smoke": "site",
    "pip-audit": "site",
    "lint-js": "site",
    "package": "package",
    "package-python-range": "package",
}


def _fleet_minor() -> str:
    """The single source: the Dockerfile's FROM tag."""
    for line in (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines():
        m = re.match(r"FROM\s+python:(\S+)", line)
        if m:
            return m.group(1)
    raise AssertionError("Dockerfile has no `FROM python:` line")


def _uncommented(path) -> list[str]:
    return [
        ln for ln in (REPO_ROOT / path).read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#")
    ]


def _jobs(path) -> dict[str, list[str]]:
    """ci.yml/cd.yml split into `job name -> its lines`.

    Two-space indent is a workflow job key; anything deeper belongs to the
    job above it. Comment lines are already gone, so a commented-out pin
    cannot be mistaken for a live one.
    """
    out: dict[str, list[str]] = {}
    current = None
    in_jobs = False
    for ln in _uncommented(path):
        if ln.startswith("jobs:"):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        m = re.match(r"^  ([a-z][a-z0-9_-]*):\s*$", ln)
        if m:
            current = m.group(1)
            out[current] = []
        elif current is not None:
            out[current].append(ln)
    return out


def _site_lines() -> list[str]:
    jobs = _jobs(CI)
    return [ln for name, lines in jobs.items()
            if _JOB_LANES.get(name) == "site" for ln in lines]


def test_every_ci_job_is_assigned_a_lane():
    """The scoping above is only honest if it is exhaustive.

    A new job with an unclassified python pin would otherwise be invisible
    to every assertion below — the file would keep passing while the thing
    it exists to prevent happened in the job it never looked at.
    """
    unassigned = sorted(set(_jobs(CI)) - set(_JOB_LANES))
    assert not unassigned, (
        f"ci.yml jobs with no lane in _JOB_LANES: {unassigned} — classify "
        "them as 'site' (installs requirements.txt / boots the docs app) or "
        "'package' (exercises the wheel's own requires-python window)"
    )
    stale = sorted(set(_JOB_LANES) - set(_jobs(CI)))
    assert not stale, f"_JOB_LANES names jobs ci.yml no longer has: {stale}"


def test_dockerfile_tag_is_minor_only():
    """The patch pin IS the security bug: `3.11.8-slim` never receives a
    3.11.x fix release. The minor tag tracks them through Docker Hub."""
    tag = _fleet_minor()
    assert re.fullmatch(r"\d+\.\d+-slim", tag), (
        f"Dockerfile FROM tag is {tag!r} — must be a MINOR tag "
        "(python:X.Y-slim), never a patch pin"
    )


def test_render_yaml_agrees_with_the_image():
    """BRANCHES on the service runtime, and this fork is the `python` one.

    `runtime: python` — Render's native runtime reads PYTHON_VERSION and
    requires a full X.Y.Z (its encoding, not ours). The value is REQUIRED
    and its MINOR must be the fleet Python; the patch is a human bump. On
    THIS host that line is the interpreter production actually runs, which
    is why it is the one encoding whose drift a visitor could feel.

    `runtime: docker` — nothing reads PYTHON_VERSION; the image is the
    interpreter, and a key there reads like the platform's setting while
    never being true. Carried so the test flips branches by itself if the
    service type ever changes.
    """
    minor = _fleet_minor().removesuffix("-slim")
    lines = _uncommented("render.yaml")
    runtime = None
    for ln in lines:
        m = re.match(r"\s*runtime:\s*(\S+)", ln)
        if m:
            runtime = m.group(1)
            break
    assert runtime, "render.yaml declares no `runtime:`"

    value = None
    for i, ln in enumerate(lines):
        if re.match(r"\s*- key: PYTHON_VERSION$", ln):
            m = re.search(r'value:\s*"([^"]+)"', lines[i + 1])
            value = m and m.group(1)
            break

    if runtime == "docker":
        assert value is None, (
            f"render.yaml declares PYTHON_VERSION {value!r} on a docker "
            "runtime — nothing reads it there; a string that looks like the "
            "platform's setting and can never be true is the drift class "
            "this file exists to kill. Delete the key."
        )
        return
    assert runtime == "python", (
        f"render.yaml runtime is {runtime!r} — this test knows `python` and "
        "`docker`; extend the branch deliberately"
    )
    assert value, "render.yaml declares no PYTHON_VERSION"
    assert re.fullmatch(r"\d+\.\d+\.\d+", value), (
        f"PYTHON_VERSION {value!r} — Render's native runtime requires X.Y.Z"
    )
    assert value.startswith(minor + "."), (
        f"render.yaml PYTHON_VERSION {value} vs image python:{minor}-slim — "
        "the runtime that serves traffic and the image CI certifies disagree"
    )


def test_site_lane_ci_jobs_agree_with_the_image():
    minor = _fleet_minor().removesuffix("-slim")
    site = _site_lines()

    mains = [m.group(1) for ln in site
             if (m := re.match(r'\s*python:\s*\["([\d.]+)"\]\s*$', ln))]
    assert mains == [minor], (
        f"site-lane matrix main {mains} vs image python:{minor}-slim"
    )

    literals = [m.group(1) for ln in site
                if (m := re.match(r'\s*python-version:\s*"([\d.]+)"\s*$', ln))]
    assert literals and set(literals) == {minor}, (
        f"site-lane jobs pin python-version {literals}, image is "
        f"python:{minor}-slim"
    )


def test_the_package_lane_is_left_alone():
    """The other half of the split, and the reason it needs saying.

    Nothing above may creep into `package`/`package-python-range`: the
    wheel's supported window is a claim about what users can install it on,
    not about what serves this documentation site. A future session moving
    the fleet Python must leave these jobs untouched, and this test is
    where it finds that out.
    """
    jobs = _jobs(CI)
    package = [ln for name, lines in jobs.items()
               if _JOB_LANES.get(name) == "package" for ln in lines]
    windows = [ln for ln in package if re.match(r'\s*python:\s*\[', ln)]
    assert windows, (
        "no python window left in the package lane — if the wheel's "
        "requires-python range stopped being tested, say so deliberately"
    )


def test_cd_verify_job_agrees_with_the_image():
    """CD's verify job runs network_smoke and smoke_live against
    production, so its interpreter is a deploy artifact like the image."""
    minor = _fleet_minor().removesuffix("-slim")
    cd = _uncommented(CD)
    literals = [m.group(1) for ln in cd
                if (m := re.match(r'\s*python-version:\s*"([\d.]+)"\s*$', ln))]
    assert literals and set(literals) == {minor}, (
        f"cd.yml pins python-version {literals}, image is python:{minor}-slim"
    )


def test_site_matrix_legs_are_the_adjacent_minors():
    """The compat window stays three wide: the site matrix's include legs
    are X.Y-1 and X.Y-2 (or X.Y+1 once it exists).

    These legs were 3.10 and 3.13 while the site lane sat on 3.12 — a
    five-wide window with holes in it once the image reached 3.14. The
    3.9-3.13 coverage that move gave up was never lost: it lives in
    `package-python-range`, where the wheel's own claim is the subject.
    """
    major, y = (int(p) for p in _fleet_minor().removesuffix("-slim").split("."))
    allowed = {f"{major}.{y - 1}", f"{major}.{y - 2}", f"{major}.{y + 1}"}
    legs = [m.group(1) for ln in _site_lines()
            if (m := re.match(r'\s*python:\s*"([\d.]+)"\s*$', ln))]
    assert legs, "the site matrix has no include legs — the window collapsed"
    outside = [leg for leg in legs if leg not in allowed]
    assert not outside, (
        f"site matrix legs {outside} fall outside the three-wide window "
        f"around {major}.{y}"
    )
