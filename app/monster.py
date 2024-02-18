from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Sequence, Callable, Optional


class OutOfEnergyException(Exception):
    pass


class TypeAdvantage(Enum):
    SUPER = auto()
    NORMAL = auto()
    NOT_VERY = auto()


class MonsterType(Enum):
    GRASS = auto()
    FIRE = auto()
    WATER = auto()

    def has_advantage(self, other: TypeAdvantage) -> TypeAdvantage:
        match (self, other):
            case (MonsterType.GRASS, MonsterType.FIRE):
                return TypeAdvantage.NOT_VERY
            case (MonsterType.GRASS, MonsterType.WATER):
                return TypeAdvantage.SUPER
            case (MonsterType.GRASS, MonsterType.GRASS):
                return TypeAdvantage.NORMAL
            case (MonsterType.FIRE, MonsterType.FIRE):
                return TypeAdvantage.NORMAL
            case (MonsterType.FIRE, MonsterType.WATER):
                return TypeAdvantage.NOT_VERY
            case (MonsterType.FIRE, MonsterType.GRASS):
                return TypeAdvantage.SUPER
            case (MonsterType.WATER, MonsterType.FIRE):
                return TypeAdvantage.SUPER
            case (MonsterType.WATER, MonsterType.WATER):
                return TypeAdvantage.NORMAL
            case (MonsterType.WATER, MonsterType.GRASS):
                return TypeAdvantage.NOT_VERY
            case _:
                raise RuntimeError("You somehow added more type combinations and fucked everything up")


class MonsterState(Enum):
    NORMAL = auto()
    DEFEND = auto()
    POISON = auto()


class Monster(ABC):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._name = cls.__name__
        instance.__init__(*args, **kwargs)
        return instance

    def __init__(
            self,
            health: float,
            energy: int,
            moves: Sequence[Move],
            nickname: Optional[str] = None,
        ):
        self.nickname = nickname
        self.health = health
        self.energy = energy
        self.moves = moves
        self.state = MonsterState.NORMAL

    @property
    def name(self) -> str:
        return self.nickname or self._name

    @property
    @abstractmethod
    def type(self) -> MonsterType:
        pass

    def list_moves(self):
        for i, move in enumerate(self.moves):
            print(f"{i + 1}: {move.name}")
        print()

    def perform_move(self, move_choice, target):
        match self.state:
            case MonsterState.POISON:
                self.health -= 1
            case _:
                self.state = MonsterState.NORMAL
        self.moves[move_choice - 1](self, target)

    def damage(self, amount):
        multiplier = 1.0
        if self.state is MonsterState.DEFEND:
            if self.energy == 0:
                multiplier = 0
            else:
                multiplier = 1 / self.energy
        self.health -= (amount * multiplier)


class FireMonster(Monster):
    @property
    def type(self):
        return MonsterType.FIRE


class WaterMonster(Monster):
    @property
    def type(self):
        return MonsterType.WATER


class GrassMonster(Monster):
    @property
    def type(self):
        return MonsterType.GRASS


# Moves -------------------------------------------------------------------------------------------
def get_advantage_multiplier(self: TypeAdvantage, target: TypeAdvantage) -> float:
    match self.has_advantage(target):
        case TypeAdvantage.SUPER:
            return 1.5
        case TypeAdvantage.NOT_VERY:
            return 0.5
        case _:
            return 1.0


class Move(ABC):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._name = cls.__name__
        instance.__init__(*args, **kwargs)
        return instance

    def _check_energy(self, origin):
        if origin.energy - self.energy < 0:
            raise OutOfEnergyException

    def __call__(self, origin, target=None):
        self._check_energy(origin)
        self._call(origin, target)

    @property
    def name(self):
        return self._name

    @abstractmethod
    def _call(self, *args):
        pass


class Attack(Move):

    energy = 0
    damage = 1.0

    def _call(self, origin, target):
        multiplier = get_advantage_multiplier(origin.type, target.type)
        target.damage(self.damage * multiplier)


class Defend(Move):

    energy = 0

    def _call(self, origin, *args):
        origin.state = MonsterState.DEFEND
        origin.energy -= self.energy


class Rampage(Move):

    energy = 1
    damage = 2.0

    def _call(self, origin, target):
        multiplier = get_advantage_multiplier(origin.type, target.type)
        target.damage(self.damage * multiplier)
        origin.energy -= self.energy


class DrainEnergy(Move):

    energy = 1
    damage = 0

    def _call(self, origin, target):
        if target.energy > 0:
            target.energy -= self.energy
            origin.energy += self.energy
        else:
            origin.energy -= self.energy


class Poison(Move):

    energy = 2
    damage = 0

    def _call(self, origin, target):
        target.state = MonsterState.POISON
        origin.energy -= self.energy
