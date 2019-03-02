from __future__ import annotations
from typing import List, Set
from dataclasses import dataclass
import json
import random

from gaia.board.hexagons import Hexagon
from gaia.board.sectors import Sector
from gaia.board.federations import Federation
from gaia.board.buildings import Building
from gaia.utils.utils import CustomJSONSerialization
from gaia.utils.enums import FactionType, BuildingType


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

    def get_hexagons_in_range(self, hexagon: Hexagon, distance: int, only_inhabited: bool = False) \
            -> Set[Hexagon]:
        hexagons_in_range = hexagon.get_hexagons_in_range(distance)
        map_hexagons_in_range = set()

        for hexagon in hexagons_in_range:
            map_hexagon = self.get_hexagon(hexagon)
            if only_inhabited:
                if map_hexagon is not None and map_hexagon.planet is not None and map_hexagon.planet.is_inhabited():
                    map_hexagons_in_range.add(map_hexagon)
            else:
                map_hexagons_in_range.add(map_hexagon)

        return map_hexagons_in_range

    def inhabit_planet(self, hexagon: Hexagon, building: Building) -> bool:
        for sector in self.sectors:
            map_hexagon = sector.get_hexagon(hexagon)
            if map_hexagon is not None and map_hexagon.planet is not None:
                map_hexagon.planet.building = building
                return True
        return False

    def add_buildings_to_all_planets(self):
        for sector in self.sectors:
            for hexagon in sector.hexagons:
                self.inhabit_planet(hexagon, Building(random.choice(list(FactionType)), random.choice(list(BuildingType))))
