import json
from dataclasses import dataclass

from twilio.rest import Client

@dataclass
class User:
    number: str
    name: str = None

    def get_number(self) -> str:
        return f"whatsapp:+{self.number}"

    @classmethod
    def from_raw(cls, raw_text: str):
        raw_text = raw_text.replace("whatsapp:", "")
        cls(raw_text)


class OutboundSender:

    def __init__(self, account_sid: str, auth_token: str):
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token

        self._client: Client = Client(account_sid, auth_token)

    def send(self, sender: User, recipent: User, message: str):
        self._client.messages.create(
            body=message,
            from_=sender.get_number(),
            to=recipent.get_number()
        )
