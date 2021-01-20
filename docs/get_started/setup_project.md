# Setup your project

In Azure Devops, your project's repository and your project's work items do not have to be linked. To be able to find work items related to a repo, `doing` requires a setup file for each repository you work in.

Create a `.devops-ing` file in the root of your repository. For information on how to find these parameters see the reference [.devops-ing config file](../reference/config_file.md)

```yaml
# .devops-ing
# Example config file to be used with the `doing` CLI tool
organization=https://dev.azure.com/IngEurCDaaS01
project=IngOne 
team=T01894-RiskandPricingAdvancedAna
area=IngOne\P01908-Default\taco
iteration=IngOne\T01894-RiskandPricingAdvancedAna\taco_sprint6
```


## Verifying the setup

In the root of your repository, you can check if your configuration works using:

```shell
doing list
```
