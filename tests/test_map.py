import pytest
from copy import copy

from gaia.map import Hexagon, Planet, InhabitedPlanet, Sector
from gaia.players import Factions
from gaia.buildings import Buildings


@pytest.mark.parametrize("hex1,hex2,distance", [
    (Hexagon(0, 0), Hexagon(0, 1), 1),
    (Hexagon(0, 0), Hexagon(2, 1), 3),
    (Hexagon(0, 0), Hexagon(2, 2), 4),
    (Hexagon(-3, 0), Hexagon(3, 0), 6),
    (Hexagon(-3, -2), Hexagon(5, -3), 8),
    (Hexagon(2, -5), Hexagon(3, 2), 8),
    (Hexagon(-3, -2), Hexagon(3, 2), 10)
])
def test_hexagon_get_distance(hex1, hex2, distance):
    assert hex1.distance(hex2) == distance


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
    assert (Planet(orig, Planet.Type.ORANGE).rotate(degrees) ==
            Planet(new, Planet.Type.ORANGE))
    assert (InhabitedPlanet(orig, Planet.Type.ORANGE, Factions.AMBAS, Buildings.MINE).rotate(degrees) ==
            InhabitedPlanet(new, Planet.Type.ORANGE, Factions.AMBAS, Buildings.MINE))


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
    assert sector.get_planet(0, 0) == planets[0]
    assert sector.get_planet(0, 5) == planets[1]
    assert sector.get_planet(0, 4) == planets[2]
    assert sector.get_planet(100, -100) is None
