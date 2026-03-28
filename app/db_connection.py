import os
from pymongo import MongoClient

# --------------------------
# MongoDB connection
# --------------------------
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

url = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(url)
db = client[DATABASE_NAME]