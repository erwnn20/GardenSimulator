import random
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from pydantic.types import confloat, conint

from product.product import Product
from utils.prompt import Prompt
from exceptions import PlantException

if TYPE_CHECKING:
    from plants.plantation import Plantation


class Plant(ABC):
    def __init__(self, *,
                 emoji: str = '🌱',
                 product: Product = Product.PRODUCT,
                 water_needs: confloat(gt=0),
                 growth_rate: confloat(gt=0, le=15),
                 size: conint(gt=0, le=10),
                 fertilizer_limit: confloat(gt=0, le=1.5),
                 growth: float = 0, fertilizer_quantity: float = 0):
        self.emoji = emoji
        self.product = product
        self.water_needs: float = water_needs
        self.growth_rate: float = growth_rate
        self.growth = growth
        self.size: int = size
        self.fertilizer_limit: float = fertilizer_limit
        self.fertilizer_quantity = fertilizer_quantity
        self.health = 100.0

    def __str__(self) -> str:
        return f'{self.emojis}{type(self).__name__} (health: {self.health:.1f}%, growth: {self.growth:.1f}%)'

    def __repr__(self):
        return f'{type(self)}(health={self.health:.1f}%, growth={self.growth:.1f}%)'

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def emojis(self) -> str:
        output = '⚠️' if 85.0 < self.growth <= 120.0 else ''
        output += self.emoji if self.is_alive else '☠️'

        return output + ' '

    @dataclass
    class GrowthReport:
        @dataclass
        class Growth:
            total: float
            by_water: float
            soil_multiplier: float

        @dataclass
        class Damages:
            total: float
            by_growth: float
            by_soil: float
            soil_humidity_status: 'Plantation.Humidity.Status'
            by_fertilizer: float

        growth: Growth
        damages: Damages
        water_consumption: float

    def grow(self, p: 'Plantation') -> GrowthReport:
        if not self.is_alive:
            raise PlantException.Dead(self)

        soil_humidity = p.soil_humidity

        # plant growth
        water_consumption = min(self.water_needs, p.water_content)
        water_efficiency = water_consumption / self.water_needs
        growth_water = self.growth_rate * water_efficiency * soil_humidity.bonus

        fertilizer_bonus = sum(
            [fertilizer.value.efficiency for fertilizer, turn in p.soil.fertilizers.items() if turn > 0])
        soil_multiplier = 1 + (p.soil.growth_bonus + fertilizer_bonus if growth_water > 0 else 0)

        growth_total = growth_water * soil_multiplier

        # plant damages
        damages_by_growth = (0 if self.growth + growth_total <= 120
                             else growth_total * 0.35 if self.growth >= 120 else 120 - self.growth)
        growth_total -= damages_by_growth

        damages_by_water = soil_humidity.status.value * 2 if soil_humidity.ultra_status else 1

        self.fertilizer_quantity = max(0.0, self.fertilizer_quantity - 0.1) + fertilizer_bonus
        damages_by_fertilizer = (2 * (
                self.fertilizer_limit - self.fertilizer_quantity)) if self.fertilizer_quantity > self.fertilizer_limit else 0

        damages = min(damages_by_growth + damages_by_water + damages_by_fertilizer, self.health)
        self.health -= damages
        self.growth += growth_total

        return Plant.GrowthReport(
            growth=Plant.GrowthReport.Growth(
                total=growth_total,
                by_water=growth_water,
                soil_multiplier=soil_multiplier),
            damages=Plant.GrowthReport.Damages(
                total=damages,
                by_growth=damages_by_growth,
                by_soil=damages_by_water,
                soil_humidity_status=soil_humidity.status,
                by_fertilizer=damages_by_fertilizer),
            water_consumption=water_consumption,
        )

    def maintain(self):
        if not self.is_alive:
            raise PlantException.Dead(self)

        self.growth = min(120.0, self.growth + 5)
        self.health += min(100.0, self.growth + 10)

    def collect(self) -> int:
        if not self.is_alive:
            raise PlantException.Dead(self)
        if not 85.0 < self.growth <= 120.0:
            raise PlantException.Growth(f'The {type(self).__name__} is not growing well enough to be collected.')

        perfect = 95.0 < self.growth < 105.0

        self.growth -= 50
        return int(random.randint(1, 3) * (1.5 if perfect else 1))


class PlantType(Enum):
    from plants.types.tree import TreeType
    from plants.types.vegetable import VegetableType
    from plants.types.herb import HerbType

    TREE = TreeType
    VEGETABLE = VegetableType
    HERB = HerbType

    @staticmethod
    def select() -> type[Plant]:
        return Prompt.select(
            prompt='Select a type of Plant:',
            choices=list(PlantType),
            display_func=lambda t: t.name,
        ).element.value.select()
