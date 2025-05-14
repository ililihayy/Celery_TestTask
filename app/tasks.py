from celery import Celery
import requests
from .db import users_collection, addresses_collection, credit_cards_collection
from .config import CELERY_BROKER

app = Celery("tasks", broker=CELERY_BROKER)


@app.task
def fetch_users() -> str:
    fetched = requests.get("https://jsonplaceholder.typicode.com/users")
    users = fetched.json()
    inserted = 0
    for user in users:
        existing = users_collection.find_one({"id": user["id"]})
        if not existing:
            users_collection.insert_one(user)
            inserted += 1
    return f"Inserted {inserted} users"


@app.task
def fetch_addresses() -> str:
    users = list(users_collection.find())
    updated = 0
    for user in users:
        fetched = requests.get("https://random-data-api.com/api/address/random_address")
        address = fetched.json()
        address["uid"] = user["id"]
        addresses_collection.update_one({"uid": user["id"]}, {"$set": address}, upsert=True)
        updated += 1
    return f"Updated {updated} addresses"


@app.task
def fetch_credit_cards() -> str:
    users = list(users_collection.find())
    updated = 0
    for user in users:
        fetched = requests.get("https://random-data-api.com/api/v2/credit_cards")
        credit_card = fetched.json()
        credit_card["uid"] = user["id"]
        credit_cards_collection.update_one({"uid": user["id"]}, {"$set": credit_card}, upsert=True)
        updated += 1
    return f"Updated {updated} credit cards"
