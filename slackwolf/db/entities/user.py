from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from slackwolf.db import Base


class User(Base):
    """User entity"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    slack_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    team_id = Column(String, ForeignKey('team.id'), nullable=False)
    team = relationship('Team', back_populates='users')
    games = relationship('GameUser',
                         back_populates='user',
                         cascade='all, delete-orphan')

    __table_args__ = (UniqueConstraint('team_id', 'slack_id'),)
