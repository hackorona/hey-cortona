import json
import random
from queue import Queue
from threading import Thread
from typing import List

from bot_interaction.outbound_communication import BotSender
from database.questions_database import QuestionsDatabase
from database.user_database import UserDatabase
from model.question import Question
from model.questions_category import QuestionsCategory
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
        self._questions_thread.daemon = True

        self._train_thread_active: bool = False
        self._train_thread: Thread = Thread(target=self._train_loop)
        self._train_thread.daemon = True

    def _send_questions_loop(self):
        while self._train_thread_active:
            self._questions_database.watch_for_change().next()
            self._classifier.train()

    def _train_loop(self):
        while self._question_thread_active:
            self._questions_queue.get()()

    def start(self):
        self._question_thread_active = True
        self._train_thread_active = True
        self._questions_thread.start()
        self._train_thread.start()

    def stop(self):
        self._question_thread_active = False
        self._train_thread_active = False
        self._questions_thread.join()
        self._train_thread.join()

    def ask_question(self, asking_user: User, question: Question, number_of_people_to_ask: int = None,
                     exclude_users: List[User] = []):
        number_of_people_to_ask = number_of_people_to_ask or self._number_of_users_to_ask

        def ask():
            self._classifier.add_question(question)
            category: QuestionsCategory = self._questions_database.find_questions_category(question)
            if len(category.answers) < 1:
                self._outbound_sender.send_from_bot(asking_user,
                                                    "Oops. Looks like I don't have an answer. I'll be right back with an answer.")
                msg: str = f"{asking_user.name} asked:\n{question.question}\n(if you don't have an answer, respond '!')"
                users: List[User] = self._users_database.get_all_users()

                exclude_numbers: List[str] = [u.get_user_id() for u in exclude_users]
                users = [user for user in users if
                         "yes" in user.help_us.lower() and user.answer_qid is None and
                         user.get_user_id() not in exclude_numbers]
                if asking_user in users:
                    users.remove(asking_user)

                selected_users: List[User] = []
                for i in range(min(number_of_people_to_ask, len(users))):
                    user = random.choice(users)
                    selected_users.append(user)
                    users.remove(user)
                    self._users_database.update_user(user, {"answer_qid": question.qid,
                                                            "asking_user_id": asking_user.get_user_id(),
                                                            "asked_question": question.question})

                for user in selected_users:
                    self._outbound_sender.send_from_bot(user, msg)
            else:
                msg: str = category.answers[-1]
                self._outbound_sender.send_from_bot(asking_user, msg)

        self._questions_queue.put(ask)

    def answer_question(self, answering_user: User, answer: str):
        asking_user: User = User.from_user_id(answering_user.asking_user_id)
        msg: str = f"You asked: {answering_user.asked_question}\nThe answer is: {answer}"
        self._questions_database.add_answer(answering_user.answer_qid, answer)
        self._outbound_sender.send_from_bot(asking_user, msg)
        self._users_database.update_user(answering_user, {"answer_qid": None,
                                                          "asking_user_id": None,
                                                          "asked_question": None})

    def decline_question(self, declining_user: User):
        asking_user: User = self._users_database.find_user(User.from_user_id(declining_user.asking_user_id))
        self.ask_question(asking_user, Question(asking_user.asked_question), 1, [asking_user])
        self._users_database.update_user(declining_user, {"answer_qid": None,
                                                          "asking_user_id": None,
                                                          "asked_question": None})
