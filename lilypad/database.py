import pymongo, pytz
from datetime import datetime
import json
from config import MONGODB_DBNAME as dbname
from config import MONGODB_PASSWORD as password

class Database(object):

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://cpratim:<password>@cluster0.chv2xt0.mongodb.net/?retryWrites=true&w=majority")
        self.collection = self.client.test

    def add_user(self, user_id, near_id, password_hash):
        user = {
            "_id": user_id,
            "near_id": near_id,
            "password_hash": password_hash,
            "stocks": {},
            "transactions": []
        }
        self.collection.insert_one(user)
        return user
        
    def verify_login(self, user_id, password_hash):
        user = self.collection.find_one({"_id": user_id})
        if user is None:
            return False
        return user["password_hash"] == password_hash
    
    def get_user(self, user_id):
        user = self.collection.find_one({"_id": user_id})
        if user is None:
            return None
        return user
    
if __name__ == '__main__':
    db = Database()
    db.add_user("test", "test", "test")