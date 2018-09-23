import pytest

from gaia.map import Hexagon, Planet, InhabitedPlanet
from gaia.players import Factions
from gaia.buildings import Buildings


@pytest.fixture()
def planets():
    return [
        Planet(Hexagon(0, 0), Planet.Type.BLUE),
        Planet(Hexagon(0, 5), Planet.Type.RED),
        InhabitedPlanet(Hexagon(0, 4), Planet.Type.ORANGE, Factions.AMBAS, Buildings.MINE)
    ]
