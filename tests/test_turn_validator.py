from gaia.turn_validator import Turn
from gaia.actions import PlaceMineAction, PassAction, GaiaformAction
from gaia.map import Hexagon


def test_early_terminators_are_illegal(starting_gamestate):
    actions = [
        PlaceMineAction(Hexagon(0, 0)),
        PassAction()
    ]

    turn = Turn(actions, starting_gamestate, "p1")
    valid, reasons = turn.validate()
    assert not valid
    assert ("PlaceMineAction ends the turn, but was not the last action in the turn." in reasons)


def test_last_action_must_ends_turn(patch_check_all_actions, starting_gamestate):
    actions = [
        GaiaformAction(Hexagon(0, 0))
    ]

    turn = patch_check_all_actions(Turn(actions, starting_gamestate, "p1"))

    valid, reasons = turn.validate()
    assert not valid
    assert ("The last action in a turn must end the turn, but GaiaformAction did not" in reasons)


def test_empty_turn_is_invalid(starting_gamestate):
    turn = Turn([], starting_gamestate, "p1")

    valid, reasons = turn.validate()
    assert not valid
    assert ("The turn had no actions in it" in reasons)


def test_partial_actions_has_valid_following_action(patch_check_all_actions, starting_gamestate):
    actions = [GaiaformAction(Hexagon(0, 0)), PassAction]

    turn = patch_check_all_actions(Turn(actions, starting_gamestate, "p1"))

    valid, reasons = turn.validate()
    assert not valid
    assert 'GaiaformAction is a partial action, and the action that follows it is not valid for that partial action' in reasons
