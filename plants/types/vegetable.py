from enum import Enum

from pydantic import confloat, conint

from plants.plant import Plant
from utils.prompt import Prompt


class Vegetable(Plant):
    def __init__(self, *, water_needs: confloat(gt=1.5), growth_rate: confloat(gt=7, le=15), size: conint(ge=2, le=6),
                 fertilizer_limit: confloat(gt=0, le=1.5), growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(water_needs=water_needs, growth_rate=growth_rate, size=size, fertilizer_limit=fertilizer_limit,
                         growth=growth, fertilizer_quantity=fertilizer_quantity)


class Carrot(Vegetable):
    def __init__(self):
        super().__init__(water_needs=2.0, growth_rate=10, size=2, fertilizer_limit=1.2)


class Tomato(Vegetable):
    def __init__(self):
        super().__init__(water_needs=2.5, growth_rate=12, size=4, fertilizer_limit=1.5)


class Lettuce(Vegetable):
    def __init__(self):
        super().__init__(water_needs=1.8, growth_rate=9, size=3, fertilizer_limit=1.0)


class Potato(Vegetable):
    def __init__(self):
        super().__init__(water_needs=2.2, growth_rate=8, size=3, fertilizer_limit=1.3)


class Pepper(Vegetable):
    def __init__(self):
        super().__init__(water_needs=2.8, growth_rate=13, size=5, fertilizer_limit=1.4)


class Cucumber(Vegetable):
    def __init__(self):
        super().__init__(water_needs=3.0, growth_rate=14, size=6, fertilizer_limit=1.5)


class VegetableType(Enum):
    CARROT = Carrot
    TOMATO = Tomato
    LETTUCE = Lettuce
    POTATO = Potato
    PEPPER = Pepper
    CUCUMBER = Cucumber

    def __str__(self):
        vegetable_instance = self.value()
        return (f'{self.name.capitalize()} '
                f'(size: {vegetable_instance.size}, '
                f'water needs: {vegetable_instance.water_needs:.1f} L, '
                f'growth rate: {vegetable_instance.growth_rate:.1f}%)')

    @staticmethod
    def select() -> type(Vegetable):
        return Prompt.select(
            prompt='Select a type of Vegetable:',
            choices=list(VegetableType),
            display_func=lambda t: str(t)
        ).element.value
