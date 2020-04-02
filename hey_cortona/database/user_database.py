from database.database import Database
from model.user import User


class UserDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "users")

    def addUser(self, user: User):
        post = {"phone_number": user.phone_number, "name": user.name, "city": user.city, "help_us": user.help_us, "admin": user.admin}
        self._collection.insert_one(post)

    def findUser(self, user: User):
        result = self._collection.find_one({"phone_number": user.phone_number})

        if result is not None:
            return User.from_mongo(result)

        return result

    def deleteUser(self, user: User):
        self._collection.delete_one({"phone_number": user.phone_number})