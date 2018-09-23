from dataclasses import dataclass
from enum import Enum
from typing import List

from gaia.players import Factions
from gaia.buildings import Buildings


class Planets(Enum):
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


@dataclass(frozen=True)
class Hexagon(object):
    x: int
    z: int

    @property
    def y(self):
        return -self.x - self.z

    def distance_from_coordinates(self, x, z):
        return (abs(self.x - x) + abs(self.y - (-x - z)) + abs(self.z - z)) / 2

    def distance(self, other):
        return self.distance_from_coordinates(other.x, other.z)

    def __str__(self):
        return "({0.x},{0.z})".format(self)


@dataclass(frozen=True)
class Planet(object):
    hex: Hexagon
    planet_type: Planets

    def is_inhabited(self):
        return False


@dataclass(frozen=True)
class InhabitedPlanet(Planet):
    faction: Factions
    buildings: Buildings

    def is_inhabited(self):
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

    def get_planet(self, x, z):
        h = Hexagon(x, z)
        return self.planets[h] if h in self.planets else None

    def rotate(self, degrees: int):
        assert degrees in range(0, 361) and degrees % 60 == 0
        pass


class Map:
    def __init__(self, sectors):
        self.sectors = sectors
