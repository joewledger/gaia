from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod
from copy import deepcopy

from gaia.players import Player, Cost
from gaia.map import Hexagon, InhabitedPlanet
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

    def _check_partial_action_has_following_action(self) -> List[str]:
        validation_errors = []

        for i in range(len(self.actions) - 1):
            action, next_action = self.actions[i], self.actions[i+1]
            if isinstance(action, PartialAction):
                if not any(isinstance(next_action, allowed_type) for allowed_type in action.valid_following_actions):
                    validation_errors.append(
                        "{} is a partial action, and the action that follows it is not valid for that partial action"
                        .format(str(action))
                    )

        return validation_errors

    def _check_all_actions_are_valid(self) -> List[str]:
        gamestate = deepcopy(self.gamestate)
        validation_errors = []

        for action in self.actions:
            valid, reason = action.validate(gamestate, self.player_id)
            if not valid:
                validation_errors.append("{} is not valid for the following reason: {}".format(str(action), reason))

        return validation_errors


class Action(ABC):
    @property
    @abstractmethod
    def ends_turn(self) -> bool:
        pass

    @abstractmethod
    def validate(self, gamestate: GameState, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate: GameState, player_id: str) -> Tuple[bool, str]:
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
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon

    def validate(self, gamestate: GameState, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        game_map = gamestate.game_map

        planet = game_map.get_planet(self.hexagon)
        if planet is None:
            return False, "There is not planet on the specified hexagon"

        if isinstance(planet, InhabitedPlanet):
            return False, "This planet is already occupied"

        navigation_range = gamestate.research_board.get_player_navigation_ability(player)
        planets_in_range = game_map.get_planets_in_range(self.hexagon, navigation_range, only_inhabited=True)

        if not any(planet.faction == player.faction for planet in planets_in_range):
            return False, "The player is not in range"

        gaiaforming_ability = gamestate.research_board.get_player_gaiaforming_cost(player)
        total_cost = Cost(ore=gaiaforming_ability*player.get_distance_from_planet_color(planet)) + self.cost

        if not player.can_afford(total_cost):
            return False, "The player cannot afford to place a mine at {}".format(str(planet.hex))

        return True, "The player can place a mine at {}".format(str(planet.hex))

    def perform_action(self, gamestate: GameState, player_id: str) -> Tuple[bool, str]:
        pass

    @property
    def cost(self):
        return Cost(ore=1, credits=2)


class StartGaiaProjectAction(FullAction):
    pass


class PassAction(FullAction):
    @abstractmethod
    def validate(self, gamestate: GameState, player: Player) -> Tuple[bool, str]:
        return True, "It is always valid to pass at the end of the turn"
