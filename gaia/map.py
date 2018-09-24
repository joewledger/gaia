from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List
import random

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

    def rotate(self, degrees: int) -> Planet:
        attrs = self.__dict__
        attrs['hex'] = self.hex.rotate(degrees)
        return type(self)(**attrs)

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


class Map:
    def __init__(self, sectors):
        self.sectors = sectors
        self.federations = []

    def add_federation(self, federation):
        self.federations.append(federation)
