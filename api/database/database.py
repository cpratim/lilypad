import pymongo, pytz
from datetime import datetime
import json
from config import MONGODB_DBNAME as dbname
from config import MONGODB_PASSWORD as password
from config import INITIAL_BALANCE

class Database(object):

    def __init__(self, dbname, password):
        self.client = pymongo.MongoClient(f"mongodb+srv://stocksbotdb:{password}@stonkbot.mphmc.mongodb.net/{dbname}?retryWrites=true&w=majority")
        self.collection = self.client.lilypad.users

    def add_user(self, user_id, near_id, password_hash):
        user = {
            "_id": user_id,
            "near_id": near_id,
            "password_hash": password_hash,
            "balance": INITIAL_BALANCE,
            "stocks": {},
            "transactions": []
        }
        self.collection.insert_one(user)
        
    def verify_login(self, user_id, password_hash):
        user = self.collection.find_one({"_id": user_id})
        if user is None:
            return False
        return user["password_hash"] == password_hash
    