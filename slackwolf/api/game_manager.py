from typing import Tuple
from slackwolf.api.dao import ChannelDao, GameDao, TeamDao, UserDao
from slackwolf.db.entities import Game, GameUser

TeamIdentity = Tuple[str, str]
ChannelIdentity = Tuple[str, str]
UserIdentity = Tuple[str, str]


def get_game(team_id: str, channel_id: str) -> Game:
    channel = ChannelDao().find_by_sid(team_id, channel_id)
    return channel and channel.game


def create_new_game(team_data: TeamIdentity,
                    channel_data: ChannelIdentity,
                    user_data: UserIdentity) -> None:
    TeamDao().get_or_create_by_sid(*team_data)
    channel = ChannelDao().get_or_create_by_sid(team_data[0], *channel_data)
    user = UserDao().get_or_create_by_sid(team_data[0], *user_data)

    game = Game(channel=channel, users=[GameUser(user=user)])
    GameDao().save(game)


def join_game_lobby(user_data: UserIdentity, game: Game) -> None:
    team_sid = game.channel.team.slack_id
    user = UserDao().get_or_create_by_sid(team_sid, *user_data)

    GameDao().add_user(game, user)


def leave_game_lobby(team_id: str, user_id: str, game: Game) -> None:
    user = UserDao().find_by_sid(team_id, user_id)
    if user:
        GameDao().remove_user(game, user)
