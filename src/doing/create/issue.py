from doing.exceptions import InputError
from doing.utils import run_command, get_az_devop_user_email

from rich.console import Console

console = Console()


def cmd_create_issue(
    title: str,
    mine: bool,
    assigned_to: str,
    type: str,
    parent: str,
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
) -> int:
    """
    Create a new issue.
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

    console.print(f"[dark_orange3]>[/dark_orange3] Created issue {issue_id} '[cyan]{title}[/cyan]' ({type})")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added area-path '{area}'")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added iteration-path '{iteration}'")
    if assigned_to:
        console.print(f"\t[dark_orange3]>[/dark_orange3] added assignee '{assigned_to}'")

    if parent:
        cmd = "az boards work-item relation add "
        cmd += f"--id {issue_id} "
        cmd += "--relation-type 'parent' "
        cmd += f"--target-id {parent} "
        cmd += f"--org '{organization}' "
        run_command(cmd)
        console.print(f"\t[dark_orange3]>[/dark_orange3] added work-item #{parent} as a parent")

    return issue_id
