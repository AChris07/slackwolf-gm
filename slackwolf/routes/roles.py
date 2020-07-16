from flask import Blueprint, request
from operator import itemgetter

from slackwolf.api import game_manager
from slackwolf.models.exceptions import RoleCommandException
from slackwolf.roles.utils import get_role_class
from slackwolf.routes.response import Response

bp = Blueprint('role_commands', __name__, url_prefix='/api/v1/roles')


@bp.route('/see', methods=['POST'])
def see():
    """See the identity of another player.

    See the identity of another player in the current game.
    The bot will reply with whether that player is a Werewolf or not.

    - Will fail and inform the user if he's is not part of the
    current game, or if the game has not started.
    - Will fail and inform the user if his role does not have a see
    command (ie. Seer)
    - Will also fail and inform the user if he can't use the command
    in the current game status (ie. during the day)

    """
    team_id, channel_id, user_id = \
        itemgetter('team_id', 'channel_id', 'user_id')(request.form)
    text = request.form['text']
    target_username = text.split()[0]

    current_game = game_manager.get_game(team_id, channel_id)
    try:
        game_user = current_game and \
            next(x for x in current_game.users if x.user.slack_id == user_id)
    except StopIteration:
        game_user = None

    if not game_user:
        return Response(
            "You haven't joined the current game lobby yet!"
        ).as_ephimeral()
    else:
        try:
            user_role = get_role_class(game_user.role)
            msg = user_role.see(game_user, target_username)
        except RoleCommandException as e:
            msg = str(e)
        except AttributeError:
            msg = "You can't use this ability!"

        return Response(msg).as_ephimeral()
