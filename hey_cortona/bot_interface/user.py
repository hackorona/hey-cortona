from dataclasses import dataclass

@dataclass
class User:
    number: str
    name: str = None

    def get_number(self) -> str:
        return f"whatsapp:{self.number}"

    @classmethod
    def from_raw(cls, raw_text: str):
        raw_text = raw_text.replace("whatsapp:", "")
        return cls(raw_text)
