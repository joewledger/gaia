from gaia.players.players import BasePlayer
from gaia.utils.enums import FactionType, PlanetType, BuildingType
from gaia.players.players import PlayerResources, Income, Cost


from typing import Dict, List


class Terrans(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.TERRANS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.BLUE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Lantids(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.LANTIDS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.BLUE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Xenos(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.XENOS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.YELLOW

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Gleens(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.GLEENS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.YELLOW

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Taklons(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.TAKLONS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.BROWN

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Ambas(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.AMBAS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.BROWN

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class HadschHallas(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.HADSCH_HALLAS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.RED

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Ivits(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.IVITS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.RED

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Geodens(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.GEODENS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.ORANGE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Baltaks(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.BALTAKS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.ORANGE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Firaks(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.FIRAKS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.GREY

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Bescods(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.BESCODS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.GREY

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Nevlas(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.NEVLAS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.WHITE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class Itars(BasePlayer):
    @property
    def faction(self) -> FactionType:
        return FactionType.ITARS

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.WHITE

    def get_starting_resources(self) -> PlayerResources:
        pass

    def get_starting_board_income(self) -> Income:
        pass

    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def get_building_costs(self) -> Dict[BuildingType, Cost]:
        pass

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        pass


class PlayerFactory:
    faction_mapping = {
        FactionType.TERRANS: Terrans,
        FactionType.LANTIDS: Lantids,
        FactionType.XENOS: Xenos,
        FactionType.GLEENS: Gleens,
        FactionType.TAKLONS: Taklons,
        FactionType.AMBAS: Ambas,
        FactionType.HADSCH_HALLAS: HadschHallas,
        FactionType.IVITS: Ivits,
        FactionType.GEODENS: Geodens,
        FactionType.BALTAKS: Baltaks,
        FactionType.FIRAKS: Firaks,
        FactionType.BESCODS: Bescods,
        FactionType.NEVLAS: Nevlas,
        FactionType.ITARS: Itars
    }

    @classmethod
    def get_player(cls, faction: FactionType) -> BasePlayer:
        return cls.faction_mapping[faction]()
