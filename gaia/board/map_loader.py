from __future__ import annotations
from typing import Dict
import json

from gaia.utils.enums import PlanetType

from gaia.board.sectors import Sector
from gaia.board.hexagons import Hexagon
from gaia.board.planets import Planet
from gaia.board.map import Map


class GameTile(object):
    """
    GameTiles are the physical pieces that form the map.
    They have either one or two sides (which are sectors)
    """
    def __init__(self):
        self.sides = []

    def __getitem__(self, idx):
        return self.sides[idx]

    @staticmethod
    def get_tile_mapping_from_config(config_path: str) -> Dict[int, GameTile]:
        with open(config_path) as config:
            config = json.load(config)

        tile_mapping = dict()

        for tile in config["tiles"]:
            game_tile = GameTile()
            tile_mapping[tile["number"]] = game_tile

            radius = tile["radius"]
            for side in tile["sides"]:
                hexagons = {Hexagon(p["x"], p["z"], Planet(PlanetType[p["type"]])) for p in side}
                game_tile.sides.append(Sector(hexagons, radius))

        return tile_mapping


class MapLoader(object):
    @staticmethod
    def load_from_config(config_path: str, game_type: str = None) -> Map:
        with open(config_path) as config:
            config = json.load(config)

        all_game_tiles = GameTile.get_tile_mapping_from_config(config_path)
        sectors = []

        if game_type:
            for tile_config in config[game_type]["tiles"]:
                tile = all_game_tiles[tile_config["number"]]
                sector = tile[tile_config["side"]]
                sector.adjust_offset(tile_config["x_offset"], tile_config["z_offset"])
                sectors.append(sector)
        else:
            # TODO implement random map generation
            raise NotImplementedError

        return Map(sectors, [])
