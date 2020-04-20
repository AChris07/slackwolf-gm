import slackwolf.api.game_manager as game_manager
from slackwolf.models.Game import GameStatus


def join_game(client, data):
    return client.post('/api/v1/commands/join', data=data)


class TestJoinGame:
    data = {
        'team_id': "mock-team-id",
        'team_domain': "Mock Team",
        'channel_id': "mock-channel-id",
        'channel_name': "Mock Channel",
        'user_id': "mock-user-id",
        'user_name': "Mock User"
    }

    def test_game_created(self, client):
        store = game_manager.game_store
        assert store == {}

        rv = join_game(client, self.data)

        assert rv.status_code == 200
        assert rv.data == b'Welcome to the game lobby! Users: @mock-user-id'
        created_game = store['mock-team-id']\
            .channels['mock-channel-id'].game
        assert created_game is not None
        assert len(created_game.users.keys()) == 1

    def test_game_exists_joined(self, client, mock_game_store):
        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "Mock User 2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        assert rv.data == b'Welcome to the game lobby! ' \
            b'Users: @mock-user-id,@mock-user-id-2'

    def test_user_already_joined(self, client, mock_game_store):
        rv = join_game(client, self.data)

        assert rv.status_code == 200
        assert rv.data == b'You\'ve already joined @mock-user-id!'

    def test_game_underway(self, client, mock_game_store):
        game = mock_game_store['mock-team-id'].channels['mock-channel-id'].game
        game.status = GameStatus.STARTED

        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "Mock User 2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        assert rv.data == b'Sorry, a game is already in progress ' \
            b'on this channel'
