# doing pr list

List pull requests related to the project.

```shell
doing pr list [flags]
```

## Example usage

```shell
doing pr list
doing pr list -assignee "John.Doe@company.com"
doing pr list -a "John.Doe@company.com"
doing list -a @me
doing list --label "some_tag"
doing list --label "some_tag, another tag"
doing list --state all
doing list --state merged
doing list -a @me -s all -l a_tag
doing list --web -s merged
```

!!! Note "PR Statuses"

    For consistency with GitHub CLI's [`gh pr list`](https://cli.github.com/manual/gh_pr_list),
    we use `{open|closed|merged|all}` for PR status and internally translate to devops's `{active|abandoned|completed|all}`.
    This is useful for developers working cross-platform.

## Options

```nohighlight
{{ shell_out('doing pr list --help') }}
```
