from slackwolf.api import get_game


class TestGetGame:
    def test_game_not_found(self):
        game = get_game("mock-team-id", "mock-channel-id")
        assert game is None

    def test_game_found(self, mock_game_store):
        game = get_game("mock-team-id", "mock-channel-id")
        mock_game = mock_game_store['mock-team-id']\
            .channels['mock-channel-id'].game
        assert game is mock_game
