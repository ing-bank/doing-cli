# Getting started guide

## Commands

- `doing init`: create `.devops-ing` file
- `doing status`: See if you're connected, which branch, issue and pr you are working on
> branch name is not in format NNN-snakecase. Cannot find related issue.
> Maybe check all workitems and PRs and their info?

- `doing issue list`: shows list of open issues related to the repository
> To work on an issue, git checkout <> or doing issue update 1234

- `doing issue create 'quick change to README`: 
> create issue #12345
> assign area
> assign iteration
> assignee set to git config email
> created origin/branch
> git fetch origin
> to workon the issue, "git checkout 12356-description"

- `doing issue update #1235`: updates issue with all assignments, if necessary


- `doing open board`
- `doing open repo`
- `doing open pr`
- `doing open pipelines`
- `doing open #1234`


## Notes

We'll do the PR stuff later.

<issuenumber>-<quick-change-to-README>

`doing status`: 
> on branch ...
> linked issue: ...
> etc

- `doing pr`: creates a pull request for the current branch / issue

doing status
doing issue list
doing workon #1234

doing pr --review "ryan.chaves@ing.com"
git checkout master

doing workon "quick change"
git commit -am
doing pr --reviewer "ryan.chaves@ing.com"


FEEDBACK:
- WIP PR?
- work items already exist often
- git commits explicit user
- git GUI stuff
- open board link
- open pr


HIER GEBLEVEN. 
- wat als je met `doing status` op een branch zit die nog geen bijbehorende issue heeft?
- wat als je tussendoor wilt werken aan een andere issue?. 
- explain premise of 'ING way of working': every commit is part of a branch that is part of a pull request that is part of an issue, that is part of a sprint.
- explain RPAA way of working. every work item also has an area to be able to link it to a certain repo.


## Workflow

```bash
# Normal clone
git clone <your repo>
git checkout <your repo>

# Work on something new
ado workon "make an update to the readme"
> created new work-item #12341 "make an update to the readme"
   > added area-path "your-repo"
> created new branch origin/12341-make-an-update-to-the-readme
> created new branch 12341-make-an-update-to-the-readme
> switched to branch 12341-make-an-update-to-the-readme

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