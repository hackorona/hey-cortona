from typing import Dict
from textblob.classifiers import NaiveBayesClassifier
from database.questions_database import QuestionsDatabase
from model.question import Question
from fuzzywuzzy import fuzz


class Classifier:
    def __init__(self, questions_database: QuestionsDatabase):
        self._classifier: NaiveBayesClassifier = None
        self._set: Dict[str, int] = {}
        self.pass_percentage = 50
        self.questions_database = questions_database
        self.train_data = None
        self.train()

    def _fuzzy_check(self, sentence, qid):
        sum = 0
        amount = 0
        for sent in self.train_tuples_array():
            if sent[1] == qid:
                sum += fuzz.partial_ratio(sentence, sent[0])
                amount += 1

        return sum / amount

    def add_question(self, question: Question):
        print("\nstart nlp\n")
        qid: str = self._classifier.classify(question.question)

        similarity_percentage: float = self._fuzzy_check(question.question, qid)

        print(f'\nqid: {qid}, sim_prec: {similarity_percentage}\n')
        if similarity_percentage >= self.pass_percentage:
            self.questions_database.add_question(question)
        else:
            self.questions_database.add_questions(question)

        self.train()

    def train_tuples_array(self):
        train_tuples = []
        for questions in self.train_data:
            for question in questions.questions:
                print(f'que : {question}')
                train_tuples.append((question,questions.qid))
        return train_tuples        

    def train(self):
        self.train_data = self.questions_database.get_all_questions()
        self._classifier = NaiveBayesClassifier(self.train_tuples_array())
