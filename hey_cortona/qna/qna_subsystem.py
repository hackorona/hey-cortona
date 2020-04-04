import json
import random
from queue import Queue
from threading import Thread
from typing import List

from bot_interaction.outbound_communication import BotSender
from database.questions_database import QuestionsDatabase
from database.user_database import UserDatabase
from model.question import Question
from model.user import User
from nlp.classifier import Classifier


class QNASubsystem:

    def __init__(self, users_database: UserDatabase, questions_database: QuestionsDatabase, outbound_sender: BotSender,
                 number_of_users_to_ask: int):
        self._users_database: UserDatabase = users_database
        self._questions_database: QuestionsDatabase = questions_database
        self._outbound_sender: BotSender = outbound_sender
        self._number_of_users_to_ask = number_of_users_to_ask
        self._classifier = Classifier(self._questions_database)

        self._questions_queue: Queue = Queue()
        self._question_thread_active: bool = False
        self._questions_thread: Thread = Thread(target=self._send_questions_loop)

        self._train_thread_active: bool = False
        self._train_thread: Thread = Thread(target=self._train_loop)

    def _send_questions_loop(self):
        while self._train_thread_active:
            self._questions_database.watch_for_change().next()
            self._classifier.train()

    def _train_loop(self):
        while self._question_thread_active:
            self._questions_queue.get()()

    def start(self):
        self._question_thread_active = True
        self._questions_thread.start()

    def stop(self):
        self._question_thread_active = False
        self._train_thread_active = False
        self._questions_thread.join()
        self._train_thread.join()

    def ask_question(self, asking_user: User, question: Question):
        def ask():
            msg: str = f"{asking_user.name} asked:\n{question.question}(if you don't have an answer, respond '!')"
            users: List[User] = self._users_database.get_all_users()

            users = [user for user in users if "yes" in user.help_us.lower()]

            if asking_user in users:
                users.remove(asking_user)

            selected_users: List[User] = []
            for i in range(min(self._number_of_users_to_ask, len(users))):
                user = random.choice(users)
                selected_users.append(user)
                users.remove(user)
                self._users_database.update_user(user, {"answer_qid": question.qid})

            for user in selected_users:
                self._outbound_sender.send_from_bot(user, msg)

            self._classifier.add_question(question)

        self._questions_queue.put(ask)
