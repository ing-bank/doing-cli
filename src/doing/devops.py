from sys import stdout
from doing.utils import run_command
from rich.console import Console
console = Console()
import re



def get_repo_name():
    process = run_command("git remote get-url origin", return_process=True)
    if 'not a git' in process.stderr:
        console.print("Current directory (or parents) are not a git directory.")
        sys.exit(1)
    
    git_remote = process.stdout
    git_remote = "git@gitlab.com:ing_rpaa/training_material/training-advanced-python-alm-2020.git"
    repo_name = os.path.basename(git_remote)
    return repo_name


def get_purpose_id(repo_name):
    matches = re.compile('P[0-9]+').findall(repo_name)
    if len(matches) == 0:
        raise AssertionError(f"Purpose ID not found in string '{repo_name}'")
    return matches[0]
    
    

def find_area_path():
    
    

    # TODO extract purpose_id from the git remote.
    # TODO determine default repo
    
    # TODO determine potential area path
    
    # TODO: if the area from the git repo is not in the area children list, 
    # use the default area path, and explain to user the naming convention.
    areas = run_command("az boards area project list --path='\\IngOne\\Area\\P01908-Default' -o json")
    areas.keys()
    
    
    area_path = f"{project}\{default_repo}\{area}"

    
def get_iterations(team_id: str):
    """
    Example:
    
    team_id = "T01894-RiskandPricingAdvancedAna"
    get_iterations(team_id)
    """
    
    assert team_id.startswith("T")
    
    az_cmd = f"az boards iteration team list --team '{team_id}'"
    # From the team, find all iterations
    all_iterations = run_command(az_cmd)
    
    return [i.get('name') for i in all_iterations]