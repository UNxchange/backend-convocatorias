import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_URL")
MONGO_DB = os.getenv("MONGODB_DB")

client = None
db = None

async def connect():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    db = client[MONGO_DB]

async def close():
    client.close()