from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
import random
import json

from gaia.players import Factions
from gaia.buildings import Buildings


@dataclass(frozen=True)
class Hexagon(object):
    x: int
    z: int

    @property
    def y(self) -> int:
        return -self.x - self.z

    def distance_from_coordinates(self, x: int, z: int) -> int:
        return (abs(self.x - x) + abs(self.y - (-x - z)) + abs(self.z - z)) // 2

    def distance(self, other: Hexagon) -> int:
        return self.distance_from_coordinates(other.x, other.z)

    def rotate(self, degrees: int) -> Hexagon:
        assert degrees % 60 == 0
        x, y, z = self.x, self.y, self.z
        num_turns = degrees // 60
        for i in range(num_turns):
            x, y, z = -z, -x, -y
        return Hexagon(x, z)

    def adjust_offset(self, x_offset_diff: int, z_offset_diff: int) -> Hexagon:
        return Hexagon(self.x + x_offset_diff, self.z + z_offset_diff)

    def __str__(self) -> str:
        return "({0.x},{0.z})".format(self)


@dataclass(frozen=True)
class Planet(object):
    class Type(Enum):
        RED = 1
        ORANGE = 2
        WHITE = 3
        GREY = 4
        YELLOW = 5
        BROWN = 6
        BLUE = 7
        GAIA = 8
        TRANSDIM = 9
        LOST = 10

    hex: Hexagon
    planet_type: Type

    def move_hex(self, new_hex: Hexagon) -> Planet:
        attrs = self.__dict__
        attrs['hex'] = new_hex
        return type(self)(**attrs)

    def rotate(self, degrees: int) -> Planet:
        return self.move_hex(self.hex.rotate(degrees))

    def is_inhabited(self) -> bool:
        return False


@dataclass(frozen=True)
class InhabitedPlanet(Planet):
    faction: Factions
    buildings: Buildings

    def is_inhabited(self) -> bool:
        return True


class Sector(object):
    def __init__(self, planets: List[Planet], radius: int=3, x_offset: int=0, z_offset: int=0):
        assert radius >= 1, "Radius must be greater or equal to zero"
        assert isinstance(planets, list), "Planets must be a list"

        self.radius = radius
        self.x_offset = x_offset
        self.z_offset = z_offset

        self.hexagons = set()
        self.planets = {p.hex: p for p in planets}

        center = Hexagon(self.x_offset, self.z_offset)
        for x in range(self.x_offset - self.radius, self.x_offset + self.radius + 1):
            for z in range(self.z_offset - self.radius, self.z_offset + self.radius + 1):
                if center.distance_from_coordinates(x, z) < self.radius:
                    self.hexagons.add(Hexagon(x, z))

    def get_planet(self, x: int, z: int) -> Planet:
        h = Hexagon(x, z)
        return self.planets[h] if h in self.planets else None

    def rotate(self, degrees: int) -> None:
        self.planets = {hexagon.rotate(degrees): planet.rotate(degrees)
                        for hexagon, planet in self.planets.items()}

    def random_rotate(self) -> None:
        self.rotate(random.randint(0, 6) * 60)

    def adjust_offset(self, x_offset: int, z_offset: int) -> None:
        x_offset_diff = x_offset - self.x_offset
        z_offset_diff = z_offset - self.z_offset

        self.x_offset, self.z_offset = x_offset, z_offset
        new_hexagons = set()
        new_planets = dict()
        for old_hex in self.hexagons:
            new_hex = old_hex.adjust_offset(x_offset_diff, z_offset_diff)
            new_hexagons.add(new_hex)
            if old_hex in self.planets:
                new_planets[new_hex] = self.planets[old_hex].move_hex(new_hex)

        self.hexagons = new_hexagons
        self.planets = new_planets


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
                planets = [Planet(Hexagon(p["x"], p["z"]), planet_type=Planet.Type[p["type"]]) for p in side]
                game_tile.sides.append(Sector(planets, radius))

        return tile_mapping


class Map:
    def __init__(self, sectors: List[Sector]):
        self.sectors = sectors
        self.federations = []

    @classmethod
    def load_from_config(cls, config_path: str, game_type: str = None):
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

    def add_federation(self, federation):
        self.federations.append(federation)
