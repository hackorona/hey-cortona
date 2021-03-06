from bot_interaction.outbound_communication import BotSender
from database.user_database import UserDatabase
from model.user import User


class ImmediateSubsystem:
    def __init__(self, database: UserDatabase, outbound_sender: BotSender):
        self._database: UserDatabase = database
        self._outbound_sender: BotSender = outbound_sender

    def broadcast(self, message: str):
        for recipient in self._database.get_all_users():
            self._outbound_sender.send_from_bot(recipient, ImmediateSubsystem.message_formatter(message))
    
    @staticmethod
    def message_formatter(message: str):
        return f"*System message:*\n{message}"
