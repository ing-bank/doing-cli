# Workflow using sprints to manage issues

In azure devops, all work items already have both an area path and an iteration path (a sprint). You can use these in different ways to group and structure your work items, even across multiple repositories (see [this discussion](../discussion/oneproject_setup.md) for more background).

## Viewing your current sprint

A sprint is basically an iteration path. You can view the issues using `doing open sprint`, `doing open board` or `doing open issues`.

Note that [`doing list`](../reference/manual/list.md) will show all active issues under the iteration path. This means that if you specify *`<projectname>/<teamname>`* as your iteration path, you might see issues with iteration path *`<projectname>/<teamname>/<sprint name>`* as well as issues with *`<projectname>/<teamname>`*.

## Changing sprints

If you [create a new sprint](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/set-iteration-paths-sprints?view=azure-devops&tabs=browser), you will have to update the `.doing-cli-config.yml` file as well.

If you have a frequent sprint schedule, or don't want new issues to enter your sprint, you can specify a higher level iteration path instead (so *`<projectname>/<teamname>`* instead of *`<projectname>/<teamname>/<sprint name>`*). `doing list` will still show all active items under the iteration path, and you can use the backlog management (open quickly via `doing open sprint`) to manually manage the work items in your current sprint.
