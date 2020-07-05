from slackwolf.db.entities import Channel,\
    Game,\
    GameUser,\
    Team,\
    User
from slackwolf.db.entities.game import GameStatus


def get_mock_channel():
    mock_team = Team(slack_id='mock-team-id',
                     name='Mock Team')

    return Channel(slack_id='mock-channel-id',
                   name='Mock Channel',
                   team=mock_team)


def get_mock_user():
    mock_channel = get_mock_channel()

    return User(slack_id='mock-user-id',
                username='mockuser',
                team=mock_channel.team)


def get_mock_game():
    mock_channel = get_mock_channel()
    mock_user = get_mock_user()

    return Game(channel=mock_channel,
                users=[GameUser(user=mock_user)],
                status=GameStatus.WAITING)


def get_mock_slack_users_data():
    return [{
        "id": "mock-user-im-id",
        "created": 1587093834,
        "is_archived": False,
        "is_im": True,
        "is_org_shared": False,
        "user": "mock-user-id",
        "is_user_deleted": False,
        "priority": 0
    }]
