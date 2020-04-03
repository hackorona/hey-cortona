from dataclasses import dataclass
from typing import Dict, List

from model.question import Question


@dataclass
class Questions:
    qid: str
    questions: List[Question]
    answers: Dict[str, float]

    @classmethod
    def from_mongo(cls, mongo_questions: Dict):
        return cls(mongo_questions["qid"], mongo_questions["questions"], mongo_questions["answers"])

    def to_mongo(self):
        mongo_obj: Dict = {
            "qid": self.qid,
            "questions": [q.question for q in self.questions],
            "answers": self.answers
        }


    def __str__(self):
        return f"{self.qid}:{self.questions} - answers: {self.answers}"
