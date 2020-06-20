from .types import RoleTypes
from .villager import Villager


class Seer(Villager):
    name = RoleTypes.SEER
    max_number = 1

    def see(self):
        pass
