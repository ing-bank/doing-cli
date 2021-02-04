import os
import click

from rich.console import Console

from doing.utils import get_repo_name, run_command
from doing.options import common_options

console = Console()


@click.group()
def open():
    """
    Quickly open certain links
    """
    pass


@open.command()
@common_options
def board(team, area, iteration, organization, project):
    """
    Open board view
    """
    console.print(f"Opening the Azure board. Make sure to filter on:")

    iteration_short = os.path.basename(iteration.replace("\\", "/"))
    area_short = os.path.basename(area.replace("\\", "/"))
    console.print(f"\titeration = '{iteration_short}'")
    console.print(f"\tarea = '{area_short}'")

    click.launch(f"{organization}/{project}/_boards/board/t/{team}")


@open.command()
@common_options
def sprint(team, area, iteration, organization, project):
    """
    Open current sprint view
    """
    iteration = os.path.basename(iteration.replace("\\", "/"))
    click.launch(f"{organization}/{project}/_sprints/taskboard/{team}/{iteration}")


@open.command()
@common_options
def repo(team, area, iteration, organization, project):
    """
    Open repo view
    """
    click.launch(f"{organization}/{project}/_git/{get_repo_name()}")


@open.command()
@common_options
def prs(team, area, iteration, organization, project):
    """
    Open active PRs for repository view
    """
    click.launch(
        f"{organization}/{project}/_git/{get_repo_name()}/pullrequests?_a=active"
    )


@open.command()
@common_options
def pipe(team, area, iteration, organization, project):
    """
    Open latest pipeline runs for repository view
    """

    repo_pipes = run_command(f"az pipelines list --repository {get_repo_name()}")
    if len(repo_pipes) == 0:
        console.print(f"{get_repo_name()} has no pipelines defined currently")
        return None

    pipeline_id = repo_pipes[0].get("id")
    click.launch(f"{organization}/{project}/_build?definitionId={pipeline_id}")


@open.command()
@common_options
@click.argument("issue_id")
def issue(team, area, iteration, organization, project, issue_id):
    """
    Open a specific ISSUE_ID.

    ISSUE_ID is the ID number of a work item.
    """
    click.launch(f"{organization}/{project}/_workitems/edit/{issue_id}")


@open.command()
@common_options
@click.argument("pullrequest_id")
def pr(team, area, iteration, organization, project, pullrequest_id):
    """
    Open a specific PULLREQUEST_ID.
    """
    click.launch(
        f"{organization}/{project}/_git/{get_repo_name()}/pullrequest/{pullrequest_id}"
    )


@open.command()
@common_options
@click.argument("branch_name")
def branch(team, area, iteration, organization, project, branch_name):
    """
    Open a specific BRANCH_NAME.
    """
    click.launch(
        f"{organization}/{project}/_git/{get_repo_name()}?version=GB{branch_name}"
    )
