from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod

from gaia.players import Player, Cost
from gaia.map import Hexagon, InhabitedPlanet


class Action(ABC):
    valid_str = "Action is valid"

    @property
    @abstractmethod
    def ends_turn(self) -> bool:
        pass

    @abstractmethod
    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    def __str__(self):
        return str(type(self).__name__)


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


class ExchangeOreForCreditAction(FreeAction):
    """
    Exchange one ore for one credit
    """
    def __init__(self, num_times):
        self.num_times = num_times

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


class PartialAction(Action):
    """
    Similar to an free action,
    but must be played in conjunction with an action that will end the players turn.
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @abstractmethod
    def validate_next_action(self, action: FullAction) -> bool:
        pass


class GaiaformAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction on the same hex
    """
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    def perform_action(self, gamestate, player_id: str):
        pass

    def validate_next_action(self, action: Action) -> Tuple[bool, str]:
        if not isinstance(action, PlaceMineAction):
            return False, "GaiaformAction must be followed by PlaceMineAction"
        elif not hasattr(action, "hexagon") or action.hexagon != self.hexagon:
            return False, "GaiaformAction must be on the same hexagon as PlaceMineAction"
        return True, self.valid_str


class GainRangeAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    def validate(self, gamestate, player_id: str):
        pass

    def perform_action(self, gamestate, player_id: str):
        pass

    def validate_next_action(self, action: Action) -> Tuple[bool, str]:
        if not (isinstance(action, PlaceMineAction) or isinstance(action, StartGaiaProjectAction)):
            return False, "GainRangeAction must be followed by PlaceMineAction or StartGaiaProjectAction"
        return True, self.valid_str


class PlaceMineAction(FullAction):
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
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

    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @property
    def cost(self):
        return Cost(ore=1, credits=2)


class StartGaiaProjectAction(FullAction):
    def __init__(self, hexagon: Hexagon):
        self.hexaon = hexagon

    def validate(self, gamestate, player_id: str):
        pass

    def perform_action(self, gamestate, player_id: str):
        pass


class PassAction(FullAction):
    def validate(self, gamestate, player: Player) -> Tuple[bool, str]:
        return True, "It is always valid to pass at the end of the turn"

    def perform_action(self, gamestate, player_id: str):
        pass
