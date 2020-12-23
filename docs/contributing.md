# Contributing

## Technical background

We are basically wrapping the Azure Devops CLI.

- [Azure Devops commands reference](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/?view=azure-cli-latest&viewFallbackFrom=azure-devops)


## Notes

To be put somewhere or removed.

```bash
organization=https://dev.azure.com/IngEurCDaaS01
project=IngOne 
az devops configure --defaults organization=$organization project=$project

# List areas for a team
f"az boards area team list --team {team} --org {organization} -p {project}"

az boards area team list --team=T01894-RiskandPricingAdvancedAna

az boards work-item create --title "Test from tim's command line" --type "User Story" --area "IngOne\P01908-Default\example_repo"
```
