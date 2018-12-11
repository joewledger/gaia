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


def planet_type_to_hex_color(planet_type: PlanetType) -> str:
    return {
        PlanetType.RED: "#ff0000",
        PlanetType.ORANGE: "#ff6600",
        PlanetType.WHITE: "#ffffff",
        PlanetType.GREY: "#b3b3b3",
        PlanetType.YELLOW: "#ffff00",
        PlanetType.BROWN: "#663300",
        PlanetType.BLUE: "#0000ff",
        PlanetType.GAIA: "#00ff00",
        PlanetType.TRANSDIM: "#cc00cc",
        PlanetType.LOST: "#cc6699"
    }[planet_type]
