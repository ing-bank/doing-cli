# Contributing

The `doing` tool is an acronym for **d**ev**o**ps-ing. The tool was built to help speed up development a data science teams using Azure Devops but more accustomed to a github/gitlab style workflow.

The tool uses modern python packages like [Click](https://click.palletsprojects.com/) and [rich](https://github.com/willmcgugan/rich) and is built on top of the [azure devops CLI](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/devops?view=azure-cli-latest).

## Documentation

We use [mkdocs](https://www.mkdocs.org) with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme. The docs are structured using the [divio documentation system](https://documentation.divio.com/). To view the docs locally:

```shell
pip install mkdocs-material
mkdocs serve
```

## Setup

- We use [pre-commit](https://pre-commit.com/). Setup using `pip install pre-commit` and then `pre-commit install`.
- For development, use an editable install: `pip install -e .`
- For publishing, use syntax: `git tag -a v0.1 -m "doing-cli v0.1" && git push origin v0.1`

## Technical background

We are basically wrapping the Azure Devops CLI.

- [Azure Devops commands reference](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/?view=azure-cli-latest&viewFallbackFrom=azure-devops)
- [Tips for using azure devops cli effectively](https://docs.microsoft.com/en-us/cli/azure/use-cli-effectively)

## Examples of using azure devops CLI

Here for reference. To view all shell commands being executed during a `doing` command, set `verbose_shell` to `True` in the `.doing-cli-config.yml` file (see [config reference](https://ing-bank.github.io/doing-cli/reference/config_file/)), or use environment variables: `export DOING_CONFIG_VERBOSE_SHELL=true`.

```bash
# Settings
organization={your organization url}
project={your project}
team={your team}
iteration={your iteration path}
area={your area path}
repo_name={name of your repo in azure devops}

# Configuration
az devops configure -l
az devops configure --defaults organization=$organization project=$project

# List areas for a team
az boards area team list --team=$team

# list work items
az boards work-item show --id 37222
az boards query --wiql "SELECT * FROM WorkItems WHERE ([System.State] = 'Active' OR [System.State] = 'New') AND [System.IterationPath] = '$iteration' AND [System.AreaPath] = '$area'"
# list relation types
az boards work-item relation list-type --query 'name'

# Update a work item
az boards work-item relation add --id 112011 --relation-type 'Branch' --target-id 6566809
# Artifact Link
az boards work-item relation add --id 112011 --relation-type 'Artifact Link' --target-id 6566809
# from ojbectID of a branch with
az repos ref list --repository $repo_name
az boards work-item relation add --id 112011 --target-id "<hash>" --relation-type "Artifact Link"

# List iterations
#https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards?view=azure-cli-latest#ext_azure_devops_az_boards_query
#https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
az boards iteration team show-backlog-iteration --team $team
az boards iteration project list --path '$organization/$project/$repo_name/sprintname'
az boards iteration project show --id '<hash>'
az boards iteration team list --team $team

# List remote branches
az repos ref list --repository $repo_name --query '[].name'

# Creating work items
az boards work-item create --title "Test from command line" --type "User Story" --area $area
az boards work-item create --title "testing" --type "User Story" --area $area --iteration $iteration --assigned-to "<your email>"

# Deleting work items
az boards work-item delete --id 112011

# Creating a branch
# 1) get object id of master branch:
az repos ref list --repository $repo_name --query "[?name=='refs/heads/master'].objectId"
# 2) get branch
az repos ref create --name "heads/<branch name>" --repository $repo_name --object-id "<hash>"

# Creating a PR
az repos pr create --repository $repo_name --work-items '112011' --draft --title "test pr" --source-branch "<branch name>" --transition-work-items 'true'
```


