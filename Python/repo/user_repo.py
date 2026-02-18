from datetime import datetime, timezone
from bson import ObjectId
from config.db import db

class UserRepo:
    def __init__(self):
        self.collection = db["users"]

    def find_user_by_email(self, encoded_email):
        return self.collection.find_one({"email": encoded_email})

    def find_all_users(self):
        return list(self.collection.find())

    def create_user(self, data):
        data.setdefault("created_at", datetime.now(timezone.utc))
        data.setdefault("status", "active")
        data.setdefault("role", "user")
        return self.collection.insert_one(data)

    def update_user(self, query, update):
        return self.collection.update_one(query, update)

    def delete_user(self, query):
        return self.collection.delete_one(query)
