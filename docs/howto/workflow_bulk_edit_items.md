# Workflow bulk editing work items

Sometimes you want to edit multiple work items in one go. You can use [`doing list`](../reference/manual/list.md) to filter the work items that you want to edit and use `--output_format='array'` to return a bash array that you can loop over.

## Bulk update story points

For example, you might want to update all work items that do not have story points assigned yet. You can do that with this bash script that uses the [`az boards work-item update`](https://docs.microsoft.com/en-us/cli/azure/boards/work-item?view=azure-cli-latest#az_boards_work_item_update) command:

```bash
for id in $(doing list --story_points 'unassigned' -o 'array')
do
	az boards work-item update --id "$id" --fields "Microsoft.VSTS.Scheduling.StoryPoints=1"
    echo "$id updated with 1 story points"
done
```


