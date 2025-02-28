from dataclasses import dataclass
from enum import Enum

from exceptions import PlantationException
from plants.add.fertilizer import FertilizerType
from plants.plant import Plant
from plants.soil import Soil


class Plantation:
    def __init__(self, *, size: int,
                 soil: Soil,
                 plant: Plant | None = None,
                 max_water_content: float,
                 water_content: float = 0):
        self.size = size
        self.soil = soil
        self.max_water_content = max_water_content
        self.water_content = water_content
        self.plant = plant

    class StrType(Enum):
        WATER = 0

    def __str__(self) -> str:
        return (f'Soil: {type(self.soil).__name__} | '
                f'{f"Plant: {self.plant}" if self.plant else f"No plant (size: {self.size})"} | '
                f'Water: {self.water_content:.2f}/{self.max_water_content:.2f} L')

    @property
    def is_empty(self) -> bool:
        return self.plant is None and self.soil is None

    @property
    def is_soiled(self) -> bool:
        return self.soil is not None

    @property
    def is_soiled_no_seed(self) -> bool:
        return self.is_soiled and self.plant is None

    @property
    def is_seeded(self) -> bool:
        return self.plant is not None

    def plant_seed(self, new_plant: Plant) -> 'Plantation':
        if self.is_seeded:
            raise PlantationException.Seed(f'a plant is already growing in this {type(self)} -> {repr(self.plant)}')
        if not self.is_soiled:
            raise PlantationException.Soil(f'there is no soil in which to plant the plant')
        if new_plant.size > self.size:
            raise PlantationException.Seed(f'this {type(self)} is too small for {repr(self.plant)}')

        self.plant = new_plant
        return self

    def dig_up(self) -> 'Plantation':
        self.plant = None
        return self

    def change_soil(self, new_soil: Soil) -> 'Plantation':
        if self.is_seeded:
            raise PlantationException.Soil(
                f'you cannot change plant if this {type(self)} contains a plant. self.plant: {repr(self.plant)}')

        self.soil = new_soil
        return self

    def watering_up(self, water_quantity: float) -> float:
        if not self.is_soiled:
            raise PlantationException.Water('no soil to water')

        added = min(self.water_content + water_quantity, self.max_water_content)
        self.water_content = added
        return added

    @property
    def soil_water_needs(self) -> float:
        return self.soil.water_per_unit * self.size

    @dataclass
    class Humidity:
        class Status(Enum):
            DRY = 2.5
            CORRECT = 0
            WET = 1.5

            @staticmethod
            def get(water_ratio: float) -> 'Plantation.Humidity.Status':
                if water_ratio < 0.85:
                    return Plantation.Humidity.Status.DRY
                elif water_ratio > 1.15:
                    return Plantation.Humidity.Status.WET
                return Plantation.Humidity.Status.CORRECT

        bonus: float
        status: Status
        ultra_status: bool

    @property
    def soil_humidity(self) -> Humidity:
        water_ratio = self.water_content / self.soil_water_needs
        clamped_bonus = round(water_ratio if water_ratio <= 1 else 1.0 - (water_ratio - 1.0), 3)

        return Plantation.Humidity(
            bonus=clamped_bonus,
            status=Plantation.Humidity.Status.get(water_ratio),
            ultra_status=clamped_bonus < 0,
        )

    def fertilize(self, fertiliser: FertilizerType) -> 'Plantation':
        if not self.is_soiled:
            raise PlantationException.Soil('no soil to fertilize')
        self.soil.fertilize(fertiliser)
        return self
