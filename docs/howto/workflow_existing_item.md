# Workflow existing work item

You'll likely want to review existing issues first. `cd` into your repository and use `doing list` for a quick view.
If you need more detail, considering opening the relevant views in the azure devops web portal using commands like `doing open issues`, `doing open board` or `doing open sprint`.

## Starting work on an existing issue

Once you have the issue ID you want to work on, you'll need to create a remote branch and a pull request to be able to start work. You can do that with the `doing create pr` command. `doing` follows the branch naming convention *`<issue_id>_<issue title>`*, where the issue title is transformed to [snake_case](https://en.wikipedia.org/wiki/Snake_case). You can safely run this command multiple times: if the branch already exists, it will use that one, and if the PR already exists for that branch, `doing` will let you know.

<div class="termy termy-small">

```console
$ doing create pr 146545 
> Created remote branch '146545_fixing_a_small_typo'
> Created pull request #49281 'fixing a small typo'
        > linked work-item #146545
        To start work on the PR run:
        git fetch origin
        git checkout -b 146545_fixing_a_small_typo origin/146545_fixing_a_small_typo
```

</div>

You can also create a draft PR, assign reviewers, run the git checkout commands and more. See `doing create pr --help` for the options. Some examples:

```shell
doing create pr 146545 --reviewer "john.doe@email.com"
doing create pr 146545 --checkout --draft
```

When you're done you can view the:

- pull request using `doing open pr <pullrequest id>`. Use `doing list` to find your PR id.
- issue using `doing open issue <issue id>`. The git branch name has the issue id as a prefix, or alternatively you can use `doing list` to find the issue id.
- active pull requests using `doing open prs`
- pipeline runs using `doing open pipe` 


