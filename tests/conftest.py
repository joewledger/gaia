import pytest
import os

from gaia.map import Hexagon, Planet, InhabitedPlanet, Map
from gaia.players import Factions, Player, PlayerResources
from gaia.buildings import Building
from gaia.planet_types import PlanetType
from gaia.gamestate import GameState, ResearchBoard, ScoringBoard, AvailableRoundBonuses


@pytest.fixture()
def planets():
    return [
        Planet(Hexagon(0, 0), PlanetType.BLUE),
        Planet(Hexagon(0, 2), PlanetType.RED),
        InhabitedPlanet(Hexagon(-1, 1), PlanetType.ORANGE, Factions.AMBAS, Building.MINE)
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


@pytest.fixture()
def starting_gamestate(default_map):
    return GameState(
        {
            "p1": Player(Factions.AMBAS),
            "p2": Player(Factions.BALTAKS)
        },
        default_map,
        ResearchBoard(),
        ScoringBoard(),
        AvailableRoundBonuses(5)
    )


@pytest.fixture()
def patch_check_all_actions(mocker):
    def patch_turn(turn):
        mocker.patch.object(turn, '_check_all_actions_are_valid')
        turn._check_all_actions_are_valid.return_value = (True, [])
        return turn

    return patch_turn
