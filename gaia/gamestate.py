from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple

from gaia.players import Player, Income
from gaia.bonuses import AvailableRoundBonuses
from gaia.board.map import Map
from gaia.enums import ResearchTracks


@dataclass
class GameState(object):
    players: Dict[str, Player]
    game_map: Map
    research_board: ResearchBoard
    scoring_board: ScoringBoard
    round_bonuses: AvailableRoundBonuses
    
    def add_player(self, player: Player):
        self.players[player.player_id] = player

    def get_player(self, player_id: str):
        return self.players.get(player_id)


class ScoringBoard(object):
    pass


class ResearchBoard(object):
    """
    Takes care of the state of the games research board. One should be initialized per game.

    The board can be queried for permanent player attributes. However, one-time bonuses will not be stored,
    and will be applied to the relevant player object when the bonus is granted.
    """
    def __init__(self):
        self.player_placements = {
            track: dict() for track in ResearchTracks
        }

    def place_player(self, player: Player, track: ResearchTracks, level: int = 0):
        self.player_placements[track][player] = level

    def get_placement(self, player: Player, track: ResearchTracks):
        return self.player_placements[track].get(player, 0)

    def advance_player(self, player: Player, track: ResearchTracks):
        pass

    def get_player_gaiaforming_cost(self, player: Player):
        level = self.get_placement(player, ResearchTracks.TERRAFORMING)
        if level <= 1:
            return 3
        elif level <= 2:
            return 2
        return 1

    def get_player_navigation_ability(self, player: Player):
        level = self.get_placement(player, ResearchTracks.NAVIGATION)
        if level <= 1:
            return 1
        elif level <= 3:
            return 2
        elif level <= 4:
            return 3
        return 4

    def get_player_available_gaiaformers_and_cost(self, player: Player) -> Tuple[int, int]:
        level = self.get_placement(player, ResearchTracks.GAIA_PROJECT)
        if level == 0:
            return 0, 0
        elif level <= 2:
            return 1, 6
        elif level <= 3:
            return 2, 4
        return 3, 3

    def get_player_economy_bonus(self, player: Player):
        level = self.get_placement(player, ResearchTracks.ECONOMY)
        if level == 1:
            return Income(credits=2, power=1)
        elif level == 2:
            return Income(ore=1, credits=2, power=2)
        elif level == 3:
            return Income(ore=1, credits=3, power=3)
        elif level == 4:
            return Income(ore=2, credits=4, power=4)
        return Income()

    def get_player_science_bonus(self, player: Player):
        level = self.get_placement(player, ResearchTracks.SCIENCE)
        if level <= 4:
            return level
        return 0
