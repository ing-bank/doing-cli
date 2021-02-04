import click

from doing.options import common_options

from doing.workon._workon import cmd_workon


@click.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--type",
    required=True,
    default="User Story",
    type=click.Choice(
        ["Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story"]
    ),
    help="Type of work item. Defaults to 'User Story'",
)
@common_options
def workon(issue, type, assigned_to, team, area, iteration, organization, project):
    """
    Start work on a new issue. Creates a new work item on Azure DevOps.

    ISSUE is the title to be used for the new work item.
    """
    cmd_workon(issue, type, assigned_to, team, area, iteration, organization, project)
