import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = "user_data"

CELERY_BROKER = os.getenv("CELERY_BROKER", "amqp://localhost")
