from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    id: int
    user_id: int
    text: str
    timestamp: datetime


__all__ = [
    'Message'
]
