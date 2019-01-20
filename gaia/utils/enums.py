from enum import IntEnum


class PlanetType(IntEnum):
    RED = 1
    ORANGE = 2
    WHITE = 3
    GREY = 4
    YELLOW = 5
    BROWN = 6
    BLUE = 7
    GAIA = 8
    TRANSDIM = 9
    LOST = 10

class Factions(IntEnum):
    TERRANS = 0
    LANTIDS = 1
    XENOS = 2
    GLEENS = 3
    TAKLONS = 4
    AMBAS = 5
    HADSCH_HALLAS = 6
    IVITS = 7
    GEODENS = 8
    BALTAKS = 9
    FIRAKS = 10
    BESCODS = 11
    NEVLAS = 12
    ITARS = 13

class BuildingType(IntEnum):
    MINE = 0
    TRADING_STATION = 1
    RESEARCH_LAB = 2
    PLANETARY_INSTITUTE = 3
    ACADEMY = 4

class ResearchTracks(IntEnum):
    TERRAFORMING = 0
    NAVIGATION = 1
    ARTIFICIAL_INTELLIGENCE = 2
    GAIA_PROJECT = 3
    ECONOMY = 4
    SCIENCE = 5