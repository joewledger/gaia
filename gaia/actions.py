from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod
from copy import deepcopy

from gaia.players import Player, Cost
from gaia.map import Hexagon, InhabitedPlanet
from gaia.planet_types import PlanetType
from gaia.buildings import Building


class Action(ABC):
    valid_str = "Action is valid"

    @property
    @abstractmethod
    def ends_turn(self) -> bool:
        pass

    def __str__(self):
        return str(type(self).__name__)


class ModifiesFinalActionWithBonus(object):
    @abstractmethod
    def modify_final_action(self, action: FinalAction) -> FinalAction:
        pass


class FinalAction(Action):
    """
    Any action that when taken will end the players turn
    """
    @property
    def ends_turn(self) -> bool:
        return True

    @abstractmethod
    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


class FreeAction(Action):
    """
    Any action that does not end a players turn.
    These include currency conversion actions (i.e. power -> gold)
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @abstractmethod
    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


class PartialAction(Action, ModifiesFinalActionWithBonus):
    """
    Similar to an free action,
    but must be played in conjunction with an action that will end the players turn.
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @abstractmethod
    def validate_next_action(self, action: FinalAction) -> bool:
        pass


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


class IllegalFinalActionException(Exception):
    pass


class GaiaformAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction on the same hex
    """
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon

    def validate_next_action(self, action: Action) -> Tuple[bool, str]:
        if not isinstance(action, PlaceMineAction):
            return False, "GaiaformAction must be followed by PlaceMineAction"
        elif not hasattr(action, "hexagon") or action.hexagon != self.hexagon:
            return False, "GaiaformAction must be on the same hexagon as PlaceMineAction"
        return True, self.valid_str

    def modify_final_action(self, action: PlaceMineAction) -> PlaceMineAction:
        if not hasattr(action, "base_gaiaforming"):
            raise IllegalFinalActionException("Final action must have property base_gaiaforming")

        copy_action = deepcopy(action)
        copy_action.base_gaiaforming += 3
        return copy_action


class GainRangeAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """

    def validate_next_action(self, action: Action) -> Tuple[bool, str]:
        if not (isinstance(action, PlaceMineAction) or isinstance(action, StartGaiaProjectAction)):
            return False, "GainRangeAction must be followed by PlaceMineAction or StartGaiaProjectAction"
        return True, self.valid_str

    def modify_final_action(self, action: FinalAction) -> FinalAction:
        if not hasattr(action, "base_navigation"):
            raise IllegalFinalActionException("Final action must have property base_navigation")

        copy_action = deepcopy(action)
        copy_action.base_navigation += 3
        return copy_action


class PlaceMineAction(FinalAction):
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon
        self.base_navigation = 0
        self.base_gaiaforming = 0

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        game_map = gamestate.game_map

        planet = game_map.get_planet(self.hexagon)
        if planet is None:
            return False, "There is not planet on the specified hexagon"

        if isinstance(planet, InhabitedPlanet):
            return False, "This planet is already occupied"

        navigation_range = self.base_navigation + gamestate.research_board.get_player_navigation_ability(player)
        planets_in_range = game_map.get_planets_in_range(self.hexagon, navigation_range, only_inhabited=True)

        if not any(planet.faction == player.faction for planet in planets_in_range):
            return False, "The player is not in range"

        if planet.planet_type == PlanetType.LOST:
            return False, "Cannot build on lost planets"
        elif planet.planet_type == PlanetType.GAIA:
            total_cost = self.cost + Cost(qic=1)
        else:
            gaiaforming_ability = self.base_gaiaforming + gamestate.research_board.get_player_gaiaforming_cost(player)
            total_cost = Cost(ore=gaiaforming_ability * player.get_distance_from_planet_color(planet)) + self.cost

        if not player.can_afford(total_cost):
            return False, "The player cannot afford to place a mine at {}".format(str(planet.hex))

        return True, "The player can place a mine at {}".format(str(planet.hex))

    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        result = gamestate.game_map.inhabit_planet(self.hexagon, player.faction, Building.MINE)
        return result, ("Successfully built mine"
                        if result else
                        "Unable to build mine")

    @property
    def cost(self):
        return Cost(ore=1, credits=2)


class StartGaiaProjectAction(FinalAction):
    def __init__(self, hexagon: Hexagon):
        self.hexagon = hexagon
        self.base_navigation = 0

    def validate(self, gamestate, player_id: str):
        pass

    def perform_action(self, gamestate, player_id: str):
        pass


class PassAction(FinalAction):
    def validate(self, gamestate, player: Player) -> Tuple[bool, str]:
        return True, "It is always valid to pass at the end of the turn"

    def perform_action(self, gamestate, player_id: str):
        pass
