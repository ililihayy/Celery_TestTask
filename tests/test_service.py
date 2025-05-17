from unittest.mock import patch, Mock
from json import JSONDecodeError
import requests

from app.service import fetch_data


def test_fetch_data_success() -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = fetch_data("http://example.com")
        assert result == {"key": "value"}


def test_fetch_data_http_error() -> None:
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        result = fetch_data("http://example.com")
        assert result is None


def test_fetch_data_json_decode_error() -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = JSONDecodeError("Expecting value", "doc", 0)

    with patch("requests.get", return_value=mock_response):
        result = fetch_data("http://example.com")
        assert result is None


def test_fetch_data_request_exception() -> None:
    with patch("requests.get", side_effect=requests.ConnectionError("Connection failed")):
        result = fetch_data("http://example.com")
        assert result is None
