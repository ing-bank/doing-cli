import os
import subprocess
import sys

from doing.utils import run_command, get_repo_name, to_snake_case, get_az_devop_user_email, get_git_current_branch

from rich.console import Console

console = Console()


def cmd_create_pr(
    work_item_id: str,
    draft: bool,
    auto_complete: bool,
    self_approve: bool,
    reviewers: str,
    checkout: bool,
    delete_source_branch: bool,
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
) -> int:
    """
    Run command `doing create pr`.

    API doc:
    https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/repos/pr?view=azure-cli-latest#ext_azure_devops_az_repos_pr_create
    """
    work_item_id = str(work_item_id).lstrip("#")

    if checkout:
        check_uncommitted_work()

    repo_name = get_repo_name()
    user_email = get_az_devop_user_email()

    # Info on related work item
    work_item = run_command(f"az boards work-item show --id {work_item_id} --query 'fields' --org '{organization}'")
    work_item_title = work_item.get("System.Title")

    # Info on remote branches
    remote_branches = run_command(
        f"az repos ref list --repository {repo_name} --query '[].name' --org '{organization}' -p '{project}'"
    )
    remote_branches = [x.rpartition("/")[2] for x in remote_branches if x.startswith("refs/heads")]

    # Create a new branch, only if it does yet exist
    cmd = f"az repos ref list --repository '{repo_name}' --query \"[?name=='refs/heads/master'].objectId\" "
    cmd += f"--org '{organization}' -p '{project}'"
    master_branch_object_id = run_command(cmd)[0]
    branch_name = f"{work_item_id}_{to_snake_case(work_item_title)}"
    if branch_name in remote_branches:
        console.print(
            f"[dark_orange3]>[/dark_orange3] Remote branch '[cyan]{branch_name}[/cyan]' already exists, using that one"
        )
        # Check if there is not already an existing PR for this branch
        prs = run_command(f"az repos pr list -r {repo_name} -s {branch_name} --org '{organization}' -p '{project}'")
        if len(prs) >= 1:
            pr_id = prs[0].get("pullRequestId")
            console.print(
                f"[dark_orange3]>[/dark_orange3] Pull request {pr_id} already exists",
                f"for branch '[cyan]{branch_name}[/cyan]', aborting.",
            )
            if not checkout and (get_git_current_branch() != branch_name):
                explain_checkout(branch_name)
            if checkout and (get_git_current_branch() != branch_name):
                git_checkout(branch_name)
                # TODO:
                # Users might get a
                # fatal: A branch named '121323_test_tim_28jan_2' already exists.
                # if local branch already exists.
                # We could test to see if it is setup to track the remote branch, and if not set that right
                # Might help some less experienced git users.

            return pr_id
    else:
        cmd = f"az repos ref create --name 'heads/{branch_name}' --repository '{repo_name}' "
        cmd += f"--object-id '{master_branch_object_id}' -p '{project}' --org '{organization}'"
        branch = run_command(cmd)
        assert branch.get("success")
        console.print(f"[dark_orange3]>[/dark_orange3] Created remote branch '[cyan]{branch_name}[/cyan]'")

    # Create the PR
    command = f"az repos pr create --repository '{repo_name}' "
    command += f"--draft '{str(draft).lower()}' "
    command += f"--work-items '{work_item_id}' "
    command += f"--source-branch '{branch_name}' "
    command += f"--title '{work_item_title}' "
    command += f"--project '{project}' --organization '{organization}' "

    # Some sensible defaults
    command += "--transition-work-items 'true' "
    command += f"--delete-source-branch '{str(delete_source_branch).lower()}' "

    # auto-complete.
    command += f"--auto-complete '{str(auto_complete).lower()}' "
    if self_approve:
        if len(reviewers) > 0:
            reviewers = f"{reviewers} {user_email}"
        else:
            reviewers = user_email

    if reviewers != "":
        command += f"--reviewers '{reviewers}' "

    pr = run_command(command)

    # Report to user
    pr_id = pr.get("pullRequestId")
    console.print(f"[dark_orange3]>[/dark_orange3] Created pull request {pr_id} [cyan]'{work_item_title}'[cyan]")
    console.print(f"\t[dark_orange3]>[/dark_orange3] linked work-item {work_item_id}")
    if draft:
        console.print("\t[dark_orange3]>[/dark_orange3] marked as draft pull request")
    if auto_complete:
        console.print("\t[dark_orange3]>[/dark_orange3] set auto-complete to True'")
    if delete_source_branch:
        console.print("\t[dark_orange3]>[/dark_orange3] set to delete remote source branch after PR completion")
    if len(reviewers) > 0:
        console.print(f"\t[dark_orange3]>[/dark_orange3] added reviewers: '{reviewers}'")
    if self_approve:
        run_command(f"az repos pr set-vote --id {pr_id} --vote 'approve' --org '{organization}'")
        console.print(f"\t[dark_orange3]>[/dark_orange3] Approved PR {pr_id} for '{user_email}'")

    if not checkout:
        explain_checkout(branch_name)
    else:
        git_checkout(branch_name)

    return pr_id


def explain_checkout(branch_name: str) -> None:
    """
    Explain how to checkout a remote branch locally.
    """
    console.print("\tTo start work on the PR run:")
    console.print("\t[bright_black]git fetch origin[/bright_black]")
    console.print(f"\t[bright_black]git checkout -b {branch_name} origin/{branch_name}[/bright_black]")


def git_checkout(branch_name: str, verbose: bool = True) -> None:
    """
    Checkout a remote branch locally.
    """
    if verbose:
        console.print("\t[dark_orange3]$[/dark_orange3] Running command: [bright_black]git fetch origin[/bright_black]")
    os.system("git fetch origin")

    if verbose:
        console.print(
            "\t[dark_orange3]$[/dark_orange3] Running command:",
            f"[bright_black]git checkout -b {branch_name} origin/{branch_name}[/bright_black]",
        )
    os.system(f"git checkout -b {branch_name} origin/{branch_name}")


def check_uncommitted_work() -> None:
    """
    See if there are unstaged changes in git repo that would prevent switching branches.
    """
    result = subprocess.Popen(
        ["git", "diff", "--exit-code"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    result.communicate()[0]
    if result.returncode != 0:
        console.print(
            "You have local unstaged changes (see [bright_black]git diff[/bright_black]).",
            "Commit them before running this command.",
        )
        sys.exit(1)
