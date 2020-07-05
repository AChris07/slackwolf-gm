from .types import RoleTypes, TeamTypes


class Werewolf:
    name = RoleTypes.WEREWOLF
    team = TeamTypes.WEREWOLVES

    @staticmethod
    def vote():
        pass

    @staticmethod
    def kill():
        pass
