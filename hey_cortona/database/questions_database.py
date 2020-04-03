from database.database import Database
from model.question import Question
from model.questions import Questions
from model.user import User


class QuestionsDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "questions")

    # def add_question(self, question: Question):
    #     result = self._collection.find_one({"qid": question.qid})
    #     print (f'\n\nresult : {result} , qid : {question.qid} , origin_que : {question}\n\n')
    #     if result is not None:
    #         result = Questions.from_mongo(result)
    #         print (f'\n\nque from mongo : {result}\n\n')
    #         result.questions.append(question.question)
    #         self._collection.replace_one({"qid": question.qid}, result.questions)
    #
    #     return result

    def add_question(self, question: str, qid: str):
        result = self._collection.find_one({"qid": qid})
        print (f'\n\nresult : {result} , qid : {qid} , origin_que : {question}\n\n')
        if result is not None:
            result = Questions.from_mongo(result)
            result.questions.append(question)
            print (f'\n\nque from mongo : {result}\n\n')
            self._collection.replace_one({"qid": qid}, result.to_mongo())

        return result

    def find_question(self, question: Question):
        #TODO fix this crap code !!!!!!!!!!!
        result = self._collection.find_one({"qid": question.qid})

        if result is not None:
            return Question.from_mongo(result)

        return result

    def get_all_questions(self):
        questions = self._collection.find({})
        questions_arr = []
        for question in questions:
            questions_arr.append(Questions.from_mongo(question))
        return questions_arr

    def add_questions(self, question: Question):
        result = Questions.from_mongo({"qid": question.question, "questions": [question.question], "answers": {}})
        self._collection.insert_one(result)

    def delete_question(self, questions: Questions):
        self._collection.delete_one({"qid": questions.qid})
