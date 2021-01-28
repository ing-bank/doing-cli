
from os import umask
from doing.utils import run_command

from rich.console import Console
console = Console()

def cmd_workon(title:str, type:str, assigned_to:str, team: str, area: str, iteration: str, organization: str, project: str):
    """
    az CLI:
    https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards/work-item?view=azure-cli-latest#ext_azure_devops_az_boards_work_item_create
    """

    cmd = f"az boards work-item create "
    cmd += f"--title '{title}' --type '{type}' --assigned-to {assigned_to} "
    cmd += f"--area '{area}' --iteration '{iteration}' --project '{project}' --organization '{organization}'"

    print(cmd)
    print()
    issue = run_command(cmd)


    issue_id = issue.get('id')
    issue_url = f"{organization}/{project}/_workitems/edit/{issue_id}"
    
    console.print(f"[red]>[/red] Created issue #{issue_id} '[cyan]{title}[/cyan]'")
    console.print(f"\t[red]>[/red] added area-path '{area}'")
    console.print(f"\t[red]>[/red] added iteration-path '{iteration}'")
    console.print(f"\t[red]>[/red] added assignee '{assigned_to}'")

    # az boards work-item update --id 49618 --area 'IngOne\\P01908-Default\\example_repo'

    # Link a branch
    # Update a work item

    # using relation-type is 
    # https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards/work-item/relation?view=azure-cli-latest#ext_azure_devops_az_boards_work_item_relation_add
    
    # https://docs.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference?view=azure-devops

    #az boards work-item relation add --id 112011 --relation-type 'Branch' --target-id 6566809

    # list relation types
    # az boards work-item relation list-type --query 'name'
    # Artifact Link"
    #az boards work-item relation add --id 112011 --relation-type 'Artifact Link' --target-id 6566809
    # from ojbectID of a branch with 
    # az repos ref list --repository P01908-taco
    #az boards work-item relation add --id 112011 --target-id "475bdee470cab59ccd1d8e25b29ed7f9285504b2" --relation-type "Artifact Link"


    # Maybe, instead of adding branches to an issue
    # Add a Pr directly to a work item:
    # az repos pr work-item add --id --work-items
    # Or create + add work item in one go
    # --draft is not needed (parameter?)
    # az repos pr create --repository 'P01908-taco' --work-items '112011' --draft --title "test pr from tim" --source-branch "testbranchtim" --transition-work-items 'true'

    # Still.. branch is not linked to work item :(
    # update idea:
    # leave out the entire idea of linked branches.
    # eitehr an issue has no PR yet, or a linked PR
    # add `doing create pr issue 1234
    # 
    # az repos pr list --repository 'P01908-taco' --include-links

    breakpoint()
    

   # Todo:
   #  option to checkout locally
   # az repos pr checkout --id  
    
    
    

    


# Work on something *new*
# ado workon "make an update to the readme"
# > created new work-item #12341 "make an update to the readme"
#    > added area-path "your-repo"
#    > added 'your name' as assignee
# > created & linked new branch origin/12341-make-an-update-to-the-readme
# > To work on the issue, use the following commands:
#    > git fetch --all
#    > git checkout 12341-make-an-update-to-the-readme
#    > Tip: lazy? next time use `doing workon -g`

