import pytest

from doing.list._list import build_table, work_item_query


@pytest.fixture
def work_items():
    """Create a mock list of work items."""
    work_items = [
        {
            "fields": {
                "System.AssignedTo": {
                    "descriptor": "descriptor_mock_value",
                    "displayName": "John Doe",
                    "id": "id_mock_value",
                    "imageUrl": "https://imageUrl.mock.value",
                    "uniqueName": "john.doe@email.com",
                    "url": "https://url.mock.value",
                },
                "System.CreatedDate": "2022-01-11T12:00:00.000Z",
                "System.Id": 1,
                "System.State": "Active",
                "System.Title": "Mock User Story work item",
                "System.WorkItemType": "User Story",
            },
            "id": 1,
            "relations": None,
            "rev": 5,
            "url": "https://dev.azure.com/mockProject/_apis/wit/workItems/1",
        },
        {
            "fields": {
                "System.CreatedDate": "2022-02-15T12:00:00.000Z",
                "System.Id": 2,
                "System.State": "New",
                "System.Title": "Mock Task work item",
                "System.WorkItemType": "Task",
            },
            "id": 2,
            "relations": None,
            "rev": 3,
            "url": "https://dev.azure.com/mockProject/_apis/wit/workItems/2",
        },
    ]
    return work_items


@pytest.fixture
def workitem_prs():
    """Create a mock list of work items and their associated PRs."""
    workitem_prs = {1: ["3"], 2: ["4"]}
    return workitem_prs


def test_build_table_show_state(work_items, workitem_prs):
    """Test the show_state option of the build_table function."""
    iteration = "Test Iteration"

    # Generate table without state column
    table = build_table(
        work_items=work_items, workitem_prs=workitem_prs, iteration=iteration, last_build=False, show_state=False
    )
    headers = [col.header for col in table.columns]
    assert "State" not in headers

    # Generate table with state column
    table = build_table(
        work_items=work_items, workitem_prs=workitem_prs, iteration=iteration, last_build=False, show_state=True
    )
    headers = [col.header for col in table.columns]
    assert "State" in headers

    # Check if state column values are correct
    state_col = [col for col in table.columns if col.header == "State"][0]
    work_item_states = []
    for item in work_items:
        work_item_states.append(item.get("fields").get("System.State"))
    assert state_col._cells == work_item_states


def test_work_item_query_state(mocker):
    """Test the state argument of the work_item_query function."""
    settings = {
        "area": "test\\area",
        "iteration": "test\\iteration",
        "assignee": "",
        "author": "",
        "label": "",
        "work_item_type": "",
        "story_points": "",
    }

    # No state is passed
    query = work_item_query(state=None, **settings)
    assert "AND [System.State]" not in query

    # 'open' state is passed
    query = work_item_query(state="open", **settings)
    assert "AND [System.State] NOT IN ('Resolved','Closed','Done','Removed') " in query

    # arbitrary state is passed
    query = work_item_query(state="'Active'", **settings)
    assert "AND [System.State] = 'Active' " in query

    # invalid state is passed
    with pytest.raises(ValueError):
        work_item_query(state="exception", **settings)

    # mock a 'custom_states' setting
    mocker.patch("doing.list._list.get_config", return_value={"test1": "Active", "test2": ["Active", "Resolved"]})

    # custom state with 1 state is passed
    query = work_item_query(state="test1", **settings)
    assert "AND [System.State] IN ('Active') " in query

    # custom state with 2 states is passed
    query = work_item_query(state="test2", **settings)
    assert "AND [System.State] IN ('Active','Resolved') " in query
