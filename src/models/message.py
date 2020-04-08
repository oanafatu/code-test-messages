from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    # pylint: disable=C0103
    id: str
    user_id: int
    text: str
    timestamp: datetime


__all__ = [
    'Message'
]
