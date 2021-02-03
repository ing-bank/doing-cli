# Overview

`doing` is a CLI tool for Azure DevOps that helps mimic the common repository/issue workflow from Github and Gitlab.

## Features

In Azure DevOps a work item is not directly related to a repository. This is because 1) a project can have multiple repositories, and 2) work items are linked to iterations (sprints), areas, and potentially certain repo branches.

To solve this, `doing` adds a `.doing` config file to the root of a project providing linked area and iteration paths. This enables `doing` to list and work with repository-related work items. 

### listing issues

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

## Documentation

- [Getting started](get_started/install.md): A hands-on introduction to `doing` for developers. *Recommended for all new users*
- [How-to guides](): Step-by-step guides. Covers key tasks and operations and common problems.
- [Reference](): Technical reference. Covers tools, components, commands and resources.
- [Discussion](): Explanation. Clarification and discussion of key topics.
