from typing import List, Tuple
import random

from slackwolf.api.dao import ChannelDao, GameDao, TeamDao, UserDao
from slackwolf.db.entities import Game, GameUser
from slackwolf.db.entities.game import GameStatus
from slackwolf.roles import RoleTypes, TeamTypes, Villager, Werewolf, roles

TeamIdentity = Tuple[str, str]
ChannelIdentity = Tuple[str, str]
UserIdentity = Tuple[str, str]


def get_game(team_id: str, channel_id: str) -> Game:
    """Retrieves a game, given a team and channel ID."""

    channel = ChannelDao().find_by_sid(team_id, channel_id)
    return channel and channel.game


def create_new_game(team_data: TeamIdentity,
                    channel_data: ChannelIdentity,
                    user_data: UserIdentity) -> None:
    """Creates a new game in a given channel, with the given user."""

    TeamDao().get_or_create_by_sid(*team_data)
    channel = ChannelDao().get_or_create_by_sid(team_data[0], *channel_data)
    user = UserDao().get_or_create_by_sid(team_data[0], *user_data)

    game = Game(channel=channel, users=[GameUser(user=user)])
    GameDao().save(game)


def join_game_lobby(user_data: UserIdentity, game: Game) -> None:
    """Adds a user to the given game."""

    team_sid = game.channel.team.slack_id
    user = UserDao().get_or_create_by_sid(team_sid, *user_data)

    GameDao().add_user(game, user)


def leave_game_lobby(user_id: str, game: Game) -> None:
    """Removes a user from the given game, if found."""

    team_sid = game.channel.team.slack_id
    user = UserDao().find_by_sid(team_sid, user_id)
    if user:
        GameDao().remove_user(game, user)


def get_game_roles(game: Game) -> List[RoleTypes]:
    """Get the list of assignable roles for a given game.

    The list contains the role types and numbers to assign to users of a given
    game.
    It uses the following criteria to create this list:
    - Number of players in the game.
    - Available roles per game settings.

    TODO: Implement game settings to enable/disable roles.

    """

    num_players = len(game.users)

    # Set a dict to keep track of the team counts
    team_count = dict()
    team_count[TeamTypes.WEREWOLVES] = int(num_players / 3)
    team_count[TeamTypes.VILLAGERS] = num_players - team_count[TeamTypes.WEREWOLVES]

    base_roles = [RoleTypes.VILLAGER, RoleTypes.WEREWOLF]
    result = []

    def is_role_available(role):
        # Exclude non-base roles. They are managed manually below
        # (since they're added last to pad team numbers)
        is_base = role.name in base_roles
        has_capacity = hasattr(role, 'max_number') \
            and result.count(role.name) < role.max_number
        has_team_capacity = bool(team_count[role.team])

        return not is_base and has_capacity and has_team_capacity

    while len(result) < num_players:
        new_role = next((x for x in roles if is_role_available(x)), None)

        # If all other roles have been assigned, look into padding
        # teams with base roles
        if new_role is None:
            new_role = Werewolf() if team_count[TeamTypes.WEREWOLVES] \
                else Villager()

        team_count[new_role.team] -= 1

        # At this point, this should not happen.
        # If it is the case, however, throw an error.
        if team_count[new_role.team] < 0:
            raise IndexError

        result.append(new_role.name)

    # Arbitrarily shuffle roles before returning them, for random assignment
    random.shuffle(result)

    return result


def start_game(game: Game) -> None:
    """Starts the given game and assign random roles to its users."""

    game_roles = get_game_roles(game)
    users = [x.user for x in game.users]
    game_dao = GameDao()

    for user, role in zip(users, game_roles):
        game_dao.assign_role(game, user, role)

    game_dao.update(game.id, status=GameStatus.STARTED)
