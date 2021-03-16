# The .doing-cli-config.yml config file

`doing` searches for YAML config file named `.doing-cli-config.yml`. 

## Required parameters

The config must contain the following parameters (in lowercase):

| Parameter      | Description                          |
| ----------- | ------------------------------------ |
| `organization`       | Azure DevOps organization URL. You can quickly find the organization in your devops url, right after *https://dev.azure.com*. Example: *https://dev.azure.com/organization_name*.  |
| `project`       | Name of the project. You can quickly find the organization in a devops url, right after the organization url. Example: The project for *https://dev.azure.com/your_organization/your_project/...* is *your_project*. |
| `team`    | The name of your team. You can quickly find it when navigating on Azure Devops to Boards > Boards. Example: The team in *https://dev.azure.com/organization_name/project_name/_boards/board/t/my_team/Stories* is *my_team*. |
| `area`    | The area path assigned to work items. You can find it by going to a work item (Azure Devops > Boards > Work items) and copying the Area field. This corresponds to the work item field *System.AreaPath*. [More about area and iteration paths](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/about-areas-iterations?view=azure-devops). |
| `iteration`    | The iteration path assigned to work items. You can find it going by to a work item (Azure Devops > Boards > Work items) and copying the Iteration field. This corresponds to the work item field *System.IterationPath*. [More about area and iteration paths](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/about-areas-iterations?view=azure-devops). |

Example `.doing-cli-config.yml`:

```yaml
# .doing-cli-config.yml
organization: https://dev.azure.com/organization_name
project: project_name
team: team-name
area: organization_name\repo_name\area_name
iteration: organization_name\team_name\iteration_name
```

## Optional parameters

The config can also contain some optional parameters that are not required to be set:

| Optional Parameter      | Description |
| ----------------------- | ------------------------------------ |
| `default_workitem_type` | The default work item type used when creating work items. Should be one of "Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story". Defaults to "User Story" if not specified. 
| `default_reviewers` | The default reviewers assigned when creating pull requests. Space separated list of user emails (case sensitive). Find your own with `az ad signed-in-user show --query 'mail'`.
| `verbose_shell` | Set to 'true' to print every shell command `doing` runs for you in the background. Meant for debugging and interested developers.
| `user_aliases` | A list of user aliases that you can use when specifying reviewers or assignees.

Example `.doing-cli-config.yml`:

```yaml
# .doing-cli-config.yml
# ... other required parameters ...
default_workitem_type: Task
default_reviewers: 'john.doe@domain.com'
verbose_shell: False
user_aliases:
    john: John.Doe@company.com
    jane: Jane.Doe@email.net
```

## Using environment variables

You can overwrite the values set in `doing-cli-config.yml` using environment variables. Use the prefix `DOING_CONFIG_` followed by the parameter name in uppercase. 

Some examples: 

| Parameter      | Environment variable |
| -------------- | -------------------- |
| `team`         | `DOING_CONFIG_TEAM` |
| `iteration`    | `DOING_CONFIG_ITERATION` |
| `default_workitem_type`    | `DOING_CONFIG_DEFAULT_WORKITEM_TYPE` |

!!! note ""
    See also the [workflow using environment variables](../howto/workflow_envvars.md) for examples on how to use these in practice

