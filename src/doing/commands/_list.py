from doing.utils import run_command
from clumper import Clumper
from rich.table import Table

def cmd_list(team: str, area: str, iteration: str, organization: str, project: str):


    # First, get list of all iterations from the team
    cmd = f"az boards iteration team list --team {team}"
    iterations = run_command(cmd)

    # Then find the unique ID of the current iteration
    iteration_id = (Clumper(iterations)
        .keep(lambda d: d['name'] == iteration)
        .unique('id')    
    )[0]

    # Get all the work items in an iteration:
    cmd = f"az boards iteration team list-work-items --id '{iteration_id}' --team {team}"
    work_items = run_command(cmd)
    work_items = [d['target']['id'] for d in work_items.get('workItemRelations')]

    # TODO, filter on only open users / tasks?
    # TODO, we should use the MUCH faster `az boards query`
    breakpoint()
    https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards?view=azure-cli-latest#ext_azure_devops_az_boards_query
    https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
    # Create our table
    table = Table(title=f"Work-items in current iteration {iteration}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", justify="right", style="cyan", no_wrap=True)
    table.add_column("Created by", justify="right", style="cyan", no_wrap=True) 
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Link", justify="right", style="cyan", no_wrap=True)

    for work_item_id in work_items:

        item = run_command(f"az boards work-item show --id {work_item_id} --fields 'System.Title,System.CreatedBy,System.WorkItemType'")
        breakpoint()
        item = item.get('fields')

        item_title = item.get('System.Title')
        item_createdby = item.get("System.CreatedBy").get('displayName')
        item_type = item.get('System.WorkItemType')
        item_link = f"https://dev.azure.com/IngEurCDaaS01/IngOne/_workitems/edit/{work_item_id}"

        table.add_row(str(work_item_id), item_title, item_createdby, item_type, item_link)


    return table


