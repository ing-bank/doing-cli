import os

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
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
):
    """
    Run command `doing create pr`.

    API doc:
    https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/repos/pr?view=azure-cli-latest#ext_azure_devops_az_repos_pr_create
    """
    repo_name = get_repo_name()
    user_email = get_az_devop_user_email()

    # Info on related work item
    work_item = run_command(f"az boards work-item show --id {work_item_id} --query 'fields'")
    work_item_title = work_item.get("System.Title")

    # Info on remote branches
    remote_branches = run_command(f"az repos ref list --repository {repo_name} --query '[].name'")
    remote_branches = [x.rpartition("/")[2] for x in remote_branches if x.startswith("refs/heads")]

    # Create a new branch, only if it does yet exist
    master_branch_object_id = run_command(
        f"az repos ref list --repository '{repo_name}' --query \"[?name=='refs/heads/master'].objectId\""
    )[0]
    branch_name = f"{work_item_id}_{to_snake_case(work_item_title)}"
    if branch_name in remote_branches:
        console.print(f"> Branch '[cyan]{branch_name}[/cyan]' already exists on remote, using that one")
        # Check if there is not already an existing PR for this branch
        prs = run_command(f"az repos pr list -r {repo_name} -s {branch_name}")
        if len(prs) >= 1:
            console.print(
                f"> Pull request {prs[0].get('pullRequestId')} already exists",
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

            return None
    else:
        branch = run_command(
            f"az repos ref create --name 'heads/{branch_name}' --repository '{repo_name}'",
            f"--object-id '{master_branch_object_id}' --project '{project}' --organization '{organization}'",
        )
        assert branch.get("success")
        console.print(f"[red]>[/red] Created branch '[cyan]{branch_name}[/cyan]'")

    # Create the PR
    command = f"az repos pr create --repository '{repo_name}' "
    command += f"--draft '{str(draft).lower()}' "
    command += f"--work-items '{work_item_id}' "
    command += f"--source-branch '{branch_name}' "
    command += f"--title '{work_item_title}' "
    command += f"--project '{project}' --organization '{organization}' "

    # Some sensible defaults
    command += "--transition-work-items 'true' "
    command += "--delete-source-branch 'true' "

    # auto-complete.
    command += f"--auto-complete '{str(auto_complete).lower()}' "
    if self_approve:
        reviewers = f"{reviewers} {user_email}"

    if reviewers != "":
        command += f"--reviewers '{reviewers}' "

    pr = run_command(command)

    # Report to user
    pr_id = pr.get("pullRequestId")
    console.print(f"[red]>[/red] Created pr #{pr_id} '{work_item_title}'")
    console.print(f"\t[red]>[/red] linked work-item #{work_item_id}")
    if draft:
        console.print("\t[red]>[/red] marked PR as draft'")
    if auto_complete:
        console.print("\t[red]>[/red] Set auto-complete to True'")
    if self_approve:
        console.print(f"\t[red]>[/red] Added self ({user_email}) as reviewer'")
        run_command(f"az repos pr set-vote --id {pr_id} --vote 'approve'")
        console.print(f"\t[red]>[/red] Approved PR {pr_id} for {user_email}.")

    if not checkout:
        explain_checkout(branch_name)
    else:
        git_checkout(branch_name)


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
        console.print("\tRunning command: [bright_black]git fetch origin[/bright_black]")
    os.system("git fetch origin")

    if verbose:
        console.print(
            f"\tRunning command: [bright_black]git checkout -b {branch_name} origin/{branch_name}[/bright_black]"
        )
    os.system(f"git checkout -b {branch_name} origin/{branch_name}")
