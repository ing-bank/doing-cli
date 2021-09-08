import click
from urllib.parse import quote

from doing.options import get_common_options
from doing.list._list import cmd_list, work_item_query
from doing.utils import get_config


@click.command()
@click.option(
    "--assignee",
    "-a",
    required=False,
    default="",
    type=str,
    help="Filter by assignee (email address)",
    show_envvar=True,
)
@click.option(
    "--author",
    "-A",
    required=False,
    default="",
    type=str,
    help="Filter by author (email address)",
    show_envvar=True,
)
@click.option(
    "--label",
    "-l",
    required=False,
    default="",
    type=str,
    help="Filter by labels (tag). Comma separate multiple tags.",
    show_envvar=True,
)
@click.option(
    "--state",
    "-s",
    required=False,
    default="open",
    type=click.Choice(["open", "closed", "all"]),
    help="Filter by state. Defaults to 'open'",
    show_envvar=True,
)
@click.option(
    "--type",
    "-t",
    required=False,
    default="",
    type=str,
    help="Type of work item. E.g.: 'Bug', 'User Story', 'Task'",
    show_envvar=True,
)
@click.option(
    "--web/--no-web",
    "-w",
    required=False,
    default=False,
    type=bool,
    help="Open overview of issues in the web browser.",
    show_envvar=True,
)
@click.option(
    "--story_points",
    required=False,
    default="",
    type=str,
    help="Filter on number of story points. Use 'unassigned' to find empty. You can use the following inequality symbols as prefixes: '>', '>=', '<' and '<='.",  # noqa
    show_envvar=True,
)
@click.option(
    "--output_format",
    "-o",
    required=False,
    default="table",
    type=str,
    help="Output format. 'table' has a rich display, 'array' will return a string list with ID's.",
    show_envvar=True,
)
def list(assignee, author, label, state, type, web, story_points, output_format):
    """
    List issues related to the project.
    """
    if web:
        iteration = get_config("iteration")
        area = get_config("area")
        project = get_config("project")
        organization = get_config("organization")
        query = work_item_query(
            assignee=assignee,
            author=author,
            label=label,
            state=state,
            area=area,
            iteration=iteration,
            type=type,
            story_points=story_points,
        )
        click.launch(f"{organization}/{project}/_workitems/?_a=query&wiql={quote(query)}")
    else:
        cmd_list(
            assignee,
            author,
            label,
            state,
            type=type,
            story_points=story_points,
            output_format=output_format,
            **get_common_options(),
        )
