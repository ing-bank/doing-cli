import os
import sys
import json
from rich.console import Console
import sh
import subprocess
from dotenv import find_dotenv, dotenv_values

from doing.exceptions import ConfigurationError, devops_error_tips

console = Console()
REQUESTS_CA_BUNDLE = os.path.expanduser("~/Developer/ING/certificates/ing.ca-bundle")


def to_snake_case(string):
    string = string.lower().replace(" ", "_")
    return string


def get_az_devop_user_email():
    """
    Retrieves email from azure devops
    """
    # email = sh.az.ad("signed-in-user","show","--query","mail")
    # email = email.rstrip() # remove trailing newlines.
    email = os.popen("az ad signed-in-user show --query 'mail'").read().rstrip()
    email = email.lstrip('"').rstrip('"')
    assert email, "Could not find azure devops email. Are you logged in?"
    return email


def get_git_user_email():
    """
    Gets emailadres from git config
    """
    email = sh.git("config", "user.email")
    email = email.rstrip()  # remove trailing newlines.
    assert (
        email
    ), "Could not find git email. Are you in a git repository? Do you have your git config setup?"
    return email


def get_repo_name():
    """
    Determines name of remote origin repo.
    """
    origin_url = os.popen("git config --get remote.origin.url").read().rstrip()
    assert (
        origin_url
    ), "This repository has no remote.origin.url. Is it created on azure devops yet?"

    repo_name = os.popen(f"basename -s .git {origin_url}").read().rstrip()
    return repo_name


def get_config(key=""):

    conf = dotenv_values(find_dotenv(".devops-ing", usecwd=True))
    if not conf or len(conf) == 0:
        raise FileNotFoundError("Could not find the configuration file '.devops-ing'")

    if key:
        try:
            return conf[key]
        except KeyError:
            raise ConfigurationError(
                f"Your '.devops-ing' configuration file does not contain an entry for '{key}'"
            )

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
    process = subprocess.run(
        [command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        #  universal_newlines=True,
        shell=True,
    )

    if return_process:
        return process

    if process.returncode != 0:
        console.print(f"[bright_black]{command}[/bright_black]")
        console.print(f"[red]{process.stderr}[/red]")
        # Help the user
        devops_error_tips(process.stderr)
        sys.exit(process.returncode)

    if process.stdout:
        return json.loads(process.stdout)
    else:
        return []
