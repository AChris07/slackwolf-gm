from slackwolf.api import game_manager
from tests import fixtures


class TestGetGame:
    game_data = ("mock-team-id", "mock-channel-id")

    def test_game_not_found(self, mocker):
        channel_find = mocker.patch(
            'slackwolf.api.game_manager.ChannelDao.find_by_sid'
        )
        channel_find.return_value = None

        game = game_manager.get_game(*self.game_data)
        channel_find.assert_called_once_with(*self.game_data)
        assert game is None

    def test_channel_without_game(self, mocker):
        mock_channel = fixtures.get_mock_channel()
        channel_find = mocker.patch(
            'slackwolf.api.game_manager.ChannelDao.find_by_sid'
        )
        channel_find.return_value = mock_channel

        game = game_manager.get_game(*self.game_data)
        channel_find.assert_called_once_with(*self.game_data)
        assert game is None

    def test_game_found(self, mocker):
        mock_game = fixtures.get_mock_game()
        channel_find = mocker.patch(
            'slackwolf.api.game_manager.ChannelDao.find_by_sid'
        )
        channel_find.return_value = mock_game.channel

        game = game_manager.get_game(*self.game_data)
        channel_find.assert_called_once_with(*self.game_data)
        assert game is mock_game


class TestCreateNewGame:
    team_data = ('mock-team-id', 'Mock Team')
    channel_data = ('mock-channel-id', 'Mock Channel')
    user_data = ('mock-user-id', 'mockuser')

    def test_create_new_game(self, mocker):
        mock_channel = fixtures.get_mock_channel()
        mock_user = fixtures.get_mock_user()

        team_get_create = mocker.patch(
            'slackwolf.api.game_manager.TeamDao.get_or_create_by_sid'
        )

        channel_get_create = mocker.patch(
            'slackwolf.api.game_manager.ChannelDao.get_or_create_by_sid'
        )
        channel_get_create.return_value = mock_channel

        user_get_create = mocker.patch(
            'slackwolf.api.game_manager.UserDao.get_or_create_by_sid'
        )
        user_get_create.return_value = mock_user

        game_create = mocker.patch(
            'slackwolf.api.game_manager.GameDao.save'
        )

        game_manager.create_new_game(self.team_data,
                                     self.channel_data,
                                     self.user_data)
        team_get_create.assert_called_once_with(*self.team_data)
        channel_get_create.assert_called_once_with(self.team_data[0],
                                                   *self.channel_data)
        user_get_create.assert_called_once_with(self.team_data[0],
                                                *self.user_data)

        game_create.assert_called_once()
        created_game = game_create.call_args.args[0]

        assert created_game.channel == mock_channel
        assert len(created_game.users) == 1
        assert created_game.users[0].user == mock_user


class TestJoinGameLobby:
    user_data = ('mock-user-id', 'mockuser')
    mock_game = fixtures.get_mock_game()

    def test_join_game_lobby(self, mocker):
        mock_user = fixtures.get_mock_user()

        user_get_create = mocker.patch(
            'slackwolf.api.game_manager.UserDao.get_or_create_by_sid'
        )
        user_get_create.return_value = mock_user

        add_user = mocker.patch(
            'slackwolf.api.game_manager.GameDao.add_user'
        )

        game_manager.join_game_lobby(self.user_data, self.mock_game)
        add_user.assert_called_once_with(self.mock_game, mock_user)


class TestLeaveGomeLobby:
    mock_team_id = 'mock-team-id'
    mock_user_id = 'mock-user-id'
    mock_game = fixtures.get_mock_game()

    def test_leave_game_lobby(self, mocker):
        mock_user = fixtures.get_mock_user()

        find_user = mocker.patch(
            'slackwolf.api.game_manager.UserDao.find_by_sid'
        )
        find_user.return_value = mock_user

        remove_user = mocker.patch(
            'slackwolf.api.game_manager.GameDao.remove_user'
        )

        game_manager.leave_game_lobby(self.mock_user_id, self.mock_game)
        remove_user.assert_called_once_with(self.mock_game, mock_user)

    def test_no_user_found(self, mocker):
        find_user = mocker.patch(
            'slackwolf.api.game_manager.UserDao.find_by_sid'
        )
        find_user.return_value = None

        remove_user = mocker.patch(
            'slackwolf.api.game_manager.GameDao.remove_user'
        )

        game_manager.leave_game_lobby(self.mock_user_id, self.mock_game)
        assert not remove_user.called
