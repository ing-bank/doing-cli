# Setup authentication

## Creating a personal access token

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
