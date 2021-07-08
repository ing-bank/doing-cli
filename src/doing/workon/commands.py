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
    default="User Story",
    type=click.Choice(["Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story"]),
    help='Type of work item. Defaults to "User Story"',
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
@click.option(
    "--draft/--no-draft",
    required=False,
    default=True,
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
    "--story-points",
    "-s",
    required=False,
    default="",
    type=str,
    help="The number of story points to assign. Not assigned if not specified.",
    show_envvar=True,
)
def workon(
    issue,
    type,
    parent,
    reviewers,
    draft: bool,
    auto_complete: bool,
    self_approve: bool,
    checkout: bool,
    delete_source_branch: bool,
    story_points,
):
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
        title=issue,
        mine=True,
        assignee="",
        label="",
        body="",
        type=type,
        parent=parent,
        story_points=story_points,
        **get_common_options(),
    )

    # Open a PR.
    cmd_create_pr(
        work_item_id=str(work_item_id),
        draft=draft,  # Default true, note: `doing create pr` defaults to False
        auto_complete=auto_complete,
        self_approve=self_approve,
        reviewers=reviewers,
        checkout=checkout,
        delete_source_branch=delete_source_branch,
        **get_common_options(),
    )
