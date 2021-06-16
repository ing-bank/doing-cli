# Upgrading

!!! Note "Doing Releases"

    All release details can be found on the [doing releases page](https://github.com/ing-bank/doing-cli/releases).

## v1.0

See [release notes](https://github.com/ing-bank/doing-cli/releases/tag/v1.0)

### Upgrading from `0.x` to `1.0`

- Update any reference to renamed commands:
    - `doing create pr` is renamed to `doing pr create`
    - `doing close pr` is renamed to `doing pr close`
    - `doing create issue` is renamed to `doing issue create`
    - `doing close issue` is renamed to `doing issue close`
- `doing pr create` now has changed defaults. The command now has similar output to `doing workon` which leads to a more natural workflow. If you prefer the old behaviour, set the [defaults in the config file](../config/config_file.md#setting-command-defaults):
    - `--checkout` is now default (was `--no-checkout`)
    -  `--delete-source-branch` is now default (was `--no-delete-source-branch`)
    - `--auto-complete` is now default (was `--no-auto-complete`)
    - `--draft` is now default (was `--no-draft`)
- Note the use of the `@me` alias:
    - `doing pr create` will now always add `@me` to the `--reviewers` (a default user alias pointing to the logged in users's azure account).
    - `doing workon` will now always add `@me` to the `--reviewers` (a default user alias pointing to the logged in users's azure account).
- `doing issue create` has been changed:
    - `-a/--assigned-to` is renamed to `-a/--assignee`, and supports `@me` alias.





