from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from uuid import uuid4
from abc import ABC, abstractmethod

from gaia.utils.enums import PlanetType, FactionType, BuildingType
from gaia.utils.utils import CustomJSONSerialization, obj_to_json
from gaia.board.planets import Planet


class BasePlayer(ABC):
    def __init__(self):
        self._player_id = uuid4()
        self.player_resources = self.get_starting_resources()
        self.board_income = self.get_starting_board_income()
        self.round_bonus = None

    @property
    def player_id(self) -> str:
        return str(self._player_id)

    @property
    @abstractmethod
    def faction(self) -> FactionType:
        pass

    @property
    @abstractmethod
    def native_planet(self) -> PlanetType:
        pass

    def get_distance_from_planet_color(self, target_planet: PlanetType) -> int:
        return Planet.get_terraforming_distance(self.native_planet, target_planet)

    def get_legal_building_upgrades(self) -> Dict[BuildingType, List[BuildingType]]:
        return {
            BuildingType.MINE: [BuildingType.TRADING_STATION],
            BuildingType.TRADING_STATION: [BuildingType.RESEARCH_LAB, BuildingType.PLANETARY_INSTITUTE],
            BuildingType.RESEARCH_LAB: [BuildingType.ACADEMY]
        }

    @abstractmethod
    def get_starting_resources(self) -> PlayerResources:
        pass

    @abstractmethod
    def get_starting_board_income(self) -> Income:
        pass

    def can_afford(self, cost: Cost):
        player_resources = self.player_resources.to_json()

        return all(player_resources[key] >= cost[key] for key in list(cost.__dict__.keys())
                   if key in player_resources)

    def __eq__(self, other):
        return self.player_id == other.player_id

    def __hash__(self):
        return self._player_id.int


@dataclass
class PlayerResources(CustomJSONSerialization):
    ore: int
    credits: int
    knowledge: int
    qic: int
    power_bowls: Dict[int, int]

    MAX_ORE = 15
    MAX_KNOWLEDGE = 15
    MAX_CREDITS = 30

    def gain_power(self, power: int):
        for i in range(power):
            if self.power_bowls[0] > 0:
                self.power_bowls[1] += 1
                self.power_bowls[0] -= 1
            elif self.power_bowls[1] > 0:
                self.power_bowls[2] += 1
                self.power_bowls[1] -= 1

    def to_json(self):
        return obj_to_json(self, {
            "power": self.power_bowls[2]
        })


@dataclass
class Income(object):
    ore: int = 0
    credits: int = 0
    knowledge: int = 0
    qic: int = 0
    power: int = 0
    power_tokens: int = 0

    def __add__(self, other: Income):
        return Income(self.ore + other.ore,
                      self.credits + other.credits,
                      self.knowledge + other.knowledge,
                      self.qic + other.qic,
                      self.power + other.power,
                      self.power_tokens + other.power_tokens)


@dataclass
class Cost(object):
    ore: int = 0
    credits: int = 0
    knowledge: int = 0
    qic: int = 0
    power: int = 0
    power_tokens: int = 0

    def __add__(self, other: Cost):
        return Cost(self.ore + other.ore,
                    self.credits + other.credits,
                    self.knowledge + other.knowledge,
                    self.qic + other.qic,
                    self.power + other.power,
                    self.power_tokens + other.power_tokens)

    def __getitem__(self, item):
        return self.__dict__[item]
