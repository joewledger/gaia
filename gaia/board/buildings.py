from __future__ import annotations
from dataclasses import dataclass

from gaia.utils.enums import FactionTypes, BuildingType
from gaia.utils.utils import CustomJSONSerialization, obj_to_json


@dataclass(frozen=True)
class Building(CustomJSONSerialization):
    faction: FactionTypes
    building_type: BuildingType

    def to_json(self):
        return obj_to_json(self, {
            "faction": self.faction,
            "building_type": self.building_type
        })
