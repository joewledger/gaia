from dataclasses import dataclass
from gaia.players import Income
from gaia.actions import PartialAction


class ScoringBonus(object):
    pass


@dataclass
class RoundBonus(object):
    income_bonus: Income
    action_bonus: PartialAction
    scoring_bonus: ScoringBonus
