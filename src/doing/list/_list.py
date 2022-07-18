from __future__ import annotations

import datetime
from datetime import timezone

import timeago
from rich.console import Console
from rich.live import Live
from rich.progress import track
from rich.table import Table

from doing.utils import get_config, get_repo_name, replace_user_aliases, run_command, validate_work_item_type

console = Console()


def work_item_query(
    assignee: str,
    author: str,
    label: str,
    state: str,
    area: str,
    iteration: str,
    work_item_type: str,
    story_points: str,
):
    """Build query in wiql.

    # More on 'work item query language' syntax:
    # https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
    """
    # ensure using user aliases
    assignee = replace_user_aliases(assignee)
    author = replace_user_aliases(author)

    # Get all workitems
    query = "SELECT [System.Id],[System.Title],[System.AssignedTo],"
    query += "[System.WorkItemType],[System.State],[System.CreatedDate], [System.State] "
    query += f"FROM WorkItems WHERE [System.AreaPath] = '{area}' "
    # Filter on iteration. Note we use UNDER so that user can choose to provide teams path for all sprints.
    query += f"AND [System.IterationPath] UNDER '{iteration}' "

    if assignee:
        query += f"AND [System.AssignedTo] = '{assignee}' "

    if author:
        query += f"AND [System.CreatedBy] = '{author}' "

    if label:
        for lab in label.split(","):
            query += f"AND [System.Tags] Contains '{lab.strip()}' "

    if state:
        custom_states = get_config("custom_states", {})
        if state in custom_states.keys():
            if type(custom_states[state]) is not list:
                custom_states[state] = [custom_states[state]]
            state_list = ",".join([f"'{x}'" for x in custom_states[state]])
            query += f"AND [System.State] IN ({state_list}) "
        elif state == "open":
            query += "AND [System.State] NOT IN ('Resolved','Closed','Done','Removed') "
        elif state == "closed":
            query += "AND [System.State] IN ('Resolved','Closed','Done') "
        elif state == "all":
            query += "AND [System.State] <> 'Removed' "
        elif state.startswith("'") and state.endswith("'"):
            query += f"AND [System.State] = {state} "
        else:
            raise ValueError(
                f"Invalid state: '{state}'. State should be:\n"
                "- one of the doing-cli default states: 'open', 'closed', 'all'\n"
                "- a custom state defined under 'custom_states' in the .doing-cli.config.yml file\n"
                "- a state available in this team, between quotes, e.g. \"'Active'\""
            )

    if work_item_type:
        validate_work_item_type(work_item_type)
        query += f"AND [System.WorkItemType] = '{work_item_type}' "

    if story_points:
        if story_points == "unassigned":
            query += "AND [Microsoft.VSTS.Scheduling.StoryPoints] = '' "
        elif story_points.startswith("<="):
            story_points = story_points.lstrip("<=")
            query += f"AND [Microsoft.VSTS.Scheduling.StoryPoints] <= '{story_points}' "
        elif story_points.startswith(">="):
            story_points = story_points.lstrip(">=")
            query += f"AND [Microsoft.VSTS.Scheduling.StoryPoints] >= '{story_points}' "
        elif story_points.startswith(">"):
            story_points = story_points.lstrip(">")
            query += f"AND [Microsoft.VSTS.Scheduling.StoryPoints] > '{story_points}' "
        elif story_points.startswith("<"):
            story_points = story_points.lstrip("<")
            query += f"AND [Microsoft.VSTS.Scheduling.StoryPoints] < '{story_points}' "
        else:
            query += f"AND [Microsoft.VSTS.Scheduling.StoryPoints] = '{story_points}' "

    # Ordering of results
    query += "ORDER BY [System.CreatedDate] asc"

    return query


