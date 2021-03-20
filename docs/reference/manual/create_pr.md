# doing create pr

Create a pull request.

```shell
doing create pr [flags]
```

## Example usage

```shell
doing create pr 1234
doing create pr 1234 --draft -r "john.doe@company.com"
doing create pr 1234 --draft -r "john.doe@company.com jane.doe@company.com"
doing create pr 1234 --draft --checkout 
doing create pr 1234 --delete-source-branch --self-approve --auto-complete
```

!!! notes ""
    `doing` will create a branch name using the format *{issue_id}*_*{issue_title}*, where the *{issue_title}* is in lowercase, [snake_case](https://en.wikipedia.org/wiki/Snake_case) with all special characters removed. Example: issue #13 'Fix @ bug !' becomes *13_fix bug*. If that branch already exists on the remote, `doing` will use that one.

## Options

```nohighlight
{{ shell_out('doing create pr --help') }}
```

## In use

Using user_aliases set in the [config file](../config_file.md):

=== "Shell"

    ```shell
    doing create pr 1234 --reviewers 'john jane'
    # > Created pull request #49281 'fixing a small typo'
    #     > linked work-item #1234
    #     > added reviewers: 'John.Doe@company.com Jane.Doe@email.net'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    user_aliases:
        john: John.Doe@company.com
        jane: Jane.Doe@email.net
    ```

Using default_reviewers set in the [config file](../config_file.md):

=== "Shell"

    ```shell
    doing create pr 1234
    # > Created pull request #49281 'fixing a small typo'
    #     > linked work-item #1234
    #     > added reviewers: 'John.Doe@company.com Jane.Doe@email.net'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    default_reviewers: "john jane"
    user_aliases:
        john: John.Doe@company.com
        jane: Jane.Doe@email.net
    ```
