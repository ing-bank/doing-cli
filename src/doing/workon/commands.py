import click

from doing.issue.create_issue import cmd_create_issue
from doing.pr.create_pr import cmd_create_pr, check_uncommitted_work
from doing.options import get_common_options
from doing.utils import get_config


@click.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--type",
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
    "--reviewers",
    "-r",
    required=False,
    default=lambda: get_config("default_reviewers", ""),
    type=str,
    help=f"Space separated list of reviewer emails. Defaults to \"{get_config('default_reviewers','')}\"",
    show_envvar=True,
)
def workon(issue, type, parent, reviewers):
    """
    Create issue with PR and switch git branch.

    Create self-assigned issue, draft pull request and switch git branch all in one go.

    ISSUE is the title to be used for the new work item.
    """
    # Make sure we can change git branch before creating stuff.
    check_uncommitted_work()

    # Create the issue. Note we changed some defaults:
    # - it's assigned to self (mine = True)
    work_item_id = cmd_create_issue(
        title=issue, mine=True, assignee="", label="", body="", type=type, parent=parent, **get_common_options()
    )

    # Open a PR. Note we use the same defaults as `doing create pr`
    cmd_create_pr(
        work_item_id=work_item_id,
        draft=True,
        auto_complete=True,
        self_approve=False,
        reviewers=reviewers,
        checkout=True,
        delete_source_branch=True,
        **get_common_options(),
    )
