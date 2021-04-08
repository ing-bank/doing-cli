import click
import collections
import os

from rich.console import Console

from doing.pr import commands as pr_group
from doing.issue import commands as issue_group
from doing.open import commands as open_group
from doing.list import commands as list_command
from doing.utils import get_config
from doing.workon import commands as workon_command
from doing.init import commands as init_command
from doing import __version__

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
@click.version_option(__version__, prog_name="doing-cli")
def cli():
    """
    CLI for repository/issue workflow on Azure Devops.
    """
    # Set doing default as environment variables
    defaults = get_config("defaults", fallback="")
    if defaults:
        for setting, default in defaults.items():
            if setting not in os.environ:
                os.environ[setting] = default
            else:
                if os.environ[setting] != default:
                    console.print(
                        f"Warning: Trying to set {setting} to '{default}' (specified in .doing-ing-config.yml)"
                    )
                    console.print(
                        f"\tbut {setting} has already been set to '{os.environ[setting]}' in the environment variables."
                    )


cli.add_command(init_command.init)
cli.add_command(list_command.list)
cli.add_command(issue_group.issue)
cli.add_command(pr_group.pr)
cli.add_command(workon_command.workon)
cli.add_command(open_group.open)
