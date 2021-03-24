import click

from doing.issue.create_issue import cmd_create_issue
from doing.options import get_common_options, get_config
from doing.issue.open_issue import cmd_open_issue
from doing.utils import run_command

from rich.console import Console

console = Console()


@click.group()
def issue():
    """
    Work with issues.
    """
    pass


@issue.command()
@click.argument("issue_id", nargs=-1, required=True)
def close(issue_id):
    """
    Close a specific ISSUE_ID.

    ISSUE_ID is the ID number of a work item. '#' prefix is allowed.
    You can specify multiple IDs by separating with a space.
    """
    organization = get_config("organization")
    state = "Closed"

    for id in issue_id:
        id = str(id).lstrip("#")
        cmd = f"az boards work-item update --id {id} --state '{state}' "
        cmd += f"--org '{organization}'"
        result = run_command(cmd)
        assert result.get("fields").get("System.State") == state
        console.print(f"[dark_orange3]>[/dark_orange3] work-item #{id} set to '{state}'")


@issue.command()
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
def create(
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
        cmd_open_issue(issue_id)
