from typing import Callable

from data.save import Data
from plants.add.fertilizer import FertilizerType
from plants.plantation import Plantation
from utils.prompt import Prompt


class Garden(Data):
    def __init__(self, name: str):
        self.name = name
        self.plantations: list[Plantation] = []

    def __str__(self) -> str:
        return (f'{self.name}: {len(self.plants)}/{len(self.plantations)} plant(s)'
                '\n  - ' + '\n  - '.join([str(p) for p in self.plantations]))

    def __add__(self, new_plant: Plantation | list[Plantation]):
        self.plantations += new_plant if isinstance(new_plant, list) else [new_plant]
        return self

    @property
    def plants(self) -> list[Plantation]:
        return [plant for plant in self.plantations if not plant.is_empty]

    def str(self) -> str:
        avg_health = 0.0 if len(self.plants) == 0 else sum([p1.plant.health for p1 in self.plants]) / len(self.plants)
        avg_growth = 0.0 if len(self.plants) == 0 else sum([p2.plant.growth for p2 in self.plants]) / len(self.plants)

        return (f"Garden {self.name}: {len(self.plants)}/{len(self.plantations)} plant(s) "
                f"[avg -> health: {avg_health:.1f}% ; growth: {avg_growth * 100:.1f}%] ")

    def select_plantations(self, message: str, *, empty: bool,
                           plantation_str: Callable[[Plantation], str] = lambda p: str(p)) -> list[Plantation]:
        out_list: list[Plantation] = []
        plant_list: list[Plantation] = self.plantations if empty else self.plants

        if not plant_list:
            print(f'there are no {"plantations" if empty else "plants"} in {self.name}')
            return out_list

        while True:
            choices = [
                'All',
                *[p for p in plant_list if p not in out_list],
                'Exit'
            ]

            selected = Prompt.select(message, choices,
                                     lambda x: plantation_str(x) if isinstance(x, Plantation) else str(x)).element
            match selected:
                case 'All':
                    return plant_list
                case 'Exit':
                    return out_list
                case _:
                    out_list.append(selected)
                    print()

    def watering(self) -> 'Garden':
        plant_str: Callable[[Plantation], str] = lambda p: (f'Soil: {type(p.soil).__name__} | '
                                                            f'{"Plant: " + f"{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, water needs: {p.plant.water_needs:.2f} L)" if p.plant else f"No plant"} | '
                                                            f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L')

        plants = self.select_plantations('Which plants do you want to water?', empty=True, plantation_str=plant_str)
        plants_str = (f'Selected:\n'
                      '  - ' + '\n  - '.join([plant_str(p) for p in plants]))

        print()
        print(plants_str)
        all_plants = Prompt.select('You want to :',
                                   [
                                       'water all plantations equally',
                                       'choose the quantity of water for each plantation'
                                   ], lambda x: x).index == 1

        water: float | None = None
        if all_plants:
            water = float(Prompt.get('Enter the amount of water you want to use per plant :',
                                     excluded_condition=lambda x: x < 0.0))

        for plant in plants:
            if not all_plants: print()
            plant.watering_up(water if all_plants else float(Prompt.get(
                prompt=f'{type(plant).__name__}: {plant_str(plant)}\n'
                       'Enter the amount of water you want to use for this plant:',
                excluded_condition=lambda x: x < 0.0
            )))
        return self

    def fertilizing(self) -> 'Garden':
        plant_str: Callable[[Plantation], str] = lambda p: (
            f'Soil: {type(p.soil).__name__} {"(fertilized) " if any(value > 0 for value in p.soil.fertilizers.values()) else ""}| '
            f'{"Plant: " + f"{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, fertilize quantity: {p.plant.fertilizer_quantity:.2f}/{p.plant.fertilizer_limit:.2f})" if p.plant else f"No plant"} | '
            f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L')

        fertilizer = FertilizerType.select()
        plants = self.select_plantations('Which plants do you want to fertilize?', empty=True, plantation_str=plant_str)

        for plant in plants:
            plant.fertilize(fertilizer)

        return self

    def maintain(self) -> 'Garden':
        for plantation in self.plants: plantation.plant.maintain()
        return self
