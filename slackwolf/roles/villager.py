from .types import RoleTypes, TeamTypes


class Villager:
    name = RoleTypes.VILLAGER
    team = TeamTypes.VILLAGERS

    @staticmethod
    def vote():
        pass
