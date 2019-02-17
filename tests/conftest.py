import pytest
import os

from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet, InhabitedPlanet
from gaia.board.map import Map
from gaia.board.sectors import Sector

from gaia.gamestate.players import Player, PlayerResources
from gaia.utils.enums import PlanetType, Factions, BuildingType
from gaia.gamestate.gamestate import GameState, ResearchBoard, ScoringBoard, AvailableRoundBonuses

from tests.util import TestFaction


@pytest.fixture()
def planets():
    return [
        Planet(Hexagon(0, 0), PlanetType.BLUE),
        Planet(Hexagon(0, 2), PlanetType.RED),
        InhabitedPlanet(Hexagon(-1, 1), PlanetType.ORANGE, Factions.AMBAS, BuildingType.MINE)
    ]


@pytest.fixture()
def config_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "configs", "board.json")


@pytest.fixture()
def default_map(config_path):
    return Map.load_from_config(config_path=config_path,
                                game_type="1p_2p_default")


@pytest.fixture()
def default_players():
    return {
        "p1": Player(Factions.AMBAS),
        "p2": Player(Factions.BALTAKS)
    }


@pytest.fixture()
def test_player():
    return Player(TestFaction.TEST)


@pytest.fixture()
def default_player_resources():
    return PlayerResources(ore=4, credits=15, knowledge=3, qic=1, power_bowls={0: 4, 1: 4, 2: 0})


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
    starting_gamestate.game_map.inhabit_planet(Hexagon(0, 1), player_1.faction, BuildingType.MINE)

    return starting_gamestate


@pytest.fixture()
def one_sector_map(planets):
    sector = Sector(planets, radius=10)
    return Map([sector])


@pytest.fixture()
def one_sector_gamestate(test_player, one_sector_map, starting_gamestate):
    starting_gamestate.game_map = one_sector_map
    starting_gamestate.players = {}
    starting_gamestate.add_player(test_player)
    return starting_gamestate
