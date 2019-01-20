from __future__ import annotations
from dataclasses import dataclass

from gaia.utils.enums import Factions, BuildingType
from gaia.utils.utils import create_object_property_generator

@dataclass(frozen=True)
class Building(object):
    faction: Factions
    type: BuildingType

    def __iter__(self):
        return create_object_property_generator(self, {
            "faction": self.faction,
            "building_type": self.type
        })
