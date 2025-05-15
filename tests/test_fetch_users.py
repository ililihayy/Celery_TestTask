from unittest.mock import patch, MagicMock
from app.tasks import fetch_users
from typing import Optional, Dict, Any


def test_fetch_users_inserts_new_users() -> None:
    mock_api_response = MagicMock()
    mock_api_response.json.return_value = [{"id": 1, "name": "Existing User"}, {"id": 2, "name": "New User"}]

    mock_collection = MagicMock()

    def mock_find_one(query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if query.get("id") == 1:
            return {"id": 1, "name": "Existing User"}
        return None

    mock_collection.find_one.side_effect = mock_find_one

    with (
        patch("app.tasks.requests.get", return_value=mock_api_response),
        patch("app.tasks.users_collection", mock_collection),
    ):
        result = fetch_users()

        assert result == "Inserted 1 users"

        mock_collection.insert_one.assert_called_once_with({"id": 2, "name": "New User"})


def test_fetch_users_when_all_exist() -> None:
    mock_api_response = MagicMock()
    mock_api_response.json.return_value = [{"id": 1, "name": "Existing User 1"}, {"id": 2, "name": "Existing User 2"}]

    mock_collection = MagicMock()
    mock_collection.find_one.return_value = True

    with (
        patch("app.tasks.requests.get", return_value=mock_api_response),
        patch("app.tasks.users_collection", mock_collection),
    ):
        result = fetch_users()
        assert result == "Inserted 0 users"
        mock_collection.insert_one.assert_not_called()


def test_fetch_users_when_none_exist() -> None:
    mock_api_response = MagicMock()
    mock_api_response.json.return_value = [{"id": 1, "name": "New User 1"}, {"id": 2, "name": "New User 2"}]

    mock_collection = MagicMock()
    mock_collection.find_one.return_value = None
    with (
        patch("app.tasks.requests.get", return_value=mock_api_response),
        patch("app.tasks.users_collection", mock_collection),
    ):
        result = fetch_users()
        assert result == "Inserted 2 users"
        assert mock_collection.insert_one.call_count == 2
