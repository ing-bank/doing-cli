# Contributing

The `doing` tool is an acronym for **d**ev**o**ps and ING bank. This is because the tool was built to speed up development for data science teams using ING's setup of Azure Devops.

The tool is built on top of modern python tools like [Click](https://click.palletsprojects.com/), [rich](https://github.com/willmcgugan/rich) 

## TODO:

- Implement [sh](https://github.com/amoffat/sh) instead of subprocess

## Documentation

We use the [divio documentation system](https://documentation.divio.com/).

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

# list issuers
az boards query --wiql "SELECT * FROM WorkItems WHERE ([System.State] = 'Active' OR [System.State] = 'New') AND [System.IterationPath] = 'IngOne\T01894-RiskandPricingAdvancedAna\taco_sprint6' AND [System.AreaPath] = 'IngOne\P01908-Default\taco'"

# List iterations
#https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards?view=azure-cli-latest#ext_azure_devops_az_boards_query
#https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
az boards iteration team show-backlog-iteration --team 'T01894-RiskandPricingAdvancedAna'
az boards iteration project list --path 'https://dev.azure.com/IngEurCDaaS01/IngOne/P01908-Default/taco_sprint5'
az boards iteration project show --id 'bd352cb3-129d-432e-ac36-a07daba5a8ee'
az boards iteration team list --team 'T01894-RiskandPricingAdvancedAna'


az boards work-item create --title "Test from tim's command line" --type "User Story" --area "IngOne\P01908-Default\example_repo"
```


