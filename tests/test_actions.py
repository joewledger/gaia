import pytest

from gaia.map import Planet, InhabitedPlanet, Hexagon, PlanetType
from gaia.buildings import Building
from gaia.actions import PlaceMineAction

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


def test_place_mine_cost_validation():
    pass


def test_place_mine_perform_action():
    pass
