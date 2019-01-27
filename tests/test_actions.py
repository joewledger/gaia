import pytest

from gaia.board.map import Planet, InhabitedPlanet, Hexagon, PlanetType
from gaia.utils.enums import Building
from gaia.turns.actions import PlaceMineAction
from gaia.gamestate.players import PlayerResources

from tests.util import TestFaction


@pytest.mark.parametrize("planets,action,should_be_valid,main_reason", [
    (
        [
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        True,
        None
    ),
    (
        [
            Planet(Hexagon(0, 1), PlanetType.TRANSDIM),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "Cannot build on transdim planets"
    ),
    (
        [
            InhabitedPlanet(Hexagon(0, 1), PlanetType.WHITE, TestFaction.TEST, Building.MINE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "This planet is already occupied"
    ),
    (
        [
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        False,
        "There is not planet on the specified hexagon"
    )
])
def test_place_mine_destination_planet_validation(planets, action,
                                                  should_be_valid, main_reason,
                                                  one_sector_gamestate, mocker):
    player = list(one_sector_gamestate.players.values())[0]

    mocker.patch.object(player, 'get_distance_from_planet_color')
    player.get_distance_from_planet_color.return_value = 0

    valid, reason = action.validate(one_sector_gamestate, player.player_id)
    assert valid == should_be_valid
    if main_reason:
        assert reason == main_reason


@pytest.mark.parametrize("planets,action,base_navigation,research_navigation,should_be_valid,main_reason", [
    (
        [
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        0,
        1,
        True,
        None
    ),
    (
        [
            Planet(Hexagon(0, 2), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 2)),
        0,
        1,
        False,
        "The planet is not in range"
    ),
    (
        [
            Planet(Hexagon(0, 4), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 4)),
        2,
        1,
        False,
        "The planet is not in range"
    ),
    (
        [
            Planet(Hexagon(0, 4), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 4)),
        2,
        2,
        True,
        None
    )
])
def test_place_mine_range_validation(planets, action, base_navigation, research_navigation,
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
    "planets,action,player_resources,free_gaiaforming,terraforming_cost,planet_distance,should_be_valid,main_reason", [
    (
        [
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.GAIA),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
            Planet(Hexagon(0, 1), PlanetType.GAIA),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
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
def test_place_mine_cost_validation(planets, action, player_resources, free_gaiaforming, terraforming_cost, planet_distance,
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


@pytest.mark.parametrize("planets, action", [
    (
        [
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
    ),
    (
        [
            Planet(Hexagon(0, 1), PlanetType.GAIA),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
    )
])
def test_place_mine_perform_action(planets, action, one_sector_gamestate):
    player = list(one_sector_gamestate.players.values())[0]

    action.perform_action(one_sector_gamestate, player.player_id)

    original_planet = planets[0]
    inhabited_planet = one_sector_gamestate.game_map.get_planet(original_planet.hex)
    assert original_planet.hex == inhabited_planet.hex
    assert original_planet.planet_type == inhabited_planet.planet_type
    assert inhabited_planet.faction == player.faction
    assert inhabited_planet.building == Building.MINE
