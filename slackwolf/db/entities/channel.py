from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from slackwolf.db import Base


class Channel(Base):
    """Channel entity"""

    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    slack_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    team_id = Column(String, ForeignKey('team.id'), nullable=False)
    team = relationship('Team', back_populates='channels')
    game = relationship('Game', back_populates='channel', uselist=False)

    __table_args__ = (UniqueConstraint('team_id', 'slack_id'),)
