# Workflow for new issues

Before creating a new issue, you'll likely want to review existing issues first. `cd` into your repository and use [`doing list`](../reference/manual/list.md) for a quick view.
If you need more detail you can use [`doing open`](../reference/manual/open.md) to open relevant views in the azure devops web portal, for example `doing open issues`, `doing open board` or `doing open sprint`.

## Planning multiple items

If you don't plan to start work on an issue immediately, you can use [`doing issue create`](../reference/manual/issue_create.md) to create a new (unassigned) work item with:

```shell
doing issue create "something that needs to be done"
```

You can specify more options (see `doing issue create --help`). Some examples:

```shell
doing issue create "something that needs to be done" --mine 
doing issue create "something that needs to be done" --assigned_to "john.doe@company.com" 
doing issue create "something that needs to be done" --a "john.doe@company.com" --type "Bug"
doing issue create "something that needs to be done" --parent "1234" --type "Task"
```


## Starting work on a new issue

If you plan to start work on a new issue immediately, it is better to use [`doing workon`](../reference/manual/workon.md) instead. All you need to provide is the title:

<div class="termy termy-small">

```console
$ doing workon "fixing a small typo"
> Created issue #146545 'fixing a small typo' (User Story)
        > added area-path '{your area path}'
        > added iteration-path '{your iteration path}'
        > added assignee '{your azure account}'
> Created remote branch '146545_fixing_a_small_typo'
> Created pull request #49281 'fixing a small typo'
        > linked work item #146545
        > marked as draft pull request
        > set auto-complete to True'
        > set to delete remote source branch after PR completion
        > added reviewers: '{your azure account}'
        $ Running command: git fetch origin
        $ Running command: git checkout -b 146545_fixing_a_small_typo origin/146545_fixing_a_small_typo
```

</div>

This automates a lot of clicking in the Azure Devops web portal and even runs git commands locally, so you can immediately start your normal `git add`, `git commit` and `git push` development workflow.

!!! note ""
    See also the workflow for [starting work on an existing item](workflow_existing_item.md)

## Using aliases

To avoid having to type the emailadresses of your teammates every time (which are case sensitive in Azure), you can setup aliases in your `.doing-cli-config.yml` (see also [config file](../reference/config_file.md) reference):

=== "using aliases"

    ```shell
    doing issue create "fix bug" -a john
    # or
    doing workon "fix bug" --reviewers "john jane"
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other config items ...
    user_aliases:
       john: John.Doe@company.com
       jane: Jane.Doe@email.net
    ```

## Starting work on a new child issue

Another common workflow is to work on tasks that are part of a user story. In azure devops, work items can be linked (parent/child relationship). `doing workon` has `--parent` and `--type` to accomodate the use case:

```shell
doing workon "some work" --type 'Task' --parent 1234
```

## Wrap up

When you're done you can view the:

- pull request using `doing open pr <pullrequest id>`. Use [`doing list`](../reference/manual/list.md) to find your PR id.
- issue using `doing open issue <issue id>`. The git branch name has the issue id as a prefix, or alternatively you can use [`doing list`](../reference/manual/list.md) to find the issue id.
- active pull requests using `doing open prs`
- pipeline runs using `doing open pipe` 

