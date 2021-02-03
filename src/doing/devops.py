
import re
from doing.utils import run_command

def get_purpose_id(repo_name: str):
    matches = re.compile('P[0-9]+').findall(repo_name)
    if len(matches) == 0:
        raise AssertionError(f"Purpose ID not found in string '{repo_name}'")
    return matches[0]


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


