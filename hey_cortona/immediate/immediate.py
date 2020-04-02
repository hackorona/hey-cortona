from bot_interaction.outbound_communication import OutboundSender;
from model.user import User
from database.database import Database


class ImmediateSubsystem:
    def __init__(self, database: Database, outbound_sender: OutboundSender):
        self.database = database
        self.outbound_sender = outbound_sender

    def broadcast(self, sender: User, message: str):
        for recipient in self.database.getAllUsers():
            self.outbound_sender.send(sender, recipient, message)

    def message_formatter(self, message: str):
        return "*הודעת מערכת:*" + "\n" + message
