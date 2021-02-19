# More advanced workflows

## Overwriting configuration values

You can use [environment variables](https://en.wikipedia.org/wiki/Environment_variable) to (temporarily) overwrite configuration values (see [config file](../reference/config_file.md)).

```shell
DOING_CONFIG_TEAM=TeamA
doing list
DOING_CONFIG_TEAM=TeamB
doing list
```

## Scripting with python

You can use all `doing` functionality in a python script. Here's an example of programmatically creating a bunch of issues:

```python
from doing.options import get_common_options
from doing.create.issue import cmd_create_issue

issue_list = ['issue 1','issue 2','issue 3']

for title in issue_list:
    cmd_create_issue(title, **get_common_options())
```
