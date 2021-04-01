# Workflow existing work item

You'll likely want to review existing issues first. `cd` into your repository and use [`doing list`](../reference/manual/list.md) for a quick view.
If you need more detail you can use [`doing open`](../reference/manual/open.md) to open relevant views in the azure devops web portal, for example `doing open issues`, `doing open board` or `doing open sprint`.

## Start on an existing issue

Once you have the issue ID you want to work on, you'll need to create a remote branch and a pull request to be able to start work. You can do that with the [`doing pr create`](../reference/manual/pr_create.md) command. `doing` follows the branch naming convention *`<work_item_id>_<issue title>`*, where the issue title is transformed to [snake_case](https://en.wikipedia.org/wiki/Snake_case). You can safely run this command multiple times: if the branch already exists, it will use that one, and if the PR already exists for that branch, `doing` will let you know.

<div class="termy termy-small">

```console
$ doing pr create 146545 
> Created remote branch '146545_fixing_a_small_typo'
> Created pull request #49281 'fixing a small typo'
        > linked work item #146545
        > set auto-complete to True'
        > set to delete remote source branch after PR completion
        > added reviewers: '<your email>'
        $ Running command: git fetch origin
        ...
        # Running command: git checkout -b '146545_fixing_a_small_typo' 'origin/146545_fixing_a_small_typo'
```

</div>

You can also create a draft PR, assign reviewers, run the git checkout commands and more. See `doing pr create --help` for the options. Some examples:

```shell
doing pr create 146545 --reviewers "john.doe@email.com"
doing pr create 146545 --checkout --draft
```

## Start on existing pull request

[`doing list`](../reference/manual/list.md) will also show you if a work item already has a pull request associated with it.
Alternatively [`doing pr list`](../reference/manual/pr_list.md) will show you a list of active pull requests. Once you have a pullrequest ID that 
you want to get started on, you can use [`doing pr checkout`](../reference/manual/pr_checkout.md) to quickly `git checkout` the branch locally. 
This is more convenient than manually finding the correct branchname and checkout it out locally (the 'long worflow'):

=== "Short workflow"

    ```shell
    doing pr checkout <pullrequest_id>
    ```

=== "Long workflow"

    ```shell
    doing open pr <pullrequest_id> # find branch name
    git fetch origin
    git checkout -b '{branch_name}' 'origin/{branch_name}'
    ```


## Using aliases

To avoid having to type the emailadresses of your teammates every time (which are case sensitive in Azure), you can setup aliases in your `.doing-cli-config.yml` (see also [config file](../reference/config_file.md) reference):

=== "using aliases"

    ```shell
    doing pr create 146545 --reviewers "john jane"
    ```

=== ".doing-cli-config.yml"

    ```yaml
    # ... other config items ...
    user_aliases:
       john: John.Doe@company.com
       jane: Jane.Doe@email.net
    ```


## Wrap up

When you're done you can view the:

- pull request using `doing open pr <pullrequest id>`. Use [`doing list`](../reference/manual/list.md) to find your PR id.
- issue using `doing open issue <issue id>`. The git branch name has the issue id as a prefix, or alternatively you can use [`doing list`](../reference/manual/list.md) to find the issue id.
- active pull requests using `doing open prs`
- pipeline runs using `doing open pipe`
