import json
from typing import Dict

from twilio.rest import Client

from model.user import User


class OutboundSender:

    def __init__(self, account_sid: str, auth_token: str):
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token

        self._client: Client = Client(account_sid, auth_token)

    def send(self, sender: User, recipient: User, message: str):
        self._client.messages.create(
            body=message,
            from_=sender.get_user_id(),
            to=recipient.get_user_id()
        )


class BotSender(OutboundSender):

    def __init__(self, account_sid: str, auth_token: str, bot: User):
        super().__init__(account_sid, auth_token)
        self._bot: User = bot

    def send_from_bot(self, recipient: User, message: str):
        super().send(self._bot, recipient, message)
