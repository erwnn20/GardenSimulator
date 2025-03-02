from abc import ABC
from enum import Enum
from pydantic.types import confloat

from plants.add.fertilizer import FertilizerType
from utils.prompt import Prompt


class Soil(ABC):
    def __init__(self, *, water_per_unit: confloat(gt=0), growth_bonus: confloat(gt=0)):
        self.water_per_unit: float = water_per_unit
        self.growth_bonus: float = growth_bonus
        self.fertilizers: dict[FertilizerType, int] = {}

    def fertilize(self, fertilizer: FertilizerType) -> 'Soil':
        if fertilizer not in self.fertilizers:
            self.fertilizers[fertilizer] = 0

        self.fertilizers[fertilizer] += fertilizer.value.turn
        return self


class Clay(Soil):
    def __init__(self):
        super().__init__(water_per_unit=2.5, growth_bonus=0.25)


class Sandy(Soil):
    def __init__(self):
        super().__init__(water_per_unit=0.7, growth_bonus=0.1)


class Loamy(Soil):
    def __init__(self):
        super().__init__(water_per_unit=1.5, growth_bonus=0.3)


class Humus(Soil):
    def __init__(self):
        super().__init__(water_per_unit=1.8, growth_bonus=0.5)


class Calcareous(Soil):
    def __init__(self):
        super().__init__(water_per_unit=3.5, growth_bonus=0.05)


class Silty(Soil):
    def __init__(self):
        super().__init__(water_per_unit=1.6, growth_bonus=0.4)


class SoilType(Enum):
    CLAY = Clay
    SANDY = Sandy
    LOAMY = Loamy
    HUMUS = Humus
    CALCAREOUS = Calcareous
    SILTY = Silty

    def __str__(self):
        soil_instance = self.value()
        return (f'{self.name.capitalize()} '
                f'(water per unit: {soil_instance.water_per_unit:.2f} L, '
                f'growth bonus: +{soil_instance.growth_bonus * 100:.1f}%)')

    @staticmethod
    def select() -> type[Soil]:
        return Prompt.select(
            prompt='Select a type of Soil:',
            choices=list(SoilType),
            display_func=lambda t: str(t)
        ).element.value
