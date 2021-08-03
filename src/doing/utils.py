import os
import sys
import json
import yaml
import re
import string
import psutil

from platform import uname
from rich.console import Console
import subprocess
from typing import Dict, Union, Text, Iterator
from collections import OrderedDict

from doing.exceptions import ConfigurationError, devops_error_tips

from rich.traceback import install

from functools import lru_cache

install()
console = Console()


def to_snake_case(text: str) -> str:
    """
    Transform string to snake_case.
    """
    text = re.sub(" +", " ", text)
    text = text.lower().strip().replace(" ", "_")
    return text


def remove_special_chars(text: str) -> str:
    """
    Removes all special characters from a string.
    """
    chars = re.escape(string.punctuation)
    return re.sub(r"[" + chars + "]", "", text)


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


@lru_cache(maxsize=100)
def get_az_devop_user_email():
    """
    Retrieves email from azure devops cli configuration.
    """
    email = shell_output("az ad signed-in-user show --query 'mail'")
    assert email, "Could not find azure devops email. Are you logged in?"
    return email


@lru_cache(maxsize=100)
def get_git_current_branch():
    """
    Get name of current branch in git.
    """
    branch = shell_output("git branch --show-current")
    assert branch, "Could not retrieve current git branch. Is your working directory a git repository?"
    return branch


@lru_cache(maxsize=100)
def get_git_user_email():
    """
    Gets emailadres from git config.
    """
    email = shell_output("git config user.email")
    assert email, "Could not find git email. Are you in a git repository? Do you have your git config setup?"
    return email


@lru_cache(maxsize=100)
def get_repo_name():
    """
    Determines name of remote origin repo.
    """
    origin_url = shell_output("git config --get remote.origin.url")
    assert origin_url, "This repository has no remote.origin.url. Is it created on azure devops yet?"

    repo_name = shell_output(f"basename -s .git {origin_url}")
    return repo_name


def _walk_to_root(path: Text) -> Iterator[Text]:
    """
    Yield directories starting from the given directory up to the root.

    Credits:
    https://github.com/theskumar/python-dotenv
    """
    if not os.path.exists(path):
        raise IOError("Starting path not found")

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_dotfile() -> str:
    """
    Recursively search directories upwards for a specific file.
    """
    filename = ".doing-cli-config.yml"
    filename2 = ".doing-cli-config.yaml"
    path = os.getcwd()

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path
        check_path = os.path.join(dirname, filename2)
        if os.path.isfile(check_path):
            return check_path

    return ""


def get_config(key: str = "", fallback: Union[str, Dict] = None, envvar_prefix: str = "DOING_CONFIG_"):
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
    conf_path = find_dotfile()

    if not conf_path:
        if fallback is not None:
            return fallback
        raise FileNotFoundError("Could not find the configuration file '.doing-cli-config.yml'")

    # Load the config file
    with open(conf_path) as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    # deprecations
    if key == "default_workitem_type":
        example_type = conf.get(key, "Bug")
        msg = f"""
        The config item 'default_workitem_type' has been deprecated.
        Use 'defaults' instead (see docs). For example:

            ```yaml
            # .doing-cli-config.yml
            defaults:
                DOING_CREATE_ISSUE_TYPE: '{example_type}'
                DOING_WORKON_TYPE: '{example_type}'
            ```
        """
        raise ConfigurationError(msg)

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


def run_command(command: str, allow_verbose=True):
    """
    Run a shell command.

    Args:
        command: The shell command.
        allow_verbose: Allow printing. In some situations verbose
            printing will lead to recursion error with rich.
    """
    if allow_verbose and verbose_shell():
        console.print(f"[bright_black]{command}[/bright_black]")

    encoding = get_config("encoding", "")
    if encoding == "":
        encoding = guess_shell_encoding()

    try:
        process = subprocess.run(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding=encoding,
            shell=True,
            timeout=15,
        )
    except subprocess.TimeoutExpired as e:
        console.print(e)
        sys.exit(1)

    if process.returncode != 0:
        console.print(f"There was an error. Ran the following command with encoding '{encoding}':")
        console.print(f"[bright_black]{command}[/bright_black]")
        if process.stdout:
            console.print(f"[dark_orange3]{process.stdout}[/dark_orange3]")
        if process.stderr:
            console.print(f"[dark_orange3]{process.stderr}[/dark_orange3]")

        # Help the user
        devops_error_tips(str(process.stderr))
        sys.exit(process.returncode)

    if process.stdout:
        try:
            return json.loads(process.stdout)
        except Exception:
            console.print("[doing-cli] error: Could not process the following stdout as a JSON:")
            console.print(f"[dark_orange3]{process.stdout}[/dark_orange3]")
            sys.exit(1)
    else:
        return []


