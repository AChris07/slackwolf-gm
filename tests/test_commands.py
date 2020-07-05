import pytest
from slackwolf.api import game_manager
from slackwolf.db.entities import GameUser, User
from slackwolf.db.entities.game import GameStatus
from tests import mocks


def join_game(client, data):
    return client.post('/api/v1/commands/join', data=data)


def leave_game(client, data):
    return client.post('/api/v1/commands/leave', data=data)


def start_game(client, data):
    return client.post('/api/v1/commands/start', data=data)


@pytest.mark.usefixtures("mock_game_manager")
class TestJoinGame:
    data = {
        'team_id': "mock-team-id",
        'team_domain': "Mock Team",
        'channel_id': "mock-channel-id",
        'channel_name': "Mock Channel",
        'user_id': "mock-user-id",
        'user_name': "mockuser"
    }

    def test_game_created(self, client, monkeypatch):
        monkeypatch.setattr(game_manager, "get_game", lambda *_: None)

        rv = join_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: @mockuser'

    def test_game_exists_joined(self, client):
        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "mockuser2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: ' \
            '@mockuser,@mockuser2'

    def test_user_already_joined(self, client):
        rv = join_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You\'ve already joined, @mockuser!'

    def test_game_underway(self, client, monkeypatch):
        mock_game = mocks.get_mock_game()
        mock_game.status = GameStatus.STARTING_NIGHT
        monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)

        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "mockuser2"

        rv = join_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'Sorry, a game is already in progress ' \
            'on this channel'


@pytest.mark.usefixtures("mock_game_manager")
class TestLeaveGame:
    data = {
        'team_id': "mock-team-id",
        'team_domain': "Mock Team",
        'channel_id': "mock-channel-id",
        'channel_name': "Mock Channel",
        'user_id': "mock-user-id",
        'user_name': "mockuser"
    }

    def test_game_left_last(self, client):
        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby is empty'

    def test_game_left_not_last(self, client, monkeypatch):
        mock_game = mocks.get_mock_game()
        user = User(slack_id='mock-user-id-2', username='mockuser2')
        mock_game.users.append(GameUser(user=user))
        monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)

        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Game lobby updated: @mockuser2'

    def test_game_already_left(self, client):
        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "mockuser2"

        rv = leave_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You haven\'t joined ' \
            'the current game lobby yet!'

    def test_game_underway(self, client, monkeypatch):
        mock_game = mocks.get_mock_game()
        mock_game.status = GameStatus.STARTING_NIGHT
        monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)

        rv = leave_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'Sorry, cannot leave a game ' \
            'currently in progress'


@pytest.mark.usefixtures("mock_game_manager")
class TestStartGame:
    data = {
        'team_id': "mock-team-id",
        'team_domain': "Mock Team",
        'channel_id': "mock-channel-id",
        'channel_name': "Mock Channel",
        'user_id': "mock-user-id",
        'user_name': "mockuser"
    }

    def test_game_started(self, client, monkeypatch, mocker):
        mock_game = mocks.get_mock_game()
        monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)
        post_message = mocker.patch('slackwolf.api.slack.post_message')

        rv = start_game(client, self.data)

        assert mock_game.status == GameStatus.STARTING_NIGHT
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'in_channel'
        assert data['text'] == 'Dummy response. Game started!'

        user_im_id = mocks.get_mock_slack_users_data()[0]['id']
        post_message.assert_called_once_with(user_im_id,
                                             'Your new role is Seer. '
                                             'Type /swhelp if you need more information.'
                                             )

    def test_game_start_without_join(self, client):
        data = dict(self.data)
        data['user_id'] = "mock-user-id-2"
        data['user_name'] = "mockuser2"

        rv = start_game(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You haven\'t joined ' \
            'the current game lobby yet!'

    def test_game_start_without_game(self, client, monkeypatch):
        monkeypatch.setattr(game_manager, "get_game", lambda *_: None)

        rv = start_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'You haven\'t joined ' \
            'the current game lobby yet!'

    def test_game_underway(self, client, monkeypatch):
        mock_game = mocks.get_mock_game()
        mock_game.status = GameStatus.STARTING_NIGHT
        monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)

        rv = start_game(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'The game has already started!'
