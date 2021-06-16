# Setup your project

Work items are not directly linked to a repository in azure devops. `doing` looks for a `.doing-cli-config.yml` file in the root of your repository, that should contain information on how work items are linked. Every work item always has a organization, a devops project, a team, an area path, and an iteration path. For more background on this see [this discussion](../discussion/oneproject_setup.md).

The easiest way to setup that config file is by using a reference work item. Find the url and run `doing init <url>` in the root of your repository, which will create the config file with the required parameters for you. For example:

<div class="termy">

```console
$ doing init https://dev.azure.com/organization_name/project_name/_workitems/edit/73554
> Created new .doing-cli-config.yml file
        > Filled in required parameters using reference work item #73554
```

</div>

Alternatively, create a `.doing-cli-config.yml` file in the root of your repository (you can use `doing init` to do that quickly) and specify the parameters. The easiest way to find these parameters is by creating or opening a work item, and copying the parameters from there. For information on how to find and set these parameters see the reference [.doing-cli-config.yml config file](../config/config_file.md)

## Verifying the setup

In the root of your repository, you can check if your configuration works using:

<div class="termy termy-small">

```console
$ doing list
                 Work-items in current iteration project_name\team_name                  
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃     ID ┃             Title      ┃ Created by ┃       Type ┃    Linked Branches ┃ Linked PRs ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│  36893 │           explore data │ John       │ User Story │ 36893-explore-data │            │
│  43769 │       feature pipeline │ Artur      │ User Story │                    │            │
│  99035 │            windows bug │ Artur      │       Task │  99035-windows-bug │      39949 │
│ 104436 │ data loading functions │ Jane       │       Task │                    │            │
└────────┴────────────────────────┴────────────┴────────────┴────────────────────┴────────────┘
```

</div>
