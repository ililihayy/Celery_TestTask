from unittest.mock import Mock, patch
from pymongo.results import InsertOneResult, UpdateResult
from app.repository import insert_users, insert_addresses, insert_credit_cards
from typing import Any, Dict


TEST_USER: Dict[str, Any] = {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
        "street": "Kulas Light",
        "suite": "Apt. 556",
        "city": "Gwenborough",
        "zipcode": "92998-3874",
        "geo": {"lat": "-37.3159", "lng": "81.1496"},
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
        "name": "Romaguera-Crona",
        "catchPhrase": "Multi-layered client-server neural-net",
        "bs": "harness real-time e-markets",
    },
}

TEST_ADDRESS: Dict[str, Any] = {
    "id": 1,
    "city": "Gwenborough",
    "street_name": "Kulas Light",
    "street_address": "Apt. 556",
    "zip_code": "92998-3874",
    "country": "USA",
    "latitude": -37.3159,
    "longitude": 81.1496,
    "full_address": "Kulas Light, Apt. 556, Gwenborough, 92998-3874, USA",
}

TEST_CREDIT_CARD: Dict[str, Any] = {
    "id": 1,
    "credit_card_number": "4539-1488-0343-6467",
    "credit_card_expiry_date": "04/25",
    "credit_card_type": "visa",
}


@patch("app.repository.users_collection")
def test_insert_user_with_full_data(mock_collection: Mock) -> None:
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.return_value = InsertOneResult(1, acknowledged=True)

    inserted = insert_users([TEST_USER])

    assert inserted == 1
    mock_collection.insert_one.assert_called_once()
    inserted_doc = mock_collection.insert_one.call_args[0][0]
    assert inserted_doc["id"] == 1
    assert inserted_doc["name"] == "Leanne Graham"
    assert inserted_doc["address"]["city"] == "Gwenborough"


@patch("app.repository.users_collection")
def test_insert_user_with_missing_optional_fields(mock_collection: Mock) -> None:
    incomplete_user = {"id": 2, "name": "Ervin Howell", "email": "ervin@example.com"}
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.return_value = InsertOneResult(2, acknowledged=True)

    inserted = insert_users([incomplete_user])

    assert inserted == 1
    mock_collection.insert_one.assert_called_once()
    inserted_doc = mock_collection.insert_one.call_args[0][0]
    assert inserted_doc["id"] == 2
    assert inserted_doc["username"] is None
    assert inserted_doc["address"] is None
    assert inserted_doc["company"] is None


@patch("app.repository.users_collection")
def test_insert_user_invalid_data(mock_collection: Mock, capsys: Any) -> None:
    invalid_user = {"email": "invalid@example.com"}

    inserted = insert_users([invalid_user])

    assert inserted == 0
    mock_collection.insert_one.assert_not_called()
    captured = capsys.readouterr()
    assert "Invalid user data" in captured.out


@patch("app.repository.fetch_data")
@patch("app.repository.addresses_collection")
@patch("app.repository.users_collection")
def test_insert_address_success(mock_users: Mock, mock_addresses: Mock, mock_fetch: Mock) -> None:
    mock_users.find.return_value = [{"id": 1}]
    mock_fetch.return_value = TEST_ADDRESS
    mock_addresses.update_one.return_value = UpdateResult({}, acknowledged=True)

    inserted = insert_addresses()

    assert inserted == 1
    mock_addresses.update_one.assert_called_once()
    call_args = mock_addresses.update_one.call_args[0]
    assert call_args[0] == {"uid": 1}
    assert call_args[1]["$set"]["city"] == "Gwenborough"
    assert call_args[1]["$set"]["uid"] == 1


@patch("app.repository.fetch_data")
@patch("app.repository.addresses_collection")
@patch("app.repository.users_collection")
def test_insert_address_no_api_data(mock_users: Mock, mock_addresses: Mock, mock_fetch: Mock) -> None:
    mock_users.find.return_value = [{"id": 1}]
    mock_fetch.return_value = None

    inserted = insert_addresses()

    assert inserted == 0
    mock_addresses.update_one.assert_not_called()


@patch("app.repository.fetch_data")
@patch("app.repository.credit_cards_collection")
@patch("app.repository.users_collection")
def test_insert_credit_card_success(mock_users: Mock, mock_cards: Mock, mock_fetch: Mock) -> None:
    mock_users.find.return_value = [{"id": 1}]
    mock_fetch.return_value = TEST_CREDIT_CARD
    mock_cards.update_one.return_value = UpdateResult({}, acknowledged=True)

    inserted = insert_credit_cards()

    assert inserted == 1
    mock_cards.update_one.assert_called_once()
    call_args = mock_cards.update_one.call_args[0]
    assert call_args[0] == {"uid": 1}
    assert call_args[1]["$set"]["credit_card_number"] == "4539-1488-0343-6467"
    assert call_args[1]["$set"]["uid"] == 1


@patch("app.repository.fetch_data")
@patch("app.repository.credit_cards_collection")
@patch("app.repository.users_collection")
def test_insert_credit_card_invalid_data(mock_users: Mock, mock_cards: Mock, mock_fetch: Mock, capsys: Any) -> None:
    mock_users.find.return_value = [{"id": 1}]
    invalid_card = {"credit_card_number": "1234"}
    mock_fetch.return_value = invalid_card

    inserted = insert_credit_cards()

    assert inserted == 0
    mock_cards.update_one.assert_not_called()
    captured = capsys.readouterr()
    assert "Invalid credit card data" in captured.out
