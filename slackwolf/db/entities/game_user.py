from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from slackwolf.db import Base
from slackwolf.roles.types import RoleTypes


class GameUser(Base):
    """Game-User association entity"""

    __tablename__ = 'game_user'

    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    game = relationship('Game', back_populates='users')
    user = relationship('User', back_populates='games')
    role = Column(Enum(RoleTypes), default=RoleTypes.VILLAGER, nullable=False)
