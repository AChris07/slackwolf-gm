from typing import List

from .team_dao import TeamDao
import slackwolf.db as db
from slackwolf.db.entities.channel import Channel
from slackwolf.db.entities.team import Team


class ChannelDao:
    """Channel DAO Interface object"""

    def __init__(self):
        self.__session = db.session

    def find(self, id: int) -> Channel:
        """Find by Id"""
        return self.__session.query(Channel).get(id)

    def find_by_sid(self, team_sid: str, slack_id: str) -> Channel:
        """Find by team and channel Slack Id"""
        return self.__session.query(Channel).\
            join(Team).\
            filter(Team.slack_id == team_sid).\
            filter(Channel.slack_id == slack_id).\
            first()

    def find_all(self) -> List[Channel]:
        """Find all channels"""
        return self.__session.query(Channel).all()

    def save(self, channel: Channel) -> None:
        """Save the given channel"""
        self.__session.add(channel)
        self.__session.commit()

    def update(self, id: int, **kwargs) -> None:
        """Given a channel Id, update the channel"""
        self.__session.query(Channel).\
            filter(Channel.id == id).\
            update(kwargs)
        self.__session.commit()

    def get_or_create_by_sid(self,
                             team_sid: str,
                             slack_id: str,
                             name: str) -> Channel:
        """Find or create a channel by team and channel Slack Id"""
        channel = self.find_by_sid(team_sid, slack_id)
        if not channel:
            channel = Channel(slack_id=slack_id, name=name)
            team = TeamDao().find_by_sid(team_sid)
            channel.team = team
            self.save(channel)
        return channel
