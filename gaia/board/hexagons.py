from __future__ import annotations
from dataclasses import dataclass
from typing import Set
from math import sqrt

from gaia.utils.utils import create_object_property_generator


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
                if self.distance_from_coordinates(x, z) <= distance:
                    hexagons_in_range.add(Hexagon(x, z))

        return hexagons_in_range

    def __str__(self) -> str:
        return "({0.x},{0.z})".format(self)

    def __iter__(self):
        return create_object_property_generator(self, {
            "screen_x_factor": self.screen_x_factor,
            "screen_y_factor": self.screen_y_factor
        })
