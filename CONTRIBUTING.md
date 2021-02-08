# Contributing

The `doing` tool is an acronym for **d**ev**o**ps and ING bank. This is because the tool was built to speed up development for data science teams using ING's setup of Azure Devops.

The tool is built on top of modern python tools like [Click](https://click.palletsprojects.com/), [rich](https://github.com/willmcgugan/rich) 

## Documentation

We use the [divio documentation system](https://documentation.divio.com/).

## Setup

- We use [pre-commit](https://pre-commit.com/). Setup using `pip install pre-commit` and then `pre-commit install`.
- For development, use an editable install: `pip install -e .`

## Technical background

We are basically wrapping the Azure Devops CLI.

- [Azure Devops commands reference](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/?view=azure-cli-latest&viewFallbackFrom=azure-devops)


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

# Update a work item
az boards work-item relation add --id 112011 --relation-type 'Branch' --target-id 6566809

# list relation types
az boards work-item relation list-type --query 'name'
# Artifact Link
az boards work-item relation add --id 112011 --relation-type 'Artifact Link' --target-id 6566809
# from ojbectID of a branch with
az repos ref list --repository P01908-taco
az boards work-item relation add --id 112011 --target-id "475bdee470cab59ccd1d8e25b29ed7f9285504b2" --relation-type "Artifact Link"

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

# Creating a PR
az repos pr create --repository 'P01908-taco' --work-items '112011' --draft --title "test pr from tim" --source-branch "testbranchtim" --transition-work-items 'true'

# Creating a branch
# 1) get object id of master branch:
az repos ref list --repository P01908-taco --query "[?name=='refs/heads/master'].objectId"
# 2) get branch
az repos ref create --name "heads/testbranchtim" --repository 'P01908-taco' --object-id "684c3079fc9e496dbba885b6febc84ee3bf32bdd"
# returns
{'customMessage': None, 'isLocked': False, 'name': 'refs/heads/testbranchtim', 'newObjectId': '684c3079fc9e496dbba885b6febc84ee3bf32bdd', 'oldObjectId': '0000000000000000000000000000000000000000', 'rejectedBy': None, 'repositoryId': '4d2e7861-c3d0-4932-8f23-c8628d05d471', 'success': True, 'updateStatus': 'succeeded'}



```


