# Workflow for new issues

Before creating a new issue, you'll likely want to review existing issues first. `cd` into your repository and use `doing list` for a quick view.
If you need more detail, considering opening the relevant views in the azure devops web portal using commands like `doing open issues`, `doing open board` or `doing open sprint`.

## Planning multiple items

If you don't plan to start work on an issue immediately, you can create a new (unassigned) work item with:

```shell
doing create issue "something that needs to be done"
```

You can specify more options (see `doing create issue --help`). Some examples:

```shell
doing create issue "something that needs to be done" --mine 
doing create issue "something that needs to be done" --assigned_to "john.doe@company.com" 
doing create issue "something that needs to be done" --assigned_to "john.doe@company.com" --type "Bug"
```

!!! note ""
    See also the workflow for [starting work on an existing item](workflow_existing_item.md)

## Starting work on a new issue

If you plan to start work on a new issue immediately, it is better to use `doing workon` instead. All you need to provide is the title:

<div class="termy termy-small">

```console
$ doing workon "fixing a small typo"
> Created issue #146545 'fixing a small typo'
        > added area-path '{your area path}'
        > added iteration-path '{your iteration path}'
        > added assignee '{your azure account}'
> Created remote branch '146545_fixing_a_small_typo'
> Created pull request #49281 'fixing a small typo'
        > linked work-item #146545
        > marked as draft pull request
        > set auto-complete to True'
        > added reviewers: '{your azure account}'
        $ Running command: git fetch origin
        $ Running command: git checkout -b 146545_fixing_a_small_typo origin/146545_fixing_a_small_typo
```

</div>

This automates a lot of clicking in the Azure Devops web portal and even runs git commands locally, so you can immediately start your normal `git add`, `git commit` and `git push` development workflow.

When you're done you can view the:

- pull request using `doing open pr <pullrequest id>`. Use `doing list` to find your PR id.
- issue using `doing open issue <issue id>`. The git branch name has the issue id as a prefix, or alternatively you can use `doing list` to find the issue id.
- active pull requests using `doing open prs`
- pipeline runs using `doing open pipe` 
