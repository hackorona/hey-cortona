from database.database import Database


class QuestionsDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "questions")

    def addQuestion(self, user: User):
        post = {"phone_number": user.phone_number, "name": user.name, "city": user.city, "help_us": user.help_us, "admin": user.admin}
        self._collection.insert_one(post)
