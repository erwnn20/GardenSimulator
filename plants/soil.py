from abc import ABC
from enum import Enum


class Soil(ABC):
    class Bonus(Enum):
        Fertilized = 0

    def __init__(self, water_per_unit: float, *, growth_bonus: float = 0):
        self.water_per_unit = water_per_unit
        self.growth_bonus = growth_bonus
        self.bonus: dict[Soil.Bonus, int] = {}

    def fertilize(self, turn_added: int) -> 'Soil':
        if Soil.Bonus.Fertilized not in self.bonus:
            self.bonus[Soil.Bonus.Fertilized] = 0

        self.bonus[Soil.Bonus.Fertilized] += turn_added
        return self


class Fertilizer(Enum):
    pass