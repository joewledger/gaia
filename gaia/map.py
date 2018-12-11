from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Dict, Set, Union
import random
import json
from copy import deepcopy
from math import sqrt

from gaia.players import Factions
from gaia.buildings import Building


@dataclass(frozen=True)
class Hexagon(object):
    x: int
    z: int

    @property
    def y(self) -> int:
        return -self.x - self.z

    @property
    def q(self) -> int:
        return self.z + self.x

    @property
    def r(self) -> int:
        return -self.x

    @property
    def screen_x_factor(self) -> float:
        return self.q * (3/2)

    @property
    def screen_y_factor(self) -> float:
        return (sqrt(3) / 2) * self.q + sqrt(3) * self.r

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

    def get_hexagons_in_range(self, distance: int) -> Set[Hexagon]:
        hexagons_in_range = set()

        for x in range(self.x - distance, self.x + distance + 1):
            for z in range(self.z - distance, self.z + distance + 1):
                if self.distance_from_coordinates(x, z) < distance:
                    hexagons_in_range.add(Hexagon(x, z))

        return hexagons_in_range

    def __str__(self) -> str:
        return "({0.x},{0.z})".format(self)


@dataclass(frozen=True)
class Planet(object):
    class Type(IntEnum):
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

    @property
    def hex_color(self):
        return {
            Planet.Type.RED: "#ff0000",
            Planet.Type.ORANGE: "#ff6600",
            Planet.Type.WHITE: "#ffffff",
            Planet.Type.GREY: "#b3b3b3",
            Planet.Type.YELLOW: "#ffff00",
            Planet.Type.BROWN: "#663300",
            Planet.Type.BLUE: "#0000ff",
            Planet.Type.GAIA: "#00ff00",
            Planet.Type.TRANSDIM: "#cc00cc",
            Planet.Type.LOST: "#cc6699"
        }[self.planet_type]

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
    buildings: Building

    def is_inhabited(self) -> bool:
        return True


class Sector(object):
    def __init__(self, planets: List[Planet], radius: int=3, x_offset: int=0, z_offset: int=0):
        assert radius >= 1, "Radius must be greater or equal to zero"
        assert isinstance(planets, list), "Planets must be a list"

        self.radius = radius
        self.x_offset = x_offset
        self.z_offset = z_offset

        planets = [p.move_hex(p.hex.adjust_offset(x_offset, z_offset)) for p in planets]
        self.planets = {p.hex: p for p in planets}

        center = Hexagon(self.x_offset, self.z_offset)
        self.hexagons = center.get_hexagons_in_range(self.radius)

    def __iter__(self):
        my_dict = deepcopy(self.__dict__)
        my_dict["planets"] = list(self.planets.values())
        for key, value in my_dict.items():
            yield key, value

    @property
    def screen_x_factor(self):
        return Hexagon(self.x_offset, self.z_offset).screen_x_factor

    @property
    def screen_y_factor(self):
        return Hexagon(self.x_offset, self.z_offset).screen_y_factor

    def get_planet(self, hexagon: Hexagon) -> Planet:
        return self.planets[hexagon] if hexagon in self.planets else None

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
                elif isinstance(obj, Sector):
                    return dict(obj)
                else:
                    return obj.__dict__

        return json.dumps(self, cls=MapEncoder)

    def add_federation(self, federation):
        self.federations.append(federation)

    def get_planet(self, hexagon: Hexagon):
        for sector in self.sectors:
            planet = sector.get_planet(hexagon)
            if planet is not None:
                return planet

        return None

    def get_planets_in_range(self, hexagon: Hexagon, distance: int, only_inhabited: bool = False) \
            -> Set[Union[Planet, InhabitedPlanet]]:
        hexagons_in_range = hexagon.get_hexagons_in_range(distance)
        planets_in_range = set()

        for hexagon in hexagons_in_range:
            planet = self.get_planet(hexagon)
            if planet is not None and (not only_inhabited or planet.is_inhabited()):
                planets_in_range.add(planet)

        return planets_in_range
