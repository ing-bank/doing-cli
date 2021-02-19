import click

from doing.utils import get_config


def get_common_options():
    """
    Retrieve common config options.

    Retrieves set of config settings from config file that are used in every command.
    """
    return {
        "team": get_config("team"),
        "area": get_config("area"),
        "iteration": get_config("iteration"),
        "organization": get_config("organization"),
        "project": get_config("project"),
    }


def common_options(function):
    """
    Custom decorator to avoid repeating commonly used options.

    To be used in Click commands.
    """
    function = click.option(
        "--team",
        required=True,
        type=str,
        default=lambda: get_config("team"),
        help="The code of the team in azure",
    )(function)
    function = click.option(
        "--area",
        required=True,
        type=str,
        default=lambda: get_config("area"),
        help="The area code",
    )(function)
    function = click.option(
        "--iteration",
        required=True,
        type=str,
        default=lambda: get_config("iteration"),
        help="The current iteration (sprint)",
    )(function)
    function = click.option(
        "--organization",
        required=True,
        type=str,
        default=lambda: get_config("organization"),
        help="The organization in azure",
    )(function)
    function = click.option(
        "--project",
        required=True,
        type=str,
        default=lambda: get_config("project"),
        help="The project in azure",
    )(function)
    return function
