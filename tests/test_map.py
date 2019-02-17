import pytest
from copy import copy, deepcopy
import json

from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet, InhabitedPlanet
from gaia.board.sectors import Sector
from gaia.board.map import Map, GameTile

from gaia.utils.enums import PlanetType, Factions, BuildingType


@pytest.mark.parametrize("hex1,hex2,distance", [
    (Hexagon(0, 0), Hexagon(0, 1), 1),
    (Hexagon(0, 0), Hexagon(2, 1), 3),
    (Hexagon(0, 0), Hexagon(-2, 2), 2),
    (Hexagon(0, 0), Hexagon(2, 2), 4),
    (Hexagon(-3, 0), Hexagon(3, 0), 6),
    (Hexagon(-3, -2), Hexagon(5, -3), 8),
    (Hexagon(2, -5), Hexagon(3, 2), 8),
    (Hexagon(-3, -2), Hexagon(3, 2), 10)
])
def test_hexagon_get_distance(hex1, hex2, distance):
    assert hex1.distance(hex2) == distance


@pytest.mark.parametrize("hex1,hex2,x_offset_diff,z_offset_diff", [
    (Hexagon(0, 0), Hexagon(1, 1), 1, 1),
    (Hexagon(1, 5), Hexagon(2, 3), 1, -2),
    (Hexagon(4, -2), Hexagon(5, -3), 1, -1)
])
def test_hexagon_adjust_offset(hex1, hex2, x_offset_diff, z_offset_diff):
    assert hex1.adjust_offset(x_offset_diff, z_offset_diff) == hex2


@pytest.mark.parametrize("orig,new,degrees", [
    (Hexagon(0, 0), Hexagon(0, 0), 0),
    (Hexagon(0, -5), Hexagon(5, -5), 60),
    (Hexagon(-3, -1), Hexagon(1, -4), 60),
    (Hexagon(-4, 3), Hexagon(1, -4), 120),
    (Hexagon(-1, 4), Hexagon(3, 1), 300),
    (Hexagon(1, -4), Hexagon(-1, 4), 180)
])
def test_hexagon_rotation(orig, new, degrees):
    assert orig.rotate(degrees) == new
    assert (Planet(orig, PlanetType.ORANGE).rotate(degrees) ==
            Planet(new, PlanetType.ORANGE))
    assert (InhabitedPlanet(orig, PlanetType.ORANGE, Factions.AMBAS, BuildingType.MINE).rotate(degrees) ==
            InhabitedPlanet(new, PlanetType.ORANGE, Factions.AMBAS, BuildingType.MINE))


@pytest.mark.parametrize("degrees", [
    60, 120, 180, 240, 300, 360
])
def test_sector_rotation(planets, degrees):
    sector = Sector([copy(p) for p in planets])
    sector.rotate(degrees)
    assert all(p.rotate(degrees) in sector.planets.values() for p in planets)


def test_sector_has_correct_number_of_tiles():
    assert len(Sector([], radius=1).hexagons) == 1
    assert len(Sector([], radius=2).hexagons) == 7
    assert len(Sector([], radius=3).hexagons) == 19


@pytest.mark.parametrize("sector,hexagons", [
    (Sector([], radius=1), {Hexagon(0, 0)}),
    (Sector([], radius=2), {
        Hexagon(0, 0),
        Hexagon(0, -1),
        Hexagon(0, 1),
        Hexagon(1, -1),
        Hexagon(1, 0),
        Hexagon(-1, 1),
        Hexagon(-1, 0)
    }),
    (Sector([], radius=2, x_offset=2, z_offset=-1), {
        Hexagon(2, -1),
        Hexagon(2, -2),
        Hexagon(2, 0),
        Hexagon(3, -2),
        Hexagon(3, -1),
        Hexagon(1, 0),
        Hexagon(1, -1)
    })
])
def test_sector_has_expected_tiles(sector, hexagons):
    assert sector.hexagons == hexagons


