from enum import IntEnum

from gaia.utils.enums import ResearchTracks, BuildingType
from gaia.gamestate.gamestate import ResearchBoard
from gaia.board.buildings import Building


class TestBuilding(Building):
    def __init__(self, building_type: BuildingType):
        Building.__init__(self, TestFaction.TEST, building_type)


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
