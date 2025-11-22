import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

client = None
db = None
collection = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client["shadowtrace"]
        collection = db["attacks"]
        print("Connected to MongoDB successfully")
    except Exception as e:
        print("MongoDB connection error:", e)
