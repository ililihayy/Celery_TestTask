from pymongo import MongoClient
from .config import MONGO_URI, MONGO_DB_NAME

client: MongoClient = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

users_collection = db["users"]
addresses_collection = db["addresses"]
credit_cards_collection = db["credit_cards"]
