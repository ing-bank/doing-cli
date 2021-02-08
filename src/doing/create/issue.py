from doing.exceptions import InputError
from doing.utils import run_command, get_az_devop_user_email

from rich.console import Console

console = Console()


def cmd_create_issue(
    title: str,
    mine: bool,
    assigned_to: str,
    type: str,
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
) -> int:
    """
    Run `doing issue create` command.

    az CLI:
    https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards/work-item?view=azure-cli-latest#ext_azure_devops_az_boards_work_item_create
    """
    if mine and assigned_to:
        raise InputError("You cannot use --mine in combination with specifying --assigned-to.")

    if mine:
        assigned_to = get_az_devop_user_email()

    cmd = "az boards work-item create "
    cmd += f"--title '{title}' "
    cmd += f"--type '{type}' "
    if assigned_to:
        cmd += f"--assigned-to '{assigned_to}' "
    cmd += f"--area '{area}' --iteration '{iteration}' --project '{project}' --organization '{organization}'"

    issue = run_command(cmd)
    issue_id = issue.get("id")
    # issue_url = f"{organization}/{project}/_workitems/edit/{issue_id}"

    console.print(f"[dark_orange3]>[/dark_orange3] Created issue #{issue_id} '[cyan]{title}[/cyan]'")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added area-path '{area}'")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added iteration-path '{iteration}'")
    if assigned_to:
        console.print(f"\t[dark_orange3]>[/dark_orange3] added assignee '{assigned_to}'")

    return issue_id
