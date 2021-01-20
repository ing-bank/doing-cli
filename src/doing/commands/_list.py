from doing.utils import run_command, get_repo_name
from rich.table import Table
from rich.live import Live

def cmd_list(team: str, area: str, iteration: str, organization: str, project: str):


    query = "SELECT [System.Id],[System.Title],[System.CreatedBy],[System.WorkItemType] FROM WorkItems WHERE ([System.State] = 'Active' OR [System.State] = 'New') "

    # Filter on iteration. Note we use UNDER so that user can choose to provide teams path for all sprints.
    query += f"AND [System.IterationPath] UNDER '{iteration}' " # Example: IngOne\T01894-RiskandPricingAdvancedAna\taco_sprint5
    query += f"AND [System.AreaPath] = '{area}' "

    work_items = run_command(f"az boards query --wiql \"{query}\"")

    # remote_branches_and_prs = run_command(f"az repos ref list --repository {get_repo_name()} --query '[].name'")

    # Local branches?
    
    
    # TODO: add rows dynamically.
    # Create our table
    table = Table(title=f"Work-items in current iteration {iteration}")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", justify="right", style="cyan", no_wrap=True)
    table.add_column("Created by", justify="right", style="cyan", no_wrap=True) 
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Linked Branches", justify="right", style="cyan", no_wrap=True)
    table.add_column("Linked PRs", justify="right", style="cyan", no_wrap=True)

    with Live(table, refresh_per_second=4):
        for item in work_items:
            # item = run_command(f"az boards work-item show --id {work_item_id} --fields 'System.Title,System.CreatedBy,System.WorkItemType'")
            
            fields = item.get('fields')
            item_id = fields.get('System.Id')
            item_title = fields.get('System.Title')
            item_createdby = fields.get("System.CreatedBy").get('displayName')
            item_type = fields.get('System.WorkItemType')

            # relations = run_command(f"az boards work-item relation show --id {item_id} --query \"relations[?attributes.name=='Pull Request' || attributes.name=='Branch'].attributes\"")
            relations = run_command(f"az boards work-item show --id {item_id} --expand 'relations' --query 'relations'") # example id 99035
            
            item_linked_branches = []
            item_linked_prs = []
            for rel in relations:
                if rel.get('attributes',[]).get('name') == "Branch":
                    # Note the branch name is encoded in the URL
                    item_linked_branches.append(rel.get('url').rpartition("%2FGB")[2])

                if rel.get('attributes',[]).get('name') == "Pull Request": 
                    item_linked_prs.append(rel.get('url').rpartition("%2F")[2])

            item_linked_branches = ",".join(item_linked_branches)
            item_linked_prs = ",".join(item_linked_prs)
            
            # TODO: If current git branch equal to branch ID name, different color.
            table.add_row(str(item_id), item_title, item_createdby, item_type, item_linked_branches, item_linked_prs)



