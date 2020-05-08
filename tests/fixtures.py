from slackwolf.db.entities import Channel,\
    Game,\
    GameUser,\
    Team,\
    User


def get_mock_game():
    mock_team = Team(slack_id='mock-team-id',
                     name='Mock Team')

    mock_channel = Channel(slack_id='mock-channel-id',
                           name='Mock Channel',
                           team=mock_team)

    mock_user = User(slack_id='mock-user-id',
                     username='mockuser',
                     team=mock_team)

    return Game(channel=mock_channel,
                users=[GameUser(user=mock_user)])
