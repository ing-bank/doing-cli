import click

from doing.create.issue import cmd_create_issue
from doing.create.pr import cmd_create_pr
from doing.options import common_options


@click.group()
def create():
    """
    Create issues or pull requests.
    """
    pass


@create.command()
@click.argument("issue", required=True, type=str)
@click.option("--mine", "-m", required=True, is_flag=True, help="Assign issue to yourself")
@click.option(
    "--assigned_to",
    "-a",
    required=True,
    default="",
    type=str,
    help="Emailadres of person to assign the issue to. Defaults to empty (unassigned).",
)
@click.option(
    "--type",
    "-t",
    required=True,
    default="User Story",
    type=click.Choice(["Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story"]),
    help="Type of work item. Defaults to 'User Story'",
)
@common_options
def issue(issue, mine, assigned_to, type, team, area, iteration, organization, project):
    """
    Create an issue.

    ISSUE is the title to be used for the new work item.
    """
    cmd_create_issue(issue, mine, assigned_to, type, team, area, iteration, organization, project)


@create.command()
@click.argument("work-item-id", required=True, type=str)
@click.option(
    "--draft",
    "-d",
    required=True,
    is_flag=True,
    help="Create draft/WIP pull request. Reviewers will not be notified untill you publish.",
)
@click.option(
    "--auto-complete",
    "-a",
    required=True,
    is_flag=True,
    help="Set the PR to complete autom. when all policies have passed & source branch can be merged into the target.",
)
@click.option(
    "--self-approve",
    "-s",
    required=True,
    is_flag=True,
    help="Add yourself as reviewer and add your approval.",
)
@click.option(
    "--reviewers",
    "-r",
    required=True,
    default="",
    type=str,
    help="Additional users or groups to include as reviewers on the new pull request. Space separated.",
)
@click.option(
    "--checkout",
    "-c",
    required=True,
    is_flag=True,
    help="Run git commands to checkout remote branch locally.",
)
@common_options
def pr(
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
        team,
        area,
        iteration,
        organization,
        project,
    )
