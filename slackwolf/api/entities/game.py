from enum import Enum


class GameStatus(Enum):
    WAITING = 1
    STARTED = 2
    FINISHED = 3


class Game:
    """Game entity"""

    def __init__(self):
        self.users = []
        self.status = GameStatus.WAITING
