# Using environment variables in your workflow

!!! note ""
    See first the workflows for [starting work on a new issue](workflow_new_item.md) and [starting work on an existing issue](workflow_existing_item.md)

You can create more advanced workflows by using [environment variables](https://en.wikipedia.org/wiki/Environment_variable) to (temporarily) overwrite configuration values (see [config file](../reference/config_file.md)) or set certain command options (see the 'env var' value in the `--help` of different `doing` commands). 

!!! note ""
    You can also permanently overwrite command option defaults, see [Config File: overwriting command defaults](../reference/config_file.md#setting-command-defaults)

Below are some more advanced example workflows examples:

## Working with multiple iterations

You might want to add some issues to one of the upcoming sprints. Instead of changing the `.doing-cli-config.yml` file everytime, set an environment using `export` (make sure to [avoid `set`](https://unix.stackexchange.com/questions/71144/what-do-the-bash-builtins-set-and-export-do#:~:text=See%20help%20set%20%3A%20set%20is,mark%20a%20variable%20for%20export.))

```shell
export DOING_CONFIG_ITERATION='your_project\your_team\sprint1'
doing list
doing issue create "a new issue in the current sprint"

export DOING_CONFIG_ITERATION='your_project\your_team\sprint2'
doing list
doing issue create "a new issue in the next sprint"
```

## Setting a default work item type

Azure Devops has [different work item types](https://docs.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items?view=azure-devops&tabs=agile-process#wit) to help track different types of work. By default [`doing issue create`](../reference/manual/issue_create.md) and [`doing workon`](../reference/manual/workon.md) will create a work item of type *User Story*. You can set a different default work item type in the `.doing-cli-config.yml` [config](../reference/config_file.md) by specifying `default_workitem_type`. For example:

=== ".doing-cli-config.yml"

    ``` yaml
    # ... other required parameters ...
    default_workitem_type: 'Task'
    ```


You can also temporarily set a different default work item type using an [environment variable](https://en.wikipedia.org/wiki/Environment_variable). You can find which value to set by using `doing issue create --help` and `doing workon --help`.

=== "doing issue create"

    ```shell
    export DOING_CREATE_ISSUE_TYPE="Task"
    doing issue create "A task"
    ```

=== "doing workon"

    ```shell
    export DOING_WORKON_TYPE="Task"
    doing workon "A task"
    ```

## Setting default reviewers

You might have a project where all pull requests have the same set of reviewers. Instead of using the lengthy `doing pr create --reviewers 'email1@domain.com email2@domain.com'`, you can set a default set of reviewers in the `.doing-cli-config.yml` (see [config](../reference/config_file.md)) by specifying `default_reviewers`. For example:

=== ".doing-cli-config.yml"

    ```yaml
    # ... other required parameters ...
    default_reviewers: 'email1@domain.com email2@domain.com'
    ```

## Creating a set of tasks

You might want to quickly create a set of tasks for a user story. Instead of 

```shell
doing issue create "Thing 1" -t "Task" --parent 1234
doing issue create "Thing 2" -t "Task" --parent 1234
...
doing issue create "Thing 10" -t "Task" --parent 1234
```

You could use:

```shell
export DOING_CREATE_ISSUE_PARENT=1234
export DOING_CREATE_ISSUE_TYPE="Task"
doing issue create "Thing 1"
doing issue create "Thing 2"
...
doing issue create "Thing 10"
unset DOING_CREATE_ISSUE_PARENT
```
