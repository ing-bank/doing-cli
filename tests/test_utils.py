from doing.utils import to_snake_case


def test_to_snake_case():
    """
    Test to_snake_case works.
    """
    assert to_snake_case("Some kind of string!") == "some_kind_of_string!"
    assert to_snake_case("") == ""
    assert to_snake_case("  ") == "__"
