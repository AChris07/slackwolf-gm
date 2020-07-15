from typing import List

import slackwolf.db as db
from slackwolf.db.entities.game import Game
from slackwolf.db.entities.game_user import GameUser
from slackwolf.db.entities.user import User
from slackwolf.roles.types import RoleTypes


class GameDao:
    """Game DAO Interface object"""

    def __init__(self):
        self.__session = db.session

    def find(self, id: int) -> Game:
        return self.__session.query(Game).get(id)

    def find_all(self) -> List[Game]:
        return self.__session.query(Game).all()

    def save(self, game: Game) -> None:
        self.__session.add(game)
        self.__session.commit()

    def update(self, id: int, **kwargs) -> None:
        self.__session.query(Game).\
            filter(Game.id == id).\
            update(kwargs)
        self.__session.commit()

    def add_user(self, game: Game, user: User) -> None:
        game_user = GameUser(user=user, game=game)
        self.__session.add(game_user)
        self.__session.commit()

    def remove_user(self, game: Game, user: User) -> None:
        game_user = self.__session.query(GameUser).\
            filter(GameUser.game_id == game.id).\
            filter(GameUser.user_id == user.id).\
            first()
        self.__session.delete(game_user)
        self.__session.commit()

    def assign_role(self, game: Game, user: User, role: RoleTypes) -> None:
        self.__session.query(GameUser).\
            filter(GameUser.game_id == game.id).\
            filter(GameUser.user_id == user.id).\
            update({'role': role})
        self.__session.commit()
