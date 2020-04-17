from flask import Blueprint, request
from slackwolf.api import get_game, create_new_game
from slackwolf.models import User

from operator import itemgetter

bp = Blueprint('commands', __name__, url_prefix='/api/v1/commands')


@bp.route('/join', methods=['POST'])
def join_game():
    """Joins a game lobby.

    Triggers the bot to try and join the game lobby in the current channel.
    If no game lobby was created yet, a new lobby will be created.

    - Will list all the users currently waiting in the lobby
    for a game to start.
    - Will fail and inform the user if a game is already underway.
    - Will also fail and inform the user if he sends the command via DM
    without specifying a channel.

    TODO: Check if we can send a channel as argument and pick up the ID
    """
    game_id = itemgetter('team_id', 'channel_id')(request.form)
    team_data = itemgetter('team_id', 'team_domain')(request.form)
    channel_data = itemgetter('channel_id', 'channel_name')(request.form)
    user_data = itemgetter('user_id', 'user_name')(request.form)

    current_game = get_game(*game_id)
    if current_game is None:
        create_new_game(team_data, channel_data, user_data)
        return f"Welcome to the game lobby! Users: @{user_data[0]}", 200
    else:
        new_user = User(*user_data)
        current_game.users[new_user.id] = new_user
        users_list = [f"@{user.id}" for user in current_game.users.values()]
        return f"Welcome to the game lobby! Users: {','.join(users_list)}", 200
