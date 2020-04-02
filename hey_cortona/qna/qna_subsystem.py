import random
from typing import List

from bot_interaction.outbound_communication import BotSender
from database.questions_database import QuestionsDatabase
from model.question import Question
from model.user import User


class QNASubsystem:

    def __init__(self, database: QuestionsDatabase, outbound_sender: BotSender, number_of_users_to_ask: int):
        self._database: QuestionsDatabase = database
        self._outbound_sender: BotSender = outbound_sender
        self._number_of_users_to_ask = number_of_users_to_ask

    def ask_question(self, asking_user: User, question: Question):

        msg: str = asking_user.name + "שאל:\n"
        msg += question.question

        users: List[User] = [User.from_mongo(user) for user in self._database.get_all_elements()]

        users = [user for user in users if "כן" in user.help_us]

        selected_users: List[User] = []
        for i in range(self._number_of_users_to_ask):
            selected_users.append(random.choice(users))

        for user in selected_users:
            self._outbound_sender.send_from_bot(user, msg)
