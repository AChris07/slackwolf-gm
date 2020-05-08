from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from slackwolf.db import Base


class Team(Base):
    """Team entity"""

    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    slack_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    channels = relationship('Channel', back_populates='team')
    users = relationship('User', back_populates='team')
