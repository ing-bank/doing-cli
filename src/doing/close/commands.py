import click
from rich.console import Console
from doing.utils import get_config, run_command

console = Console()


@click.group()
def close():
    """
    Close an issue or PR.
    """
    pass


@close.command()
@click.argument("issue_id", nargs=-1, required=True)
def issue(issue_id):
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


@close.command()
@click.argument("pr_id", nargs=-1, required=True)
def pr(pr_id):
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
