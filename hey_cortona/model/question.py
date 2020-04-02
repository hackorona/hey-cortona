from dataclasses import dataclass
from typing import Dict


@dataclass
class Question:
    qid: str
    question: str

    def get_question_id(self) -> str:
        return self.qid

    def __str__(self):
        return f"qid: {self.qid} question: {self.question}"
