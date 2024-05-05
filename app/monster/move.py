from abc import ABC, abstractmethod

from app.monster.exceptions import OutOfEnergyException
from app.monster.type import TypeAdvantage
from app.monster.state import MonsterState


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

    energy = 2
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
