import pytest

from gaia.turn_validator import Turn
from gaia.actions import PlaceMineAction, PassAction, GaiaformAction
from gaia.map import Hexagon


@pytest.mark.parametrize("actions,should_be_valid,main_reason", [
    (
        [
            PlaceMineAction(Hexagon(0, 0)),
            PassAction()
        ],
        False,
        "PlaceMineAction ends the turn, but was not the last action in the turn."
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0))
        ],
        False,
        "The last action in a turn must end the turn, but GaiaformAction did not"
    ),
    (
        [],
        False,
        "The turn had no actions in it"
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0)),
            PassAction
        ],
        False,
        'GaiaformAction is a partial action, and the action that follows it is not valid for that partial action'
    )
])
def test_turn_validity(actions, should_be_valid, main_reason,
                       starting_gamestate, mocker):
    turn = Turn(actions, starting_gamestate, "p1")

    mocker.patch.object(turn, '_check_all_actions_are_valid')
    turn._check_all_actions_are_valid.return_value = (True, [])

    validity, reasons = turn.validate()
    assert validity == should_be_valid
    assert (main_reason in reasons)
