from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    phone_number: str
    name: str = None
    city: str = None
    help_us: str = None

    def get_user_id(self) -> str:
        return f"whatsapp:{self.phone_number}"

    @classmethod
    def from_user_id(cls, raw_text: str, name: str = None, city: str = None, help_us: str = None):
        raw_text = raw_text.replace("whatsapp:", "")
        return cls(raw_text, name, city, help_us)

    @classmethod
    def from_mongo(cls, mongo_user: Dict):
        return cls(mongo_user["phone_number"], mongo_user["name"], mongo_user["city"],  mongo_user["help_us"])

    def __str__(self):
        return f"{self.name}:{self.phone_number} - {self.city}"
