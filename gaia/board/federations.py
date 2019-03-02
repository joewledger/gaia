from dataclasses import dataclass
from typing import List

from gaia.utils.enums import FactionType
from gaia.board.hexagons import Hexagon


@dataclass(frozen=True)
class Federation:
    hexagons: List[Hexagon]
    faction: FactionType
    activated: bool = False
