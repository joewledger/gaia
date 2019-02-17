from __future__ import annotations
from typing import Set
import random

from gaia.utils.utils import CustomJSONSerialization, obj_to_json
from gaia.board.hexagons import Hexagon


class Sector(CustomJSONSerialization):
    def __init__(self, planet_hexagons: Set[Hexagon], radius: int=3, x_offset: int=0, z_offset: int=0):
        assert radius >= 1, "Radius must be greater or equal to zero"

        self.radius = radius
        self.x_offset = x_offset
        self.z_offset = z_offset

        planet_hexagons = {
            Hexagon(x=planet_hex.x + self.x_offset,
                    z=planet_hex.z + self.z_offset,
                    planet=planet_hex.planet)
            for planet_hex in planet_hexagons
        }

        center = Hexagon(self.x_offset, self.z_offset)
        self.hexagons = self.create_sector_hexagons(center, planet_hexagons)

    def create_sector_hexagons(self, central_hexagon: Hexagon, planet_hexagons: Set[Hexagon]) -> Set[Hexagon]:
        radius = self.radius
        sector_hexagons = set()

        for x in range(self.x_offset - radius, self.x_offset + radius + 1):
            for z in range(self.z_offset - radius, self.z_offset + radius + 1):
                if central_hexagon.distance_from_coordinates(x, z) < radius and Hexagon(x, z) not in planet_hexagons:
                    sector_hexagons.add(Hexagon(x, z))

        sector_hexagons.update(planet_hexagons)
        return sector_hexagons

    def rotate(self, degrees: int) -> None:
        self.hexagons = {hexagon.rotate(degrees) for hexagon in self.hexagons}

    def random_rotate(self) -> None:
        self.rotate(random.randint(0, 6) * 60)

    def adjust_offset(self, x_offset: int, z_offset: int) -> None:
        x_offset_diff = x_offset - self.x_offset
        z_offset_diff = z_offset - self.z_offset

        self.x_offset, self.z_offset = x_offset, z_offset
        new_hexagons = set()
        for old_hex in self.hexagons:
            new_hex = old_hex.adjust_offset(x_offset_diff, z_offset_diff)
            new_hexagons.add(new_hex)

        self.hexagons = new_hexagons

    def to_json(self):
        return obj_to_json(self, {
            "screen_x_factor": Hexagon(self.x_offset, self.z_offset).screen_x_factor,
            "screen_y_factor": Hexagon(self.x_offset, self.z_offset).screen_y_factor,
            "hexagons": list(self.hexagons)
        })
