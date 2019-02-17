from __future__ import annotations
from typing import List
import json
from dataclasses import dataclass

from gaia.board.hexagons import Hexagon
from gaia.board.sectors import Sector
from gaia.board.federations import Federation
from gaia.utils.utils import CustomJSONSerialization


@dataclass(frozen=True)
class Map(object):
    sectors: List[Sector]
    federations: List[Federation]

    def to_json(self):
        class MapEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                elif isinstance(obj, CustomJSONSerialization):
                    return obj.to_json()
                else:
                    return obj.__dict__

        return json.dumps(self, cls=MapEncoder)

    def add_federation(self, federation: Federation):
        self.federations.append(federation)

    def get_hexagon(self, hexagon: Hexagon) -> Hexagon:
        for sector in self.sectors:
            sector_hexagon = sector.get_hexagon(hexagon)
            if sector_hexagon is not None:
                return sector_hexagon

    # TODO: Reimpliment
    # def inhabit_planet(self, hexagon: Hexagon, faction: Factions, building: BuildingType) -> bool:
        # for sector in self.sectors:
        #     planet = sector.get_planet(hexagon)
        #     if planet is not None:
        #         sector.replace_planet(planet, planet.inhabit(faction, building))
        #         return True
        # return False

    # TODO: Reimplement
    # def get_planets_in_range(self, hexagon: Hexagon, distance: int, only_inhabited: bool = False) \
    #         -> Set[Union[Planet, InhabitedPlanet]]:
    #     hexagons_in_range = hexagon.get_hexagons_in_range(distance)
    #     planets_in_range = set()
    #
    #     for hexagon in hexagons_in_range:
    #         planet = self.get_planet(hexagon)
    #         if planet is not None and (not only_inhabited or planet.is_inhabited()):
    #             planets_in_range.add(planet)
    #
    #     return planets_in_range

    # TODO: implement
    # def calculate_hexagons_of_smallest_federation(self, planets: List[Planet]) -> List[Hexagon]:

    # TODO: Reimplement
    # def add_buildings_to_all_planets(self):
    #     for sector in self.sectors:
    #         for hexagon in sector.planets.keys():
    #             self.inhabit_planet(hexagon, random.choice(list(Factions)), random.choice(list(BuildingType)))
