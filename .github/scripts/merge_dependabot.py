"""Merge same-repository Dependabot PRs only after their current CI passes."""

import json
import os
import subprocess
from urllib.parse import urlencode

REQUIRED_JOBS = {"test", "lint", "build-and-test-deployment"}


def gh(*arguments):
    """Run GitHub CLI without interpreting repository data as shell code."""
    result = subprocess.run(
        ["gh", *arguments], check=True, capture_output=True, text=True
    )
    return result.stdout


def api(path, method="GET", **fields):
    """Call the repository API with string-valued JSON fields."""
    arguments = ["api", "--method", method, path]
    for name, value in fields.items():
        arguments.extend(["-f", f"{name}={value}"])
    output = gh(*arguments)
    return json.loads(output) if output.strip() else None


def items(path, key=None, **parameters):
    """Read every page of a REST collection."""
    page = 1
    while True:
        query = urlencode({**parameters, "per_page": 100, "page": page})
        response = api(f"{path}?{query}")
        batch = response[key] if key else response
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def eligible(pull, repository):
    """Limit automation to open Dependabot branches in this repository."""
    return (
        pull["state"] == "open"
        and not pull["draft"]
        and pull["user"]["login"] == "dependabot[bot]"
        and pull["base"]["ref"] == "main"
        and pull["head"]["repo"] is not None
        and pull["head"]["repo"]["full_name"] == repository
        and pull["head"]["ref"].startswith("dependabot/")
    )


def process_pull(repository, number):
    """Approve CI prompts and merge one verified head without bypassing rules."""
    root = f"repos/{repository}"
    path = f"{root}/pulls/{number}"
    pull = api(path)
    if not eligible(pull, repository):
        return False
    head = pull["head"]["sha"]
    if pull["mergeable_state"] == "dirty":
        print(f"PR #{number}: merge conflicts require attention")
        return False

    # Strict branch protection requires tests against an up-to-date base.
    comparison = api(f"{root}/compare/main...{head}")
    if comparison["behind_by"] > 0:
        api(f"{path}/update-branch", "PUT", expected_head_sha=head)
        updated = api(path)
        print(f"PR #{number}: branch update requested; head {updated['head']['sha']}")
        return False

    runs = list(
        items(
            f"{root}/actions/workflows/test.yml/runs",
            "workflow_runs",
            head_sha=head,
            event="pull_request",
        )
    )
    if not runs:
        print(f"PR #{number}: waiting for PR CI on {head}")
        return False
    run = max(runs, key=lambda entry: entry["id"])
    if run["conclusion"] == "action_required":
        # The lockfile-refresh bot's push can leave PR CI awaiting approval.
        # Never approve a run belonging to another PR or an old head.
        if any(pr["number"] == number for pr in run["pull_requests"]):
            current = api(path)
            if eligible(current, repository) and current["head"]["sha"] == head:
                api(f"{root}/actions/runs/{run['id']}/approve", "POST")
                approved = api(f"{root}/actions/runs/{run['id']}")
                print(f"PR #{number}: CI approval submitted ({approved['status']})")
        return False
    if run["status"] != "completed" or run["conclusion"] != "success":
        print(f"PR #{number}: CI has not passed on {head}")
        return False

    jobs = list(items(f"{root}/actions/runs/{run['id']}/jobs", "jobs", filter="latest"))
    successful_jobs = {job["name"] for job in jobs if job["conclusion"] == "success"}
    if not REQUIRED_JOBS.issubset(successful_jobs):
        print(f"PR #{number}: required CI jobs did not all execute successfully")
        return False
    checks = list(
        items(f"{root}/commits/{head}/check-runs", "check_runs", filter="latest")
    )
    if any(
        check["status"] != "completed"
        or check["conclusion"] not in {"success", "neutral", "skipped"}
        for check in checks
    ):
        print(f"PR #{number}: another check is pending or failed")
        return False
    statuses = list(items(f"{root}/commits/{head}/statuses"))
    latest_statuses = {}
    for status in statuses:
        latest_statuses.setdefault(status["context"], status["state"])
    if any(state != "success" for state in latest_statuses.values()):
        return False

    reviews = list(items(f"{path}/reviews"))
    decisions = {}
    for review in reviews:
        if review["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}:
            decisions[review["user"]["login"]] = review
    if any(review["state"] == "CHANGES_REQUESTED" for review in decisions.values()):
        print(f"PR #{number}: a reviewer has requested changes")
        return False

    current = api(path)
    if not eligible(current, repository) or current["head"]["sha"] != head:
        return False
    approval = decisions.get("github-actions[bot]", {})
    if approval.get("state") != "APPROVED" or approval.get("commit_id") != head:
        api(
            f"{path}/reviews",
            "POST",
            event="APPROVE",
            commit_id=head,
            body="Automated approval: Dependabot update with passing current-head CI.",
        )
        reviews = list(items(f"{path}/reviews"))
        if not any(
            review["user"]["login"] == "github-actions[bot]"
            and review["state"] == "APPROVED"
            and review["commit_id"] == head
            for review in reviews
        ):
            raise RuntimeError(f"PR #{number}: approval was not recorded")

    current = api(path)
    if (
        not eligible(current, repository)
        or current["head"]["sha"] != head
        or current["mergeable_state"] != "clean"
    ):
        print(f"PR #{number}: waiting for GitHub's remaining merge gates")
        return False
    # No --admin or bypass: GitHub enforces branch protection at merge time.
    try:
        gh(
            "pr",
            "merge",
            str(number),
            "--repo",
            repository,
            "--merge",
            "--match-head-commit",
            head,
        )
    except subprocess.CalledProcessError:
        # A transport failure may still have committed the merge server-side.
        merged = api(path)
        if not merged["merged"]:
            raise
    else:
        merged = api(path)
    if not merged["merged"]:
        raise RuntimeError(f"PR #{number}: merge was not recorded")

    # GITHUB_TOKEN merges do not trigger the normal push deployment workflow.
    gh("workflow", "run", "main.yml", "--repo", repository, "--ref", "main")
    print(f"PR #{number}: merged {merged['merge_commit_sha']}; deployment requested")
    return True


def main():
    """Reconcile open Dependabot PRs, merging at most one per run."""
    repository = os.environ["GH_REPO"]
    for pull in items(f"repos/{repository}/pulls", state="open", base="main"):
        if eligible(pull, repository) and process_pull(repository, pull["number"]):
            # Let remaining PRs update and retest against this merge first.
            break


if __name__ == "__main__":
    main()
