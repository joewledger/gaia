import pytest

from gaia.turn_validator import Turn
from gaia.actions import (PlaceMineAction, PassAction, GaiaformAction,
                          GainRangeAction, ExchangeOreForCreditAction,
                          StartGaiaProjectAction)
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
        "GaiaformAction must be on the same hexagon as PlaceMineAction"
    ),
    (
        [
            GaiaformAction(Hexagon(0, 0)),
            PassAction
        ],
        False,
        'GaiaformAction must be followed by PlaceMineAction'
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
        "GainRangeAction must be followed by PlaceMineAction or StartGaiaProjectAction"
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
