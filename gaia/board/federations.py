from dataclasses import dataclass
from typing import List

from gaia.utils.enums import Factions
from gaia.board.hexagons import Hexagon

@dataclass(frozen=True)
class Federation:
    hexagons: List[Hexagon]
    faction: Factions
    activated: bool = False
