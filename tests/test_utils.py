import os
import pytest
import yaml
from doing.utils import to_snake_case, get_config, replace_user_aliases

from contextlib import contextmanager


@contextmanager
def working_directory(path):
    """
    Temporarily change working directory.

    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    Usage:

    ```python
    # Do something in original directory
    with working_directory('/my/new/path'):
        # Do something in new directory
    # Back to old directory
    ```
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def test_to_snake_case():
    """
    Test to_snake_case works.
    """
    assert to_snake_case("Some kind of string!") == "some_kind_of_string!"
    assert to_snake_case("") == ""
    assert to_snake_case("  ") == "__"


def test_get_config_key():
    """
    Test overrides via env vars.
    """
    os.environ["DOING_CONFIG_TEAM"] = "my team"
    assert get_config("team") == "my team"


def test_get_config_fallbackl():
    """
    Test overrides via env vars.
    """
    with pytest.raises(Exception):
        get_config("team1")

    assert get_config("team1", "foobar") == "foobar"


def test_replace_user_aliases(tmp_path):
    """
    Test replacing user aliases.
    """
    config = {"user_aliases": {"john": "john.doe@email.net", "jane": "jane.doe@webmail.org"}}

    with working_directory(tmp_path):

        with open(".doing-cli-config.yml", "w") as file:
            yaml.dump(config, file)

        text = "john another_john@company.com john_doe@email.com"
        assert replace_user_aliases(text) == "john.doe@email.net another_john@company.com john_doe@email.com"

        text = "john jane john"
        assert replace_user_aliases(text) == "john.doe@email.net jane.doe@webmail.org john.doe@email.net"

        text = "johnjane"
        assert replace_user_aliases(text) == "johnjane"


def test_create_file(tmp_path):
    """
    Test reading a config file.
    """
    config = {"user_aliases": {"john": "john.doe@email.net", "jane": "jane.doe@webmail.org"}}

    with working_directory(tmp_path):

        with open(".doing-cli-config.yml", "w") as file:
            yaml.dump(config, file)

        assert get_config("user_aliases") == config["user_aliases"]
