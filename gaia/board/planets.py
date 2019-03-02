from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from gaia.utils.enums import PlanetType
from gaia.board.buildings import Building


@dataclass()
class Planet(object):
    planet_type: PlanetType
    building: Union[Building, None] = None

    terraforming_cycle = {
        PlanetType.BLUE: 0,
        PlanetType.WHITE: 1,
        PlanetType.GREY: 2,
        PlanetType.BROWN: 3,
        PlanetType.YELLOW: 4,
        PlanetType.ORANGE: 5,
        PlanetType.RED: 6
    }

    def is_inhabited(self) -> bool:
        return self.building is not None

    def get_inhabited_copy(self, building: Building) -> Planet:
        return Planet(self.planet_type, building)

    @classmethod
    def get_terraforming_distance(cls, home_planet: PlanetType, target_planet: PlanetType) -> int:
        target_planet_index = cls.terraforming_cycle[target_planet]
        native_planet_index = cls.terraforming_cycle[home_planet]
        cycle_length = len(cls.terraforming_cycle)
        return min(
            abs(native_planet_index - target_planet_index),
            abs(
                (cycle_length + min(target_planet_index, native_planet_index)) -
                max(target_planet_index, native_planet_index)
            )
        )
