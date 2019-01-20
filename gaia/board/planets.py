from __future__ import annotations
from dataclasses import dataclass

from gaia.utils.enums import PlanetType, Factions, Building
from gaia.utils.utils import create_object_property_generator
from gaia.board.hexagons import Hexagon

@dataclass(frozen=True)
class Planet(object):
    hex: Hexagon
    planet_type: PlanetType

    @property
    def planet_color(self):
        return planet_type_to_color(self.planet_type)

    def move_hex(self, new_hex: Hexagon) -> Planet:
        attrs = self.__dict__
        attrs['hex'] = new_hex
        return type(self)(**attrs)

    def rotate(self, degrees: int) -> Planet:
        return self.move_hex(self.hex.rotate(degrees))

    def is_inhabited(self) -> bool:
        return False

    def inhabit(self, faction: Factions, building: Building) -> InhabitedPlanet:
        return InhabitedPlanet(self.hex,
                               self.planet_type,
                               faction,
                               building)

    def __iter__(self):
        return create_object_property_generator(self, {
            "planet_type": self.planet_type
        })

# Todo: Deprecate
@dataclass(frozen=True)
class InhabitedPlanet(Planet):
    faction: Factions
    building: Building

    def is_inhabited(self) -> bool:
        return True

    def __iter__(self):
        return create_object_property_generator(self, {
            "planet_type": self.planet_type,
            "faction": self.faction,
            "building": self.building
        })
