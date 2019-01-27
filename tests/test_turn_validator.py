import pytest

from gaia.turns.turn_validator import Turn
from gaia.turns.actions import (PlaceMineAction, PassAction, GaiaformAction,
                          GainRangeAction, ExchangeOreForCreditAction,
                          StartGaiaProjectAction)
from gaia.board.map import Hexagon


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
            PlaceMineAction(Hexagon(0, 0))
        ],
        True,
        None
    ),
    (
        [
            ExchangeOreForCreditAction(1),
            PlaceMineAction(Hexagon(0, 0))
        ],
        True,
        None
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0))
        ],
        False,
        "The last action in a turn must end the turn, but GaiaformAction did not"
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0)),
            PlaceMineAction(Hexagon(0, 0))
        ],
        True,
        None
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0)),
            PlaceMineAction(Hexagon(1, 0))
        ],
        False,
        GaiaformAction.ILLEGAL_PLACEMENT_MESSAGE
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0)),
            PassAction
        ],
        False,
        GaiaformAction.ILLEGAL_ACTION_MESSAGE
    ),
    (
        [
            GainRangeAction(),
            PlaceMineAction(Hexagon(0, 0))
        ],
        True,
        None
    ),
    (
        [
            GainRangeAction(),
            StartGaiaProjectAction(Hexagon(0, 0))
        ],
        True,
        None
    ),
    (
        [
            GainRangeAction(),
            PassAction()
        ],
        False,
        GainRangeAction.ILLEGAL_ACTION_MESSAGE
    ),
    (
        [],
        False,
        "The turn had no actions in it"
    )
])
def test_turn_validity(actions, should_be_valid, main_reason,
                       starting_gamestate, mocker):
    turn = Turn(actions, starting_gamestate, "p1")

    mocker.patch.object(turn, '_check_all_actions_are_valid')
    turn._check_all_actions_are_valid.return_value = []

    validity, reasons = turn.validate()
    assert validity == should_be_valid
    if main_reason:
        assert (main_reason in reasons)


@pytest.mark.parametrize("actions,should_be_valid", [
    (
        [
            PlaceMineAction(Hexagon(0, -1))
        ],
        True
    ),
    (
        [
            PlaceMineAction(Hexagon(5, -3))
        ],
        False
    ),
    (
        [
            GainRangeAction(),
            PlaceMineAction(Hexagon(5, -3))
        ],
        True
    )
])
def test_final_action_modification(actions, should_be_valid,
                                   test_range_gamestate, mocker):

    mocker.patch.object(test_range_gamestate, "research_board")
    test_range_gamestate.research_board.get_player_navigation_ability.return_value = 2

    turn = Turn(actions, test_range_gamestate, "p1")
    valid, reasons = turn.validate()
    assert valid == should_be_valid
