import click
from rich.console import Console
from doing.utils import get_config, run_command
from doing.options import get_common_options
from doing.pr.create_pr import cmd_create_pr
from doing.pr.open_pr import cmd_open_pr

console = Console()


@click.group()
def pr():
    """
    Work with pull requests.
    """
    pass


@pr.command()
@click.argument("pr_id", nargs=-1, required=True)
def close(pr_id):
    """
    Close a specific PR_ID.

    PR_ID is the ID number of a pull request. '!' prefix is allowed.
    You can specify multiple IDs by separating with a space.
    """
    organization = get_config("organization")
    state = "abandoned"

    for id in pr_id:
        id = str(id).lstrip("!")
        cmd = f"az repos pr update --id {id} --status '{state}' "
        cmd += f"--org '{organization}'"
        result = run_command(cmd)
        assert result.get("status") == state
        console.print(f"[dark_orange3]>[/dark_orange3] pullrequest !{id} set to '{state}'")


@pr.command()
@click.argument("work-item-id", required=True, type=str)
@click.option(
    "--draft/--no-draft",
    required=False,
    default=False,
    help="Create draft/WIP pull request. Reviewers will not be notified until you publish. Default is --draft.",
    show_envvar=True,
)
@click.option(
    "--auto-complete/--no-auto-complete",
    required=False,
    default=True,
    help="Set the PR to complete autom. when all policies have passed. Default is --auto-complete.",
    show_envvar=True,
)
@click.option(
    "--self-approve/--no-self-approve",
    required=False,
    default=False,
    help="Add yourself as reviewer and add your approval. Default is --no-self-approve.",
    show_envvar=True,
)
@click.option(
    "--reviewers",
    "-r",
    required=False,
    default=lambda: get_config("default_reviewers", ""),
    type=str,
    help=f"Space separated list of reviewer emails or aliases. Defaults to \"{get_config('default_reviewers','')}\"",
    show_envvar=True,
)
@click.option(
    "--checkout/--no-checkout",
    required=False,
    default=True,
    help="Run git commands to checkout remote branch locally. Default is --checkout.",
    show_envvar=True,
)
@click.option(
    "--delete-source-branch/--no-delete-source-branch",
    required=False,
    default=True,
    help="Set to delete source branch when pull request completes. Default is --delete-source-branch.",
    show_envvar=True,
)
@click.option(
    "--web/--no-web",
    "-w",
    required=False,
    default=False,
    type=bool,
    help="Open newly created issue in the web browser.",
    show_envvar=True,
)
def create(
    work_item_id: str,
    draft: bool,
    auto_complete: bool,
    self_approve: bool,
    reviewers: str,
    checkout: bool,
    delete_source_branch: bool,
    web: bool,
) -> None:
    """
    Create a pull request from a work item ID.

    WORK_ITEM_ID is the work item ID that will be linked to the PR.
    """
    pr_id = cmd_create_pr(
        work_item_id,
        draft,
        auto_complete,
        self_approve,
        reviewers,
        checkout,
        delete_source_branch,
        **get_common_options(),
    )
    if web:
        cmd_open_pr(pr_id)
