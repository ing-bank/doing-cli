import click

from doing.create.issue import cmd_create_issue
from doing.create.pr import cmd_create_pr
from doing.options import get_common_options, get_config


@click.group()
def create():
    """
    Create issues or pull requests.
    """
    pass


@create.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--mine",
    "-m",
    required=False,
    is_flag=True,
    help="Assign issue to yourself",
    show_envvar=True,
)
@click.option(
    "--assigned_to",
    "-a",
    required=False,
    default="",
    type=str,
    help="Emailadres of person to assign the issue to. Defaults to empty (unassigned).",
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
def issue(
    issue,
    mine,
    assigned_to,
    type,
    parent,
):
    """
    Create an issue.

    ISSUE is the title to be used for the new work item.
    """
    cmd_create_issue(issue, mine, assigned_to, type, parent, **get_common_options())


@create.command()
@click.argument("work-item-id", required=True, type=str)
@click.option(
    "--draft",
    "-d",
    required=False,
    is_flag=True,
    help="Create draft/WIP pull request. Reviewers will not be notified untill you publish.",
    show_envvar=True,
)
@click.option(
    "--auto-complete",
    "-a",
    required=False,
    is_flag=True,
    help="Set the PR to complete autom. when all policies have passed & source branch can be merged into the target.",
    show_envvar=True,
)
@click.option(
    "--self-approve",
    "-s",
    required=False,
    is_flag=True,
    help="Add yourself as reviewer and add your approval.",
    show_envvar=True,
)
@click.option(
    "--reviewers",
    "-r",
    required=False,
    default="",
    type=str,
    help="Additional users or groups to include as reviewers on the new pull request. Space separated.",
    show_envvar=True,
)
@click.option(
    "--checkout",
    "-c",
    required=False,
    is_flag=True,
    help="Run git commands to checkout remote branch locally.",
    show_envvar=True,
)
@click.option(
    "--delete-source-branch",
    required=False,
    is_flag=True,
    help="Set to delete source branch when pull request completes.",
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
):
    """
    Create a pull request from a work item ID.

    WORK_ITEM_ID is the work item ID that will be linked to the PR.
    """
    cmd_create_pr(
        work_item_id,
        draft,
        auto_complete,
        self_approve,
        reviewers,
        checkout,
        delete_source_branch,
        **get_common_options(),
    )
