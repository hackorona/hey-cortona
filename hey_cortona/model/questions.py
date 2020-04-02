from dataclasses import dataclass
from typing import Dict
from question import Question

@dataclass
class Questions:
    qid: str
    questions: list(Question)
    answers : {str : float}

    @classmethod
    def from_mongo(cls, mongo_questions: Dict):
        return cls(mongo_questions["qid"],mongo_questions["questions"],mongo_questions["answers"])
    
    def __str__(self):
        return f"{self.qid}:{self.questions} - answers: {self.answes}"
