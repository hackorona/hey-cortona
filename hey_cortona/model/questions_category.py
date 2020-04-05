from dataclasses import dataclass
from typing import Dict, List

from model.question import Question


@dataclass
class QuestionsCategory:
    qid: str
    questions: List[Question]
    answers: List[str]

    @classmethod
    def from_mongo(cls, mongo_questions: Dict):
        qid: str = mongo_questions["qid"]
        questions: List[Question] = [Question(question, qid) for question in mongo_questions["questions"]]
        return cls(mongo_questions["qid"], questions, mongo_questions["answers"])

    def to_mongo(self):
        mongo_obj: Dict = {
            "qid": self.qid,
            "questions": [q.question for q in self.questions],
            "answers": self.answers
        }

        return mongo_obj

    def add_question(self, question: str):
        quest: Question = Question(question, self.qid)
        self.questions.append(quest)
        return quest

    def get_questions_strings(self):
        return [q.question for q in self.questions]

    def __str__(self):
        return f"{self.qid}:{self.questions} - answers: {self.answers}"
