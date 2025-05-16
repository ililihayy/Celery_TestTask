import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB_NAME = "user_data"

CELERY_BROKER = os.getenv("CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672//")

API_USERS = "https://jsonplaceholder.typicode.com/users"
API_ADDRESSES = "https://random-data-api.com/api/address/random_address"
API_CREDIT_CARDS = "https://random-data-api.com/api/v2/credit_cards"
