import click

from doing.options import common_options
from doing.list._list import cmd_list


@click.command()
@common_options
def list(team, area, iteration, organization, project):
    """
    List issues related to the project.
    """
    cmd_list(team, area, iteration, organization, project)
