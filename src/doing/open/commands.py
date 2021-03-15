import os
import click

from urllib.parse import quote
from rich.console import Console

from doing.utils import get_repo_name, run_command
from doing.options import get_config
from doing.open.pr import open_pr
from doing.open.issue import open_issue


console = Console()


@click.group()
def open():
    """
    Quickly open certain links.
    """
    pass


@open.command()
def board():
    """
    Open board view.
    """
    iteration = get_config("iteration")
    area = get_config("area")
    team = get_config("team")
    project = get_config("project")
    organization = get_config("organization")

    console.print("Opening the Azure board. Make sure to filter on:")

    iteration_short = os.path.basename(iteration.replace("\\", "/"))
    area_short = os.path.basename(area.replace("\\", "/"))
    console.print(f"\titeration = '{iteration_short}'")
    console.print(f"\tarea = '{area_short}'")

    click.launch(f"{organization}/{project}/_boards/board/t/{team}")


@open.command()
def sprint():
    """
    Open current sprint view.
    """
    iteration = get_config("iteration")
    team = get_config("team")
    project = get_config("project")
    organization = get_config("organization")

    iteration = os.path.basename(iteration.replace("\\", "/"))
    click.launch(f"{organization}/{project}/_sprints/taskboard/{team}/{iteration}")


@open.command()
def repo():
    """
    Open repository view.
    """
    project = get_config("project")
    organization = get_config("organization")
    click.launch(f"{organization}/{project}/_git/{get_repo_name()}")


@open.command()
def prs():
    """
    Open active PRs for repository view.
    """
    project = get_config("project")
    organization = get_config("organization")
    click.launch(f"{organization}/{project}/_git/{get_repo_name()}/pullrequests?_a=active")


@open.command()
def pipe():
    """
    Open latest pipeline runs for repository view.
    """
    project = get_config("project")
    organization = get_config("organization")

    repo_pipes = run_command(f"az pipelines list --repository {get_repo_name()} --org '{organization}' -p '{project}'")
    if len(repo_pipes) == 0:
        console.print(f"{get_repo_name()} has no pipelines defined currently")
        return None

    pipeline_id = repo_pipes[0].get("id")
    click.launch(f"{organization}/{project}/_build?definitionId={pipeline_id}")


@open.command()
@click.argument("issue_id")
def issue(issue_id):
    """
    Open a specific ISSUE_ID.

    ISSUE_ID is the ID number of a work item. '#' prefix is allowed.
    """
    open_issue(issue_id)


@open.command()
def issues():
    """
    Open all active issues view.
    """
    iteration = get_config("iteration")
    area = get_config("area")
    project = get_config("project")
    organization = get_config("organization")

    # More on hyperlink query syntax:
    # https://docs.microsoft.com/en-us/azure/devops/boards/queries/define-query-hyperlink?view=azure-devops
    query = f"""
    SELECT [System.Id],[System.AssignedTo],[System.WorkItemType],[System.Title],[System.Parent],[System.CreatedDate]
    FROM WorkItems
    WHERE [System.AreaPath]='{area}'
    AND ([System.State] = 'Active' OR [System.State] = 'New')
    AND [System.IterationPath] UNDER '{iteration}'
    """

    click.launch(f"{organization}/{project}/_workitems/?_a=query&wiql={quote(query)}")


@open.command()
@click.argument("pullrequest_id")
def pr(pullrequest_id):
    """
    Open a specific PULLREQUEST_ID. '!' prefix is allowed.
    """
    open_pr(pullrequest_id)


@open.command()
@click.argument("branch_name")
def branch(branch_name):
    """
    Open a specific BRANCH_NAME.
    """
    project = get_config("project")
    organization = get_config("organization")

    click.launch(f"{organization}/{project}/_git/{get_repo_name()}?version=GB{branch_name}")
