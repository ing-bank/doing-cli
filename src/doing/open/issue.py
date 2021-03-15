import click
from doing.utils import get_config
from typing import Union


def open_issue(issue_id: Union[str, int]) -> None:
    """
    Open a specific ISSUE_ID.

    ISSUE_ID is the ID number of a work item. '#' prefix is allowed.
    """
    issue_id = str(issue_id).lstrip("#")

    project = get_config("project")
    organization = get_config("organization")

    click.launch(f"{organization}/{project}/_workitems/edit/{issue_id}")
