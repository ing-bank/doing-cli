import os
import pytest
import yaml
from doing.utils import get_az_devop_user_email, remove_special_chars, to_snake_case, get_config, replace_user_aliases

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
    assert to_snake_case("  ") == ""
    assert to_snake_case("snake_case") == "snake_case"
    assert to_snake_case("! weird @ chars #") == "!_weird_@_chars_#"


def test_remove_special_chars():
    """
    Test remove_special_chars.
    """
    assert remove_special_chars("@tim hi there!") == "tim hi there"
    assert remove_special_chars("@#$^&*()!") == ""
    assert remove_special_chars("123456790") == "123456790"
    assert remove_special_chars(r"\--/") == ""
    assert remove_special_chars("my-project") == "myproject"


def test_creating_branchnames():
    """
    Combines testing remove_special_chars and to_snake_case.
    """
    assert to_snake_case(remove_special_chars(r"My issue! ~ solves #12 \--/ :)")) == "my_issue_solves_12"
    assert to_snake_case(remove_special_chars("! # issue %")) == "issue"


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
    # no aliases set just yet
    text = "john another_john@company.com john_doe@email.com"
    assert replace_user_aliases(text) == "john another_john@company.com john_doe@email.com"

    config = {"user_aliases": {"john": "john.doe@email.net", "jane": "jane.doe@webmail.org"}}

    with working_directory(tmp_path):

        with open(".doing-cli-config.yml", "w") as file:
            yaml.dump(config, file)

        text = "john another_john@company.com john_doe@email.com"
        assert replace_user_aliases(text) == "john.doe@email.net another_john@company.com john_doe@email.com"

        text = "john another_john@company.com john_doe@email.com"
        assert replace_user_aliases(text) == "john.doe@email.net another_john@company.com john_doe@email.com"

        text = "john jane john"
        assert replace_user_aliases(text) == "john.doe@email.net jane.doe@webmail.org john.doe@email.net"

        text = "johnjane"
        assert replace_user_aliases(text) == "johnjane"


@pytest.mark.skip(reason="Only works when logged into az, not on CI builds")
def test_me_alias():
    """
    Only runs in env where you can get user alias.
    """
    # test @me alias
    text = get_az_devop_user_email()
    assert replace_user_aliases(text) == get_az_devop_user_email()


def test_create_file(tmp_path):
    """
    Test reading a config file.
    """
    config = {"user_aliases": {"john": "john.doe@email.net", "jane": "jane.doe@webmail.org"}}

    with working_directory(tmp_path):

        with open(".doing-cli-config.yml", "w") as file:
            yaml.dump(config, file)

        assert get_config("user_aliases") == config["user_aliases"]
