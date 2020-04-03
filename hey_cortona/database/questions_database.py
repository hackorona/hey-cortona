from database.database import Database
from model.question import Question
from model.questions import Questions
from model.user import User


class QuestionsDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "questions")

    def addQuestion(self, question: Question):

        result = self._collection.find_one({"qid": question.qid})
        if result is not None:
            result = Questions.from_mongo(result)
            result.questions.append(question.question)
            self._collection.replace_one({"qid": question.qid}, result.questions)
            return result

    def findQuestion(self, question: Question):
        result = self._collection.find_one({"qid": question.qid})

        if result is not None:
            return User.from_mongo(result)

        return result

    def deleteQuestion(self, questions: Questions):
        self._collection.delete_one({"qid": questions.qid})
