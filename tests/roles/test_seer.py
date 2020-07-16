import pytest
from slackwolf.db.entities.game import GameStatus
from slackwolf.db.entities.game_user import GameUser
from slackwolf.db.entities.user import User
from slackwolf.models.exceptions import RoleCommandException
from slackwolf.roles.seer import Seer
from slackwolf.roles.types import RoleTypes
from tests import mocks


def get_mock_started_game():
    mock_game = mocks.get_mock_game()
    mock_game.status = GameStatus.STARTING_NIGHT
    mock_game.users[0].role = RoleTypes.SEER
    mock_target = User(slack_id='mock-target-id',
                       username='mocktarget',
                       team=mock_game.channel.team)
    mock_game.users.append(GameUser(user=mock_target,
                                    role=RoleTypes.WEREWOLF))

    return mock_game


class TestSeerSee:
    def test_see_werewolf(self):
        mock_game = get_mock_started_game()
        msg = Seer.see(mock_game.users[0], '@mocktarget')

        assert msg == 'Seer, @mocktarget is a Werewolf'

    def test_see_not_werewolf(self):
        mock_game = get_mock_started_game()
        mock_game.users[1].role = RoleTypes.VILLAGER
        msg = Seer.see(mock_game.users[0], '@mocktarget')

        assert msg == 'Seer, @mocktarget is not a Werewolf'

    def test_see_invalid_target(self):
        mock_game = get_mock_started_game()
        with pytest.raises(RoleCommandException) as e:
            assert Seer.see(mock_game.users[0], '@mockinvalidtarget')

        assert str(e.value) == 'User @mockinvalidtarget not found'

    def test_see_invalid_game_state(self):
        mock_game = get_mock_started_game()
        mock_game.status = GameStatus.DAY
        with pytest.raises(RoleCommandException) as e:
            assert Seer.see(mock_game.users[0], '@mockinvalidtarget')

        assert str(e.value) == 'Can only be used at night!'
