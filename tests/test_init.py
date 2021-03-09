from doing.init._init import parse_reference


def test_parse_reference():
    """
    Test extracting info from a work item url.
    """
    url = "https://dev.azure.com/MyOrganization/MyProject/_workitems/edit/73554"
    assert parse_reference(url) == (
        "MyOrganization",
        "MyProject",
        "73554",
    )
    url = "https://dev.azure.com/MyOrganization/MyProject/_boards/board/t/"
    url += "MyTeam/Stories/?workitem=73554"
    assert parse_reference(url) == ("MyOrganization", "MyProject", "73554")
