from flask import Blueprint, request
from slackwolf.api import game_manager, slack
from slackwolf.db.entities.game import GameStatus
from slackwolf.routes.response import Response

from operator import itemgetter

bp = Blueprint('game_commands', __name__, url_prefix='/api/v1/games')


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

    current_game = game_manager.get_game(*game_id)
    if current_game is None:
        game_manager.create_new_game(team_data, channel_data, user_data)

        return Response(f"Game lobby updated: @{user_data[1]}").as_public()
    elif user_data[0] in [x.user.slack_id for x in current_game.users]:
        return Response(
            f"You've already joined, @{user_data[1]}!"
        ).as_ephimeral()
    elif current_game.status is not GameStatus.WAITING:
        return Response(
            "Sorry, a game is already in progress on this channel"
        ).as_ephimeral()
    else:
        game_manager.join_game_lobby(user_data, current_game)
        users_list = [f"@{x.user.username}" for x in current_game.users]

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
    current_game = game_manager.get_game(team_id, channel_id)
    users_id = current_game and [x.user.slack_id for x in current_game.users]

    if current_game is None or user_id not in users_id:
        return Response(
            "You haven't joined the current game lobby yet!"
        ).as_ephimeral()
    elif current_game.status is not GameStatus.WAITING:
        return Response(
            "Sorry, cannot leave a game currently in progress"
        ).as_ephimeral()
    else:
        game_manager.leave_game_lobby(user_id, current_game)
        users_list = [f"@{x.user.username}" for x in current_game.users]
        if len(users_list):
            msg = f"Game lobby updated: {','.join(users_list)}"
        else:
            msg = "Game lobby is empty"
        return Response(msg).as_public()


@bp.route('/start', methods=['POST'])
def start_game():
    """Starts a game lobby.

    Triggers the bot to start the game lobby in the current channel.

    - Will publicly list the users present, and start the game.
    - Will assign roles to every participant, and send them a message
      with the details of their role.
    - Will fail and inform the user if he's not part of the game lobby.
    - Will fail and inform the user if a game is already underway.

    TODO: Check if we can send a channel as argument and pick up the ID

    """
    team_id, channel_id, user_id = \
        itemgetter('team_id', 'channel_id', 'user_id')(request.form)
    current_game = game_manager.get_game(team_id, channel_id)
    users_id = current_game and [x.user.slack_id for x in current_game.users]

    if current_game is None or user_id not in users_id:
        return Response(
            "You haven't joined the current game lobby yet!"
        ).as_ephimeral()
    elif current_game.status is not GameStatus.WAITING:
        return Response(
            "The game has already started!"
        ).as_ephimeral()
    else:
        game_manager.start_game(current_game)

        for game_user in current_game.users:
            users_data = slack.get_users_list()
            user_sid = game_user.user.slack_id
            user_data = next(x for x in users_data if x['user'] == user_sid)

            msg = f"Your new role is {game_user.role.value}. " \
                "Type /swhelp if you need more information."
            slack.post_message(user_data['id'], msg)

        return Response(
            "Dummy response. Game started!"
        ).as_public()
