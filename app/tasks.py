from celery import Celery
from .config import CELERY_BROKER, API_USERS
from .service import fetch_data
from .repository import insert_users, insert_addresses, insert_credit_cards

app = Celery("tasks", broker=CELERY_BROKER, backend="rpc://")


@app.task
def fetch_users() -> str:
    fetched = fetch_data(API_USERS)
    inserted = insert_users(fetched)
    return f"Inserted {inserted} users"


@app.task
def fetch_addresses() -> str:
    inserted = insert_addresses()
    return f"Inserted {inserted} addresses"


@app.task
def fetch_credit_cards() -> str:
    inserted = insert_credit_cards()
    return f"Inserted {inserted} credit cards"


def fetch_all() -> None:
    fetch_users.delay()
    fetch_addresses.delay()
    fetch_credit_cards.delay()
