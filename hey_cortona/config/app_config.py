import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    _account_sid: str
    _auth_token: str
    _mongo_uri: str
    _bot_phone_number: str
    _number_of_people_to_ask: int = 1

    @classmethod
    def from_env(cls, number_of_people_to_ask: int = 1):
        return cls(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'), os.getenv('MONGO_URI'),
                   os.getenv('BOT_PHONE_NUMBER'), number_of_people_to_ask)

    @property
    def ACCOUNT_SID(self) -> str:
        return self._account_sid

    @property
    def AUTH_TOKEN(self) -> str:
        return self._auth_token

    @property
    def MONGO_URI(self) -> str:
        return self._mongo_uri

    @property
    def BOT_PHONE_NUMBER(self) -> str:
        return self._bot_phone_number

    @property
    def number_of_people_to_ask(self):
        return self._number_of_people_to_ask

