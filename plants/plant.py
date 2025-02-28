from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import confloat

if TYPE_CHECKING:
    from plants.plantation import Plantation


class Plant(ABC):
    def __init__(self, *, water_needs: float, growth_rate: confloat(gt=0, le=15), size: int, fertilizer_limit: float,
                 growth: float = 0, fertilizer_quantity: float = 0):
        self.water_needs = water_needs
        self.growth_rate: float = growth_rate
        self.growth = growth
        self.size = size
        self.fertilizer_limit = fertilizer_limit
        self.fertilizer_quantity = fertilizer_quantity
        self.health = 100.0

    def __str__(self) -> str:
        return f'{type(self).__name__} (health: {self.health:.1f}%, growth: {self.growth:.1f}%)'

    def __repr__(self):
        return f'{type(self)}(health={self.health:.1f}%, growth={self.growth:.1f}%)'

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
            by_soil: float
            soil_humidity_status: 'Plantation.Humidity.Status'
            by_fertilizer: float

        growth: Growth
        damages: Damages
        water_consumption: float

    def grow(self, p: 'Plantation') -> GrowthReport:
        soil_humidity = p.soil_humidity

        # plant growth
        water_consumption = min(self.water_needs, p.water_content)
        water_efficiency = water_consumption / self.water_needs
        growth_water = self.growth_rate * water_efficiency * soil_humidity.bonus

        fertilizer_bonus = sum(
            [fertilizer.value.efficiency for fertilizer, turn in p.soil.fertilizers.items() if turn > 0])
        soil_multiplier = (p.soil.growth_bonus + fertilizer_bonus) if growth_water > 0 else 1

        growth_total = growth_water * soil_multiplier
        self.growth += growth_total

        # plant damages
        damages_by_water = soil_humidity.status.value * 2 if soil_humidity.ultra_status else 1

        self.fertilizer_quantity = max(0.0, self.fertilizer_quantity - 0.1) + fertilizer_bonus
        damages_by_fertilizer = (2 * (
                    self.fertilizer_limit - self.fertilizer_quantity)) if self.fertilizer_quantity > self.fertilizer_limit else 0

        damages = damages_by_water + damages_by_fertilizer
        self.health -= damages

        return Plant.GrowthReport(
            growth=Plant.GrowthReport.Growth(
                total=growth_total,
                by_water=growth_water,
                soil_multiplier=soil_multiplier),
            damages=Plant.GrowthReport.Damages(
                total=damages,
                by_soil=damages_by_water,
                soil_humidity_status=soil_humidity.status,
                by_fertilizer=damages_by_fertilizer),
            water_consumption=water_consumption,
        )

    def maintain(self):
        self.growth += 0.1
        self.health += 0.2
