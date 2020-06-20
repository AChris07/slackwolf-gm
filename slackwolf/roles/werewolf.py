from .types import RoleTypes, TeamTypes


class Werewolf:
    name = RoleTypes.WEREWOLF
    team = TeamTypes.WEREWOLVES

    def vote(self):
        pass

    def kill(self):
        pass
