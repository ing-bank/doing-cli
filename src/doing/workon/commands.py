import click

from doing.create.issue import cmd_create_issue
from doing.create.pr import cmd_create_pr, check_uncommitted_work
from doing.options import common_options
from doing.utils import get_az_devop_user_email


@click.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--type",
    required=True,
    default="User Story",
    type=click.Choice(["Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story"]),
    help="Type of work item. Defaults to 'User Story'",
)
@common_options
def workon(issue, type, team, area, iteration, organization, project):
    """
    Create issue with PR and switch git branch.

    Create self-assigned issue, draft pull request and switch git branch all in one go.

    ISSUE is the title to be used for the new work item.
    """
    # Make sure we can change git branch before creating stuff.
    check_uncommitted_work()

    # Create the issue. Note we changed some defaults:
    # - it's assigned to self (mine = True)
    issue_id = cmd_create_issue(
        title=issue,
        mine=True,
        assigned_to="",
        type=type,
        team=team,
        area=area,
        iteration=iteration,
        organization=organization,
        project=project,
    )

    user_email = get_az_devop_user_email()
    # Open a PR. Note we changed some defaults:
    # - draft = True,
    # - reviewers = (own email adress)
    # - checkout = True
    cmd_create_pr(
        work_item_id=issue_id,
        draft=True,
        auto_complete=True,
        self_approve=False,
        reviewers=user_email,
        checkout=True,
        team=team,
        area=area,
        iteration=iteration,
        organization=organization,
        project=project,
    )

    # Done.
