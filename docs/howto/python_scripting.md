# Writing python scripts

You can use `doing` functionality directly from python as well. Here's an example of programmatically creating a bunch of issues:

```python
from doing.options import get_common_options
from doing.issue.create_issue import cmd_create_issue

issue_list = ['issue 1','issue 2','issue 3']

for title in issue_list:
    cmd_create_issue(title, **get_common_options())
```
