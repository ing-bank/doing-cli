import os
import sys
import json
import yaml
from rich.console import Console
import subprocess
from dotenv import find_dotenv
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


def shell_output(command) -> str:
    """
    Lightweight function to quickly run a shell command.

    For longer queries with json output use 'run_command'
    """
    if verbose_shell():
        console.print(f"[bright_black]{command}[/bright_black]")

    std_out = os.popen(command).read().rstrip()
    std_out = std_out.lstrip('"').rstrip('"')
    return std_out.strip()


def get_az_devop_user_email():
    """
    Retrieves email from azure devops cli configuration.
    """
    email = shell_output("az ad signed-in-user show --query 'mail'")
    assert email, "Could not find azure devops email. Are you logged in?"
    return email


def get_git_current_branch():
    """
    Get name of current branch in git.
    """
    branch = shell_output("git branch --show-current")
    assert branch, "Could not retrieve current git branch. Is your working directory a git repository?"
    return branch


def get_git_user_email():
    """
    Gets emailadres from git config.
    """
    email = shell_output("git config user.email")
    assert email, "Could not find git email. Are you in a git repository? Do you have your git config setup?"
    return email


def get_repo_name():
    """
    Determines name of remote origin repo.
    """
    origin_url = shell_output("git config --get remote.origin.url")
    assert origin_url, "This repository has no remote.origin.url. Is it created on azure devops yet?"

    repo_name = shell_output(f"basename -s .git {origin_url}")
    return repo_name


def get_config(key: str = "", fallback: str = None, envvar_prefix: str = "DOING_CONFIG_"):
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

    # Find the config file
    conf_path = find_dotenv(".doing-cli-config.yml", usecwd=True)
    if not conf_path:
        if fallback is not None:
            return fallback
        raise FileNotFoundError("Could not find the configuration file '.doing-cli-config.yml'")

    # Load the config file
    with open(conf_path) as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    if not key:
        return conf

    try:
        return conf[key]
    except KeyError:
        if fallback is not None:
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


def verbose_shell():
    """
    If shell commands should be printed.

    Users can define 'verbose_shell: True' in the .doing-cli-config.yml file.
    """
    return get_config("verbose_shell", fallback=False)


def define_env(env):
    """
    Macros for mkdocs_macros_plugin.
    """

    @env.macro
    def shell_out(command: str):
        return shell_output(command)
