from enum import IntEnum

from gaia.gamestate import ResearchTracks, ResearchBoard


class TestFaction(IntEnum):
    TEST = 14


def get_research_bonus_func_for_track(track: ResearchTracks):
    return {
        ResearchTracks.TERRAFORMING: ResearchBoard.get_player_gaiaforming_cost,
        ResearchTracks.NAVIGATION: ResearchBoard.get_player_navigation_ability,
        ResearchTracks.GAIA_PROJECT: ResearchBoard.get_player_available_gaiaformers_and_cost,
        ResearchTracks.ECONOMY: ResearchBoard.get_player_economy_bonus,
        ResearchTracks.SCIENCE: ResearchBoard.get_player_science_bonus
    }[track]
