# The .doing-cli-config.yml config file

When running a command `doing` searches for YAML config file named `.doing-cli-config.yml`. This file is required and used to link issues to a repository (see [discussion](../discussion/oneproject_setup.md)).

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
organization: 'https://dev.azure.com/organization_name'
project: 'project_name'
team: 'team-name'
area: 'organization_name\repo_name\area_name'
iteration: 'organization_name\team_name\iteration_name'
```

## Optional parameters

The config can also contain some optional parameters that are not required to be set:

| Optional Parameter      | Description |
| ----------------------- | ------------------------------------ |
| `default_workitem_type` | The default work item type used when creating work items. Should be one of "Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story". Defaults to "User Story" if not specified. 
| `verbose_shell` | Set to 'true' to print every shell command `doing` runs for you in the background. Meant for debugging and interested developers.
| `user_aliases` | A list of user aliases that you can use when specifying reviewers or assignees. Note that the `@me` alias is always available.
| `default_reviewers` | The default reviewers assigned when creating pull requests. Space separated list of user emails (case sensitive). Find your own with `az ad signed-in-user show --query 'mail'`.
| `defaults` | Allows you to overwrite defaults of command options. See explanation below.

Example `.doing-cli-config.yml`:

```yaml
# .doing-cli-config.yml
# ... other required parameters ...
default_workitem_type: 'Task'
verbose_shell: False
user_aliases:
    john: 'John.Doe@company.com'
    jane: 'Jane.Doe@email.net'
default_reviewers: 'john.doe@domain.com'
```

### Setting `default_workitem_type`

Azure Devops has [different work item types](https://docs.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items?view=azure-devops&tabs=agile-process#wit) to help track different types of work. By default [`doing issue create`](../reference/manual/issue_create.md) and [`doing workon`](../reference/manual/workon.md) will create a work item of type *User Story*. You can set a different default work item type in the `.doing-cli-config.yml` [config](../config/config_file.md) by specifying `default_workitem_type`. For example:


```yaml
# .doing-cli-config.yml
default_workitem_type: 'Task'
```

### Setting `user_aliases`

Anywhere you can specify `assignee` or `reviewer`, you can fill in user email adress. These are case-sensitive, and lenghty, so you can also choose to define a set of user aliases:

```yaml
# .doing-cli-config.yml
user_aliases:
    john: 'John.Doe@company.com'
    jane: 'Jane.Doe@email.net'
```

Now you can use aliases like:

```bash
doing issue create --assignee "john"
```

### Setting `default_reviewers`

You might have a project where all pull requests have the same set of reviewers. Instead of using the lengthy `doing pr create --reviewers 'email1@domain.com email2@domain.com'`, you can set a default set of reviewers in the `.doing-cli-config.yml` (see [config](../config/config_file.md)) by specifying `default_reviewers`. For example:

```yaml
# .doing-cli-config.yml
default_reviewers: 'email1@domain.com email2@domain.com'
```

You can also use the aliases specified in `user_aliases` to specify the `default_reviewers`.

### Setting `defaults`

For every `doing` command, you can use `--help` to see any default for an option (if applicable), as well as the name (in capital letters) of that option, listed after 'env var'. For example, `doing issue create --help` has an option named `DOING_ISSUE_CREATE_LABEL` (in the help, listed as  `[env var: DOING_ISSUE_CREATE_LABEL]`).

You can use those variable names to set different defaults for commands in your `.doing-cli-config.yml` file.

Here's an example `.doing-cli-config.yml`:

```yaml
# .doing-cli-config.yml
# ... other settings ...
defaults:
    DOING_LIST_STATE: all
    DOING_WORKON_TYPE: Bug
    DOING_LIST_LABEL: "some_tag another_tag something"
```

This is a great way to set defaults for your entire team. If you would like to set personal defaults you can choose to [use environment variables](env_config.md) instead.

!!! Note "Priority of settings"

    `doing` uses the following order of priority:

    1. Options set directly on the command list, f.e.: `doing list --state all`
    1. Options set as environment variable, f.e.: `export DOING_LIST_STATE=all`
    1. Options set in the `.doing-cli-config.yml` file, f.e.: setting `DOING_LIST_STATE: all` under `defaults`


