from .db import users_collection, addresses_collection, credit_cards_collection
from .service import fetch_data
from .config import API_ADDRESSES, API_CREDIT_CARDS
from .models import User, Address, CreditCard
from typing import List, Dict, Any


def insert_users(fetched: List[Dict[str, Any]]) -> int:
    inserted = 0
    for user_data in fetched:
        try:
            user = User(**user_data)
        except Exception as e:
            print(f"Invalid user data {user_data['id'] if 'id' in user_data else user_data}: {e}")
            continue

        existing = users_collection.find_one({"id": user.id})
        if not existing:
            users_collection.insert_one(user.dict())
            inserted += 1
    return inserted


def insert_addresses() -> int:
    users = list(users_collection.find())
    inserted = 0
    for user in users:
        address_data = fetch_data(API_ADDRESSES)
        if not address_data:
            continue

        address_data["uid"] = user["id"]
        try:
            address = Address(**address_data)
        except Exception as e:
            print(f"Invalid address data for user {user['id']}: {e}")
            continue

        addresses_collection.update_one(
            {"uid": user["id"]},
            {"$set": address.dict()},
            upsert=True,
        )
        inserted += 1
    return inserted


def insert_credit_cards() -> int:
    users = list(users_collection.find())
    inserted = 0
    for user in users:
        credit_card_data = fetch_data(API_CREDIT_CARDS)
        if not credit_card_data:
            continue

        credit_card_data["uid"] = user["id"]
        try:
            credit_card = CreditCard(**credit_card_data)
        except Exception as e:
            print(f"Invalid credit card data for user {user['id']}: {e}")
            continue

        credit_cards_collection.update_one(
            {"uid": user["id"]},
            {"$set": credit_card.dict()},
            upsert=True,
        )
        inserted += 1
    return inserted
