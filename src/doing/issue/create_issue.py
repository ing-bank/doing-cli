from doing.exceptions import InputError
from doing.utils import replace_user_aliases, run_command, get_az_devop_user_email, validate_work_item_type

from rich.console import Console

console = Console()


def cmd_create_issue(
    title: str,
    mine: bool,
    assignee: str,
    body: str,
    type: str,
    label: str,
    parent: str,
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
    story_points: str,
) -> int:
    """
    Create a new issue.

    Reference:

    - [`az boards work-item create]`(https://docs.microsoft.com/en-us/cli/azure/boards/work-item?view=azure-cli-latest#az-boards-work-item-create)
    """  # noqa
    if mine and assignee:
        raise InputError("You cannot use --mine in combination with specifying --assigned-to.")

    if mine:
        assignee = get_az_devop_user_email()

    assignee = replace_user_aliases(assignee)
    validate_work_item_type(type)

    cmd = "az boards work-item create "
    cmd += f'--title "{title}" '
    cmd += f'--type "{type}" '
    if assignee:
        cmd += f'--assigned-to "{assignee}" '
    if body:
        cmd += f'--description "{body}" '

    if story_points != "" and label != "":
        cmd += f'--fields "Microsoft.VSTS.Scheduling.StoryPoints={story_points}" "System.Tags={label}" '
    if story_points != "" and label == "":
        cmd += f'--fields "Microsoft.VSTS.Scheduling.StoryPoints={story_points}" '
    if story_points == "" and label != "":
        cmd += f'--fields "System.Tags={label}" '

    cmd += f'--area "{area}" --iteration "{iteration}" --project "{project}" --organization "{organization}"'

    work_item = run_command(cmd)
    work_item_id = work_item.get("id")

    console.print(f"[dark_orange3]>[/dark_orange3] Created work item {work_item_id} '[cyan]{title}[/cyan]' ({type})")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added area-path '{area}'")
    console.print(f"\t[dark_orange3]>[/dark_orange3] added iteration-path '{iteration}'")
    if assignee:
        console.print(f"\t[dark_orange3]>[/dark_orange3] added assignee '{assignee}'")
    if label:
        console.print(f"\t[dark_orange3]>[/dark_orange3] added tags: '{label}'")
    if story_points:
        console.print(f"\t[dark_orange3]>[/dark_orange3] assigned {story_points} storypoints")

    if parent:
        cmd = "az boards work-item relation add "
        cmd += f"--id {work_item_id} "
        cmd += '--relation-type "parent" '
        cmd += f"--target-id {parent} "
        cmd += f'--org "{organization}" '
        run_command(cmd)
        console.print(f"\t[dark_orange3]>[/dark_orange3] added work item #{parent} as a parent")

    return work_item_id
