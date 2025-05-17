import requests
from typing import Any
from json.decoder import JSONDecodeError


def fetch_data(url: str) -> Any:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, JSONDecodeError) as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None
