from dataclasses import dataclass


@dataclass(frozen=True)
class Hexagon:
    x: int
    y: int
    z: int


class HexagonGrid:

    def __init__(self, radius):
        self.radius = radius
        self.hexagons = set()
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                for z in range(-radius, radius+1):
                    if x + y + z == 0:
                        self.hexagons.add(Hexagon(x, y, z))
