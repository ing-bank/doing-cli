# Azure Devops One Project Setup

Azure Devops has a limit of 250 projects per azure organization. A lot of collaboration possibilities are not between between azure organizations. This means that it is not possible for larger companies to allow teams to have one or more projects.

The solution is surprisingly simple: combine all teams into a single project. Many developers however are used to the github or gitlab way of working, where a project has a single repository and a single board with issues. In the One Project setup, the link between a repository and an issue (work item) is not so clear.

In the diagram below you can see that a work-item always has an area-path and an iteration-path, which are unique to a certain team. You can link a work-item to a *branch* of an existing repository, which is often a branch made specifically to work on the issue. Of course this enables managing projects with multiple repositories and different teams working on different aspects, but often a project means you would like a single issue board to match a single repository. 

```mermaid
erDiagram
    TEAM }|--|| ITERATION-PATHS : has
    TEAM }|--|| AREA-PATHS : has

    WORK-ITEM ||--|{ AREA-PATHS : has
    WORK-ITEM ||--|{ ITERATION-PATHS : has

    REPOSITORY-BRANCH }|--|{ WORK-ITEM : links
```

If you work on many repositories (for example as an individual contributor), figuring out which work items are related to it (like a github or gitlab issue board) is cumbersome at best. 
This is only exacerbated by common company policies set in Azure Devops that enforce every commit to be linked to a peer-reviewed pull request, and each pull request to have at least one linked work item. 

To restore the single repository and single issue board workflow, `doing` stores the *area path* and *iteration path* information in a config in the root of each repo, and uses that information to expose a small set of CLI commands that help mimic the familiar github/gitlab workflow.
