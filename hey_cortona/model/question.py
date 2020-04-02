from dataclasses import dataclass


@dataclass
class Question:
    question: str
    qid: str = None

    def get_question_id(self) -> str:
        return self.qid

    def __str__(self):
        return f"qid: {self.qid} question: {self.question}"
