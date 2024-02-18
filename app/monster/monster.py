from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Sequence, Optional

from app.monster.type import MonsterType
from app.monster.state import MonsterState


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
        if self.health <= 0:
            return
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
