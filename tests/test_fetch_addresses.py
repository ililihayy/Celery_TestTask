from unittest.mock import patch, MagicMock
from app.tasks import fetch_addresses
from typing import Generator


def mock_get_user_addresses() -> Generator[MagicMock, None, None]:
    responses = [
        {"street": "Street 1", "city": "Testville", "zip_code": "11111"},
        {"street": "Street 2", "city": "Exampletown", "zip_code": "22222"},
    ]
    for res in responses:
        mock_response = MagicMock()
        mock_response.json.return_value = res
        yield mock_response


def test_fetch_addresses_updates_all_users() -> None:
    mock_users = [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
    ]

    mock_users_collection = MagicMock()
    mock_users_collection.find.return_value = mock_users

    mock_addresses_collection = MagicMock()

    address_gen = mock_get_user_addresses()
    mock_requests = MagicMock()
    mock_requests.get.side_effect = lambda url: next(address_gen)

    with patch.multiple(
        "app.tasks",
        users_collection=mock_users_collection,
        addresses_collection=mock_addresses_collection,
        requests=mock_requests,
    ):
        result = fetch_addresses()

        assert result == "Updated 2 addresses"
        assert mock_addresses_collection.update_one.call_count == 2

        mock_addresses_collection.update_one.assert_any_call(
            {"uid": 1},
            {
                "$set": {
                    "street": "Street 1",
                    "city": "Testville",
                    "zip_code": "11111",
                    "uid": 1,
                }
            },
            upsert=True,
        )
        mock_addresses_collection.update_one.assert_any_call(
            {"uid": 2},
            {
                "$set": {
                    "street": "Street 2",
                    "city": "Exampletown",
                    "zip_code": "22222",
                    "uid": 2,
                }
            },
            upsert=True,
        )


def test_fetch_addresses_with_empty_users() -> None:
    mock_users_collection = MagicMock()
    mock_users_collection.find.return_value = []

    with patch.multiple(
        "app.tasks", users_collection=mock_users_collection, addresses_collection=MagicMock(), requests=MagicMock()
    ):
        result = fetch_addresses()
        assert result == "Updated 0 addresses"
