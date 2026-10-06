"""Exercise merge automation against simulated GitHub state, without API writes."""

import copy
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / ".github/scripts/merge_dependabot.py"
SPEC = importlib.util.spec_from_file_location("merge_dependabot", SCRIPT)
automation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(automation)

REPOSITORY = "SECQUOIA/pyomo_jupyter_book"
ROOT = f"repos/{REPOSITORY}"


@pytest.fixture
def github(monkeypatch):
    """Provide mutable GitHub responses and record attempted writes."""
    state = {
        "pull": {
            "number": 1,
            "state": "open",
            "draft": False,
            "user": {"login": "dependabot[bot]"},
            "base": {"ref": "main"},
            "head": {
                "sha": "tested-head",
                "ref": "dependabot/pip/example",
                "repo": {"full_name": REPOSITORY},
            },
            "mergeable_state": "clean",
            "merged": False,
        },
        "run": {
            "id": 10,
            "status": "completed",
            "conclusion": "success",
            "pull_requests": [{"number": 1}],
        },
        "jobs": [
            {"name": name, "conclusion": "success"} for name in automation.REQUIRED_JOBS
        ],
        "checks": [{"status": "completed", "conclusion": "success"}],
        "statuses": [],
        "reviews": [],
        "behind_by": 0,
        "writes": [],
        "commands": [],
        "reads": 0,
    }

    def fake_api(path, method="GET", **fields):
        if method != "GET":
            state["writes"].append((path, method, fields))
        if path.endswith("/reviews") and method == "POST":
            state["reviews"].append(
                {
                    "user": {"login": "github-actions[bot]"},
                    "state": "APPROVED",
                    "commit_id": fields["commit_id"],
                }
            )
            return state["reviews"][-1]
        if path == f"{ROOT}/pulls/1":
            state["reads"] += 1
            if state.get("change_head_at") == state["reads"]:
                state["pull"]["head"]["sha"] = "untested-head"
            return copy.deepcopy(state["pull"])
        if "/compare/" in path:
            return {"behind_by": state["behind_by"]}
        if path.endswith("/update-branch"):
            return {}
        if path.endswith("/approve"):
            state["run"]["status"] = "queued"
            return {}
        if path == f"{ROOT}/actions/runs/10":
            return copy.deepcopy(state["run"])
        raise AssertionError(f"Unexpected API call: {method} {path}")

    def fake_items(path, key=None, **parameters):
        if path.endswith("/test.yml/runs"):
            assert parameters == {"head_sha": "tested-head", "event": "pull_request"}
            return [] if state.get("missing_ci") else [copy.deepcopy(state["run"])]
        for suffix, field in (
            ("/jobs", "jobs"),
            ("/check-runs", "checks"),
            ("/statuses", "statuses"),
            ("/reviews", "reviews"),
        ):
            if path.endswith(suffix):
                return copy.deepcopy(state[field])
        raise AssertionError(f"Unexpected collection: {path}")

    def fake_gh(*arguments):
        state["commands"].append(arguments)
        if arguments[:2] == ("pr", "merge"):
            assert arguments[-2:] == ("--match-head-commit", "tested-head")
            assert "--admin" not in arguments
            state["pull"].update(
                state="closed", merged=True, merge_commit_sha="merged-head"
            )
        return ""

    monkeypatch.setattr(automation, "api", fake_api)
    monkeypatch.setattr(automation, "items", fake_items)
    monkeypatch.setattr(automation, "gh", fake_gh)
    return state


def test_success_approves_merges_exact_head_and_dispatches_deployment(github):
    """A passing PR is approved and merged before deployment is dispatched."""
    assert automation.process_pull(REPOSITORY, 1)
    assert github["writes"][0][2]["commit_id"] == "tested-head"
    assert [command[:2] for command in github["commands"]] == [
        ("pr", "merge"),
        ("workflow", "run"),
    ]
    assert github["commands"][-1][-2:] == ("--ref", "main")


