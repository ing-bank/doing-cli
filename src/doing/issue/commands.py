import click

from doing.issue.create_issue import cmd_create_issue
from doing.options import get_common_options, get_config
from doing.issue.open_issue import cmd_open_issue
from doing.utils import run_command
from doing.list.commands import list

from rich.console import Console

console = Console()


@click.group()
def issue():
    """
    Work with issues.
    """
    pass


issue.add_command(list)


@issue.command()
@click.argument("work_item_id", nargs=-1, required=True)
def close(work_item_id):
    """
    Close a specific WORK_ITEM_ID.

    A '#' prefix is allowed. You can specify multiple IDs by separating with a space.
    """
    organization = get_config("organization")
    state = "Closed"

    for id in work_item_id:
        id = str(id).lstrip("#")
        cmd = f"az boards work-item update --id {id} --state '{state}' "
        cmd += f"--org '{organization}'"
        result = run_command(cmd)
        assert result.get("fields").get("System.State") == state
        console.print(f"[dark_orange3]>[/dark_orange3] work item #{id} set to '{state}'")


@issue.command()
@click.argument("issue", required=True, type=str)
@click.option(
    "--mine/--not-mine",
    "-m",
    default=False,
    required=False,
    help="Assign issue to yourself. Shorthand for '-a @me'.",
    show_envvar=True,
)
@click.option(
    "--assignee",
    "-a",
    required=False,
    default="",
    type=str,
    help="Emailadres or alias of person to assign. Defaults to empty (unassigned). Use '@me' to self-assign.",
    show_envvar=True,
)
@click.option(
    "--body",
    "-b",
    required=False,
    default="",
    type=str,
    help="Optional description of the work item.",
    show_envvar=True,
)
@click.option(
    "--type",
    "-t",
    required=False,
    default=lambda: get_config("default_workitem_type", "User Story"),
    type=click.Choice(["Bug", "Epic", "Feature", "User Story", "Issue", "Task", "Test Case"]),
    help=f"Type of work item. Defaults to \"{get_config('default_workitem_type','User Story')}\"",
    show_envvar=True,
)
@click.option(
    "--label",
    "-l",
    required=False,
    default="",
    type=str,
    help="Attach tags (labels) to work item. Comma separate multiple tags.",
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
    assignee: str,
    body: str,
    type: str,
    label: str,
    parent: str,
    web: bool,
) -> None:
    """
    Create an issue.

    ISSUE is the title to be used for the new work item.
    """
    work_item_id = cmd_create_issue(issue, mine, assignee, body, type, label, parent, **get_common_options())
    if web:
        cmd_open_issue(work_item_id)
