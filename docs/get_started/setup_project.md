# Setup your project

Due to the setup of ING's Azure Devops, there is a decoupling of a repository and boards. This means we cannot automatically link a repo with a team, iteration (sprint), or area path.

This means we will need to setup a configuration file per repository.
Create a `.devops-ing` file in the root of your repository.

```yaml
# .devops-ing
# Config file to be used with the `doing` CLI tool
organization=IngEurCDaaS01
project=IngOne
area=taco
team=T01894-RiskandPricingAdvancedAna
iteration=taco_sprint1
```

??? info "How to fill in the configuration"

    `organization`
    :   Name of the organization. Almost always "IngEurCDaaS01"

    `project`
    : Name of the project. Almost always "IngOne"

    `team`
    : The path of your team. Find it <>.

    `area`
    : The area path to assigned to work items. System.AreaPath.

    `iteration`
    : The iteration path assigned to work items. System.IterationPath.


# Verifying the setup

In the root of your repository, you can check if your configuration works using:

```bash
doing status
```
