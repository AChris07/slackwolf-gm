from typing import List

from .team_dao import TeamDao
import slackwolf.db as db
from slackwolf.db.entities.team import Team
from slackwolf.db.entities.user import User


class UserDao:
    """User DAO Interface object"""

    def __init__(self):
        self.__session = db.session

    def find(self, id: int) -> User:
        """Find by Id"""
        return self.__session.query(User).get(id)

    def find_by_sid(self, team_sid: str, slack_id: str) -> User:
        """Find by team and user Slack Id"""
        return self.__session.query(User).\
            join(Team).\
            filter(Team.slack_id == team_sid).\
            filter(User.slack_id == slack_id).\
            first()

    def find_all(self) -> List[User]:
        """Find all users"""
        return self.__session.query(User).all()

    def save(self, user: User) -> None:
        """Save the given user"""
        self.__session.add(user)
        self.__session.commit()

    def update(self, id: int, **kwargs) -> None:
        """Given a user Id, update the user"""
        self.__session.query(User).\
            filter(User.id == id).\
            update(kwargs)
        self.__session.commit()

    def get_or_create_by_sid(self,
                             team_sid: str,
                             slack_id: str,
                             username: str) -> User:
        """Find or create a user by team and user Slack Id"""
        user = self.find_by_sid(team_sid, slack_id)
        if not user:
            user = User(slack_id=slack_id, username=username)
            team = TeamDao().find_by_sid(team_sid)
            user.team = team
            self.save(user)
        return user
