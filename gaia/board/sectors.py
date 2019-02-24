from __future__ import annotations
from typing import Set
import random

from gaia.utils.utils import CustomJSONSerialization, obj_to_json
from gaia.board.hexagons import Hexagon


class Sector(CustomJSONSerialization):
    def __init__(self, planet_hexagons: Set[Hexagon], radius: int=2, x_offset: int=0, z_offset: int=0):
        assert radius >= 0, "Radius must be greater or equal to zero"

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
        sector_hexagons = central_hexagon.get_hexagons_in_range(self.radius) - planet_hexagons

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

    def get_hexagon(self, hexagon: Hexagon) -> Hexagon:
        sector_hexagon = [h for h in self.hexagons if h == hexagon]
        return sector_hexagon[0] if len(sector_hexagon) == 1 else None
