from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass
from copy import deepcopy

from gaia.actions import Action, PartialAction
from gaia.gamestate import GameState


@dataclass()
class Turn(object):
    actions: List[Action]
    gamestate: GameState
    player_id: str

    def validate(self) -> Tuple[bool, List[str]]:
        validation_errors = []

        validation_errors += self._check_action_doesnt_end_prematurely()
        validation_errors += self._check_last_action_ends_turn()
        validation_errors += self._check_partial_action_has_following_action()
        validation_errors += self._check_all_actions_are_valid()

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

        return []

    def _check_partial_action_has_following_action(self) -> List[str]:
        validation_errors = []

        for i in range(len(self.actions) - 1):
            action, next_action = self.actions[i], self.actions[i+1]
            if isinstance(action, PartialAction):
                valid, reason = action.validate_next_action(next_action)
                if not valid:
                    validation_errors.append(reason)

        return validation_errors

    def _check_all_actions_are_valid(self) -> List[str]:
        gamestate = deepcopy(self.gamestate)
        validation_errors = []

        for action in self.actions:
            if isinstance(action, PartialAction):
                self.actions[-1] = action.modify_final_action(self.actions[-1])
            else:
                valid, reason = action.validate(gamestate, self.player_id)
                if not valid:
                    validation_errors.append("{} is not valid for the following reason: {}".format(str(action), reason))

        return validation_errors
