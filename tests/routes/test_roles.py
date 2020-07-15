import pytest
from slackwolf.api import game_manager
from slackwolf.db.entities.game import GameStatus
from slackwolf.db.entities.game_user import GameUser
from slackwolf.db.entities.user import User
from slackwolf.roles.seer import Seer
from slackwolf.roles.types import RoleTypes
from slackwolf.models.exceptions import RoleCommandException
from tests import mocks


def see_user(client, data):
    return client.post('/api/v1/roles/see', data=data)


@pytest.fixture
def mock_started_game(mock_game_manager, monkeypatch):
    mock_game = mocks.get_mock_game()
    mock_game.status = GameStatus.STARTING_NIGHT
    mock_game.users[0].role = RoleTypes.SEER
    mock_target = User(slack_id='mock-target-id',
                       username='mocktarget',
                       team=mock_game.channel.team)
    mock_game.users.append(GameUser(user=mock_target,
                                    role=RoleTypes.WEREWOLF))

    monkeypatch.setattr(game_manager, "get_game", lambda *_: mock_game)


@pytest.mark.usefixtures("mock_started_game")
class TestSee:
    data = {**mocks.mock_payload, 'text': "@mocktarget"}

    def test_see_success(self, client):
        rv = see_user(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == 'Seer, @mocktarget is a Werewolf'

    def test_see_failure(self, client, monkeypatch):
        def raise_command_exception(*args):
            raise RoleCommandException("Mock Exception")

        monkeypatch.setattr(Seer, "see", raise_command_exception)
        rv = see_user(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == "Mock Exception"

    def test_user_cannot_see(self, client):
        mock_game = game_manager.get_game()
        mock_game.users[0].role = RoleTypes.VILLAGER

        rv = see_user(client, self.data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == "You can't use this ability!"

    def test_user_not_in_game(self, client):
        data = {
            **self.data,
            'user_id': "mock-invalid-user-id",
            'user_name': "mockinvaliduser"
        }
        rv = see_user(client, data)

        assert rv.status_code == 200
        data = rv.get_json()
        assert data['response_type'] == 'ephimeral'
        assert data['text'] == "You haven't joined the current game lobby yet!"
