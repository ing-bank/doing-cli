from doing.utils import (
    run_command,
    get_repo_name,
    to_snake_case,
    get_az_devop_user_email,
)

from rich.console import Console

console = Console()


def cmd_create_pr(
    work_item_id: str,
    draft: bool,
    auto_complete: bool,
    self_approve: bool,
    reviewers: str,
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
                "for branch '[cyan]{branch_name}[/cyan]', aborting.",
            )
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

    print("TODO: print the git commands to start working on the PR branch locally.")
    print("TODO: add flag to automatically run those git commands for you.")
