# Overview

`doing` is a CLI tool for Azure DevOps that helps mimic the common repository/issue workflow from Github and Gitlab.

In Azure DevOps an issue (work item) is not directly related to a repository (here's [why](discussion/oneproject_setup.md)). `doing` solves this by adding a `.doing-cli-config.yml` file to the root of a repository containing information on the associated area and iteration paths. This enables `doing` to list, create and quickly access repository-related issues.

## Highlights

**listing issues linked to a repository**

<div class="termy termy-small">

```console
$ doing list
                 Work-items in current iteration IngOne\T01894-RiskandPricingAdvancedAna                  
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃     ID ┃             Title      ┃ Created by ┃       Type ┃    Linked Branches ┃ Linked PRs ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│  36893 │           explore data │ John       │ User Story │ 36893-explore-data │            │
│  43769 │       feature pipeline │ Artur      │ User Story │                    │            │
│  99035 │             window bug │ Artur      │       Task │   99035-window-bug │      39949 │
│ 104436 │ data loading functions │ Jane       │       Task │                    │            │
└────────┴────────────────────────┴────────────┴────────────┴────────────────────┴────────────┘
```

</div>

**quickly starting work on a new issue**

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
        > set auto-complete to 'True'
        > set to delete remote source branch after PR completion
        > added reviewers: '{your azure account}'
        $ Running command: git fetch origin
        $ Running command: git checkout -b 146545_fixing_a_small_typo origin/146545_fixing_a_small_typo
```

</div>


## Documentation

- [Getting started](get_started/install.md): A hands-on introduction to `doing` for developers. *Recommended for all new users*
- [How-to guides](howto/workflow_new_item.md): Step-by-step guides. Covers key tasks and operations and common problems.
- [Reference](reference/commands.md): Technical reference. Covers tools, components, commands and resources.
- [Discussion](discussion/oneproject_setup.md): Explanation. Clarification and discussion of key topics.
