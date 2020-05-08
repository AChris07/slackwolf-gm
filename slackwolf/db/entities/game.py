import enum
from sqlalchemy import Column, Integer, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from slackwolf.db import Base


class GameStatus(enum.Enum):
    WAITING = 1
    STARTED = 2
    FINISHED = 3


class Game(Base):
    """Game entity"""

    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(GameStatus),
                    default=GameStatus.WAITING,
                    nullable=False)
    channel_id = Column(String, ForeignKey('channel.id'), nullable=False)
    channel = relationship('Channel', back_populates='game')
    users = relationship('GameUser',
                         back_populates='game',
                         cascade='all, delete-orphan')