import slackwolf.api.game_manager as game_manager


def join_game(client, data):
    return client.post('/api/v1/commands/join', data=data)


class TestJoinGame:
    def test_game_created(self, client):
        store = game_manager.game_store
        assert store == {}

        data = {
            'team_id': "mock-team-id",
            'team_domain': "Mock Team",
            'channel_id': "mock-channel-id",
            'channel_name': "Mock Channel",
            'user_id': "mock-user-id",
            'user_name': "Mock User"
        }
        rv = join_game(client, data)

        assert rv.status_code == 200
        assert rv.data == b'Welcome to the game lobby! Users: @mock-user-id'
        created_game = store['mock-team-id']\
            .channels['mock-channel-id'].game
        assert created_game is not None
        assert len(created_game.users.keys()) == 1

    def test_game_exists_joined(self, client, mock_game_store):
        data = {
            'team_id': "mock-team-id",
            'team_domain': "Mock Team",
            'channel_id': "mock-channel-id",
            'channel_name': "Mock Channel",
            'user_id': "mock-user-id-2",
            'user_name': "Mock User 2"
        }
        rv = join_game(client, data)
        assert rv.status_code == 200
        assert rv.data == b'Welcome to the game lobby! ' \
            b'Users: @mock-user-id,@mock-user-id-2'
