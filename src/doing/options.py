import click

from doing.utils import get_config


def common_options(function):
    """
    Custom decorator to avoid repeating commonly used options.
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
