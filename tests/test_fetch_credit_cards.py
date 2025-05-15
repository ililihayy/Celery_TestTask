from unittest.mock import patch, MagicMock
from app.tasks import fetch_credit_cards
from copy import deepcopy
from typing import Any


def test_fetch_credit_cards_updates_all_users() -> None:
    mock_users = [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}]

    base_card_response = {"number": "1234-5678-9012-3456", "expiry_date": "12/25", "card_type": "Visa"}

    def mock_get(*args: Any, **kwargs: Any) -> MagicMock:
        mock_resp = MagicMock()
        mock_resp.json.return_value = deepcopy(base_card_response)
        return mock_resp

    mock_users_collection = MagicMock()
    mock_users_collection.find.return_value = mock_users
    mock_credit_cards_collection = MagicMock()

    with patch.multiple(
        "app.tasks",
        users_collection=mock_users_collection,
        credit_cards_collection=mock_credit_cards_collection,
        requests=MagicMock(get=mock_get),
    ):
        result = fetch_credit_cards()

        assert result == "Updated 2 credit cards"
        assert mock_credit_cards_collection.update_one.call_count == 2

        expected_call_1 = (
            {"uid": 1},
            {"$set": {**base_card_response, "uid": 1}},
        )
        expected_call_2 = (
            {"uid": 2},
            {"$set": {**base_card_response, "uid": 2}},
        )

        mock_credit_cards_collection.update_one.assert_any_call(*expected_call_1, upsert=True)
        mock_credit_cards_collection.update_one.assert_any_call(*expected_call_2, upsert=True)


def test_fetch_credit_cards_with_empty_users() -> None:
    mock_users_collection = MagicMock()
    mock_users_collection.find.return_value = []

    with patch.multiple(
        "app.tasks", users_collection=mock_users_collection, credit_cards_collection=MagicMock(), requests=MagicMock()
    ):
        result = fetch_credit_cards()
        assert result == "Updated 0 credit cards"
