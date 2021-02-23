import click

from rich.console import Console

from doing.open import commands as open_group
from doing.create import commands as create_group
from doing.list import commands as list_command
from doing.workon import commands as workon_command

console = Console()


@click.group(
    context_settings={"auto_envvar_prefix": "DOING", "default_map": {"issue": {"show_envvar": True}}},
)
def cli():
    """
    CLI for repository/issue workflow on Azure Devops.
    """
    pass


cli.add_command(open_group.open)
cli.add_command(create_group.create)
cli.add_command(list_command.list)
cli.add_command(workon_command.workon)
