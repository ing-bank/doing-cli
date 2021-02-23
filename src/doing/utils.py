import os
import sys
import json
from rich.console import Console
import subprocess
from dotenv import find_dotenv, dotenv_values
from typing import Dict

from doing.exceptions import ConfigurationError, devops_error_tips

from rich.traceback import install

install()
console = Console()


def to_snake_case(string):
    """
    Transform string to snake_case.
    """
    string = string.lower().replace(" ", "_")
    return string


def get_az_devop_user_email():
    """
    Retrieves email from azure devops cli configuration.
    """
    # email = sh.az.ad("signed-in-user","show","--query","mail")
    # email = email.rstrip() # remove trailing newlines.
    email = os.popen("az ad signed-in-user show --query 'mail'").read().rstrip()
    email = email.lstrip('"').rstrip('"')
    assert email, "Could not find azure devops email. Are you logged in?"
    return email


def get_git_current_branch():
    """
    Get name of current branch in git.
    """
    branch = os.popen("git branch --show-current").read().rstrip()
    branch = branch.lstrip('"').rstrip('"')
    assert branch, "Could not retrieve current git branch. Is your working directory a git repository?"
    return branch


def get_git_user_email():
    """
    Gets emailadres from git config.
    """
    email = os.popen("git config user.email").read().rstrip()
    email = email.lstrip('"').rstrip('"')
    assert email, "Could not find git email. Are you in a git repository? Do you have your git config setup?"
    return email


def get_repo_name():
    """
    Determines name of remote origin repo.
    """
    origin_url = os.popen("git config --get remote.origin.url").read().rstrip()
    assert origin_url, "This repository has no remote.origin.url. Is it created on azure devops yet?"

    repo_name = os.popen(f"basename -s .git {origin_url}").read().rstrip()
    return repo_name


def get_config(key: str = "", fallback="", envvar_prefix: str = "DOING_CONFIG_"):
    """
    Finds and reads doing configuration file.

    Note you can overwrite a value in the config by setting an environment variable:

    ```python
    import os
    os.environ["DOING_TEAM"] = "my team"

    from doing.utils import get_config
    assert get_config("team") == "my team"
    ```

    Args:
        key (str): Name of config item to return
        fallback (str): Value to return if key cannot be found.
        envvar_prefix (str): prefix before key to look for in environment variables
    """
    # Allow environment variable override
    if key:
        env_var = os.getenv(f"{envvar_prefix}{key.upper()}")
        if env_var:
            return env_var

    conf = dotenv_values(find_dotenv(".doing-cli-config.yml", usecwd=True))
    if not conf or len(conf) == 0:
        if fallback:
            return fallback
        raise FileNotFoundError("Could not find the configuration file '.doing-cli-config.yml'")

    if not key:
        return conf

    try:
        return conf[key]
    except KeyError:
        if fallback:
            return fallback

        msg = f"Your '.doing-cli-config.yml' configuration file does not contain an entry for '{key}'."
        msg += f"\nAlso no environment variable found with {envvar_prefix}{key}"
        raise ConfigurationError(msg)


def pprint(obj: Dict) -> None:
    """
    Pretty print dictionaries.
    """
    print(json.dumps(obj, indent=2))


def run_command(command: str):
    """
    Run a shell command.
    """
    process = subprocess.run(
        [command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        #  universal_newlines=True,
        shell=True,
    )

    if process.returncode != 0:
        console.print(f"[bright_black]{command}[/bright_black]")
        console.print(f"[dark_orange3]{str(process.stderr)}[/dark_orange3]")
        # Help the user
        devops_error_tips(str(process.stderr))
        sys.exit(process.returncode)

    if process.stdout:
        return json.loads(process.stdout)
    else:
        return []
