import pytest
import os

from gaia.map import Hexagon, Planet, InhabitedPlanet, Map
from gaia.players import Factions
from gaia.buildings import Buildings


@pytest.fixture()
def planets():
    return [
        Planet(Hexagon(0, 0), Planet.Type.BLUE),
        Planet(Hexagon(0, 2), Planet.Type.RED),
        InhabitedPlanet(Hexagon(-1, 1), Planet.Type.ORANGE, Factions.AMBAS, Buildings.MINE)
    ]


@pytest.fixture()
def config_path():
    return os.path.dirname(os.path.realpath(__file__)) + "\\..\\configs\\board.json"


@pytest.fixture()
def default_map(config_path):
    return Map.load_from_config(config_path=config_path,
                                game_type="2p_default")