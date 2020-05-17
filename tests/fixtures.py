from slackwolf.db.entities import Channel,\
    Game,\
    GameUser,\
    Team,\
    User


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
                users=[GameUser(user=mock_user)])
