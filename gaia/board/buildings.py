from __future__ import annotations
from dataclasses import dataclass

from gaia.utils.enums import Factions, BuildingType
from gaia.utils.utils import CustomJSONSerialization, obj_to_json


@dataclass(frozen=True)
class Building(CustomJSONSerialization):
    faction: Factions
    type: BuildingType

    def to_json(self):
        return obj_to_json(self, {
            "faction": self.faction,
            "building_type": self.type
        })
