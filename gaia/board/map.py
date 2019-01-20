from __future__ import annotations
from typing import List, Dict, Set, Union
import random
import json

from gaia.utils.enums import PlanetType, Factions, Building

from gaia.board.sectors import Sector
from gaia.board.federations import Federation
from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet
from gaia.board.planets import InhabitedPlanet


class GameTile(object):
    """
    GameTiles are the physical pieces that form the map.
    They have either one or two sides (which are sectors)
    """
    def __init__(self):
        self.sides = []

    def __getitem__(self, idx):
        return self.sides[idx]

    @staticmethod
    def get_tile_mapping_from_config(config_path: str) -> Dict[int, GameTile]:
        with open(config_path) as config:
            config = json.load(config)

        tile_mapping = dict()

        for tile in config["tiles"]:
            game_tile = GameTile()
            tile_mapping[tile["number"]] = game_tile

            radius = tile["radius"]
            for side in tile["sides"]:
                planets = [Planet(Hexagon(p["x"], p["z"]), planet_type=PlanetType[p["type"]]) for p in side]
                game_tile.sides.append(Sector(planets, radius))

        return tile_mapping

class Map:
    def __init__(self, sectors: List[Sector]):
        self.sectors = sectors
        self.federations = []

    @classmethod
    def load_from_config(cls, config_path: str, game_type: str = None) -> Map:
        with open(config_path) as config:
            config = json.load(config)

        all_game_tiles = GameTile.get_tile_mapping_from_config(config_path)
        sectors = []

        if game_type:
            for tile_config in config[game_type]["tiles"]:
                tile = all_game_tiles[tile_config["number"]]
                sector = tile[tile_config["side"]]
                sector.adjust_offset(tile_config["x_offset"], tile_config["z_offset"])
                sectors.append(sector)
        else:
            # TODO implement random map generation
            raise NotImplementedError

        return Map(sectors)

    def to_json(self):
        class MapEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                elif hasattr(obj, "__iter__"):
                    return dict(obj)
                else:
                    return obj.__dict__

        return json.dumps(self, cls=MapEncoder)

    def add_federation(self, federation: Federation):
        self.federations.append(federation)

    def get_planet(self, hexagon: Hexagon) -> Union[Planet, None]:
        for sector in self.sectors:
            planet = sector.get_planet(hexagon)
            if planet is not None:
                return planet
        return None

    def inhabit_planet(self, hexagon: Hexagon, faction: Factions, building: Building) -> bool:
        for sector in self.sectors:
            planet = sector.get_planet(hexagon)
            if planet is not None:
                sector.replace_planet(planet, planet.inhabit(faction, building))
                return True
        return False

    def get_planets_in_range(self, hexagon: Hexagon, distance: int, only_inhabited: bool = False) \
            -> Set[Union[Planet, InhabitedPlanet]]:
        hexagons_in_range = hexagon.get_hexagons_in_range(distance)
        planets_in_range = set()

        for hexagon in hexagons_in_range:
            planet = self.get_planet(hexagon)
            if planet is not None and (not only_inhabited or planet.is_inhabited()):
                planets_in_range.add(planet)

        return planets_in_range

    def calculate_hexagons_of_smallest_federation(self, planets: List[Planet]) -> List[Hexagon]:
        # TODO: implement
        pass

    def add_buildings_to_all_planets(self):
        for sector in self.sectors:
            for hexagon in sector.planets.keys():
                self.inhabit_planet(hexagon, random.choice(list(Factions)), random.choice(list(Building)))
