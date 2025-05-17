from unittest.mock import Mock, patch

from app.tasks import fetch_users, fetch_addresses, fetch_credit_cards, fetch_all


@patch("app.tasks.insert_users")
@patch("app.tasks.fetch_data")
def test_fetch_users(mock_fetch_data: Mock, mock_insert_users: Mock) -> None:
    mock_fetch_data.return_value = [{"id": 1}]
    mock_insert_users.return_value = 1

    result = fetch_users()

    assert result == "Inserted 1 users"
    mock_fetch_data.assert_called_once()
    mock_insert_users.assert_called_once_with([{"id": 1}])


@patch("app.tasks.insert_addresses")
def test_fetch_addresses(mock_insert_addresses: Mock) -> None:
    mock_insert_addresses.return_value = 2

    result = fetch_addresses()

    assert result == "Inserted 2 addresses"
    mock_insert_addresses.assert_called_once()


@patch("app.tasks.insert_credit_cards")
def test_fetch_credit_cards(mock_insert_cards: Mock) -> None:
    mock_insert_cards.return_value = 3

    result = fetch_credit_cards()

    assert result == "Inserted 3 credit cards"
    mock_insert_cards.assert_called_once()


@patch("app.tasks.fetch_users.delay")
@patch("app.tasks.fetch_addresses.delay")
@patch("app.tasks.fetch_credit_cards.delay")
def test_fetch_all(mock_cards: Mock, mock_addresses: Mock, mock_users: Mock) -> None:
    fetch_all()

    mock_users.assert_called_once()
    mock_addresses.assert_called_once()
    mock_cards.assert_called_once()
