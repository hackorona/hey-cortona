from typing import Dict

from textblob.classifiers import NaiveBayesClassifier

from database.questions_database import QuestionsDatabase
from model.question import Question


class Classifier:
    def __init__(self, questions_database: QuestionsDatabase):
        self._classifier: NaiveBayesClassifier = None
        self._set: Dict[str, int] = {}

    def _fuzzy_check(self, sentence, qid):
        sum = 0
        amount = 0
        for sent in train:
            if sent[1] == category:
                sum += fuzz.partial_ratio(sentence, sent[0])
                amount += 1

        return sum / amount

    def add_question(self, question: Question):

        category: int = self._classifier.classify(question.question)

        similarity_percentage: float = self._fuzzy_check(question, category)

        

        if similarity_percentage >= 50:

            .append((qna, category))
        else:
            train.append((qna, qna))

        cl = NaiveBayesClassifier(train)

    def train(self):
        pass