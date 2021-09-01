from doing.utils import run_command
from rich.console import Console
import os
import yaml
from urllib.parse import urlparse

console = Console()


def cmd_init(reference_issue: str = ""):
    """
    Create a .doing-cli-config file.

    Empty file if no reference_url is specified.

    Args:
        reference_issue: URL of work item to use as reference
    """
    if os.path.exists(".doing-cli-config.yml"):
        console.print("File '.doing-cli-config.yml' already exists.")
        return

    if not reference_issue:
        required_params = {
            "organization": "",
            "project": "",
            "team": "",
            "area": "",
            "iteration": "",
        }
        with open(".doing-cli-config.yml", "w") as file:
            file.write("# doing cli configuration file\n")
            file.write("# docs: https://github.com/ing-bank/doing-cli\n\n")
            yaml.dump(required_params, file)
            console.print("[dark_orange3]>[/dark_orange3] Created new .doing-cli-config.yml file")
            console.print("\t[dark_orange3]>[/dark_orange3] Please fill in required parameters.")
        return

    organization, project, item_id = parse_reference(reference_issue)
    organization = "https://dev.azure.com/" + organization

    required_params = {"organization": organization, "project": project}

    cmd = f"az boards work-item show --id {item_id} "
    cmd += f'--org "{organization}" '
    workitem = run_command(cmd)
    workitem = workitem.get("fields")
    assert workitem is not None
    required_params["team"] = workitem.get("System.IterationLevel2")
    required_params["area"] = workitem.get("System.AreaPath")
    required_params["iteration"] = workitem.get("System.IterationPath")

    with open(".doing-cli-config.yml", "w") as file:
        file.write("# doing cli configuration file\n")
        file.write("# docs: https://github.com/ing-bank/doing-cli\n\n")
        yaml.dump(required_params, file)
        console.print("[dark_orange3]>[/dark_orange3] Create new .doing-cli-config.yml file")
        console.print(
            f"\t[dark_orange3]>[/dark_orange3] Filled in required parameters using reference work item #{item_id}"
        )


def parse_reference(url):
    """
    Retrieve info from a url to a work item.

    Examples:

    ```python
    url = "https://dev.azure.com/MyOrganization/MyProject/_workitems/edit/73554"
    parse_reference() == ('MyOrganization','MyProject','73554')
    url = "https://dev.azure.com/MyOrganization/MyProject/_boards/board/t/"
    url += "MyTeam/Stories/?workitem=73554"
    parse_reference(url) == ('MyOrganization','MyProject','73554')
    ```

    Args:
        url (str): URL to work item on azure devops.

    Returns:
        tuple: organization, project and workitem_id
    """
    # remove trailing slash
    url = url.rstrip("/")

    # Parse the url
    parsed_url = urlparse(url)
    organization = parsed_url.path.split("/")[1]
    project = parsed_url.path.split("/")[2]

    # Support two different types of work item urls
    if parsed_url.query:
        item_id = parsed_url.query.lstrip("workitem=")
    else:
        item_id = parsed_url.path.split("/")[-1]

    return organization, project, item_id
