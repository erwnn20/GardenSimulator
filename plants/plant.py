from abc import ABC
from dataclasses import dataclass

from pydantic import confloat

from plants.plantation import Plantation
from plants.soil import Soil


class Plant(ABC):
    def __init__(self, water_needs: float, growth_rate: confloat(gt=0, le=1), size: int, fertilize_limit: int, *,
                 growth: float = 0, fertilized_for: int = 0):
        self.water_needs = water_needs
        self.growth_rate: float = growth_rate
        self.growth = growth
        self.size = size
        self.fertilize_limit = fertilize_limit
        self.fertilized_for = fertilized_for
        self.health = 100.0

    @dataclass
    class GrowthReport:
        @dataclass
        class Growth:
            total: float
            by_water: float
            fertilizer_multiplier: float

        @dataclass
        class Damages:
            total: float
            by_soil: float
            soil_humidity_status: Plantation.Humidity.Status
            by_fertilizer: float

        growth: Growth
        damages: Damages
        water_consumption: float

    def grow(self, p: Plantation) -> GrowthReport:
        soil_humidity = p.soil_humidity

        # plant growth
        water_consumption = min(self.water_needs, p.water_content)
        water_efficiency = water_consumption / self.water_needs
        growth_water = self.growth_rate * water_efficiency * soil_humidity.bonus

        fertilized = Soil.Bonus.Fertilized in p.soil.bonus and p.soil.bonus[Soil.Bonus.Fertilized] > 0
        fertilizer_multiplier = (p.soil.growth_bonus + 0.1 if fertilized else 0) if growth_water > 0 else 1

        growth_total = growth_water * fertilizer_multiplier
        self.growth += growth_total

        # plant damages
        damages_by_water = soil_humidity.status.value * 2 if soil_humidity.ultra_status else 1

        if fertilized:
            self.fertilized_for += 1
        else:
            self.fertilized_for = 0
        damages_by_fertilizer = 2 * (
                self.fertilize_limit - self.fertilized_for) if self.fertilized_for > self.fertilize_limit else 0

        damages = damages_by_water + damages_by_fertilizer
        self.health -= damages

        return Plant.GrowthReport(
            growth=Plant.GrowthReport.Growth(
                total=growth_total,
                by_water=growth_water,
                fertilizer_multiplier=fertilizer_multiplier),
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

    def __repr__(self):
        return f'{type(self)}(health={self.health}, growth={self.growth})'
