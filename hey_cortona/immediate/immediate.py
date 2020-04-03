from bot_interaction.outbound_communication import BotSender
from database.user_database import UserDatabase
from model.user import User


class ImmediateSubsystem:
    def __init__(self, database: UserDatabase, outbound_sender: BotSender):
        self._database: UserDatabase = database
        self._outbound_sender: BotSender = outbound_sender

    def broadcast(self, sender: User, message: str):
        for recipient in self._database.get_all_elements():
            self._outbound_sender.send(sender, User.from_mongo(recipient), message)

    def message_formatter(self, message: str):
        return "*הודעת מערכת:*" + "\n" + message
