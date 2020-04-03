import random
from queue import Queue
from threading import Thread
from typing import List, Callable

from bot_interaction.outbound_communication import BotSender
from database.questions_database import QuestionsDatabase
from database.user_database import UserDatabase
from model.question import Question
from model.user import User
from nlp.classifier import Classifier


class QNASubsystem:

    def __init__(self, database: UserDatabase, outbound_sender: BotSender, number_of_users_to_ask: int):
        self._database: UserDatabase = database
        self._outbound_sender: BotSender = outbound_sender
        self._number_of_users_to_ask = number_of_users_to_ask

        self._questions_queue: Queue = Queue()
        self._question_thread_active: bool = False
        self._questions_thread: Thread = Thread(target=self._send_questions_loop)

    def _send_questions_loop(self):
        while self._question_thread_active:
            self._questions_queue.get()()

    def start(self):
        self._question_thread_active = True
        self._questions_thread.start()

    def stop(self):
        self._question_thread_active = False
        self._questions_thread.join()

    def ask_question(self, asking_user: User, question: Question):
        def ask():
            msg: str = f"{asking_user.name} asked:\n{question.question}"

            users: List[User] = [User.from_mongo(user) for user in self._database.get_all_elements()]

            users = [user for user in users if "yes" in user.help_us]

            if asking_user in users:
                users.remove(asking_user)

            selected_users: List[User] = []
            for i in range(min(self._number_of_users_to_ask, len(users))):
                user = random.choice(users)
                selected_users.append(user)
                users.remove(user)

            for user in selected_users:
                self._outbound_sender.send_from_bot(user, msg)

        self._questions_queue.put(ask)
