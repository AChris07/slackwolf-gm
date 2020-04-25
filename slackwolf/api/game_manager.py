from typing import Tuple
from slackwolf.api.entities import Team, Channel, Game, User

TeamIdentity = Tuple[str, str]
ChannelIdentity = Tuple[str, str]
UserIdentity = Tuple[str, str]

game_store = {}


def get_game(team_id: str, channel_id: str) -> Game:
    team = game_store.get(team_id, Team()) or Team()
    team_channels = team.channels
    channel = next((x for x in team_channels if x.id == channel_id), Channel())
    return channel.game


def create_new_game(team_data: TeamIdentity,
                    channel_data: ChannelIdentity,
                    user_data: UserIdentity) -> None:
    new_game = Game()
    new_game.users.append(User(*user_data))
    # TODO: Refactor this
    if not game_store.get(team_data[0]):
        game_store[team_data[0]] = Team(*team_data)
    channels = game_store[team_data[0]].channels
    channel = next((x for x in channels if x.id == channel_data[0]), None)
    if not channel:
        channel = Channel(*channel_data)
        channels.append(channel)
    channel.game = new_game
