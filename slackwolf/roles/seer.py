from .types import TeamTypes, RoleTypes
from .villager import Villager
from .utils import get_role_class

from slackwolf.db.entities.game_user import GameUser
from slackwolf.db.entities.game import GameStatus
from slackwolf.models.exceptions import RoleCommandException


class Seer(Villager):
    name = RoleTypes.SEER
    max_number = 1

    @staticmethod
    def see(game_user: GameUser, target_username: str) -> str:
        game = game_user.game
        if game.status not in [GameStatus.STARTING_NIGHT, GameStatus.NIGHT]:
            raise RoleCommandException("Can only be used at night!")

        try:
            target_user = next(x for x in game.users if f"@{x.user.username}" == target_username)
        except StopIteration:
            target_user = None
        if not target_user:
            raise RoleCommandException(f"User {target_username} not found")

        target_role = get_role_class(target_user.role)
        if target_role.team == TeamTypes.WEREWOLVES:
            return f"{game_user.role.value}, " \
                 + f"{target_username} is a Werewolf"
        else:
            return f"{game_user.role.value}, " \
                 + f"{target_username} is not a Werewolf"
