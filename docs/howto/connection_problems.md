# How to fix connection problems

Some basic things to try:

- In addition to logging in through `az devops login`, make sure you are logged in to the azure devops environment on the browser as well (you need to go through the 2 factor authentication befor the command line interface works). You can do this using `az login`.
- Upgrade azure cli with `az upgrade` ([azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)).
- Disconnect from any company VPNs and check if everything works.
- Try renewing your personal access token and logging in once again through `az devops login`.

## Working behind a company proxy / virtual private network (VPN)

First check that you can access the internet from your shell. For example, try cloning a public repository or updating a package using `pip` through the public PyPi repository. If you cannot, contact your company's IT.

If you want to connect to azure devops while connected to a VPN (behind a proxy), you can try the following:

1. Install your companies's certificates, and set the environment variable `REQUESTS_CA_BUNDLE` to point to the certificate bundle.
1. See more information from Azure on [working behind a proxy](https://docs.microsoft.com/en-us/cli/azure/use-cli-effectively#work-behind-a-proxy)
1. [This](https://stackoverflow.com/questions/55463706/ssl-handshake-error-with-some-azure-cli-commands) stackoverflow question suggests trying to set these settings in your shell:
    ```shell
    export ADAL_PYTHON_SSL_NO_VERIFY=1
    export AZURE_CLI_DISABLE_CONNECTION_VERIFICATION=1
    ```


