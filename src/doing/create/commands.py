import click

from doing.create.issue import cmd_create_issue
from doing.create.pr import cmd_create_pr
from doing.options import get_common_options, get_config
from doing.open.issue import open_issue
from doing.open.pr import open_pr


@click.group()
def create():
    """
    Create issues or pull requests.
    """
    pass


@create.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--mine/--not-mine",
    "-m",
    default=False,
    required=False,
    help="Assign issue to yourself",
    show_envvar=True,
)
@click.option(
    "--assigned_to",
    "-a",
    required=False,
    default="",
    type=str,
    help="Emailadres or alias of person to assign the issue to. Defaults to empty (unassigned).",
    show_envvar=True,
)
@click.option(
    "--type",
    "-t",
    required=False,
    default=lambda: get_config("default_workitem_type", "User Story"),
    type=click.Choice(["Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story"]),
    help=f"Type of work item. Defaults to \"{get_config('default_workitem_type','User Story')}\"",
    show_envvar=True,
)
@click.option(
    "--parent",
    "-p",
    required=False,
    default="",
    type=str,
    help="To create a child work item, specify the ID of the parent work item.",
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
def issue(
    issue: str,
    mine: bool,
    assigned_to: str,
    type: str,
    parent: str,
    web: bool,
) -> None:
    """
    Create an issue.

    ISSUE is the title to be used for the new work item.
    """
    issue_id = cmd_create_issue(issue, mine, assigned_to, type, parent, **get_common_options())
    if web:
        open_issue(issue_id)


@create.command()
@click.argument("work-item-id", required=True, type=str)
@click.option(
    "--draft/--no-draft",
    "-d",
    required=False,
    default=False,
    help="Create draft/WIP pull request. Reviewers will not be notified untill you publish.",
    show_envvar=True,
)
@click.option(
    "--auto-complete/--no-auto-complete",
    "-a",
    required=False,
    default=False,
    help="Set the PR to complete autom. when all policies have passed & source branch can be merged into the target.",
    show_envvar=True,
)
@click.option(
    "--self-approve/--no-self-approve",
    "-s",
    required=False,
    default=False,
    help="Add yourself as reviewer and add your approval.",
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
    "-c",
    required=False,
    default=False,
    help="Run git commands to checkout remote branch locally.",
    show_envvar=True,
)
@click.option(
    "--delete-source-branch/--no-delete-source-branch",
    required=False,
    default=False,
    help="Set to delete source branch when pull request completes.",
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
def pr(
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
        open_pr(pr_id)
