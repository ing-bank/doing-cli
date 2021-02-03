# Setup authentication

Authentication is easy using a personal access token (PAT).

## Creating a personal access token

- Open [dev.azure.com](https://dev.azure.com/) in your browser and sign in with your account.
- Navigate to your organization's devops space. (for example *dev.azure.com/IngEurCDaaS01/*)
- In the top right setting menu choose 'Personal Access Token' and create a token. See this [detailed guide](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page) for more instructions.
- Don't worry about losing this token: you can create a new one easily and just login again with that one.

You can now login to azure devops, pasting your PAT when prompted:

<div class="termy">

```console
$ az devops login
Token: 
```

</div>