@pytest.mark.parametrize(
    "case", ["human", "fork", "deleted_fork", "draft", "base", "branch", "closed"]
)
def test_ineligible_pr_never_writes(github, case):
    """The bot name alone is insufficient to authorize a merge."""
    pull = github["pull"]
    if case == "human":
        pull["user"]["login"] = "contributor"
    elif case == "fork":
        pull["head"]["repo"]["full_name"] = "contributor/fork"
    elif case == "deleted_fork":
        pull["head"]["repo"] = None
    elif case == "draft":
        pull["draft"] = True
    elif case == "base":
        pull["base"]["ref"] = "another-branch"
    elif case == "branch":
        pull["head"]["ref"] = "human-branch"
    else:
        pull["state"] = "closed"
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


@pytest.mark.parametrize(
    "conclusion", [None, "failure", "cancelled", "skipped", "timed_out"]
)
def test_unsuccessful_ci_never_approves_or_merges(github, conclusion):
    """Incomplete, skipped, or failed CI cannot authorize approval or merging."""
    github["run"]["conclusion"] = conclusion
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


def test_missing_pr_ci_cannot_be_replaced_by_dispatch_success(github):
    """Only current-head PR runs are eligible, even if manual tests passed."""
    github["missing_ci"] = True
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


@pytest.mark.parametrize("conclusion", ["skipped", "failure"])
def test_required_jobs_must_have_executed_successfully(github, conclusion):
    """A green overall run cannot hide skipped or failed required jobs."""
    github["jobs"][0]["conclusion"] = conclusion
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


@pytest.mark.parametrize("conclusion", [None, "failure", "cancelled"])
def test_other_pending_or_failed_checks_block_merge(github, conclusion):
    """Security and other checks must also finish without failure."""
    github["checks"][0]["conclusion"] = conclusion
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


def test_stale_branch_is_updated_before_tests_can_authorize_merge(github):
    """Branch updates are bound to the inspected head and require fresh CI."""
    github["behind_by"] = 1
    assert not automation.process_pull(REPOSITORY, 1)
    assert github["writes"] == [
        (f"{ROOT}/pulls/1/update-branch", "PUT", {"expected_head_sha": "tested-head"})
    ]
    assert not github["commands"]


def test_ci_prompt_is_approved_without_merging(github):
    """Approving a workflow prompt does not count as successful CI."""
    github["run"]["conclusion"] = "action_required"
    assert not automation.process_pull(REPOSITORY, 1)
    assert github["writes"] == [(f"{ROOT}/actions/runs/10/approve", "POST", {})]
    assert not github["commands"]


def test_ci_prompt_for_other_pr_is_not_approved(github):
    """A mismatched workflow-to-PR association must fail closed."""
    github["run"].update(conclusion="action_required", pull_requests=[{"number": 2}])
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


@pytest.mark.parametrize("read_number", [2, 3])
def test_changed_head_is_never_merged(github, read_number):
    """A push between verification, approval, and merge invalidates readiness."""
    github["change_head_at"] = read_number
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["commands"]


def test_requested_changes_are_preserved(github):
    """Automation cannot clear a reviewer's requested changes."""
    github["reviews"] = [
        {"user": {"login": "maintainer"}, "state": "CHANGES_REQUESTED"}
    ]
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


def test_merge_gate_prevents_merge_even_after_bot_approval(github):
    """An approval does not bypass GitHub's remaining protections."""
    github["pull"]["mergeable_state"] = "blocked"
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["commands"]


def test_conflicting_branch_is_not_updated(github):
    """A conflicting PR must not stop automation from inspecting other PRs."""
    github["pull"]["mergeable_state"] = "dirty"
    github["behind_by"] = 1
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]


def test_failed_commit_status_blocks_merge(github):
    """Legacy commit statuses are gates in addition to Actions check runs."""
    github["statuses"] = [{"context": "external-ci", "state": "failure"}]
    assert not automation.process_pull(REPOSITORY, 1)
    assert not github["writes"] and not github["commands"]