def test_sector_has_all_planets(planets):
    sector = Sector(planets)

    assert len(sector.planets) == len(planets)
    assert sector.get_planet(Hexagon(0, 0)) == planets[0]
    assert sector.get_planet(Hexagon(0, 2)) == planets[1]
    assert sector.get_planet(Hexagon(-1, 1)) == planets[2]
    assert sector.get_planet(Hexagon(100, -100)) is None


@pytest.mark.parametrize("orig_x_offset,orig_z_offset,x_offset,z_offset", [
    (0, 0, 0, 0),
    (0, 0, 1, 2),
    (0, 0, -2, -4),
    (0, 0, 154, 163),
    (0, 0, -24, 18),
    (1, 2, 0, 0),
    (-1, 4, 1, 2),
    (-3, 5, -2, -4),
    (2, -1, 154, 163),
    (-5, 3, -24, 18)
])
def test_sector_adjust_offset(planets, orig_x_offset, orig_z_offset, x_offset, z_offset):
    planets_copy = deepcopy(planets)
    sector = Sector(planets, x_offset=orig_x_offset, z_offset=orig_z_offset)
    sector.adjust_offset(x_offset=x_offset, z_offset=z_offset)
    assert all(h.distance(Hexagon(x_offset, z_offset)) <= 2 for h in sector.hexagons)
    assert all(p.hex.distance(Hexagon(x_offset, z_offset)) <= 2 for p in sector.planets.values())
    assert all(h == p.hex for h, p in sector.planets.items())
    assert sector.x_offset == x_offset
    assert sector.z_offset == z_offset
    assert all(p.move_hex(p.hex.adjust_offset(x_offset, z_offset)) in sector.planets.values() for p in planets_copy)


@pytest.mark.integration
def test_load_gametile_mapping_from_config(config_path):
    gametiles = GameTile.get_tile_mapping_from_config(config_path=config_path)

    assert len(gametiles) == 10
    assert list(gametiles.keys()) == list(range(1, 11))
    assert all(isinstance(gt, GameTile) for gt in gametiles.values())
    assert all(len(gt.sides) in (1, 2) for gt in gametiles.values())

    sectors = set()
    for gt in gametiles.values():
        sectors.update(gt.sides)

    assert all(s.radius == 3 for s in sectors)
    assert all(s.x_offset == 0 and s.z_offset == 0 for s in sectors)

    for sector in sectors:
        planets = sector.planets.values()
        assert all(planet.hex.x in range(-2, 3) and planet.hex.z in range(-2, 3) for planet in planets)
        assert all(isinstance(planet.planet_type, PlanetType) for planet in planets)


@pytest.mark.integration
def test_map_load_from_config(config_path):
    map = Map.load_from_config(config_path=config_path,
                               game_type="1p_2p_default")
    assert len(map.sectors) == 7

    hexagons = set()
    for sector in map.sectors:
        assert len(sector.hexagons) == 19
        assert not any(h in hexagons for h in sector.hexagons)
        hexagons.update(sector.hexagons)

    # There should be 19 hexagons in each sector, and no hexagons should overlap between sectors
    assert len(hexagons) == 7 * 19


@pytest.mark.integration
def test_map_to_json(default_map):
    map_str = default_map.to_json()
    assert isinstance(map_str, str)

    map_json = json.loads(map_str)
    sectors = map_json["sectors"]
    assert len(sectors) == 7
    assert all(all(prop in sector for prop in ["radius", "x_offset", "z_offset", "screen_x_factor", "screen_y_factor", "hexagons", "planets"]) for sector in sectors)
    assert all(len(sector["hexagons"]) == 19 for sector in sectors)

    for sector in sectors:
        hexagons = sector["hexagons"]
        planets = sector["planets"]
        assert all(all(prop in hex for prop in ["x", "z", "screen_x_factor", "screen_y_factor"]) for hex in hexagons)
        assert all(all(prop in planet for prop in ["hex", "planet_type"]) for planet in planets)

    assert map_json["federations"] == []
