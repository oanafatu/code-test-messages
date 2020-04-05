from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    id: int
    username: str
    text: str
    timestamp: datetime


__all__ = [
    'Message'
]