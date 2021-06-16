# Using environment variables

`doing` supports the use of [environment variables](https://en.wikipedia.org/wiki/Environment_variable) to overwrite and set options.

Set an environment using `export` and [avoid using `set`](https://unix.stackexchange.com/questions/71144/what-do-the-bash-builtins-set-and-export-do#:~:text=See%20help%20set%20%3A%20set%20is,mark%20a%20variable%20for%20export.))

## Overwriting commands default options

You can overwrite any command option using the `env var` name specified when you type `--help`. For example, `doing issue create --help` has an option named `DOING_ISSUE_CREATE_LABEL` (in the help, listed as  `[env var: DOING_ISSUE_CREATE_LABEL]`).

Some examples:

=== "doing issue create"

    ```shell
    export DOING_ISSUE_CREATE_TYPE="Task"
    doing issue create "A task"
    ```

=== "doing workon"

    ```shell
    export DOING_WORKON_TYPE="Task"
    doing workon "A task"
    ```

=== "doing list"

    ```shell
    export DOING_CONFIG_ITERATION='your_project\your_team\sprint1'
    doing list
    doing issue create "a new issue in the current sprint"

    export DOING_CONFIG_ITERATION='your_project\your_team\sprint2'
    doing list
    doing issue create "a new issue in the next sprint"

    unset DOING_CONFIG_ITERATION
    ```


!!! Note "Priority of settings"

    `doing` uses the following order of priority:

    1. Options set directly on the command list, f.e.: `doing list --state all`
    1. Options set as environment variable, f.e.: `export DOING_LIST_STATE=all`
    1. Options set in the `.doing-cli-config.yml` file, f.e.: setting `DOING_LIST_STATE: all` under `defaults`


## Overwriting config file parameters

You can overwrite the values set in `doing-cli-config.yml` using environment variables. Use the prefix `DOING_CONFIG_` followed by the parameter name in uppercase.
Any config set as environment variable will overwrite config parameters set in the config file.

Some examples: 

| Parameter      | Environment variable |
| -------------- | -------------------- |
| `team`         | `DOING_CONFIG_TEAM` |
| `iteration`    | `DOING_CONFIG_ITERATION` |
| `default_workitem_type`    | `DOING_CONFIG_DEFAULT_WORKITEM_TYPE` |

```python
# Example usage
export DOING_CONFIG_VERBOSE_SHELL=True
doing list
```

