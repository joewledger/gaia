from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple


class Action(ABC):
    valid_str = "Action is valid"

    @property
    @abstractmethod
    def ends_turn(self) -> bool:
        pass

    def __str__(self):
        return str(type(self).__name__)


class ModifiesFinalActionWithBonus(object):
    @abstractmethod
    def modify_final_action(self, action: FinalAction) -> FinalAction:
        pass


class FinalAction(Action):
    """
    Any action that when taken will end the players turn
    """
    @property
    def ends_turn(self) -> bool:
        return True

    @abstractmethod
    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


class FreeAction(Action):
    """
    Any action that does not end a players turn.
    These include currency conversion actions (i.e. power -> gold)
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @abstractmethod
    def validate(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def perform_action(self, gamestate, player_id: str) -> Tuple[bool, str]:
        pass


class PartialAction(Action, ModifiesFinalActionWithBonus):
    """
    Similar to an free action,
    but must be played in conjunction with an action that will end the players turn.
    """
    @property
    def ends_turn(self) -> bool:
        return False

    @abstractmethod
    def validate_next_action(self, action: FinalAction) -> bool:
        pass
