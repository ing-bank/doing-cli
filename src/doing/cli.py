import click
from rich.console import Console
from rich.table import Table

from doing.commands import cmd_list
from doing.utils import run_command, get_config
from doing.devops import get_iterations


console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--team', required=True, type=str, default=get_config('team'), help="The code of the team in azure")
@click.option('--area', required=True, type=str, default=get_config('area'), help="The area code")
@click.option('--iteration', required=True, type=str, default=get_config('iteration'), help="The current iteration (sprint)")
@click.option('--organization', required=True, type=str, default=get_config('organization'), help="The organization in azure")
@click.option('--project', required=True, type=str, default=get_config('project'), help="The project in azure")
def list(team, area, iteration, organization, project):
    """
    List issues related to the project.
    """
    console.print(cmd_list(team, area, iteration, organization, project))



@cli.command()
@click.option('--team_id', required=True, type=str)
@click.option('--area', required=True, default="User Story", type=str)
@click.option('--item_type', required=True, default="User Story", type=click.Choice(['Bug','Epic','Feature','Issue','Task','Test Case','User Story']))
@click.option('--iteration', required=False, type=str)
@click.argument('issue', required=True, type=str)
def workon(team_id: str, 
           area: str,
           item_type: str,
           iteration: str,
           issue: str
           ):
    """
    Work on a new work item. Creates a new work item on Azure DevOps.
    
    ISSUE is the title to be used for the new work item.
    """
    # TODO: search for a config file (use python-dotenv )
    # write some method that gets all the input parameters.
    # note that also uses the environment variables
    # also set python-dotenv to not override any env vars.
    
    if not iteration:
        table = Table(title="Use --iteration to specify one of the following iterations:")
        table.add_column("Iteration", justify="right", style="cyan", no_wrap=True)
        table.add_column("Team", justify="right", style="cyan", no_wrap=True)
        for sprint in get_iterations(team_id):
            table.add_row(sprint, team_id)
        
        console.print(table)
    
    # Area
    # az boards work-item show --id 37222
    
    # assigned to, the uniquename is the emailaddress.
    # az boards work-item create --title "testing from tim" --type "User Story" --area 'IngOne\\P01908-Default' --iteration 'IngOne\\T01894-RiskandPricingAdvancedAna\\example_repository_sprint4' --assigned-to "tim.vink@ing.com"
    
    # https://dev.azure.com/IngEurCDaaS01/bbd257b1-b8a9-4fc6-b350-4ea7cc23c363/_apis/wit/workItems/49618
    # issue_id = response.get('url')
    # issue_url = f"https://dev.azure.com/IngEurCDaaS01/IngOne/_backlogs/backlog/T01894-RiskandPricingAdvancedAna/?workitem={issue_id}"
    
    # az boards work-item update --id 49618 --area 'IngOne\\P01908-Default\\example_repo'
    
    
    click.echo(f'Working on {issue}')
    
    console.print(f"[red]>[/red] Created issue #12345 '[cyan]{issue}[/cyan]'")


# @cli.command()
# @click.option('--vpn', required=False, default=False, type=bool, help="Use when connected to ING's VPN, sets REQUESTS_CA_BUNDLE env var.")
# def check(vpn):
#     """Checks config and connection."""
#     # TODO: check organization
#     # TODO: check project
#     # TODO: check inside a git repo
#     # TODO: determine team is set
#     # TODO: determine area path is set, otherwise show options
#     # TODO: determine iteration is set, otherwise show options
#     repos = run_command("az repos list")
#     console.print(f":white_check_mark: Connection to dev.azure.com is OK! You have access to [white]{len(repos)}[/white] repos.")
    


@cli.command()
def nothing():
    """Take a break."""
    console.print(":pile_of_poo:")

# @cli.command()
# def create_pr():
#     """
#     Create a new pull request for the current branch
#     """
#     pass
    # TODO: assert not on master branch
    # TODO: get issue number from branch namem, otherwise request.
    # ado create_pr --reviewer="daniel.timbrell@ing.com"
    # > created pull request to merge origin/12341-make-an-update-to-the-readme into master
    # > Added your own approval
    # > Added daniel.timbrell@ing.com as a reviewer



# az boards work-item create --title "Test from tim's command line" --type "User Story"
# az boards work-item show --id 37222 --organization https://dev.azure.com/IngEurCDaaS01
