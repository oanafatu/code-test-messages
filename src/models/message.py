from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    user_id: int
    text: str
    timestamp: datetime


__all__ = [
    'Message'
]
