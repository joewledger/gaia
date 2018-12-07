import pytest
import os

from gaia.map import Hexagon, Planet, InhabitedPlanet, Map
from gaia.players import Factions, PlayerResources
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
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "configs", "board.json")


@pytest.fixture()
def default_map(config_path):
    return Map.load_from_config(config_path=config_path,
                                game_type="1p_2p_default")


@pytest.fixture()
def default_player_resources():
    return PlayerResources(ore=4, credits=15, knowledge=3, qic=1, power={0: 4, 1: 4, 2: 0})
