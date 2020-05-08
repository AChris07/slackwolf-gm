from typing import List

import slackwolf.db as db
from slackwolf.db.entities import Team


class TeamDao:
    """Team DAO Interface object"""

    def __init__(self):
        self.__session = db.session

    def find(self, id: int) -> Team:
        """Find by Id"""
        return self.__session.query(Team).get(id)

    def find_by_sid(self, slack_id: str) -> Team:
        """Find by team Slack Id"""
        return self.__session.query(Team).\
            filter(Team.slack_id == slack_id).\
            first()

    def find_all(self) -> List[Team]:
        """Find all teams"""
        return self.__session.query(Team).all()

    def save(self, team: Team) -> None:
        """Save the given team"""
        self.__session.add(team)
        self.__session.commit()

    def update(self, id: int, **kwargs) -> None:
        """Given a team Id, update the team"""
        self.__session.query(Team).\
            filter(Team.id == id).\
            update(kwargs)
        self.__session.commit()

    def get_or_create_by_sid(self, slack_id: str, name: str) -> Team:
        """Find or create a team by team Slack Id"""
        team = self.find_by_sid(slack_id)
        if not team:
            team = Team(slack_id=slack_id, name=name)
            self.save(team)
        return team
