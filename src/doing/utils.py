
import os
import sys
import json
from rich.console import Console
import subprocess
from dotenv import find_dotenv, dotenv_values

from doing.exceptions import ConfigurationError

console = Console()
REQUESTS_CA_BUNDLE = os.path.expanduser("~/Developer/ING/certificates/ing.ca-bundle")

def get_config(key = ""):
    conf = dotenv_values(find_dotenv('.devops-ing'))
    if not conf or len(conf) == 0:
        raise FileNotFoundError("Could not find the configuration file '.devops-ing'")

    if key:
        try:
            return conf[key]
        except KeyError:
            raise ConfigurationError(f"Your '.devops-ing' configuration file does not contain an entry for '{key}'")
    
    return conf


def pprint(obj):
    print(json.dumps(obj, indent=2))

def set_requests_bundle():
    """
    In order to be able to connect to azure devops via the command.
    
    1) Setup certificates via guide https://academy.ing.net/learn/developer-setup/academy/generic/README#8
    2) Set the REQUESTS_CA_BUNDLE environment variable
    
    This functions fixes that the shell invoked by subprocess.run() 
    might not have the REQUESTS_CA_BUNDLE env var set.
    """
    os.environ["REQUESTS_CA_BUNDLE"] = REQUESTS_CA_BUNDLE
    console.print(f"Set environment variable REQUESTS_CA_BUNDLE={REQUESTS_CA_BUNDLE}")


def run_command(command, return_process=False):
    process = subprocess.run([command],
                         stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                        #  universal_newlines=True,
                         shell=True)
    
    if return_process:
        return process
    
    if process.returncode != 0:
        console.print(f"[red]{process.stderr}[/red]")
        sys.exit(process.returncode)
    
    return json.loads(process.stdout)
