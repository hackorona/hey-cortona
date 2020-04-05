from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    phone_number: str
    name: str = None
    city: str = None
    help_us: str = None
    admin: bool = False
    answer_qid: str = None
    asked_question: str = None
    asking_user_id: str = None

    def get_user_id(self) -> str:
        return f"whatsapp:{self.phone_number}"

    @classmethod
    def from_user_id(cls, raw_text: str, name: str = None, city: str = None, help_us: str = None, admin: bool = False):
        raw_text = raw_text.replace("whatsapp:", "")
        return cls(raw_text, name, city, help_us, admin)

    @classmethod
    def from_mongo(cls, mongo_user: Dict):
        return cls(mongo_user["phone_number"], mongo_user["name"], mongo_user["city"], mongo_user["help_us"],
                   mongo_user["admin"], mongo_user["answer_qid"], mongo_user["asked_question"],
                   mongo_user["asking_user_id"])

    @classmethod
    def from_answers(cls, user_id: str, answers: Dict):
        city: str = Null#answers.get("city").get("answer")
        name: str = answers.get("name").get("answer")
        help_us: str = answers.get("help_us").get("answer")
        return cls.from_user_id(user_id, name, city, help_us)

    def __str__(self):
        return f"{self.name}:{self.phone_number}" \
               f" - {self.city} - help-us: {self.help_us} - admin: {self.admin} - qid: {self.answer_qid}"
