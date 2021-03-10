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
doing create issue "I found a bug" --type "Bug"
doing create issue "This is a task" --type "Task" --parent 12345 
```

## Options

```nohighlight
{{ shell_out('doing create issue --help') }}
```

## In use


=== "Bash"

    ```shell
    doing create 'fixing a small typo'
    # > Created issue #146545 'fixing a small typo'
    #     > added area-path '{your area path}'
    #     > added iteration-path '{your iteration path}'
    #     > added assignee 'john.doe@domain.com'
    ```

    Or, overriding the existing config using environment variables:

    ```shell
    export DOING_CREATE_ISSUE_ASSIGNED_TO='jane@company.com'
    doing create 'fixing a small typo'
    # > Created issue #146545 'fixing a small typo'
    #     > added area-path '{your area path}'
    #     > added iteration-path '{your iteration path}'
    #     > added assignee 'jane@company.com'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    default_workitem_type: Task
    default_reviewers: 'john.doe@domain.com'
    ```

