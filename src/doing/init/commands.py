import click

from doing.init._init import cmd_init


@click.command()
@click.argument("reference_issue", required=False, default="")
def init(reference_issue):
    """
    Create a .doing-cli-config file.

    REFERENCE_ISSUE (optional): Find a representative work item and pass its url to automatically fill the config.
    """
    cmd_init(reference_issue)
