from doing.init._init import parse_reference


def test_parse_reference():
    """
    Test extracting info from a work item url.
    """
    url = "https://dev.azure.com/IngEurCDaaS01/IngOne/_workitems/edit/73554"
    assert parse_reference(url) == (
        "IngEurCDaaS01",
        "IngOne",
        "73554",
    )
    url = "https://dev.azure.com/IngEurCDaaS01/IngOne/_boards/board/t/"
    url += "T01894-RiskandPricingAdvancedAna/Stories/?workitem=73554"
    assert parse_reference(url) == ("IngEurCDaaS01", "IngOne", "73554")
