from dataclasses import dataclass
from typing import List

from gaia.utils.enums import FactionTypes
from gaia.board.hexagons import Hexagon


@dataclass(frozen=True)
class Federation:
    hexagons: List[Hexagon]
    faction: FactionTypes
    activated: bool = False
