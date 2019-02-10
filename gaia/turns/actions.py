from __future__ import annotations
from typing import Tuple
from copy import deepcopy

from gaia.gamestate.players import Player, Cost
from gaia.board.map import Hexagon, InhabitedPlanet
from gaia.utils.enums import PlanetType, Building

from gaia.turns.action_types import Action, FreeAction, PartialAction, FinalAction
from gaia.turns.action_modifiers import NavigationModifiable, GaiaformingRequirementsModifiable, HasHexagonLocation


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


class GaiaformAction(PartialAction, HasHexagonLocation):
    FREE_GAIAFORM_BONUS = 1
    ILLEGAL_ACTION_MESSAGE = "GaiaformAction must be followed by a final action that requires gaiaforming"
    ILLEGAL_PLACEMENT_MESSAGE = "GaiaformAction must be used on the same hexagon as the action it modifies"

    def __init__(self, hexagon: Hexagon):
        HasHexagonLocation.__init__(self, hexagon)

    def validate_next_action(self, action: Action) -> Tuple[bool, str]:
        if not isinstance(action, GaiaformingRequirementsModifiable):
            return False, self.ILLEGAL_ACTION_MESSAGE
        elif not isinstance(action, HasHexagonLocation) or action.hexagon != self.hexagon:
            return False, self.ILLEGAL_PLACEMENT_MESSAGE
        return True, self.valid_str

    def modify_final_action(self, action: GaiaformingRequirementsModifiable) -> GaiaformingRequirementsModifiable:
        if not isinstance(action, GaiaformingRequirementsModifiable):
            raise IllegalFinalActionException(self.ILLEGAL_ACTION_MESSAGE)

        copy_action = deepcopy(action)
        copy_action.base_free_gaiaforming += self.FREE_GAIAFORM_BONUS
        return copy_action


class GainRangeAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    NAVIGATION_BONUS = 3
    ILLEGAL_ACTION_MESSAGE = "GainRangeAction must be followed by a final action that requires navigation"

    def validate_next_action(self, action: NavigationModifiable) -> Tuple[bool, str]:
        if not (isinstance(action, NavigationModifiable) and isinstance(action, FinalAction)):
            return False, self.ILLEGAL_ACTION_MESSAGE
        return True, self.valid_str

    def modify_final_action(self, action: NavigationModifiable) -> NavigationModifiable:
        if not isinstance(action, NavigationModifiable):
            raise IllegalFinalActionException(self.ILLEGAL_ACTION_MESSAGE)

        copy_action = deepcopy(action)
        copy_action.base_navigation += self.NAVIGATION_BONUS
        return copy_action


class PlaceMineAction(FinalAction, NavigationModifiable, GaiaformingRequirementsModifiable, HasHexagonLocation):
    def __init__(self, hexagon: Hexagon):
        NavigationModifiable.__init__(self)
        GaiaformingRequirementsModifiable.__init__(self)
        HasHexagonLocation.__init__(self, hexagon)

    @property
    def cost(self):
        return Cost(ore=1, credits=2)

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        game_map = gamestate.game_map

        planet = game_map.get_planet(self.hexagon)
        if planet is None:
            return False, "There is not planet on the specified hexagon"

        if isinstance(planet, InhabitedPlanet):
            return False, "This planet is already occupied"

        if not self._planet_is_in_range(gamestate, game_map, player):
            return False, "The planet is not in range"

        if planet.planet_type == PlanetType.TRANSDIM:
            return False, "Cannot build on transdim planets"
        elif planet.planet_type == PlanetType.GAIA:
            total_cost = self.cost + Cost(qic=1)
        else:
            num_gaiaforms_required = max(player.get_distance_from_planet_color(planet) - self.base_free_gaiaforming, 0)
            total_cost = Cost(ore=num_gaiaforms_required * gamestate.research_board.get_player_gaiaforming_cost(player))

        if not player.can_afford(total_cost):
            return False, "The player cannot afford to place a mine"

        return True, "The player can place a mine at {}".format(str(planet.hex))

    def _planet_is_in_range(self, gamestate, game_map, player) -> bool:
        navigation_range = self.base_navigation + gamestate.research_board.get_player_navigation_ability(player)
        planets_in_range = game_map.get_planets_in_range(self.hexagon, navigation_range, only_inhabited=True)

        return any(planet.faction == player.faction for planet in planets_in_range)

    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        if not gamestate.game_map.inhabit_planet(self.hexagon, player.faction, Building.MINE):
            return False, "Could not inhabit planet at {}".format(str(self.hexagon))
        return True, self.valid_str


class StartGaiaProjectAction(FinalAction, NavigationModifiable, HasHexagonLocation):
    def __init__(self, hexagon: Hexagon):
        NavigationModifiable.__init__(self)
        HasHexagonLocation.__init__(self, hexagon)

    def validate(self, gamestate, player_id: str):
        pass

    def perform_action(self, gamestate, player_id: str):
        pass


class PassAction(FinalAction):
    def validate(self, gamestate, player: Player) -> Tuple[bool, str]:
        return True, "It is always valid to pass at the end of the turn"

    def perform_action(self, gamestate, player_id: str):
        pass
