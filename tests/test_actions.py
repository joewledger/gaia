import pytest

from gaia.map import Planet, InhabitedPlanet, Hexagon, PlanetType
from gaia.buildings import Building
from gaia.actions import PlaceMineAction

from tests.util import TestFaction


@pytest.mark.parametrize("planets,action,should_be_valid", [
    (
        [
            Planet(Hexagon(0, 1), PlanetType.WHITE),
            InhabitedPlanet(Hexagon(0, 0), PlanetType.WHITE, TestFaction.TEST, Building.MINE)
        ],
        PlaceMineAction(Hexagon(0, 1)),
        True
    )
])
def test_place_mine_range_validation(planets, action, should_be_valid, one_sector_gamestate, mocker):
    player = list(one_sector_gamestate.players.values())[0]

    mocker.patch.object(player, 'get_distance_from_planet_color')
    player.get_distance_from_planet_color.return_value = 0

    valid, reason = action.validate(one_sector_gamestate, player.player_id)
    assert valid == should_be_valid
