import pytest

from gaia.board.planets import Planet
from gaia.board.hexagons import Hexagon

from gaia.utils.enums import BuildingType, PlanetType
from gaia.turns.actions import PlaceMineAction
from gaia.gamestate.players import PlayerResources

from tests.util import TestBuilding


@pytest.mark.parametrize("planet_hexagons,action,should_be_valid,main_reason", [
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        True,
        None
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.TRANSDIM)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "Cannot build on transdim planets"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE))),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "This planet is already occupied"
    ),
    (
        [
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "There is not planet on the specified hexagon"
    )
])
def test_place_mine_destination_planet_validation(planet_hexagons, action,
                                                  should_be_valid, main_reason,
                                                  one_sector_gamestate, mocker):
    player = list(one_sector_gamestate.players.values())[0]

    mocker.patch.object(player, 'get_distance_from_planet_color')
    player.get_distance_from_planet_color.return_value = 0

    valid, reason = action.validate(one_sector_gamestate, player.player_id)
    assert valid == should_be_valid
    if main_reason:
        assert reason == main_reason


@pytest.mark.parametrize("planet_hexagons,action,base_navigation,research_navigation,should_be_valid,main_reason", [
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        0,
        1,
        True,
        None
    ),
    (
        [
            Hexagon(0, 2, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 2)),
        0,
        1,
        False,
        "The planet is not in range"
    ),
    (
        [
            Hexagon(0, 4, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 4)),
        2,
        1,
        False,
        "The planet is not in range"
    ),
    (
        [
            Hexagon(0, 4, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 4)),
        2,
        2,
        True,
        None
    )
])
def test_place_mine_range_validation(planet_hexagons, action, base_navigation, research_navigation,
                                     should_be_valid, main_reason,
                                     one_sector_gamestate, mocker):
    player = list(one_sector_gamestate.players.values())[0]

    mocker.patch.object(player, 'get_distance_from_planet_color')
    player.get_distance_from_planet_color.return_value = 0

    mocker.patch.object(one_sector_gamestate.research_board, 'get_player_navigation_ability')
    one_sector_gamestate.research_board.get_player_navigation_ability.return_value = research_navigation

    action.base_navigation = base_navigation

    valid, reason = action.validate(one_sector_gamestate, player.player_id)
    assert valid == should_be_valid
    if main_reason:
        assert reason == main_reason


@pytest.mark.parametrize(
    "planet_hexagons,action,player_resources,free_gaiaforming," +
    "terraforming_cost,planet_distance,should_be_valid,main_reason", [
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=2, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        0,
        True,
        "Legal because the player can afford the cost of one mine"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=1, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        0,
        True,
        "The player cannot afford to place a mine"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=2, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        1,
        False,
        "The player cannot afford to place a mine"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=4, credits=2, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        1,
        True,
        "Legal because the player has enough ore to afford one gaiaform"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=2, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        1,
        3,
        1,
        True,
        "Legal because a free gaiaform is enough to cover the cost"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.GAIA)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=2, knowledge=0, qic=0, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        1,
        False,
        "The player cannot afford to place a mine"
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.GAIA)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
        PlayerResources(ore=1, credits=2, knowledge=0, qic=1, power_bowls={0: 0, 1: 0, 2: 0}),
        0,
        3,
        1,
        True,
        "The player has a QIC, and can afford to place a mine on a gaia project"
    )
])
def test_place_mine_cost_validation(planet_hexagons, action, player_resources, free_gaiaforming, terraforming_cost, planet_distance,
                                    should_be_valid, main_reason,
                                    one_sector_gamestate, mocker):
    player = list(one_sector_gamestate.players.values())[0]
    player.player_resources = player_resources

    mocker.patch.object(one_sector_gamestate.research_board, 'get_player_gaiaforming_cost')
    one_sector_gamestate.research_board.get_player_gaiaforming_cost.return_value = terraforming_cost

    mocker.patch.object(player, 'get_distance_from_planet_color')
    player.get_distance_from_planet_color.return_value = planet_distance

    action.base_free_gaiaforming = free_gaiaforming

    valid, reason = action.validate(one_sector_gamestate, player.player_id)
    assert valid == should_be_valid
    if not valid:
        assert main_reason == reason


@pytest.mark.parametrize("planet_hexagons, action", [
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.WHITE)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
    ),
    (
        [
            Hexagon(0, 1, planet=Planet(PlanetType.GAIA)),
            Hexagon(0, 0, planet=Planet(PlanetType.WHITE, building=TestBuilding(BuildingType.MINE)))
        ],
        PlaceMineAction(Hexagon(0, 1)),
    )
])
def test_place_mine_perform_action(planet_hexagons, action, one_sector_gamestate):
    player = list(one_sector_gamestate.players.values())[0]

    action.perform_action(one_sector_gamestate, player.player_id)

    original_hexagon = list(planet_hexagons)[0]
    inhabited_hexagon = one_sector_gamestate.game_map.get_hexagon(original_hexagon)
    assert original_hexagon == inhabited_hexagon
    assert original_hexagon.planet.planet_type == inhabited_hexagon.planet.planet_type
    assert inhabited_hexagon.planet.building.faction == player.faction
    assert inhabited_hexagon.planet.building.type == BuildingType.MINE
