from fastapi import FastAPI
from pymongo import MongoClient, errors
import os, random, string, datetime

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB", "testdb")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "random_data")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/")
def root():
    try:
        client.admin.command("ping")
        return {"message": "FastAPI running", "mongo_status": "connected"}
    except errors.PyMongoError as e:
        return {"message": "FastAPI running", "mongo_status": f"error: {e}"}

@app.get("/data")
def insert_random_data():
    item = {
        "value": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
        "number": random.randint(0, 100),
        "timestamp": datetime.datetime.utcnow()
    }
    result = collection.insert_one(item)
    return {"inserted_id": str(result.inserted_id), "data": item}

