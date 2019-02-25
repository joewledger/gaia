from dataclasses import dataclass
from typing import List, Union, Type
from random import sample

from gaia.board.map import Map
from gaia.players.players import Player, Income
from gaia.turns.actions import PartialAction, GaiaformAction, GainRangeAction
from gaia.utils.enums import BuildingType


class ScoringBonus(object):
    pass


class RoundEndScoringBonus(ScoringBonus):
    def score(self, player: Player, game_map: Map) -> int:
        pass


class BuildingRoundEndScoringBonus(RoundEndScoringBonus):
    def __init__(self, building_types: List[BuildingType], scoring_amount: int):
        self.building_types = building_types
        self.scoring_amount = scoring_amount


class GaiaPlanetRoundEndScoringBonus(RoundEndScoringBonus):
    def __init__(self, scoring_amount):
        self.scoring_amount = scoring_amount


@dataclass
class RoundBonus(object):
    id: int
    income_bonus: Income
    action_bonus: Union[Type[PartialAction], None]
    scoring_bonus: Union[ScoringBonus, None]


class IllegalRoundBonusSelectionException(Exception):
    pass


class AvailableRoundBonuses(object):
    def __init__(self, num_bonuses):
        round_bonuses = [
            RoundBonus(
                id=1,
                income_bonus=Income(ore=1, knowledge=1),
                action_bonus=None,
                scoring_bonus=None
            ),
            RoundBonus(
                id=2,
                income_bonus=Income(credits=2, qic=1),
                action_bonus=None,
                scoring_bonus=None
            ),
            RoundBonus(
                id=3,
                income_bonus=Income(ore=1, power_tokens=2),
                action_bonus=None,
                scoring_bonus=None
            ),
            RoundBonus(
                id=4,
                income_bonus=Income(credits=2),
                action_bonus=GaiaformAction,
                scoring_bonus=None
            ),
            RoundBonus(
                id=5,
                income_bonus=Income(power=2),
                action_bonus=GainRangeAction,
                scoring_bonus=None
            ),
            RoundBonus(
                id=6,
                income_bonus=Income(ore=1),
                action_bonus=None,
                scoring_bonus=BuildingRoundEndScoringBonus(
                    building_types=[BuildingType.MINE],
                    scoring_amount=1
                )
            ),
            RoundBonus(
                id=7,
                income_bonus=Income(knowledge=1),
                action_bonus=None,
                scoring_bonus=BuildingRoundEndScoringBonus(
                    building_types=[BuildingType.RESEARCH_LAB],
                    scoring_amount=3
                )
            ),
            RoundBonus(
                id=8,
                income_bonus=Income(ore=1),
                action_bonus=None,
                scoring_bonus=BuildingRoundEndScoringBonus(
                    building_types=[BuildingType.TRADING_STATION],
                    scoring_amount=2
                )
            ),
            RoundBonus(
                id=9,
                income_bonus=Income(knowledge=1),
                action_bonus=None,
                scoring_bonus=BuildingRoundEndScoringBonus(
                    building_types=[BuildingType.PLANETARY_INSTITUTE, BuildingType.ACADEMY],
                    scoring_amount=4
                )
            ),
            RoundBonus(
                id=10,
                income_bonus=Income(credits=4),
                action_bonus=None,
                scoring_bonus=GaiaPlanetRoundEndScoringBonus(
                    scoring_amount=1
                )
            )
        ]

        bonuses_to_keep = sample(round_bonuses, num_bonuses)
        self.round_bonuses = {
            round_bonus.id: round_bonus for round_bonus in bonuses_to_keep
        }

    def take_round_bonus(self, player, bonus_id):
        pass
