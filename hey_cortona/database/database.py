from typing import List, Dict

from pymongo import MongoClient

from model.user import User

class Database:

    def __init__(self, uri: str, collection_name: str):
        self._uri: str = uri
        self._cluster = MongoClient(self._uri)
        self._db = self._cluster["heyCortona"]
        self._collection = self._db[collection_name]

    def get_all_elements(self):
        users: List[User] = []
        mongo_users: List[Dict] = self._collection.find({})

        for user in mongo_users:
            users.append(User.from_mongo(user))

        return users

    def delete_all_elements(self):
        self._collection.delete_many({})


