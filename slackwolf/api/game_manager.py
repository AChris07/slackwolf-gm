from typing import Tuple
from slackwolf.models import Team, Channel, Game, User

TeamIdentity = Tuple[str, str]
ChannelIdentity = Tuple[str, str]
UserIdentity = Tuple[str, str]

game_store = {}


def get_game(team_id: str, channel_id: str) -> Game:
    team = game_store.get(team_id, Team()) or Team()
    channel = team.channels.get(channel_id, Channel())
    return channel.game


def create_new_game(team_data: TeamIdentity,
                    channel_data: ChannelIdentity,
                    user_data: UserIdentity) -> None:
    new_game = Game()
    new_game.users[team_data[0]] = User(*team_data)
    # TODO: Refactor this
    if not game_store.get(team_data[0]):
        game_store[team_data[0]] = Team(*team_data)
    if not game_store[team_data[0]].channels.get(channel_data[0]):
        game_store[team_data[0]].channels[channel_data[0]] = \
            Channel(*channel_data)
    game_store[team_data[0]].channels[channel_data[0]].game = new_game
