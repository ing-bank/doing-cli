# Contributing

The `doing` tool is an acronym for **d**ev**o**ps and ING bank. This is because the tool was built to speed up development for data science teams using ING's setup of Azure Devops.

The tool is built on top of modern python tools like [Click](https://click.palletsprojects.com/), [rich](https://github.com/willmcgugan/rich) 

## Documentation

We use the [divio documentation system](https://documentation.divio.com/).

## Technical background

We are basically wrapping the Azure Devops CLI.

- [Azure Devops commands reference](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/?view=azure-cli-latest&viewFallbackFrom=azure-devops)

## Ideas for future development

- Specify default work item type to create, in config.
- `doing init`: create `.devops-ing` file
- `doing status`: See if you're connected, which branch, issue and pr you are working on
- `doing change iteration "<path>"`. If a project requires changing the `.devops-ing` file every time a sprint changes, that might get annoying. This command could automate 1) creating a new work item (using `doing workon`), 2) Updating `.devops-ing`, 3) adding, committing and pushin changes, 4) creating the PR. --> Seems hacky. Better to define a way to define a path to the default iteration?

## Examples of using azure devops CLI

```bash
# Configuration
az devops configure -l
organization=https://dev.azure.com/IngEurCDaaS01
project=IngOne 
az devops configure --defaults organization=$organization project=$project

# List areas for a team
f"az boards area team list --team {team} --org {organization} -p {project}"
az boards area team list --team=T01894-RiskandPricingAdvancedAna

# list work items
az boards work-item show --id 37222
az boards query --wiql "SELECT * FROM WorkItems WHERE ([System.State] = 'Active' OR [System.State] = 'New') AND [System.IterationPath] = 'IngOne\T01894-RiskandPricingAdvancedAna\taco_sprint6' AND [System.AreaPath] = 'IngOne\P01908-Default\taco'"

# List iterations
#https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/boards?view=azure-cli-latest#ext_azure_devops_az_boards_query
#https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops
az boards iteration team show-backlog-iteration --team 'T01894-RiskandPricingAdvancedAna'
az boards iteration project list --path 'https://dev.azure.com/IngEurCDaaS01/IngOne/P01908-Default/taco_sprint5'
az boards iteration project show --id 'bd352cb3-129d-432e-ac36-a07daba5a8ee'
az boards iteration team list --team 'T01894-RiskandPricingAdvancedAna'

# Listing PRs

# List remote branches
az repos ref list --repository {get_repo_name()} --query '[].name'

# Creating work items
az boards work-item create --title "Test from tim's command line" --type "User Story" --area "IngOne\P01908-Default\example_repo"
az boards work-item create --title "testing from tim" --type "User Story" --area 'IngOne\\P01908-Default' --iteration 'IngOne\\T01894-RiskandPricingAdvancedAna\\example_repository_sprint4' --assigned-to "tim.vink@ing.com"

# Deleting work items
az boards work-item delete --id 112011

# Creating a branch

# 1) get object id of master branch:
az repos ref list --repository P01908-taco --query "[?name=='refs/heads/master'].objectId"
# 2) get branch
az repos ref create --name "heads/testbranchtim" --repository 'P01908-taco' --object-id "684c3079fc9e496dbba885b6febc84ee3bf32bdd"
# returns
{'customMessage': None, 'isLocked': False, 'name': 'refs/heads/testbranchtim', 'newObjectId': '684c3079fc9e496dbba885b6febc84ee3bf32bdd', 'oldObjectId': '0000000000000000000000000000000000000000', 'rejectedBy': None, 'repositoryId': '4d2e7861-c3d0-4932-8f23-c8628d05d471', 'success': True, 'updateStatus': 'succeeded'}



```


