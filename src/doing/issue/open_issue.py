from __future__ import annotations

import click

from doing.utils import get_config


def cmd_open_issue(work_item_id: str | int) -> None:
    """
    Open a specific WORK_ITEM_ID.

    '#' prefix is allowed.
    """
    work_item_id = str(work_item_id).lstrip("#")

    project = get_config("project")
    organization = get_config("organization")

    click.launch(f"{organization}/{project}/_workitems/edit/{work_item_id}")
