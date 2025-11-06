import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "Reply to the message from last week that’s been sitting in the inbox.",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "Finally take care of those parking fines before they increase again.",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "Give the flowers and plants a good soak before sunset.",
            "is_complete": False}
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "Give the flowers and plants a good soak before sunset.",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "Finally take care of those parking fines before they increase again.",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "Reply to the message from last week that’s been sitting in the inbox.",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_by_title_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc&description=in")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Finally take care of those parking fines before they increase again.",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "Reply to the message from last week that’s been sitting in the inbox.",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]