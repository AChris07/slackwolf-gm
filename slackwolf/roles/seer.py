from .types import TeamTypes, RoleTypes
from .villager import Villager
from .utils import get_role_class

from slackwolf.db.entities import Game
from slackwolf.db.entities.game import GameStatus
from slackwolf.models.exceptions import RoleCommandException


class Seer(Villager):
    name = RoleTypes.SEER
    max_number = 1

    @staticmethod
    def see(target: str, game: Game) -> bool:
        if game.status not in [GameStatus.STARTING_NIGHT, GameStatus.NIGHT]:
            raise RoleCommandException("Can only be used at night!")

        try:
            game_user = next(x for x in game.users if f"@{x.user.username}" == target)
        except StopIteration:
            game_user = None
        if not game_user:
            raise RoleCommandException(f"User {target} not found")

        target_role = get_role_class(game_user.role)
        return target_role.team == TeamTypes.WEREWOLVES
