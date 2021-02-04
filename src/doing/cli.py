import click

from rich.console import Console

from doing.open import commands as open_group
from doing.create import commands as create_group
from doing.list import commands as list_command
from doing.workon import commands as workon_command

console = Console()


@click.group()
def cli():
    """
    Main entrypoint for doing CLI.

    Groups all main commands together.
    """
    pass


cli.add_command(open_group.open)
cli.add_command(create_group.create)
cli.add_command(list_command.list)
cli.add_command(workon_command.workon)
