from enum import IntEnum
from gaia.players import Player, Income


class ResearchTracks(IntEnum):
    TERRAFORMING = 0
    NAVIGATION = 1
    ARTIFICIAL_INTELLIGENCE = 2
    GAIA_PROJECT = 3
    ECONOMY = 4
    SCIENCE = 5


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

    def get_player_terraforming_cost(self, player: Player):
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
        elif level <= 2:
            return 2
        elif level <= 4:
            return 3
        return 4

    def get_player_available_gaiaformers(self, player: Player):
        level = self.get_placement(player, ResearchTracks.GAIA_PROJECT)
        if level == 0:
            return 0
        elif level <= 1:
            return 1
        elif level <= 3:
            return 2
        return 3

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