from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    phone_number: str
    name: str = None
    city: str = None

    def get_number(self) -> str:
        return f"whatsapp:{self.phone_number}"

    @classmethod
    def from_phone_number(cls, raw_text: str):
        raw_text = raw_text.replace("whatsapp:", "")
        return cls(raw_text)

    @classmethod
    def from_mongo(cls, mongo_user: Dict):
        return cls(mongo_user["phone_number"], mongo_user["name"], mongo_user["city"])

    def __str__(self):
        return f"{self.name}:{self.phone_number} - {self.city}"
