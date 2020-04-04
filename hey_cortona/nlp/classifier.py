from threading import Thread, Lock
from typing import Dict, Union, List, Tuple
from textblob.classifiers import NaiveBayesClassifier
from database.questions_database import QuestionsDatabase
from model.question import Question
from fuzzywuzzy import fuzz


class Classifier:

    def __init__(self, questions_database: QuestionsDatabase, similarity_percentage: float = 50):
        self._classifier: Union[NaiveBayesClassifier, None] = None
        self._set: Dict[str, int] = {}
        self._pass_percentage: float = max(min(similarity_percentage, 100), 0)
        self._questions_database: QuestionsDatabase = questions_database
        self._train_data: Dict = {}
        self._classifier_lock: Lock = Lock()
        self.train()

    def _fuzzy_check(self, sentence: str, qid: str) -> float:
        _sum = 0
        amount = 0
        for sent in self._train_tuples_array():
            if sent[1] == qid:
                _sum += fuzz.token_sort_ratio(sentence, sent[0].lower())
                amount += 1

        return _sum / amount

    def add_question(self, question: Question):

        # if there are no categories, add one
        if self._train_data:
            question.qid = question.question
            self._questions_database.add_question_category(question.qid)
        else:
            # use classifier
            self._classifier_lock.acquire()
            qid: str = self._classifier.classify(question.question.lower())
            self._classifier_lock.release()

            similarity_percentage: float = self._fuzzy_check(question.question.lower(), qid)

            if similarity_percentage >= self._pass_percentage:
                question.qid = qid
            else:
                question.qid = question.question

            self._questions_database.add_question(question)

    def _train_tuples_array(self) -> List[Tuple[str, str]]:
        train_tuples = []

        for questions in self._train_data:
            for question in questions.questions:
                train_tuples.append((question.question, questions.qid))
        return train_tuples

    def train(self):
        self._train_data = self._questions_database.get_all_questions_categories()
        if self._train_data:
            classifier: NaiveBayesClassifier = NaiveBayesClassifier(self._train_tuples_array())
            # replace classifier with re trained one
            self._classifier_lock.acquire()
            self._classifier = classifier
            self._classifier_lock.release()
