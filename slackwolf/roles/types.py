from enum import Enum


class RoleTypes(Enum):
    VILLAGER = 'Villager'
    WEREWOLF = 'Werewolf'
    SEER = 'Seer'


class TeamTypes(Enum):
    VILLAGERS = 'Villagers',
    WEREWOLVES = 'Werewolves'
