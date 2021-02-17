# Setup authentication

--8<-- "docs/assets/abbreviations.md"

`doing` needs authentication to Azure Devops in order to work. The easiest way to provide authorization is through using a *personal access token* (PAT).

## Creating a personal access token

- Open [dev.azure.com](https://dev.azure.com/) in your browser and sign in with your account.
- Navigate to your organization's devops space. (for example *dev.azure.com/IngEurCDaaS01/*)
- In the top right menu, click on the user gear icon (:fontawesome-solid-user-cog:) and choose 'Personal Access Token' to create a token. See this [guide](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page) for more detailed instructions.
- Don't worry about losing this token: you can create a new one easily and just login again with that one.

You can now login to azure devops, pasting your PAT when prompted:

<div class="termy">

```console
$ az devops login
Token: 
```

</div>

If you want to check if you are logged in and have a connection, run the commands `az account show -o jsonc` and `az devops project list -o jsonc`. You should see a JSON response. Not working? See [Connection problems](http://localhost:8000/howto/connection_problems/).