from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str


__all__ = [
    'User'
]