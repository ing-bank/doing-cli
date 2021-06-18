# doing open

Quickly open certain links.

```shell
doing open [flags]
```

## Example usage

Most `doing open` commands do not take arguments:

```shell
doing open board
doing open issues
doing open pipe
doing open prs
doing open repo
doing open sprint
doing open policies
```

Some do:

```shell
doing open issue 12345
doing open branch master
doing open pr 54321
```

And for some it is optional (attempts to auto-detect argument):

```shell
doing open issue
```

## Options

```nohighlight
{{ shell_out('doing open --help') }}
```
