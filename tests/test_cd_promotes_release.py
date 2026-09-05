"""CD promotes main → release on a green matrix; nothing else writes release.

The road since 1.6.35 (owner decision A, 2026-08-29): Render auto-deploys
the `release` branch and ONLY cd.yml's `deploy` job writes it, as a
fast-forward push of the run's own sha after the CI matrix is green. The
measurement behind it: 14:12Z that day, de0bcff pushed to main; Render,
watching main, built it within the minute; its CD run went red at 14:13Z
with the deploy job skipped; /healthz served the red build for ~6 minutes.
CI cannot stop a deploy while the platform watches the branch CI is still
judging.

These pins hold the STRUCTURE — the part a fork can drift silently:
`deploy` still needs `test`; the promote step exists and is not a force
push; the write grant is on that one job, not the workflow; the hook
step is gone; render.yaml watches `release`.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CD = REPO / ".github" / "workflows" / "cd.yml"
RENDER = REPO / "render.yaml"


def _cd() -> dict:
    return yaml.safe_load(CD.read_text())


def _deploy() -> dict:
    return _cd()["jobs"]["deploy"]


def _promote_step() -> dict:
    steps = [s for s in _deploy()["steps"] if s.get("name") == "Promote to release"]
    assert len(steps) == 1, "cd.yml deploy job must have exactly one 'Promote to release' step"
    return steps[0]


def test_release_is_only_written_after_a_green_matrix():
    """needs: [test] is the whole gate — a red matrix never reaches the push."""
    assert "test" in _deploy()["needs"]
    assert _cd()["jobs"]["test"]["uses"].endswith("ci.yml")


def test_the_promote_step_is_a_fast_forward_push_of_this_sha():
    # Commands only — the step's comments explain why NOT to force.
    run = "\n".join(
        line for line in _promote_step()["run"].splitlines()
        if not line.lstrip().startswith("#")
    )
    assert re.search(r"git push origin\s+\"?HEAD:refs/heads/release\"?", run), run
    assert "--force" not in run and " -f " not in run and "+HEAD" not in run, (
        "a non-fast-forward push must FAIL the job — someone wrote release "
        "by hand — never be forced over"
    )


def test_the_promote_checkout_is_not_shallow():
    """A depth-1 clone cannot fast-forward an EXISTING ref: the push is
    rejected as non-fast-forward. Run 33262495272 (747d8b3, 2026-08-29)
    failed its promote step in one second for exactly this; the first
    promote had only passed because `release` did not exist yet."""
    steps = _deploy()["steps"]
    checkouts = [s for s in steps if str(s.get("uses", "")).startswith("actions/checkout")]
    assert checkouts, "the promote job must check out before it can push"
    assert checkouts[0].get("with", {}).get("fetch-depth") == 0, (
        "promote's checkout must be fetch-depth: 0 — a shallow HEAD pushed "
        "onto an existing release is rejected ('fetch first')"
    )


def test_a_verify_only_dispatch_does_not_promote():
    cond = _promote_step().get("if", "")
    assert "inputs.target_url == ''" in cond and "github.event_name == 'push'" in cond, cond


def test_the_write_grant_is_on_the_deploy_job_only():
    assert _deploy()["permissions"] == {"contents": "write"}
    assert _cd()["permissions"] == {"contents": "read"}, (
        "the workflow-level grant stays read; only the promote job writes"
    )
    for name, job in _cd()["jobs"].items():
        if name != "deploy":
            assert job.get("permissions", {}).get("contents") != "write", name


def test_the_deploy_hook_is_gone():
    """Sync item 13's detect, from the inside: the secret's name must not
    appear anywhere in the file, comments included."""
    assert "RENDER_DEPLOY_HOOK" + "_URL" not in CD.read_text()
    assert not any("hook" in (s.get("id") or "") for s in _deploy()["steps"])


def test_verify_never_runs_on_a_failed_deploy():
    """Run 33262495272 (747d8b3): the promote step failed, verify ran
    anyway under `!= 'cancelled' && != 'skipped'` and went GREEN against
    the previous build. Verify must require success AND check the sha."""
    verify = _cd()["jobs"]["verify"]
    assert "deploy" in verify["needs"]
    assert verify.get("if", "").strip() == "needs.deploy.result == 'success'", verify.get("if")
    sha_steps = [s for s in verify["steps"] if s.get("name") == "The live build IS this run's sha"]
    assert len(sha_steps) == 1, "verify must assert /healthz build == github.sha itself"
    run = sha_steps[0]["run"]
    assert "/healthz" in run and "GITHUB_SHA" in run and "exit 1" in run


def test_render_watches_release():
    doc = yaml.safe_load(RENDER.read_text())
    web = [s for s in doc["services"] if s.get("type") == "web"]
    assert web and all(s.get("branch") == "release" for s in web), (
        "render.yaml must deploy `release` — main is where CI judges, "
        "release is what it certified"
    )
    # autoDeploy stays unset (Render default: on) — it IS the mechanism.
    assert all("autoDeploy" not in s or s["autoDeploy"] is True for s in web)


def test_the_posture_fence_declares_the_road():
    text = (REPO / "DIVERGENCES.md").read_text()
    fence = re.search(r"^```yaml posture[ \t]*\n(.*?)^```", text, re.M | re.S).group(1)
    assert re.search(r"^deploy:\s*release-branch\s*$", fence, re.M), fence


# --------------------------------------------------- sync 1.6.44 item 12 ----

CI = REPO / ".github" / "workflows" / "ci.yml"


def _triggers(path: Path) -> dict:
    """A workflow's `on:` block, read past PyYAML's boolean trap.

    THE TRAP, and it is the whole reason this helper exists: YAML 1.1 parses
    an unquoted `on:` key as the BOOLEAN True, so `workflow["on"]` raises
    KeyError on every workflow file ever written. A test that catches that
    and moves on asserts NOTHING — it reports green on a file it never read,
    which is exactly the shape item 12 warns about.
    """
    doc = yaml.safe_load(path.read_text())
    for key in (True, "on"):
        if key in doc:
            return doc[key] or {}
    raise AssertionError(
        f"{path.name}: no `on:` block found under either the boolean True "
        f"key or the string 'on' — the parse is wrong, not the file"
    )


def test_the_boolean_on_key_trap_is_real():
    """Non-vacuity for the helper: prove the KeyError actually happens.

    Without this, `_triggers` looks like defensive padding and the next
    person simplifies it back to `doc["on"]`.
    """
    doc = yaml.safe_load(CI.read_text())
    assert True in doc, "PyYAML no longer folds `on:` to the boolean True"
    assert "on" not in doc


def test_cd_calls_ci_as_a_reusable_workflow():
    """Half one of the detect."""
    jobs = _cd()["jobs"]
    calls = [j for j in jobs.values()
             if str(j.get("uses", "")).endswith(".github/workflows/ci.yml")]
    assert len(calls) == 1, "cd.yml must call ci.yml exactly once"


def test_ci_does_not_also_run_itself_on_a_push_to_main():
    """Half two — and the defect the pair produces.

    cd.yml runs on push to main and its first job `uses:` ci.yml. If ci.yml
    ALSO triggered on that push, one push would start two runs contending
    for the same concurrency group and cancelling each other. A
    `workflow_call` must create no run of its own.
    """
    triggers = _triggers(CI)
    push = triggers.get("push")
    assert not push, (
        f"ci.yml triggers on push ({push!r}) while cd.yml calls it — one push "
        f"would start two contending runs"
    )
    assert "workflow_call" in triggers, "ci.yml is not callable by cd.yml"


def test_cd_is_the_one_that_owns_main():
    """The complement: main must still be covered by something."""
    triggers = _triggers(CD)
    branches = (triggers.get("push") or {}).get("branches") or []
    assert "main" in branches, "nothing runs on a push to main"


# --------------------------------------------------- sync 1.6.44 item 17 ----

def test_the_timing_trap_names_its_concrete_form():
    """The detect: three phrases, matched with WHITESPACE FLATTENED.

    Flattened because the kit is hard-wrapped prose — "eight samples at 45"
    wraps across a line in the source, so an unflattened search for it finds
    nothing on a file that says it. That is the item's own note, and it is
    the reason this test does not simply grep.
    """
    text = (REPO / ".claude" / "CLAUDE.md").read_text()
    flat = re.sub(r"\s+", " ", text)
    for phrase in ("eight samples at 45", "completed_at", "unreadable"):
        assert phrase in flat, f"trap 3(a) does not mention {phrase!r}"


def test_the_trap_was_amended_not_appended():
    """The item says AMEND IN PLACE; do not append a second entry.

    Two entries about the same measurement is how a traps section grows to
    the point where nobody reads it, and how a fork ends up with the old
    diagnosis still sitting above the correction.
    """
    text = (REPO / ".claude" / "CLAUDE.md").read_text()
    flat = re.sub(r"\s+", " ", text)
    assert flat.count("Which branch Render actually builds") == 1
    # The concrete form must live INSIDE that entry, not in one of its own.
    entry = flat.split("Which branch Render actually builds", 1)[1]
    entry = entry.split("- Verify the artifact the claim is about", 1)[0]
    assert "eight samples at 45" in entry, (
        "the sampler was appended as a separate trap instead of amending 3(a)"
    )


def test_the_sampler_exists_and_points_at_this_host():
    sampler = REPO / "scripts" / "promote_sampler.py"
    assert sampler.is_file()
    src = sampler.read_text()
    assert "muicharts.2plot.dev" in src, "the sampler still points at the template"
    assert "boilerplate.2plot.dev" not in src


def test_the_sampler_refuses_a_bracket_it_did_not_observe():
    """The item's note: a single "new" sample cannot say what it followed."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_sampler", REPO / "scripts" / "promote_sampler.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # `unreadable` must be a state of its own, never folded into `old`.
    assert mod.UNREADABLE != mod.OLD != mod.NEW
    assert mod.classify(None, "abc") == mod.UNREADABLE
    assert mod.classify("abc", "abc") == mod.NEW
    assert mod.classify("def", "abc") == mod.OLD
