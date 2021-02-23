import os
import pytest
from doing.utils import to_snake_case, get_config


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
