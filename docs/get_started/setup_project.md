# Setup your project

Work items are not directly linked to a repository in azure devops. `doing` looks for a `.doing-cli-config.yml` file in the root of your repository, that should contain information on how work items are linked. Every work item always has a organization, a devops project, a team, an area path, and an iteration path. For more background on this see [this discussion](../discussion/oneproject_setup.md).

Create a `.doing-cli-config.yml` file in the root of your repository and specify the parameters. The easiest way to find these parameters is by creating or opening a work item, and copying the parameters from there. For information on how to find these parameters see the reference [.doing-cli-config.yml config file](../reference/config_file.md)

```yaml
# .doing-cli-config.yml
# Example config file to be used with the `doing` CLI tool
organization=https://dev.azure.com/IngEurCDaaS01
project=IngOne 
team=T01894-RiskandPricingAdvancedAna
area=IngOne\P01908-Default\taco
iteration=IngOne\T01894-RiskandPricingAdvancedAna\taco_sprint6
```

## Verifying the setup

In the root of your repository, you can check if your configuration works using:

<div class="termy termy-small">

```console
$ doing list
                 Work-items in current iteration IngOne\T01894-RiskandPricingAdvancedAna                  
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
