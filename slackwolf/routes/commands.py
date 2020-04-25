from flask import Blueprint, request
from slackwolf.api import get_game, create_new_game
from slackwolf.api.entities import User
from slackwolf.api.entities.game import GameStatus
from slackwolf.routes.response import Response

from operator import itemgetter

bp = Blueprint('commands', __name__, url_prefix='/api/v1/commands')


@bp.route('/join', methods=['POST'])
def join_game():
    """Joins a game lobby.

    Triggers the bot to try and join the game lobby in the current channel.
    If no game lobby was created yet, a new lobby will be created.

    - Will list all the users currently waiting in the lobby
    for a game to start.
    - Will fail and inform the user if he already joined.
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
        return Response(f"Game lobby updated: @{user_data[0]}").as_public()
    elif user_data[0] in [x.id for x in current_game.users]:
        return Response(
            f"You've already joined, @{user_data[0]}!"
        ).as_ephimeral()
    elif current_game.status is GameStatus.STARTED:
        return Response(
            "Sorry, a game is already in progress on this channel"
        ).as_ephimeral()
    else:
        new_user = User(*user_data)
        current_game.users.append(new_user)
        users_list = [f"@{user.id}" for user in current_game.users]
        return Response(
            f"Game lobby updated: {','.join(users_list)}"
        ).as_public()


@bp.route('/leave', methods=['POST'])
def leave_game():
    """Leaves a game lobby.

    Triggers the bot to leave the game lobby in the current channel.

    - Will publicly update the list of all the users in the lobby, and
    inform the user.
    - Will fail and inform the user if he had not joined the lobby previously.
    - Will fail and inform the user if a game is already underway.
    - Will also fail and inform the user if he sends the command via DM
    without specifying a channel.

    TODO: Check if we can send a channel as argument and pick up the ID
    """
    team_id, channel_id, user_id = \
        itemgetter('team_id', 'channel_id', 'user_id')(request.form)
    current_game = get_game(team_id, channel_id)
    users_id = current_game and [x.id for x in current_game.users]
    if current_game is None or user_id not in users_id:
        return Response(
            "You haven't joined the current game lobby yet!"
        ).as_ephimeral()
    elif current_game.status is GameStatus.STARTED:
        return Response(
            "Sorry, cannot leave a game currently in progress"
        ).as_ephimeral()
    else:
        new_users = [x for x in current_game.users if not x.id == user_id]
        current_game.users = new_users
        users_list = [f"@{user.id}" for user in current_game.users]
        if len(users_list):
            msg = f"Game lobby updated: {','.join(users_list)}"
        else:
            msg = "Game lobby is empty"
        return Response(msg).as_public()
