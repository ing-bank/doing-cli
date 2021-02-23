# The .doing-cli-config.yml config file

`doing` searches for YAML config file named `.doing-cli-config.yml`. The config must contain the following parameters (in lowercase):

| Parameter      | Description                          |
| ----------- | ------------------------------------ |
| `organization`       | Name of the organization. You can quickly find the organization in your devops url, after *https://dev.azure.com*. Example: The organization for *https://dev.azure.com/IngEurCDaaS01/IngOne* is *IngEurCDaaS01*.  |
| `project`       | Name of the project. You can quickly find the organization in your devops url, after *https://dev.azure.com/YourOrganization/*. Example: The project for *https://dev.azure.com/IngEurCDaaS01/IngOne* is *IngOne*. |
| `team`    | The name of your team. You can quickly find it when navigating on Azure Devops to Boards > Boards. Example: The team in *https://dev.azure.com/IngEurCDaaS01/IngOne/_boards/board/t/T01894-RiskandPricingAdvancedAna/Stories* is *T01894-RiskandPricingAdvancedAna*. |
| `area`    | The area path assigned to work items. You can find it by going to a work item (Azure Devops > Boards > Work items) and copying the Area field. This corresponds to the work item field *System.AreaPath*. |
| `iteration`    | The iteration path assigned to work items. You can find it going by to a work item (Azure Devops > Boards > Work items) and copying the Iteration field. This corresponds to the work item field *System.IterationPath*. |

The config can also contain some optional parameters that are not required to be set: 

| Optional Parameter      | Description |
| ----------------------- | ------------------------------------ |
| `default_workitem_type` | The default work item type used when creating work items. Should be one of "Bug", "Epic", "Feature", "Issue", "Task", "Test Case", "User Story". Defaults to "User Story" if not specified. 

## Using environment variables

You can overwrite the values set in `doing-cli-config.yml` using environment variables. Use the prefix `DOING_CONFIG_` followed by the parameter name in uppercase. 

Some examples: 

| Parameter      | Environment variable |
| -------------- | -------------------- |
| `team`         | `DOING_CONFIG_TEAM` |
| `iteration`    | `DOING_CONFIG_ITERATION` |
| `default_workitem_type`    | `DOING_CONFIG_DEFAULT_WORKITEM_TYPE` |

!!! note ""
    See also the [workflow using environment variables](../howto/workflow_envvars.md) for examples on how to use these in practice

