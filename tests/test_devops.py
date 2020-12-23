from doing.devops import get_purpose_id

def test_get_purpose_id():
    assert get_purpose_id("P01908-Default") == "P01908"
    assert get_purpose_id("P01908-rpaa_tmd_template") == "P01908"

