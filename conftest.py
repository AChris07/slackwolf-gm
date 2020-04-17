import pytest

from slackwolf import create_app
import slackwolf.api.game_manager as game_manager
from slackwolf.models import Team, Channel, Game, User


@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_game_store():
    initial_game_store = dict(game_manager.game_store)
    yield
    game_manager.game_store = initial_game_store


@pytest.fixture
def mock_game_store(monkeypatch) -> dict:
    mock_game_store = {}
    mock_team = Team("mock-team-id", "Mock Team")
    mock_channel = Channel("mock-channel-id", "Mock Channel")
    mock_user = User("mock-user-id", "Mock User")
    mock_game = Game()

    mock_game.users[mock_user.id] = mock_user
    mock_channel.game = mock_game
    mock_team.channels[mock_channel.id] = mock_channel
    mock_game_store[mock_team.id] = mock_team

    monkeypatch.setattr(game_manager, "game_store", mock_game_store)
    return mock_game_store
