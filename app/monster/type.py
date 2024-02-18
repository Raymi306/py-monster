from enum import Enum, auto


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
