from doing.utils import run_command, get_repo_name, replace_user_aliases
from rich.table import Table
from rich.live import Live
from rich.progress import track
from rich.console import Console

from typing import List, Dict

console = Console()


def work_item_query(assignee: str, author: str, label: str, state: str, area: str, iteration: str):
    """
    Build query in wiql.

    # More on 'work item query language' syntax:
    # https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
    """
    # ensure using user aliases
    assignee = replace_user_aliases(assignee)
    author = replace_user_aliases(author)

    # Get all workitems
    query = "SELECT [System.Id],[System.Title],[System.AssignedTo],[System.WorkItemType],[System.State]"
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
    if state == "open":
        query += "AND [System.State] IN ('Active', 'New', 'To Do', 'Doing', 'Approved', 'Committed', 'Proposed') "
    if state == "closed":
        query += "AND [System.State] IN ('Resolved','Closed','Done') "
    if state == "all":
        query += "AND [System.State] <> 'Removed' "

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
) -> None:
    """
    Run `doing list` command.
    """
    # Get config settings
    assignee = replace_user_aliases(assignee)
    author = replace_user_aliases(author)

    query = work_item_query(assignee, author, label, state, area, iteration)
    work_items = run_command(f'az boards query --wiql "{query}" --org "{organization}" -p "{project}"')

    workitem_prs = {}  # type: Dict

    # Now for each work item we could get linked PRs
    # However, APIs requests are slow, and most work items don't have a PR.
    # Instead, we'll retrieve all active PRs and see which items are linked (less API calls)
    repo_name = get_repo_name()
    query = f"az repos pr list --repository '{repo_name}' --org '{organization}' -p '{project}' "
    query += "--status 'active' --query '[].pullRequestId'"
    active_pullrequest_ids = run_command(query)

    with Live(build_table(work_items, workitem_prs, iteration, False), refresh_per_second=4, console=console) as live:

        # For each PR, get linked work items. Note that "az repos pr list --include-links" does not work :(
        # Posted issue on bug here: https://github.com/Azure/azure-cli-extensions/issues/2946
        for pr_id in track(active_pullrequest_ids, description="Processing pull requests"):
            linked_workitems = run_command(
                f"az repos pr work-item list --id {pr_id} --query '[].id' --org '{organization}'", allow_verbose=False
            )
            for work_item in linked_workitems:
                if work_item in workitem_prs.keys():
                    workitem_prs[work_item].append(str(pr_id))
                else:
                    workitem_prs[work_item] = [str(pr_id)]

            live.update(build_table(work_items, workitem_prs, iteration, False))

        live.update(build_table(work_items, workitem_prs, iteration, last_build=True))


def build_table(work_items: List, workitem_prs: Dict, iteration: str, last_build: bool = False) -> Table:
    """
    Build rich table with open issues.
    """
    # Create our table
    table = Table(title=f"Work-items in current iteration {iteration}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", justify="right", style="cyan", no_wrap=True)
    table.add_column("Assignee", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
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

        # relations = run_command(f"az boards work-item relation show --id {item_id}",
        #     "--query \"relations[?attributes.name=='Pull Request' || attributes.name=='Branch'].attributes\"")
        # )
        # relations = run_command(
        #   f"az boards work-item show --id {item_id}",
        #   f"--query \"relations[?attributes.name=='Pull Request'].url\"") # example id 99035
        # )
        # item_linked_prs = []
        # for url in relations:
        #    item_linked_prs.append(url.lower().rpartition("%2f")[2])
        # item_linked_prs = ",".join(item_linked_prs)

        if int(item_id) in workitem_prs.keys():
            item_linked_prs = ",".join(workitem_prs[int(item_id)])
        elif last_build:
            item_linked_prs = ""
        else:
            item_linked_prs = "[bright_black]loading..[bright_black]"

        # TODO: If current git branch equal to branch ID name, different color.
        table.add_row(str(item_id), item_title, item_createdby, item_type, item_linked_prs)

    return table
