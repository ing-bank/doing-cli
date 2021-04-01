from doing.utils import get_repo_name, replace_user_aliases, run_command

from rich.table import Table
from rich.console import Console

console = Console()


def cmd_list_pr(assignee, label, limit, state, project, organization):
    """
    Command for listing pull requests.

    devops: https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/repos/pr?view=azure-cli-latest#ext_azure_devops_az_repos_pr_list
    github cli: https://cli.github.com/manual/gh_pr_list
    """  # noqa
    assignee = replace_user_aliases(assignee)

    query = "az repos pr list "
    query += f"--status '{state}' "
    query += f"--top {limit} "
    query += f"--org '{organization}' "
    query += f"--project '{project}' "
    query += f"--repository '{get_repo_name()}' "

    # Generate a jmespath.org query
    # Example:
    # az repos pr list --status active --query "[*].{title: title, pullRequestID: pullRequestID, status: status, labels:labels[*].name, reviewers: reviewers[*].uniqueName} | [*].labels" -o jsonc # noqa
    jmespath_query = "[*].{title: title, pullRequestId: pullRequestId, status: status, labels:labels[*].name, reviewers: reviewers[*].uniqueName}"  # noqa
    if assignee and label:
        jmespath_query += " | [? reviewers!=\`null\` && labels!=\`null\`]"  # noqa
        jmespath_query += f" | [?{generate_jmespath(assignee, 'reviewers')} && {generate_jmespath(label, 'labels')}]"
    elif assignee:
        jmespath_query += " | [? reviewers!=\`null\`]"  # noqa
        jmespath_query += f" | [?{generate_jmespath(assignee, 'reviewers')}]"
    elif label:
        jmespath_query += " | [? labels!=\`null\`]"  # noqa
        jmespath_query += f" | [?{generate_jmespath(label, 'labels')}]"

    query += f'--query "{jmespath_query}" '

    prs = run_command(query)

    table = Table(title=f"{state} Pull requests")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", justify="right", style="cyan", no_wrap=True)
    table.add_column("Reviewers", justify="right", style="cyan", no_wrap=True)
    table.add_column("Status", justify="right", style="cyan", no_wrap=True)

    for pr in prs:
        reviewers = ", ".join(pr.get("reviewers"))
        table.add_row(str(pr.get("pullRequestId")), pr.get("title"), reviewers, pr.get("status"))

    console.print(table)


def generate_jmespath(text: str, name_contains_array: str) -> str:
    """
    Helper function to generate a bit of jmespath.org code.

    Example:

    ```python
    reference = "contains(labels, 'hi') && contains(labels, 'there')"
    assert generate_jmespath("hi, there", 'labels') == reference

    assert generate_jmespath("hi", 'labels') == "contains(labels, 'hi')"
    ```
    """
    raw_items = text.split(",")
    items = []
    for item in raw_items:
        item = item.strip()
        item = f"contains({name_contains_array}, '{item}')"
        items.append(item)

    return " && ".join(items)
