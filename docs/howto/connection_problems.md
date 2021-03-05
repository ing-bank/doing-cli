# How to fix connection problems

Some basic things to try:

- In addition to logging in through `az devops login`, make sure you are logged in to the azure devops environment on the browser as well (you need to go through the 2 factor authentication befor the command line interface works). You can do this using `az login`.
- Upgrade azure cli with `az upgrade` ([azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)).
- Disconnect from any company VPNs and check if everything works.
- Try renewing your personal access token and logging in once again through `az devops login`.

## Working behind a corporate proxy / virtual private network (VPN)

First check that you can access the internet from your shell. 
When connected to a VPN, your company may require you to do this behind a corporate proxy. 
For example, try cloning a public repository or updating a package using `pip` through the public PyPi repository. 
If you cannot, contact your company's IT.

To use Azure DevOps, you might have to add the certificates of your company to the ones from [`certifi`](https://pypi.org/project/certifi/), which the Python `requests` package uses to connect to the internet.
If this is the case, you will receive an error indicating that you might not have the right certificates to connect to Azure DevOps.

To fix this you must install your company's certificates. 
Then, set the environment variable `REQUESTS_CA_BUNDLE` to a bundle of your company's and `certifi`'s certificate bundles with `export REQUESTS_CA_BUNDLE=<bundle location>`.

You can add the following script to the end of your `.zshrc` to keep the certificate bundle up-to-date:
```bash
# Set CA bundle certificate for doing-cli to connect to AzDo
CERTIFICATES_DIR=$HOME/Documents/certificates
## Check if there's a new version of the certifi bundle
if ! cmp -s $CERTIFICATES_DIR/certifi.ca-bundle $(python -m certifi) ; then
    echo "certifi has new certificates. Updating the local certificate bundle."
    cat $(python -m certifi) > $CERTIFICATES_DIR/certifi.ca-bundle
    cat $CERTIFICATES_DIR/<corporate.ca-bundle> $CERTIFICATES_DIR/certifi.ca-bundle > $CERTIFICATES_DIR/corporate-certifi.ca-bundle
fi
export REQUESTS_CA_BUNDLE=$CERTIFICATES_DIR/corporate-certifi.ca-bundle
```
where:
- `CERTIFICATES_DIR` is the directory where your company's certificate bundle is stored;
- <corporate.ca-bundle> is your company's certificate bundle;

See more information from Azure on [working behind a proxy](https://docs.microsoft.com/en-us/cli/azure/use-cli-effectively#work-behind-a-proxy)


