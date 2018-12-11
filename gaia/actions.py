from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod

from gaia.players import Player
from gaia.map import Map, Hexagon
from gaia.gamestate import GameState, ResearchBoard


@dataclass()
class Turn(object):
    actions: List[Action]
    player: Player

    def validate(self, gamestate: GameState) -> Tuple[bool, List[str]]:
        validation_errors = []

        validation_errors += self._check_action_doesnt_end_prematurely()
        validation_errors += self._check_last_action_ends_turn()
        validation_errors += self._check_partial_action_has_following_action()
        validation_errors += self._check_all_actions_are_valid(gamestate)

        return len(validation_errors) == 0, validation_errors

    def _check_action_doesnt_end_prematurely(self) -> List[str]:
        return [
            "{} ends the turn, but was not the last action in the turn.".format(str(action))
            for action in self.actions[:-1] if action.ends_turn
        ]

    def _check_last_action_ends_turn(self) -> List[str]:
        if len(self.actions) == 0:
            return ["The turn had no actions in it"]

        last_action = self.actions[-1]

        if not last_action.ends_turn:
            return ["The last action in a turn must end the turn, but {} did not".format(str(last_action))]

    def _check_partial_action_has_following_action(self) -> List[str]:
        validation_errors = []

        for i in range(len(self.actions) - 1):
            action, next_action = self.actions[i], self.actions[i+1]
            if isinstance(action, PartialAction) and not isinstance(next_action, FullAction):
                validation_errors.append(
                    "{} is a partial action, but the action that follows it is not a full action"
                    .format(str(action))
                )

        return validation_errors

    def _check_all_actions_are_valid(self, gamestate: GameState) -> List[str]:
        validation_errors = []

        for action in self.actions:
            valid, reason = action.validate(gamestate, self.player)
            if not valid:
                validation_errors.append("{} is not valid for the following reason: {}".format(str(action), reason))

        return validation_errors


class Action(ABC):
    @property
    @abstractmethod
    def ends_turn(self) -> bool:
        pass

    @abstractmethod
    def validate(self, gamestate: GameState, player: Player) -> Tuple[bool, str]:
        pass


class FullAction(Action):
    """
    Any action that when taken will end the players turn
    """
    @property
    def ends_turn(self) -> bool:
        return True


class FreeAction(Action):
    """
    Any action that does not end a players turn.
    These include currency conversion actions (i.e. power -> gold)
    """

    @property
    def ends_turn(self) -> bool:
        return False


class PartialAction(Action):
    """
    Similar to an free action,
    but must be played in conjunction with an action that will end the players turn.
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @property
    @abstractmethod
    def valid_following_actions(self):
        pass


class GaiaformAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    @property
    def valid_following_actions(self):
        return [PlaceMineAction, StartGaiaProjectAction]


class GainRangeAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    @property
    def valid_following_actions(self):
        return [PlaceMineAction, StartGaiaProjectAction]


class PlaceMineAction(FullAction):
    def __init__(self, player: Player, hexagon: Hexagon, map: Map, research_board: ResearchBoard):
        pass


class StartGaiaProjectAction(FullAction):
    pass
