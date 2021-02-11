# How to fix connection problems

!!! attention "Draft"
    This page is not yet complete.

Some basic things to try:

- Make sure you are logged in to the azure devops environment on the browser as well (you need to go through the 2 factor authentication befor the command line interface works). You can do this using `az login`.
- Upgrade azure cli with `az upgrade` ([azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)).
- Disconnect from any company VPNs
- Try renewing your personal access token.

## Setting up ING certificates (_optional_)

You might want to interface with Azure Devops while connected to the ING VPN.
To do that, you need to install the ING certificate bundle, which is a lot easier than it sounds.

- Follow the [ING python developer certificate setup guide](https://academy.ing.net/learn/developer-setup/academy/generic/README#8)
- Run the following command: `export REQUESTS_CA_BUNDLE=$HOME/Developer/ING/certificates/ing.ca-bundle`.
   - You will need to re-run this command everytime you start your bash session, so you might want to update your `.bashrc`.
   - You will need to `unset REQUESTS_CA_BUNDLE` when you disconnect from the ING network 
