# Releases

## v1.0

- `doing pr create` now has similar defaults as `doing workon` (#22) 


### Upgrading from `0.x` to `1.0`

- `doing create pr` is renamed to `doing pr create`
- `doing pr create` now has changed defaults. The command now has similar output to `doing workon` which leads to a more natural workflow. If you prefer the old behaviour, set the [defaults in the config file](../reference/config_file.md#setting-command-defaults).
    - `--checkout` is now default (was `--no-checkout`)
    -  `--delete-source-branch` is now default (was `--no-delete-source-branch`)
    - `--auto-complete` is now default (was `--no-auto-complete`)
    - `--draft` is now default (was `--no-draft`)
    - `doing` will now always add `@me` to the `--reviewers` (a default user alias pointing to the logged in users's azure account).
- `doing workon`
    - `doing` will now always add `@me` to the `--reviewers` (a default user alias pointing to the logged in users's azure account).







