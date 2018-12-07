from gaia.players import Player
from gaia.map import Map, Hexagon
from gaia.gamestate import ResearchBoard


class Action(object):
    """
    Any action that when taken will end the players turn
    """
    pass


class FreeAction(object):
    """
    Any action that does not end a players turn.
    These include currency conversion actions (i.e. power -> gold)
    """
    pass


class PartialAction(object):
    """
    Similar to an free action,
    but must be played in conjunction with an action that will end the players turn.

    """
    pass


class GaiaformAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    pass


class GainRangeAction(PartialAction):
    """
    Must be followed followed by the PlaceMineAction or StartGaiaProjectAction
    """
    pass


class PlaceMineAction(Action):
    def __init__(self, player: Player, hexagon: Hexagon, map: Map, research_board: ResearchBoard):
        pass


class StartGaiaProjectAction(Action):
    pass
