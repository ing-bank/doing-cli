# The .doing-cli-config.yml config file

`doing` searches for YAML config file named `.doing-cli-config.yml`. The config must contain the following parameters (in lowercase):

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `organization`       | Name of the organization. You can quickly find the organization in your devops url, after *https://dev.azure.com*. Example: The organization for *https://dev.azure.com/IngEurCDaaS01/IngOne* is *IngEurCDaaS01*.  |
| `project`       | Name of the project. You can quickly find the organization in your devops url, after *https://dev.azure.com/YourOrganization/*. Example: The project for *https://dev.azure.com/IngEurCDaaS01/IngOne* is *IngOne*. |
| `team`    | The name of your team. You can quickly find it when navigating on Azure Devops to Boards > Boards. Example: The team in *https://dev.azure.com/IngEurCDaaS01/IngOne/_boards/board/t/T01894-RiskandPricingAdvancedAna/Stories* is *T01894-RiskandPricingAdvancedAna*. |
| `area`    | The area path assigned to work items. You can find it by going to a work item (Azure Devops > Boards > Work items) and copying the Area field. This corresponds to the work item field *System.AreaPath*. |
| `iteration`    | The iteration path assigned to work items. You can find it going by to a work item (Azure Devops > Boards > Work items) and copying the Iteration field. This corresponds to the work item field *System.IterationPath*. |

