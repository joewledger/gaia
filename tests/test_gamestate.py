import pytest

from gaia.gamestate.gamestate import ResearchBoard
from gaia.utils.enums import ResearchTracks
from gaia.gamestate.players import Income
from tests.util import get_research_bonus_func_for_track


@pytest.mark.parametrize("track,level,bonus", [
    (ResearchTracks.TERRAFORMING, 0, 3),
    (ResearchTracks.TERRAFORMING, 1, 3),
    (ResearchTracks.TERRAFORMING, 2, 2),
    (ResearchTracks.TERRAFORMING, 3, 1),
    (ResearchTracks.TERRAFORMING, 4, 1),
    (ResearchTracks.TERRAFORMING, 5, 1),
    (ResearchTracks.NAVIGATION, 0, 1),
    (ResearchTracks.NAVIGATION, 1, 1),
    (ResearchTracks.NAVIGATION, 2, 2),
    (ResearchTracks.NAVIGATION, 3, 2),
    (ResearchTracks.NAVIGATION, 4, 3),
    (ResearchTracks.NAVIGATION, 5, 4),
    (ResearchTracks.GAIA_PROJECT, 0, (0, 0)),
    (ResearchTracks.GAIA_PROJECT, 1, (1, 6)),
    (ResearchTracks.GAIA_PROJECT, 2, (1, 6)),
    (ResearchTracks.GAIA_PROJECT, 3, (2, 4)),
    (ResearchTracks.GAIA_PROJECT, 4, (3, 3)),
    (ResearchTracks.GAIA_PROJECT, 5, (3, 3)),
    (ResearchTracks.ECONOMY, 0, Income()),
    (ResearchTracks.ECONOMY, 1, Income(credits=2, power=1)),
    (ResearchTracks.ECONOMY, 2, Income(ore=1, credits=2, power=2)),
    (ResearchTracks.ECONOMY, 3, Income(ore=1, credits=3, power=3)),
    (ResearchTracks.ECONOMY, 4, Income(ore=2, credits=4, power=4)),
    (ResearchTracks.ECONOMY, 5, Income()),
    (ResearchTracks.SCIENCE, 0, 0),
    (ResearchTracks.SCIENCE, 1, 1),
    (ResearchTracks.SCIENCE, 2, 2),
    (ResearchTracks.SCIENCE, 3, 3),
    (ResearchTracks.SCIENCE, 4, 4),
    (ResearchTracks.SCIENCE, 5, 0)
])
def test_research_board_persistant_bonuses(track, level, bonus, test_player):
    board = ResearchBoard()
    board.place_player(test_player, track, level=level)
    bonus_func = get_research_bonus_func_for_track(track)
    assert bonus_func(board, test_player) == bonus
