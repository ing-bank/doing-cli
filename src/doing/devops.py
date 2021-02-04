from doing.utils import run_command


def get_iterations(team_id: str):
    """
    Find iterations belonging to a certain team.

    Example:

    ```python
    team_id = "T01894-RiskandPricingAdvancedAna"
    get_iterations(team_id)
    ```
    """
    assert team_id.startswith("T")

    az_cmd = f"az boards iteration team list --team '{team_id}'"
    # From the team, find all iterations
    all_iterations = run_command(az_cmd)

    return [i.get("name") for i in all_iterations]
