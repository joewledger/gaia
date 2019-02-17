from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from math import sqrt

from gaia.board.planets import Planet
from gaia.utils.utils import CustomJSONSerialization, obj_to_json


@dataclass(frozen=True)
class Hexagon(CustomJSONSerialization):
    x: int
    z: int
    planet: Union[Planet, None] = None

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

    def to_json(self):
        return obj_to_json(self, {
            "screen_x_factor": self.screen_x_factor,
            "screen_y_factor": self.screen_y_factor
        })

    def __str__(self) -> str:
        return "({0.x},{0.z})".format(self)

    def __eq__(self, other):
        return self.x == other.x and self.z == other.z

    def __hash__(self):
        return (str(self.x) + ',' + str(self.z)).__hash__()
