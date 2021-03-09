# Adding shell completion

When enabling autocompletion you can hit ++tab++ to complete `doing` commands and see follow-up commands. Setup is easy:

=== "Bash"

    For Bash, add this to `~/.bashrc`:

    ```shell
    eval "$(_DOING_COMPLETE=source_bash doing)"
    ```

=== "Zsh"

    For Zsh, add this to `~/.zshrc`:

    ```shell
    eval "$(_DOING_COMPLETE=source_zsh doing)"
    ```

    Ensure that the following is present in your `~/.zshrc`:

    ```shell
    autoload -U compinit
    compinit -i
    ```

    Zsh version 5.7 or later is recommended.

=== "Fish"

    For Fish, add this to `~/.config/fish/completions/foo-bar.fish`:

    ```shell
    eval (env _DOING_COMPLETE=source_fish doing)
    ```

Once setup, typing `doing` and hitting ++tab++ should give you a list of follow-up commands like shown below. Hitting ++tab++ again will cycle through the options.

<div class="termy">

```console
$ doing
close   -- Close an issue or PR.
create  -- Create issues or pull requests.
init    -- Create a .doing-cli-config file.
list    -- List issues related to the project.
open    -- Quickly open certain links.
workon  -- Create issue with PR and switch git branch.
```

</div>