def cmd_list(
    assignee: str,
    author: str,
    label: str,
    state: str,
    team: str,
    area: str,
    iteration: str,
    organization: str,
    project: str,
    work_item_type: str,
    show_state: bool,
    story_points: str = "",
    output_format: str = "table",
) -> None:
    """Run `doing list` command."""
    # Get config settings
    assignee = replace_user_aliases(assignee)
    author = replace_user_aliases(author)

    query = work_item_query(assignee, author, label, state, area, iteration, work_item_type, story_points)
    work_items = run_command(f'az boards query --wiql "{query}" --org "{organization}" -p "{project}"')

    if len(work_items) == 0:
        msg = f"[dark_orange3]>[/dark_orange3] No issues in sprint '{iteration}' given filters used"
        console.print(msg)
        return

    if output_format == "array":
        wi_array = [str(x.get("id")) for x in work_items]
        console.print(" ".join(wi_array))
        return

    workitem_prs: dict = {}

    # Now for each work item we could get linked PRs
    # However, APIs requests are slow, and most work items don't have a PR.
    # Instead, we'll retrieve all active PRs and see which items are linked (less API calls)
    repo_name = get_repo_name()
    query = f'az repos pr list --repository "{repo_name}" --org "{organization}" -p "{project}" '
    query += '--status active --query "[].pullRequestId"'
    active_pullrequest_ids = run_command(query)

    with Live(
        build_table(
            work_items=work_items,
            workitem_prs=workitem_prs,
            iteration=iteration,
            last_build=False,
            show_state=show_state,
        ),
        refresh_per_second=4,
        console=console,
    ) as live:

        # For each PR, get linked work items. Note that "az repos pr list --include-links" does not work :(
        # Posted issue on bug here: https://github.com/Azure/azure-cli-extensions/issues/2946
        for pr_id in track(active_pullrequest_ids, description="Processing pull requests", transient=False):
            linked_workitems = run_command(
                f'az repos pr work-item list --id {pr_id} --query "[].id" --org "{organization}"', allow_verbose=False
            )
            for work_item in linked_workitems:
                if work_item in workitem_prs.keys():
                    workitem_prs[work_item].append(str(pr_id))
                else:
                    workitem_prs[work_item] = [str(pr_id)]

            live.update(
                build_table(
                    work_items=work_items,
                    workitem_prs=workitem_prs,
                    iteration=iteration,
                    last_build=False,
                    show_state=show_state,
                )
            )

        live.update(
            build_table(
                work_items=work_items,
                workitem_prs=workitem_prs,
                iteration=iteration,
                last_build=False,
                show_state=show_state,
            )
        )


def build_table(
    work_items: list, workitem_prs: dict, iteration: str, show_state: bool, last_build: bool = False
) -> Table:
    """Build rich table with open issues."""
    # Create our table
    table = Table(title=f"Work-items in current iteration {iteration}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", justify="left", style="cyan", no_wrap=False)
    table.add_column("Assignee", justify="left", style="cyan", no_wrap=False)
    table.add_column("Type", justify="left", style="cyan", no_wrap=True)
    if show_state:
        table.add_column("State", justify="right", style="cyan", no_wrap=True)
    table.add_column("Created", justify="right", style="cyan", no_wrap=True)
    table.add_column("PRs", justify="right", style="cyan", no_wrap=True)

    for item in work_items:
        # item = run_command(f"az boards work-item show --id {work_item_id}",
        # "--fields 'System.Title,System.CreatedBy,System.WorkItemType'")
        # )

        fields = item.get("fields")
        item_id = fields.get("System.Id")
        item_title = fields.get("System.Title")
        item_createdby = fields.get("System.AssignedTo", {}).get("displayName", "")
        item_type = fields.get("System.WorkItemType")
        item_state = fields.get("System.State")

        # For example:
        # '2020-11-17T13:33:32.463Z'
        # details: https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops#date-time-pattern # noqa
        item_datetime = fields.get("System.CreatedDate")
        try:
            item_datetime = datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # sometimes milliseconds is missing from the timestamp, try without
            item_datetime = datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%SZ")
        item_datetime = item_datetime.replace(tzinfo=timezone.utc)
        now = datetime.datetime.now(timezone.utc)
        item_datetime = timeago.format(item_datetime, now)

        if int(item_id) in workitem_prs.keys():
            item_linked_prs = ",".join(workitem_prs[int(item_id)])
        elif last_build:
            item_linked_prs = ""
        else:
            item_linked_prs = "[bright_black]loading..[bright_black]"

        # TODO: If current git branch equal to branch ID name, different color.
        row = [str(item_id), item_title, item_createdby, item_type, item_datetime, item_linked_prs]
        if show_state:
            row.insert(4, item_state)
        table.add_row(*row)

    return table
