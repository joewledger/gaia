import pytest
import os

from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet
from gaia.board.map import Map
from gaia.board.sectors import Sector
from gaia.board.buildings import Building
from gaia.board.map_loader import MapLoader

from gaia.players.players import BasePlayer, PlayerResources
from gaia.players.player_types import PlayerFactory
from gaia.utils.enums import PlanetType, FactionType, BuildingType
from gaia.gamestate.gamestate import GameState, ResearchBoard, ScoringBoard, AvailableRoundBonuses

from tests.util import TestFaction


@pytest.fixture()
def planet_hexagons():
    return {
        Hexagon(0, 0, planet=Planet(PlanetType.BLUE)),
        Hexagon(0, 2, planet=Planet(PlanetType.RED)),
        Hexagon(-1, 1, planet=Planet(
            PlanetType.ORANGE,
            building=Building(FactionType.AMBAS, BuildingType.MINE)
        ))
    }


@pytest.fixture()
def config_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "configs", "board.json")


@pytest.fixture()
def default_map(config_path):
    return MapLoader.load_from_config(config_path=config_path,
                                      game_type="1p_2p_default")


@pytest.fixture()
def default_player_resources():
    return PlayerResources(ore=4, credits=15, knowledge=3, qic=1, power_bowls={0: 4, 1: 4, 2: 0})


class TestPlayer(BasePlayer):
    def __init__(self, faction: TestFaction):
        super().__init__()
        self._faction = faction

    @property
    def faction(self) -> TestFaction:
        return self._faction

    @property
    def native_planet(self) -> PlanetType:
        return PlanetType.WHITE

    def get_starting_resources(self):
        return default_player_resources()

    def get_starting_board_income(self):
        pass

    def get_building_costs(self):
        pass

    def get_legal_building_upgrades(self):
        pass


@pytest.fixture()
def test_player():
    return TestPlayer(TestFaction.TEST)


@pytest.fixture()
def default_players(test_player):
    return {
        "p1": TestPlayer(TestFaction.TEST),
        "p2": TestPlayer(TestFaction.TEST2)
    }


@pytest.fixture()
def starting_gamestate(default_players, default_map):
    return GameState(
        default_players,
        default_map,
        ResearchBoard(),
        ScoringBoard(),
        AvailableRoundBonuses(5)
    )


@pytest.fixture()
def test_range_gamestate(starting_gamestate):
    player_1 = starting_gamestate.players["p1"]
    starting_gamestate.game_map.inhabit_planet(Hexagon(0, 1), Building(player_1.faction, BuildingType.MINE))

    return starting_gamestate


@pytest.fixture()
def one_sector_map(planet_hexagons):
    sector = Sector(planet_hexagons, radius=10)
    return Map([sector], [])


@pytest.fixture()
def one_sector_gamestate(test_player, one_sector_map, starting_gamestate):
    starting_gamestate.game_map = one_sector_map
    starting_gamestate.players = {}
    starting_gamestate.add_player(test_player)
    return starting_gamestate
