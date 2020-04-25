import slackwolf.api.game_manager as game_manager
from slackwolf.api.entities.game import GameStatus
from slackwolf.api.entities import User


def join_game(client, data):
    return client.post('/api/v1/commands/join', data=data)


def leave_game(client, data):
    return client.post('/api/v1/commands/leave', data=data)


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
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: @mock-user-id'
        created_game = store['mock-team-id'].channels[0].game
        assert created_game is not None
        assert len(created_game.users) == 1

    def test_game_exists_joined(self, client, mock_game_store):
        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "Mock User 2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: ' \
            '@mock-user-id,@mock-user-id-2'

    def test_user_already_joined(self, client, mock_game_store):
        rv = join_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You\'ve already joined, @mock-user-id!'

    def test_game_underway(self, client, mock_game_store):
        game = mock_game_store['mock-team-id'].channels[0].game
        game.status = GameStatus.STARTED

        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "Mock User 2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'Sorry, a game is already in progress ' \
            'on this channel'


class TestLeaveGame:
    data = {
        'team_id': "mock-team-id",
        'team_domain': "Mock Team",
        'channel_id': "mock-channel-id",
        'channel_name': "Mock Channel",
        'user_id': "mock-user-id",
        'user_name': "Mock User"
    }

    def test_game_left_last(self, client, mock_game_store):
        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby is empty'

    def test_game_left_not_last(self, client, mock_game_store):
        user = User('mock-user-id-2', 'Mock User 2')
        game = mock_game_store['mock-team-id'].channels[0].game
        game.users.append(user)

        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: @mock-user-id-2'

    def test_game_already_left(self, client):
        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You haven\'t joined ' \
            'the current game lobby yet!'

    def test_game_underway(self, client, mock_game_store):
        game = mock_game_store['mock-team-id'].channels[0].game
        game.status = GameStatus.STARTED

        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'Sorry, cannot leave a game ' \
            'currently in progress'
