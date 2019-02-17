from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from gaia.utils.enums import PlanetType
from gaia.board.buildings import Building


@dataclass(frozen=True)
class Planet(object):
    planet_type: PlanetType
    building: Union[Building, None] = None

    def is_inhabited(self) -> bool:
        return self.building is not None

    def get_inhabited_copy(self, building: Building) -> Planet:
        return Planet(self.planet_type, building)
