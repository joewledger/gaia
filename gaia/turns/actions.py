from __future__ import annotations
from typing import Tuple
from copy import deepcopy

from gaia.players.players import Player, Cost
from gaia.board.hexagons import Hexagon
from gaia.board.buildings import Building
from gaia.utils.enums import PlanetType, BuildingType

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
    Must be followed followed by an Action that requires navigation (i.e. implements NavigationModifiable)
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
    ILLEGAL_HEXAGON_MESSAGE = "The hexagon provided is not part of the map"
    MISSING_PLANET_MESSAGE = "There is no planet on the specified hexagon"
    OCCUPIED_PLANET_MESSAGE = "This planet is already occupied"
    PLANET_OUT_OF_RANGE_MESSAGE = "The planet is not in range"
    TRANSDIM_PLANET_MESSAGE = "Cannot build on transdim planets"
    EXPENSIVE_MINE_MESSAGE = "The player cannot afford to place a mine"
    MINE_FAILURE_MESSAGE = "Unable to inhabit planet"

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

        map_hexagon = game_map.get_hexagon(self.hexagon)

        if map_hexagon is None:
            return False, self.ILLEGAL_HEXAGON_MESSAGE

        planet = map_hexagon.planet
        if planet is None:
            return False, self.MISSING_PLANET_MESSAGE

        if planet.building is not None:
            return False, self.OCCUPIED_PLANET_MESSAGE

        if not self._planet_is_in_range(gamestate, game_map, player):
            return False, self.PLANET_OUT_OF_RANGE_MESSAGE

        if planet.planet_type == PlanetType.TRANSDIM:
            return False, self.TRANSDIM_PLANET_MESSAGE
        elif planet.planet_type == PlanetType.GAIA:
            total_cost = self.cost + Cost(qic=1)
        else:
            num_gaiaforms_required = max(player.get_distance_from_planet_color(planet) - self.base_free_gaiaforming, 0)
            total_cost = Cost(ore=num_gaiaforms_required * gamestate.research_board.get_player_gaiaforming_cost(player))

        if not player.can_afford(total_cost):
            return False, self.EXPENSIVE_MINE_MESSAGE

        return True, "The player can place a mine at {}".format(str(self.hexagon))

    def _planet_is_in_range(self, gamestate, game_map, player) -> bool:
        navigation_range = self.base_navigation + gamestate.research_board.get_player_navigation_ability(player)
        hexagons_in_range = game_map.get_hexagons_in_range(self.hexagon, navigation_range, only_inhabited=True)

        return any(hexagon.planet.building.faction == player.faction for hexagon in hexagons_in_range)

    def perform_action(self, gamestate, player_id: str):
        player = gamestate.players[player_id]

        if not gamestate.game_map.inhabit_planet(self.hexagon, Building(player.faction, BuildingType.MINE)):
            raise RuntimeError(self.MINE_FAILURE_MESSAGE)


class UpgradeBuildingAction(FinalAction, HasHexagonLocation):
    def __init__(self, hexagon: Hexagon, target_building: BuildingType):
        self.target_building = target_building
        HasHexagonLocation.__init__(self, hexagon)

    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        player = gamestate.players[player_id]
        game_map = gamestate.game_map

        map_hexagon = game_map.get_hexagon(self.hexagon)
        if map_hexagon is None:
            return False, self.ILLEGAL_HEXAGON_MESSAGE

        planet = map_hexagon.planet
        if planet is None:
            return False, self.MISSING_PLANET_MESSAGE

        building = planet.building
        if building is None:
            return False, self.MISSING_BUILDING_MESSAGE

        if building.faction != player.faction:
            return False, self.INVALID_FACTION_MESSAGE

        pass

    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


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
