from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod
from copy import deepcopy

from gaia.players import Player, Cost
from gaia.map import Hexagon, InhabitedPlanet


class Action(ABC):
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
    pass


class PassAction(FullAction):
    def validate(self, gamestate, player: Player) -> Tuple[bool, str]:
        return True, "It is always valid to pass at the end of the turn"
