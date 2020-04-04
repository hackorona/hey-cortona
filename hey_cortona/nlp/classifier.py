from typing import Dict, Union, List, Tuple
from textblob.classifiers import NaiveBayesClassifier
from database.questions_database import QuestionsDatabase
from model.question import Question
from fuzzywuzzy import fuzz


class Classifier:
    def __init__(self, questions_database: QuestionsDatabase, similarity_percentage: float = 50):
        self._classifier: Union[NaiveBayesClassifier, None] = None
        self._set: Dict[str, int] = {}
        self.pass_percentage: float = max(min(similarity_percentage, 100), 0)
        self.questions_database: QuestionsDatabase = questions_database
        self.train_data: Union[Dict, None] = None
        self.train()

    def _fuzzy_check(self, sentence: str, qid: str) -> float:
        _sum = 0
        amount = 0
        for sent in self.train_tuples_array():
            if sent[1] == qid:
                _sum += fuzz.token_sort_ratio(sentence, sent[0].lower())
                amount += 1

        return _sum / amount

    def add_question(self, question: Question):
        print("\nstart nlp\n")
        qid: str = self._classifier.classify(question.question.lower())

        similarity_percentage: float = self._fuzzy_check(question.question.lower(), qid)

        print(f'\nqid: {qid}, sim_prec: {similarity_percentage}, question: {question.question.lower()}\n')
        if similarity_percentage >= self.pass_percentage:
            question.qid = qid
            self.questions_database.add_question(question.question, question.qid)

        else:
            question.qid = question.question
            self.questions_database.add_questions(question.qid)

        self.train()

    def train_tuples_array(self) -> List[Tuple[str, str]]:
        train_tuples = []

        assert self.train_data, "Train data is None!"

        for questions in self.train_data:
            for question in questions.questions:
                train_tuples.append((question, questions.qid))
        return train_tuples

    def train(self):
        self.train_data = self.questions_database.get_all_questions()
        self._classifier = NaiveBayesClassifier(self.train_tuples_array())
