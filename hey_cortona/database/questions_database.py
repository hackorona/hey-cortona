from typing import Dict, List

from database.database import Database
from model.question import Question
from model.questions_category import QuestionsCategory


class QuestionsDatabase(Database):

    def __init__(self, uri: str):
        super().__init__(uri, "questions")

    def add_question(self, question: Question):
        mongo_questions_category: Dict = self._collection.find_one({"qid": question.qid})

        if mongo_questions_category is not None:
            questions_category = QuestionsCategory.from_mongo(mongo_questions_category)
            questions_category.add_question(question.question)
            self._collection.update_one({"qid": questions_category.qid},
                                        {"$set": {"questions": questions_category.get_questions_strings()}})
        else:
            # if category does not exists add new one
            self.add_question_category(question.question)

    def add_answer(self, qid: str, answer: str):

        mongo_question_category: Dict = self._collection.find_one({"qid": qid})
        mongo_question_category["answers"][answer] = None  # add answer
        self._collection.update_one({"qid": qid}, {"$set": {"answers": mongo_question_category["answers"]}})

    def find_questions_category(self, question: Question):
        mongo_questions_category: Dict = self._collection.find_one({"qid": question.qid})
        if mongo_questions_category is not None:
            return QuestionsCategory.from_mongo(mongo_questions_category)

        return mongo_questions_category

    def get_all_questions_categories(self):
        mongo_questions_categories: List[Dict] = super()._get_all_elements()
        questions: List[Question] = [QuestionsCategory.from_mongo(question_category) for question_category in
                                     mongo_questions_categories]
        return questions

    def add_question_category(self, qid: str):
        question_category: QuestionsCategory = QuestionsCategory(qid, [Question(qid, qid)], {})
        self._collection.insert_one(question_category.to_mongo())

    def delete_question_category(self, questions: QuestionsCategory):
        self._collection.delete_one({"qid": questions.qid})

    def watch_for_change(self):
        return self._collection.watch()