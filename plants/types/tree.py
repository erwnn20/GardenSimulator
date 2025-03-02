from enum import Enum
from pydantic.types import confloat, conint

from plants.plant import Plant
from utils.prompt import Prompt


class Tree(Plant):
    def __init__(self, *, water_needs: confloat(gt=5), growth_rate: confloat(gt=0, le=5.5), size: conint(ge=7, le=10),
                 fertilizer_limit: confloat(gt=0, le=1.5),
                 growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(water_needs=water_needs, growth_rate=growth_rate, size=size, fertilizer_limit=fertilizer_limit,
                         growth=growth, fertilizer_quantity=fertilizer_quantity)


class Oak(Tree):
    def __init__(self):
        super().__init__(water_needs=6.0, growth_rate=1.2, size=10, fertilizer_limit=1.2)


class Pine(Tree):
    def __init__(self):
        super().__init__(water_needs=5.5, growth_rate=1.8, size=9, fertilizer_limit=1.125)


class Maple(Tree):
    def __init__(self):
        super().__init__(water_needs=7.0, growth_rate=2.5, size=8, fertilizer_limit=1.35)


class Willow(Tree):
    def __init__(self):
        super().__init__(water_needs=8.5, growth_rate=3.5, size=10, fertilizer_limit=1.425)


class AppleTree(Tree):
    def __init__(self):
        super().__init__(water_needs=6.5, growth_rate=2.0, size=7, fertilizer_limit=1.275)


class TreeType(Enum):
    OAK = Oak
    PINE = Pine
    MAPLE = Maple
    WILLOW = Willow
    APPLE_TREE = AppleTree

    def __str__(self):
        tree_instance = self.value()
        return (f'{self.name.capitalize()} '
                f'(size: {tree_instance.size}, '
                f'water needs: {tree_instance.water_needs:.1f} L, '
                f'growth rate: {tree_instance.growth_rate:.1f}%)')

    @staticmethod
    def select() -> type[Tree]:
        return Prompt.select(
            prompt='Select a type of Tree:',
            choices=list(TreeType),
            display_func=lambda t: str(t)
        ).element.value
