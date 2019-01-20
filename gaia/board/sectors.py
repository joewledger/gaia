from __future__ import annotations
from typing import List
import random
from gaia.utils.utils import create_object_property_generator

from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet


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
        self.hexagons = center.get_hexagons_in_range(self.radius - 1)

    def __iter__(self):
        return create_object_property_generator(self, {
            "screen_x_factor": Hexagon(self.x_offset, self.z_offset).screen_x_factor,
            "screen_y_factor": Hexagon(self.x_offset, self.z_offset).screen_y_factor,
            "planets": list(self.planets.values())
        })

    def get_planet(self, hexagon: Hexagon) -> Planet:
        return self.planets[hexagon] if hexagon in self.planets else None

    def replace_planet(self, old_planet: Planet, new_planet: Planet):
        self.planets[old_planet.hex] = new_planet

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