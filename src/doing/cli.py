import click
import collections

from rich.console import Console

from doing.open import commands as open_group
from doing.create import commands as create_group
from doing.list import commands as list_command
from doing.workon import commands as workon_command
from doing.init import commands as init_command
from doing.close import commands as close_command

console = Console()


class OrderedGroup(click.Group):
    """
    List click commands in order added.

    Credits: https://stackoverflow.com/a/58323807/5525118
    """

    def __init__(self, name=None, commands=None, **attrs):
        """
        Init.
        """
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        """
        List commands.
        """
        return self.commands


@click.group(
    context_settings={"auto_envvar_prefix": "DOING"},
    cls=OrderedGroup,
)
def cli():
    """
    CLI for repository/issue workflow on Azure Devops.
    """
    pass


cli.add_command(init_command.init)
cli.add_command(create_group.create)
cli.add_command(list_command.list)
cli.add_command(open_group.open)
cli.add_command(workon_command.workon)
cli.add_command(close_command.close)
