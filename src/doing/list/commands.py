import click

from doing.options import get_common_options
from doing.list._list import cmd_list


@click.command()
def list():
    """
    List issues related to the project.
    """
    cmd_list(**get_common_options())
