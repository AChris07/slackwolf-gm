import pytest

from slackwolf import create_app
import slackwolf.api.game_manager as game_manager


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
    game_manager.create_new_game(
        ("mock-team-id", "Mock Team"),
        ("mock-channel-id", "Mock Channel"),
        ("mock-user-id", "Mock User")
    )

    mock_game_store = game_manager.game_store.copy()
    monkeypatch.setattr(game_manager, "game_store", mock_game_store)
    return mock_game_store
