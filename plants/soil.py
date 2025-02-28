from abc import ABC

from plants.add.fertilizer import FertilizerType


class Soil(ABC):
    def __init__(self, *, water_per_unit: float, growth_bonus: float = 0):
        self.water_per_unit = water_per_unit
        self.growth_bonus = growth_bonus
        self.fertilizers: dict[FertilizerType, int] = {}

    def fertilize(self, fertilizer: FertilizerType) -> 'Soil':
        if fertilizer not in self.fertilizers.keys():
            self.fertilizers[fertilizer] = 0

        self.fertilizers[fertilizer] += fertilizer.value.turn
        return self

