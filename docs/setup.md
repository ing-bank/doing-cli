# Setup

## Installing Azure CLI

`doing` basically wraps the `az` CLI tool, and we need to install it in order to deal with authentication and such.

- Install [azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Install [azure cli devops extension](https://docs.microsoft.com/en-us/azure/devops/cli/?view=azure-devops)

If you're on mac, you can do this via the command line:

```shell
brew update && brew install azure-cli
az extension add --name azure-devops
```

## Setting up authentication

Create a personal access token (PAT):

- Open [dev.azure.com](https://dev.azure.com/) in your browser and sign in with your ING account.
- Navigate to [dev.azure.com/IngEurCDaaS01/](https://dev.azure.com/IngEurCDaaS01/)
- In the top right setting menu choose 'Personal Access Token'. See [detailed guide](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page).
- You might want to save this token somewhere safe, like in your password manager. Alternatively, you can use this only once in the step below, and forgot about it (you can create a new one easily and login again with that one).

You can now login to azure devops using your PAT:

```bash
az devops login
```

## Setting up ING certificates (_optional_)

You might want to interface with Azure Devops while connected to the ING VPN.
To do that, you need to install the ING certificate bundle, which is a lot easier than it sounds.

- Follow the [ING python developer certificate setup guide](https://academy.ing.net/learn/developer-setup/academy/generic/README#8)
- Run the following command: `export REQUESTS_CA_BUNDLE=$HOME/Developer/ING/certificates/ing.ca-bundle`.
   - You will need to re-run this command everytime you start your bash session, so you might want to update your `.bashrc`.
   - You will need to `unset REQUESTS_CA_BUNDLE` when you disconnect from the ING network 


## Per repository setup

Due to the setup of ING's Azure Devops, there is a decoupling of a repository and boards. This means we cannot automatically link a repo with a team, iteration (sprint), or area path.

This means we will need to setup a configuration file per repository.
Create a `.devops-ing` file in the root of your repository.

```yaml
# .devops-ing
# Config file to be used with the `doing` CLI tool
organization=IngEurCDaaS01
project=IngOne
area=taco
team=T01894-RiskandPricingAdvancedAna
iteration=taco_sprint1
```

??? info "How to fill in the configuration"

    `organization`
    :   Name of the organization. Almost always "IngEurCDaaS01"

    `project`
    :   bla bla

    `area`
    :   bla bla

    `team`
    :   bla bla

    `repo`
    :   bla bla

    `iteration`
    :   bla bla

# Verifying the setup

In the root of your repository, you can check if your configuration works using:

```bash
doing status
```