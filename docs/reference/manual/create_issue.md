# doing create issue

Create an issue.

```shell
doing create issue [flags]
```

## Example usage

```shell
doing create issue "I found a bug"
doing create issue "I found a bug" --mine
doing create issue "I found a bug" -a "john.doe@company.com"
doing create issue "I found a bug" -a @me
doing create issue "I found a bug" --type "Bug"
doing create issue "This is a task" --type "Task" --parent 12345 
doing create issue "This is a task" --web
```

## Options

```nohighlight
{{ shell_out('doing create issue --help') }}
```

## In use

Setting default_reviewers and default_workitem_type in the config file:

=== "Bash"

    ```shell
    doing create 'fixing a small typo'
    # > Created issue #146545 'fixing a small typo' (Task)
    #     > added area-path '{your area path}'
    #     > added iteration-path '{your iteration path}'
    #     > added assignee 'john.doe@domain.com'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    default_workitem_type: Task
    default_reviewers: 'john.doe@domain.com'
    ```

Overriding the existing config using environment variables:

=== "Bash"

    ```shell
    export DOING_CREATE_ISSUE_ASSIGNED_TO='jane@company.com'
    doing create 'fixing a small typo'
    # > Created issue #146545 'fixing a small typo' (User Story)
    #     > added area-path '{your area path}'
    #     > added iteration-path '{your iteration path}'
    #     > added assignee 'jane@company.com'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    default_reviewers: 'john.doe@domain.com'
    ```


Using user_aliases set in the [config file](../config_file.md):

=== "Shell"

    ```shell
    doing create 'fixing a small typo' -a john
    # > Created issue #146545 'fixing a small typo' (User Story)
    #     > added area-path '{your area path}'
    #     > added iteration-path '{your iteration path}'
    #     > added assignee 'john.doe@domain.com'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    user_aliases:
        john: John.Doe@company.com
        jane: Jane.Doe@email.net
    ```
