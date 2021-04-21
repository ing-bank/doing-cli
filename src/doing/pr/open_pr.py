import click
from doing.utils import get_config
from doing.utils import get_repo_name
from typing import Union


def cmd_open_pr(pullrequest_id: Union[str, int]) -> None:
    """
    Open a specific PULLREQUEST_ID. '!' prefix is allowed.
    """
    pullrequest_id = str(pullrequest_id).lstrip("!").strip()

    project = get_config("project")
    organization = get_config("organization")

    click.launch(f"{organization}/{project}/_git/{get_repo_name()}/pullrequest/{pullrequest_id}")