@lru_cache(maxsize=100)
def guess_shell_encoding() -> str:
    """
    Try to determine the encoding used by host shell.
    """
    # Issue with Windows Subsystem for linux
    # where "echo $LC_ALL" says UTF-8
    # but bytes in stdout are actually in windows-1252 encoding
    # Detect if running inside Windows System For Linux (WSL).
    # WSL is thought to be the only common Linux kernel with Microsoft in the name, per Microsoft:
    # https://github.com/microsoft/WSL/issues/4071#issuecomment-496715404
    if "Microsoft" in uname().release:
        return "windows-1252"
    # Same issue for windows powershell
    # how to detect:
    # https://stackoverflow.com/a/59459612/5525118
    process_name = str(psutil.Process(os.getppid()).name()).lower()
    if "powershell" in process_name:
        return "cp1252"
    elif "cmd.exe" in process_name:
        return "cp1252"
    else:
        return sys.stdout.encoding


def verbose_shell():
    """
    If shell commands should be printed.

    Users can define 'verbose_shell: True' in the .doing-cli-config.yml file.
    """
    return get_config("verbose_shell", fallback=False)


def define_env(env):
    """
    Macros for mkdocs_macros_plugin.

    Allows use to use jinja2 tags inside .md files in docs/.

    For example '{{ shell_out('echo hello') }}' would be replaced by 'hello'

    More info: https://mkdocs-macros-plugin.readthedocs.io/
    """

    @env.macro
    def shell_out(command: str):
        return shell_output(command)


def replace_user_aliases(text: str) -> str:
    """
    Replace alias with emailadres in a string.

    User aliases are defined under 'user_aliases' in the .doing-cli.config.yml file.
    Additionally, the @me alias point to current user.
    """
    words = text.split()
    words = list(OrderedDict.fromkeys(words))  # deduplicate keeping ordering

    aliases = get_config("user_aliases", {})

    # If the user is logged in, replace the @me alias
    # Otherwise, just move on. Helps with unit testing on CI.
    try:
        aliases["@me"] = get_az_devop_user_email()
    except Exception:
        pass

    if not aliases:
        return " ".join(words)
    else:
        return " ".join([aliases.get(word, word) for word in words])


def get_current_work_item_id():
    """
    Retrieves current work item id from the current branchname.
    """
    branch_name = shell_output("git branch --show-current")
    wi_id = re.search(r"^([0-9]+)_", branch_name)
    if wi_id is None or len(wi_id.group(1)) == 0:
        console.print(
            "Could not find work item id in current branch name: "
            + get_git_current_branch()
            + " (usually the branch name starts with the workitem id)"
        )
        sys.exit(1)
    return wi_id.group(1)


def get_current_pr_id() -> int:
    """
    Find the current PR id based on the git branch name.
    """
    organization = get_config("organization")
    project = get_config("project")

    current_branch = get_git_current_branch()
    repo_name = get_repo_name()

    cmd = 'az repos pr list --status "active" '
    cmd += f'--repository "{repo_name}" --source-branch "{current_branch}" '
    cmd += f'--project "{project}" --organization "{organization}"'

    result = run_command(cmd)

    if len(result) == 0:
        console.print("Could not find a PR associated with the current branch: " + get_git_current_branch())
        sys.exit(1)
    else:
        return result[0].get("pullRequestId")


def validate_work_item_type(type: str) -> None:
    """
    Check if the work item is in the list of default work items.

    The default work items can be checked [here](https://docs.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items?view=azure-devops&tabs=cmmi-process)
    """  # noqa
    default_work_items = [
        "Bug",
        "Epic",
        "Feature",
        "User Story",
        "Issue",
        "Task",
        "Test Case",
        "Product Backlog Item",
        "Requirement",
        "Code Review Request",
        "Code Review Response",
        "Feedback Request",
        "Feedback Response",
        "Shared Step",
        "Shared Parameter",
        "Test Case",
        "Test Plan",
        "Test Suite",
        "Change Request",
        "Review",
        "Risk",
    ]

    if type not in default_work_items:
        console.print(
            f"[dark_orange3]>[/dark_orange3] Warning: '[cyan]{type}[/cyan]' is not in the list of default work items"
        )
