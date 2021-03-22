# doing list

List issues related to the project.

```shell
doing list [flags]
```

## Example usage

```shell
doing list
doing list -assignee "John.Doe@company.com"
doing list -a "John.Doe@company.com"
doing list -a @me
doing list -author "John.Doe@company.com"
doing list --label "some_tag"
doing list --state all
doing list -a "John.Doe@company.com" -s all
doing list --web
```

!!! Note "Issue state open or closed?"

    To determine if an issue is open or closed, `doing` maps the different [workflow states](https://docs.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops&tabs=cmmi-process#workflow-states). 


## Options

```nohighlight
{{ shell_out('doing list --help') }}
```
