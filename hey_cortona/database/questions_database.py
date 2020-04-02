from database.database import Database
from model.question import Question
from model.questions import Questions


class QuestionsDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "questions")

    def addQuestion(self, question: Question):
        self._collection.insert_one(post)
        result = self._collection.find_one({"qid": question.qid})
        if result is not None:
            result = Questions.from_mongo(result)
            result.questions.append(question.question)
            self._collection.replace_one({"qid":question.qid},result.questions)
            return result

    def findQuestions(self, question: Question):
        result = self._collection.find_one({"qid": user.qid})

        if result is not None:
            return User.from_mongo(result)

        return result

    def deleteQuestions(self, questions: Questions):
        self._collection.delete_one({"qid": questions.qid})
