# doing pr create

Create a pull request.

```shell
doing pr create [flags]
```

## Example usage

```shell
doing pr create 1234
doing pr create 1234 --draft -r "john.doe@company.com"
doing pr create 1234 --draft -r "john.doe@company.com jane.doe@company.com"
doing pr create 1234 --draft -r "@me jane.doe@company.com"
doing pr create 1234 --draft --checkout
doing pr create 1234 --delete-source-branch --self-approve --auto-complete
doing pr create 1234 --default-branch develop
```

!!! notes ""
    `doing` will create a branch name using the format *{work_item_id}*_*{issue_title}*, where the *{issue_title}* is in lowercase, [snake_case](https://en.wikipedia.org/wiki/Snake_case) with all special characters removed. Example: issue #13 'Fix @ bug !' becomes *13_fix bug*. If that branch already exists on the remote, `doing` will use that one.

!!! notes ""
    If a new branch is created while doing `pr create`, it will be branched from the default branch in Azure Devops, which usually will be `master`, but might be a different branch. Where to branch from can be overridden by using the option default-branch. This can be The pull request will target this same branch.

## Options

```nohighlight
{{ shell_out('doing pr create --help') }}
```

## In use

Using `user_aliases` set in the [config file](../../config/config_file.md):

=== "Shell"

    ```shell
    doing pr create 1234 --reviewers 'john jane'
    # > Created pull request #49281 'fixing a small typo'
    #     > linked work item #1234
    # ...
    #     > added reviewers: 'John.Doe@company.com Jane.Doe@email.net'
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other (required) config items...
    user_aliases:
        john: John.Doe@company.com
        jane: Jane.Doe@email.net
    ```

Using `default_reviewers` set in the [config file](../../config/config_file.md):

=== "Shell"

    ```shell
    doing pr create 1234
    # > Created pull request #49281 'fixing a small typo'
    #     > linked work item #1234
    # ...
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
