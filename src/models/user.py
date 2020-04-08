from dataclasses import dataclass


@dataclass
class User:
    # pylint: disable=C0103
    id: int
    username: str


__all__ = [
    'User'
]
