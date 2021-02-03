# Workflow for a new work item




## Notes

- `doing init`: create `.devops-ing` file
- `doing status`: See if you're connected, which branch, issue and pr you are working on
> branch name is not in format NNN-snakecase. Cannot find related issue.
> Maybe check all workitems and PRs and their info?

<issuenumber>-<quick-change-to-README>

`doing status`: 
> on branch ...
> linked issue: ...
> etc

- `doing pr`: creates a pull request for the current branch / issue

doing status
doing workon #1234

doing pr --reviewer "ryan.chaves@ing.com"
git checkout master

doing workon "quick change"
git commit -am
doing pr --reviewer "ryan.chaves@ing.com"


FEEDBACK:
- WIP PR?
- work items already exist often
- git commits explicit user
- git GUI stuff

HIER GEBLEVEN. 
- wat als je met `doing status` op een branch zit die nog geen bijbehorende issue heeft?
- wat als je tussendoor wilt werken aan een andere issue?. 

## Workflow

```bash
# Normal clone
git clone <your repo>
git checkout <your repo>

# Work on something *new*
ado workon "make an update to the readme"
> created new work-item #12341 "make an update to the readme"
   > added area-path "your-repo"
   > added 'your name' as assignee
> created & linked new branch origin/12341-make-an-update-to-the-readme
> To work on the issue, use the following commands:
   > git fetch --all
   > git checkout 12341-make-an-update-to-the-readme
   > Tip: lazy? next time use `doing workon -g`


# Your normal workflow
echo "some change" >> README.md
git add README.md && git commit -m "Improved the readme"
git push

# Create PR
ado create_pr --reviewer="daniel.timbrell@ing.com"
> created pull request to merge origin/12341-make-an-update-to-the-readme into master
> Added your own approval
> Added daniel.timbrell@ing.com as a reviewer

# And again
git checkout master
ado workon "something else"
```

## feedback round 2

- `doing workon` with `-g` `--execute-git-commands` for lazy ppl.
- `doing workon --assignee` with default on yourself (empty / nothing) but option to change it.
- WIP PR request by creating a 'dummy' commit?
   - label the name with prefix WIP
   - prevents errors merging into wrong repo
 
