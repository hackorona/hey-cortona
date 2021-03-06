from typing import Dict

from database.database import Database
from model.user import User


class UserDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "users")

    def add_user(self, user: User):
        post = {"phone_number": user.phone_number, "name": user.name, "city": user.city, "help_us": user.help_us,
                "admin": user.admin, "answer_qid": user.answer_qid, "asked_question": user.asked_question,
                "asking_user_id": user.asking_user_id}
        self._collection.insert_one(post)

    def find_user(self, user: User):
        result = self._collection.find_one({"phone_number": user.phone_number})

        if result is not None:
            return User.from_mongo(result)

        return result

    def update_user(self, user: User, update: Dict):
        self._collection.update_one({"phone_number": user.phone_number}, {"$set": update})

    def get_all_users(self):
        users = super()._get_all_elements()
        users_arr = []
        for user in users:
            users_arr.append(User.from_mongo(user))
        return users_arr

    def delete_user(self, user: User):
        self._collection.delete_one({"phone_number": user.phone_number})
