import pytest

from slackwolf import create_app
from slackwolf.api import game_manager
from slackwolf.db.entities import User, GameUser
from tests import fixtures


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///test.db'
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_game_manager(monkeypatch):
    monkeypatch.setattr(game_manager,
                        "get_game",
                        lambda *_: fixtures.get_mock_game())

    monkeypatch.setattr(game_manager, "create_new_game", lambda *_: None)

    def mock_join_game(user_data, game):
        id, name = user_data
        user = User(slack_id=id, username=name)
        game.users.append(GameUser(user=user))

    monkeypatch.setattr(game_manager, "join_game_lobby", mock_join_game)

    def mock_leave_game(team_id, user_id, game):
        new_game_users = [x for x in game.users if x.user.slack_id != user_id]
        game.users = new_game_users

    monkeypatch.setattr(game_manager, "leave_game_lobby", mock_leave_game)
