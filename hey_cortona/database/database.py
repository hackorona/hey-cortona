from typing import List, Dict

from pymongo import MongoClient

from bot_interaction.user import User


class Database:

    def __init__(self, uri: str):
        # remember to add the server ip to the ip whitelist in the mongoDB
        self._uri: str = uri
        self.cluster = MongoClient(self._uri)
        self.db = self.cluster["heyCortona"]
        self.users_collection = self.db["users"]
        print("connected to server")

    def addUser(self, user: User):
        post = {"phone_number": user.phone_number, "name": user.name, "city": user.city, "help_us": user.help_us, "admin": user.admin}
        self.users_collection.insert_one(post)

    def findUser(self, user: User):
        result = self.users_collection.find_one({"phone_number": user.phone_number})

        if result is not None:
            return User.from_mongo(result)

        return result

    def getAllUsers(self):

        users: List[User] = []
        mongo_users: List[Dict] = self.users_collection.find({})

        for user in mongo_users:
            users.append(User.from_mongo(user))

        return users

    def deleteUser(self, user: User):
        self.users_collection.delete_one({"phone_number": user.phone_number})

    def deleteAllUsers(self):
        self.users_collection.delete_many({})
