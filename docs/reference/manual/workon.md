# doing workon

Create issue with PR and switch git branch.

```shell
doing workon [flags]
```

## Example usage

```shell
doing workon "an issue"
doing workon "an issue" --type Bug
doing workon "an issue" --type 'User Story'
doing workon "an issue" --parent 12345
doing workon "an issue" --reviewers "john.doe@company.com jane.doe@company.com"
doing workon "an issue" --no-auto-complete --no-draft --self-approve
```

## Options

```nohighlight
{{ shell_out('doing workon --help') }}
```

