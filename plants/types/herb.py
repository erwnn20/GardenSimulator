from enum import Enum
from pydantic.types import confloat, conint

from plants.plant import Plant
from product.product import Product
from utils.prompt import Prompt


class Herb(Plant):
    def __init__(self, *,
                 emoji: str = '🌿',
                 product: Product,
                 water_needs: confloat(ge=0.5, le=2.5),
                 growth_rate: confloat(gt=5, le=12),
                 size: conint(ge=1, le=3),
                 fertilizer_limit: confloat(gt=0, le=0.8),
                 growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            emoji=emoji,
            product=product,
            water_needs=water_needs,
            growth_rate=growth_rate,
            size=size,
            fertilizer_limit=fertilizer_limit,
            growth=growth,
            fertilizer_quantity=fertilizer_quantity
        )


class Basil(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            product=Product.BASIL,
            water_needs=1.5,
            growth_rate=10,
            size=2,
            fertilizer_limit=0.6,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class Mint(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            emoji='🍃',
            product=Product.MINT,
            water_needs=2.0,
            growth_rate=12,
            size=3,
            fertilizer_limit=0.8,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class Parsley(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            emoji='🌱',
            product=Product.PARSLEY,
            water_needs=1.2,
            growth_rate=9,
            size=2,
            fertilizer_limit=0.7,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class Chives(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            emoji='🧄',
            product=Product.CHIVES,
            water_needs=1.0,
            growth_rate=9,
            size=1,
            fertilizer_limit=0.5,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class Rosemary(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            emoji='🌾',
            product=Product.ROSEMARY,
            water_needs=0.8,
            growth_rate=6,
            size=3,
            fertilizer_limit=0.4,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class Thyme(Herb):
    def __init__(self, *, growth: float = 0, fertilizer_quantity: float = 0):
        super().__init__(
            product=Product.THYME,
            water_needs=0.5,
            growth_rate=8,
            size=2,
            fertilizer_limit=0.3,
            growth=growth, fertilizer_quantity=fertilizer_quantity
        )


class HerbType(Enum):
    BASIL = Basil
    MINT = Mint
    PARSLEY = Parsley
    CHIVES = Chives
    ROSEMARY = Rosemary
    THYME = Thyme

    def __str__(self):
        herb_instance = self.value()
        return (f'{herb_instance.emojis}{self.name.capitalize()} '
                f'(size: {herb_instance.size}, '
                f'water needs: {herb_instance.water_needs:.1f} L, '
                f'growth rate: {herb_instance.growth_rate:.1f}%)')

    @staticmethod
    def select() -> type[Herb]:
        return Prompt.select(
            prompt='Select a type of Herb:',
            choices=list(HerbType),
            display_func=lambda t: str(t)
        ).element.value
