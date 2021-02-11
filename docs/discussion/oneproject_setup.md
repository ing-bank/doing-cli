# OneProject Setup

!!! attention "Draft"
    This page is not yet complete.


TODO:

- explain premise of 'ING way of working': every commit is part of a branch that is part of a pull request that is part of an issue, that is part of a sprint.
- explain RPAA way of working. every work item also has an area to be able to link it to a certain repo.

```mermaid
erDiagram
    TEAM }|--|| ITERATION-PATHS : has
    TEAM }|--|| AREA-PATHS : has

    WORK-ITEM ||--|| AREA-PATHS : bla
    WORK-ITEM ||--|| ITERATION-PATHS : bla

    REPOSITORY-BRANCH ||--|| WORK-ITEM : has
```

Discuss: is is a better approach to simply search for work items that have a linked branch of a repo?
No, because there is no view within azure devops, we'll follow the UI. Note we can now do stuff like `doing open board`, which otherwise wouldn't be possible. 

1) a project can have multiple repositories, and 2) work items are linked to iterations (sprints), areas, and potentially certain repo branches.