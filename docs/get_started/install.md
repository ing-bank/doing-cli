# Installation

## Installing the tool

You can install the tool with

<div class="termy">

```console
$ pip install doing-cli
---> 100%
Successfully installed doing-cli
```

</div>


You should then be able to run `doing`:

<div class="termy">

```console
$ doing

Usage: doing [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list     List issues related to the project.
  nothing  Take a break.
  open     Quickly open certain links
  workon   Work on a new work item.
```

</div>

## Installing Azure CLI

`doing` basically wraps the Azure's `az` CLI tool, so we need to install it in order to deal with authentication and such.

- Install [azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Install [azure cli devops extension](https://docs.microsoft.com/en-us/azure/devops/cli/?view=azure-devops)

If you're on mac, you can install both quickly via the command line:

<div class="termy">

```console
$ brew update && brew install azure-cli
$ az extension add --name azure-devops
```

</div>
