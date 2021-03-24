import click
from doing.utils import get_config
from typing import Union


def cmd_open_issue(work_item_id: Union[str, int]) -> None:
    """
    Open a specific WORK_ITEM_ID.

    '#' prefix is allowed.
    """
    work_item_id = str(work_item_id).lstrip("#")

    project = get_config("project")
    organization = get_config("organization")

    click.launch(f"{organization}/{project}/_workitems/edit/{work_item_id}")
