from gaia.map import Sector


def test_sector_has_correct_number_of_tiles():
    assert len(Sector([], radius=1).hexagons) == 1
    assert len(Sector([], radius=2).hexagons) == 7
    assert len(Sector([], radius=3).hexagons) == 19
