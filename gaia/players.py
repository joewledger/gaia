from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict
from uuid import uuid4
from abc import abstractmethod

from gaia.planet_types import PlanetType
from gaia.utils import create_object_property_generator


class Factions(IntEnum):
    TERRANS = 0
    LANTIDS = 1
    XENOS = 2
    GLEENS = 3
    TAKLONS = 4
    AMBAS = 5
    HADSCH_HALLAS = 6
    IVITS = 7
    GEODENS = 8
    BALTAKS = 9
    FIRAKS = 10
    BESCODS = 11
    NEVLAS = 12
    ITARS = 13


class Player(object):
    def __init__(self, faction: Factions):
        self._player_id = uuid4()
        self.faction = faction
        self.player_resources = PlayerResources(ore=4, credits=15, knowledge=3, qic=1, power_bowls={0: 4, 1: 4, 2: 0})
        self.board_income = Income(ore=1, knowledge=1)
        self.round_bonus = None

    @property
    def player_id(self):
        return str(self._player_id)

    def __eq__(self, other):
        return self.player_id == other.player_id

    def __hash__(self):
        return self._player_id.int

    @abstractmethod
    def get_distance_from_planet_color(self, planet: PlanetType) -> int:
        pass

    def can_afford(self, cost: Cost):
        player_resources = dict(self.player_resources)

        return all(player_resources[key] >= cost[key] for key in list(cost.__dict__.keys())
                   if key in player_resources)


@dataclass
class PlayerResources(object):
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

    def __iter__(self):
        return create_object_property_generator(self, {
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
