from dataclasses import dataclass
from enum import Enum
from typing import Set


class Planets(Enum):
    SPACE = 0
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
    planet_type: Planets = Planets.SPACE

    @property
    def y(self):
        return -self.x - self.y

    def distance_from_coordinates(self, x, z):
        return (abs(self.x - x) + abs(self.y - (-x - z)) + abs(self.z - z)) / 2

    def distance(self, other):
        return self.distance_from_coordinates(other.x, other.z)

    def __hash__(self):
        return hash((self.x, self.z))

    def __eq__(self, other):
        return (self.x, self.z) == (other.x, other.z)

    def __str__(self):
        return "({0.x},{0.z})".format(self)


class Sector(object):
    def __init__(self, radius: int=3, x_offset: int=0, z_offset: int=0, hexagon_overrides: Set[Hexagon]=None):
        assert radius > 0 and (hexagon_overrides is None or isinstance(hexagon_overrides, list))

        self.radius = radius
        self.x_offset = x_offset
        self.z_offset = z_offset

        self.hexagons = set()
        center = Hexagon(self.x_offset, self.z_offset)
        for x in range(self.x_offset - self.radius, self.x_offset + self.radius + 1):
            for z in range(self.z_offset - self.radius, self.z_offset + self.radius + 1):
                local_hexagon = Hexagon(x, z)
                if local_hexagon in hexagon_overrides:
                    self.hexagons.add([h for h in hexagon_overrides if h == local_hexagon][0])
                elif center.distance_from_coordinates(x, z) < self.radius:
                    self.hexagons.add(local_hexagon)

    def rotate(self, degrees: int):
        assert degrees in range(0, 361) and degrees % 60 == 0
        pass


class Map:
    def __init__(self, sectors):
        self.sectors = sectors
