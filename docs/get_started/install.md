# Installation

## Installing the tool

You can install the tool with

```shell
pip install <ssh link to repo>
```

You should then be able to run `doing`:

```bash
doing --help
```

## Installing Azure CLI

`doing` basically wraps the Azure's `az` CLI tool, so we need to install it in order to deal with authentication and such.

- Install [azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Install [azure cli devops extension](https://docs.microsoft.com/en-us/azure/devops/cli/?view=azure-devops)

If you're on mac, you can install both quickly via the command line:

```shell
brew update && brew install azure-cli
az extension add --name azure-devops
```