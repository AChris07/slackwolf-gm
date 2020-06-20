from .types import RoleTypes, TeamTypes
from .seer import Seer
from .villager import Villager
from .werewolf import Werewolf


roles = [
    Villager(),
    Werewolf(),
    Seer()
]

__all__ = ["RoleTypes",
           "TeamTypes",
           "roles",
           "Seer",
           "Villager",
           "Werewolf"]
